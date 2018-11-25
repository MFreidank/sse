from Bio import Entrez
from Bio import Medline
from django.core.management.base import BaseCommand
from sse.core.entity_engines import extract_entity
from sse.core.models import Article
from sse.core.models import Author
from sse.core.models import Entity
from sse.core.models import Match
from sse.core.models import Tag
from sse.core.vocabulary.match_text import generate_matches
import logging
import os
import pickle
import re

class Command(BaseCommand):

    article_field_mapping = {
        "title": "TI",
        "abstract": "AB",
        "journal": "JT",
    }
    batch_size = 5
    database = "pubmed"
    id_list_key = "IdList"
    max_documents = 100
    rettype = "medline"
    search_terms = ["liver", "Hippopotamus amphibius"]

    def add_arguments(self, parser):
        default_api_key = os.environ.get("AZURE_COGNITIVE_API_KEY", None)

        parser.add_argument("--api-key", default=default_api_key, nargs="?", type=str)
        parser.add_argument("--automaton-file", nargs=1, type=str)
        parser.add_argument("--entrez-email", nargs=1, type=str)

    def load_automaton(self, **options):
        with open(options.get("automaton_file")[0], "rb") as automaton_file:
            automaton = pickle.load(automaton_file)
        return automaton

    def configure_entrez(self, **options):
        Entrez.email = options.get("entrez_email")[0]

    def get_entrez_id_list(self, *, search_term, **options):
        handle = Entrez.esearch(
            db=self.database,
            retmax=self.max_documents,
            term=search_term,
        )
        results = Entrez.read(handle)
        return results[self.id_list_key]

    def get_entrez_records(self, *args, search_term, **options):
        handle = Entrez.efetch(
            db=self.database,
            retmax=self.max_documents,
            id=self.get_entrez_id_list(search_term=search_term, **options),
            rettype=self.rettype,
        )
        return self.filter_records(Medline.parse(handle))

    def filter_records(self, records):
        """
        Filter all records which aren in english and have a title
        """
        return list(filter(
            lambda record: "eng" in record["LA"] and "TI" in record,
            records
        ))

    def handle(self, *args, **options):
        for search_term in self.search_terms:
            # create entrez data
            self.records = self.get_entrez_records(*args, search_term=search_term, **options)
            logging.info("Created all the records")
            self.create_articles(*args, **options)
            logging.info("Created all the articles")
            self.create_vocabulary_matches(*args, **options)
            logging.info("Created the vocabulary matches")
            self.create_authors(*args, **options)
            logging.info("Created the authors")
            # self.assign_articles_to_authors(*args, **options)
            # self.create_tags(*args, **options)
            # self.assign_tags_to_articles(*args, **options)

        # create azure data
        self.cognitive_batches = self.get_cognitive_batches(*args, **options)
        self.create_cognitive_matches(*args, **options)

    def get_article_data_as_keywords(self, record):
        return {
            model_key: record.get(record_key)
            for model_key, record_key in self.article_field_mapping.items()
        }

    def create_articles(self, *args, **options):
        Article.objects.bulk_create([
            Article(
                **self.get_article_data_as_keywords(record)
            )
            for record in self.records
            if "AB" in record
        ])

    def create_vocabulary_matches(self, *args, **options):
        self.automaton = self.load_automaton(*args, **options)
        articles = Article.objects.filter(abstract__isnull=False)
        entities = {
            entity.omop_id: entity
            for entity in Entity.objects.all()
        }

        Match.objects.bulk_create([
            Match(
                article=article,
                entity=entities.get(omop_id),
                length=len(match),
                offset=end - len(match) + 1,
            )
            for article in articles
            for end, (omop_id, match) in generate_matches(
                self.automaton,
                article.abstract,
            )
            if entities.get(omop_id)
        ])

    def get_cognitive_batches(self, *args, **options):
        api_key = options.get('api_key')
        batch_size = options.get("batch_size", self.batch_size)
        records = list(filter(lambda record: "AB" in record, self.records))

        batches = [
            records[index:index + batch_size]
            for index in range(0, len(records), batch_size)
        ]

        return [
            extract_entity({
                "documents": [
                    {
                        "id": record["PMID"],
                        "language": "en",
                        "text": record["AB"],
                    }
                    for record in batch
                ]
            }, api_key=api_key)
            for batch in batches
        ]

    def create_cognitive_matches(self, *args, **kwargs):
        for batch in self.cognitive_batches:
            for records_index, document in enumerate(batch['documents']):
                self.create_matches_from_azure_cognitive_document(records_index, document)

    def create_matches_from_azure_cognitive_document(self, records_index, document):
        found_entities = document.get('entities')
        entity_names = {entity['name'] for entity in found_entities}

        automaton_matches = {
            omop_id: entity_name
            for entity_name in entity_names
            for _, (omop_id, _) in generate_matches(self.automaton, entity_name)
        }

        filtered_matches = {}
        for omop_id, entity_name in automaton_matches.items():
            filtered_set = [
                entity
                for entity in found_entities
                if entity['name'] == entity_name
            ]
            filtered_matches[omop_id] = [
                match
                for automaton_match in filtered_set
                for match in automaton_match['matches']
            ]

        entities = {
            entity.omop_id: entity
            for entity in Entity.objects.all()
        }

        article = Article.objects.get(
            **self.get_article_data_as_keywords(self.records[records_index])
        )

        Match.objects.bulk_create([
            Match(
                article=article,
                entity=entities[omop_id],
                length=match.get('length'),
                offset=match.get('offset'),
            )
            for omop_id, matches in filtered_matches.items()
            for match in matches
        ])

    def create_authors(self, *args, **options):

        def get_email(record):
            email = re.findall(r"[\w\.-]+@[\w\.-]+", record.get("AD", ""))
            if email:
                return email[0].strip('.')
            return None

        Author.objects.bulk_create([
            Author(
                affiliation=record.get("AD"),
                email=get_email(record),
                name=name,
            )
            for record in self.records
            for name in record.get("AU", [])
        ])

    def assign_articles_to_authors(self, *args, **options):
        pass

    def create_tags(self, *args, **options):
        tags = {
            tag
            for record in self.records
            for tag in record.get("MH", [])
        }

        Tag.objects.bulk_create([
            Tag(tag=tag)
            for tag in tags
        ])

    def assign_tags_to_articles(self, *args, **options):
        pass
