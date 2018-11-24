from django.core.management.base import BaseCommand
import pandas as pd
import os
from sse.core.models import Entity
from sse.core.models import Domain

vocabulary_directory = os.path.join("data", "vocabulary")

class Command(BaseCommand):

    def handle(self, *args, **options):
        # Load concepts
        concept_path = os.path.join(vocabulary_directory, "CONCEPT.csv")
        concept_data = pd.read_csv(concept_path, delimiter="\t")
        for i in range(concept_data.shape[0]):
            omop_id = concept_data["concept_id"][i]
            name = concept_data["concept_name"][i]
            vocabulary_id = concept_data["vocabulary_id"][i]
            concept_code = concept_data["concept_code"][i]
            domain_id = concept_data["domain_id"][i]
            synonyms = []
            domain, _ = Domain.objects.get_or_create(name = domain_id)
            Entity.objects.create(omop_id=omop_id, name=name, 
                vocabulary_id=vocabulary_id, concept_code=concept_code, 
                domain=domain)
        
        # Load concept synonyms
        concept_synonym_path = os.path.join(vocabulary_directory, 
            "CONCEPT_SYNONYM.csv")
        concept_synonym_data = pd.read_csv(concept_synonym_path, delimiter="\t")
        for i in range(concept_synonym_data.shape[0]):
            omop_id = concept_synonym_data["concept_id"][i]
            synonym = concept_synonym_data["concept_synonym_name"][i]
            Entity.objects.get(omop_id=omop_id).synonyms.add(synonym)
