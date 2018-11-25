from django.core.management.base import BaseCommand
import pandas as pd
import os
from sse.core.models import Entity
from sse.core.models import Domain
from sse.core.models import Synonym

vocabulary_directory = os.path.join("data", "vocabulary")

class Command(BaseCommand):

    entity_field_mapping = {
        "omop_id": "concept_id",
        "name": "concept_name",
        "vocabulary_id": "vocabulary_id",
        "concept_code": "concept_code",
    }

    def add_arguments(self, parser):
        parser.add_argument('--concept-file', type=str)
        parser.add_argument('--synonyms-file', type=str)

    def handle(self, *args, **options):
        self.concept_data = pd.read_csv(
            options.get('concept_file'),
            delimiter="\t",
        )
        self.synonym_data = pd.read_csv(
            options.get('synonyms_file'),
            delimiter="\t",
        )

        self.domains = self.create_domains(*args, **options)
        self.entities = self.create_entities(*args, **options)
        self.create_synonyms(*args, **options)

    def create_domains(self, *args, **options):
        domain_ids = self.concept_data["domain_id"].unique()
        Domain.objects.bulk_create([
            Domain(name=domain)
            for domain in domain_ids
        ])
        return {domain.name: domain for domain in Domain.objects.all()}
    
    def get_domain(self, index):
        return self.domains[self.concept_data["domain_id"][index]]

    def get_data_as_keywords(self, index):
        return {
            model_key: self.concept_data[omop_key][index]
            for model_key, omop_key in self.entity_field_mapping.items()
        }

    def create_entities(self, *args, **options):
        Entity.objects.bulk_create([
            Entity(
                domain=self.get_domain(index),
                **self.get_data_as_keywords(index)
            ) for index in range(self.concept_data.shape[0])
        ])
        return {entity.omop_id: entity for entity in Entity.objects.all()}

    def get_entity(self, index):
        return self.entities[self.synonym_data["concept_id"][index]]

    def create_synonyms(self, *args, **options):
        Synonym.objects.bulk_create([
            Synonym(
                entity=self.get_entity(index),
                name=self.synonym_data["concept_synonym_name"][index],
            )
            for index in range(self.synonym_data.shape[0])
        ])
