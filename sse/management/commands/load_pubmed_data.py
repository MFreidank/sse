from django.core.management.base import BaseCommand
import os
import pickle
import re
from Bio import Entrez
from Bio import Medline
from sse.core.vocabulary.match_text import generate_matches
from sse.core.entity_engines import extract_entity
from sse.core.models import Article
from sse.core.models import Author
from sse.core.models import Entity
from sse.core.models import Match
from sse.core.models import Tag

class Command(BaseCommand):

    def handle(self, *args, **options):
        # initialize batches [for Intelligent Backend (TM) ;) ]
        batch_size = 5
        pubmed_id_batch = []
        abstract_batch = []
        
        # load text matching automaton
        automaton_path = os.path.join(os.path.dirname(__file__), "..", "..", 
            "..", "data", "processed", "vocabulary_automaton.pkl")
        automaton = pickle.load(open(automaton_path, "rb"))
        
        # search for papers and store the PubMed IDs
        max_documents = 10
        Entrez.email = "diegovs87@yahoo.fr"
        handle = Entrez.esearch(db="pubmed", retmax=max_documents, term="liver")
        results = Entrez.read(handle)
        ids = results["IdList"]
        
        # fetch the papers
        handle = Entrez.efetch(db="pubmed", retmax=max_documents, id=ids, 
            rettype="medline")
        data = []
        for record in Medline.parse(handle):
            # Exclude non-english articles
            if "eng" not in record["LA"]:
                continue
        
            # Article
            if "TI" not in record.keys():
                continue
            title = record["TI"]
            abstract = None
            if "AB" in record.keys():
                abstract = record["AB"]
            pubmed_id_batch.append(record["PMID"])
            abstract_batch.append(record["AB"])
            publication_date = record["MHDA"]
            journal_title = record["JT"]
            article = Article.objects.create(title=title, abstract=abstract, 
                journal=journal_title)
        
            if abstract != None:
                # Add matches from Aho-Corasick Automaton
                matches = generate_matches(automaton, abstract)
                for end, (omop_id, match) in matches:
                    end = end + 1
                    length = len(match)
                    offset = end - len(match)
                    entity = Entity.objects.get(omop_id=omop_id)
                    match = Match.objects.create(article=article, entity=entity,
                        offset=offset, length=length)
        
            # Author
            name = None
            affiliation = None
            email = None
            if "AU" in record.keys():
                name = record["AU"]
            if "AD" in record.keys():
                affiliation = record["AD"]
                email_regex = r"[a-zA-Z0-9._-]+\@[a-zA-Z0-9._-]+\.[a-zA-Z0" + \
                    "-9_-]+"
                email_matches = list(re.finditer(email_regex, record["AD"]))
                if len(email_matches) > 0:
                    start, end = email_matches[0].span()
                    email = record["AD"][start:end]
                author = Author.objects.update_or_create(name=name, 
                    email=email, affiliation=affiliation)
                author.articles.add(article)
        
            # Tags (MeSH Terms)
            if "MH" in record.keys():
                tags = record["MH"]
                for tag in tags:
                    description = "TEST"
                    tag_object = Tag.objects.get_or_create(tag=tag, 
                        description=description)
                    tag_object.articles.add(article)
        
            # Check if Intelligent Backend batches are ready to be processed
            if len(pubmed_id_batch) == batch_size:
                data_batch = { "documents" : [{ "id" : pubmed_id_batch[j], 
                    "language" : "en", "text" : abstract_batch[j] } for j in 
                    range(len(pubmed_id_batch)) ] }
                endpoint = "https://westeurope.api.cognitive.microsoft.com/" + \
                    "text/analytics/v2.0/entities"
                #matches = extract_entity(data_batch, api_key=api_key, endpoint=endpoint)
                pubmed_id_batch = []
                abstract_batch = []
