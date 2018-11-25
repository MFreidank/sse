import argparse
from ahocorasick import Automaton
import logging
from os import makedirs, path
from os.path import basename, splitext
import pickle
import zipfile

import pandas as pd


DATA_PATH = path.join(path.dirname(__file__), "..", "..", "..", "data")
RAW_DATA_PATH = path.join(DATA_PATH, "raw")
PROCESSED_DATA_PATH = path.join(DATA_PATH, "processed")


def prepare_data(zip_filename):
    logging.info("Preparing data from zip file at '{}'.".format(zip_filename))
    vocabulary_name, _ = splitext(basename(zip_filename))

    target_directory = path.join(PROCESSED_DATA_PATH, vocabulary_name)
    makedirs(target_directory, exist_ok=True)

    logging.info("Extracting data to '{}'.".format(target_directory))
    with zipfile.ZipFile(zip_filename) as zip_file:
        zip_file.extractall(target_directory)

    logging.info("Done.")

    return target_directory


def add_concepts(automaton, concepts):
    for concept_name, concept_id in concepts:
        logging.debug("Trying to add concept: ({name}, (id))".format(
            name=concept_name, id=concept_id
        ))
        automaton.add_word(concept_name, (concept_id, concept_name))
        logging.debug("Added successfully.")

    return automaton


def update_automaton(dataframe, automaton_filename=path.join(PROCESSED_DATA_PATH, "vocabulary_automaton.pkl"), name_column="concept_name"):
    # Assert we have the same amount of concept names and ids.
    assert len(dataframe[name_column] == dataframe["concept_id"])

    try:
        with open(automaton_filename, "rb") as automaton_file:
            automaton = pickle.load(automaton_file)

        logging.info("Loaded previous automaton from path '{}'.".format(automaton_filename))
    except FileNotFoundError:
        logging.info("Created new automaton.")
        automaton = Automaton()

    automaton = add_concepts(automaton, zip(dataframe[name_column], dataframe["concept_id"]))

    automaton.make_automaton()

    with open(automaton_filename, "wb") as automaton_file:
        pickle.dump(automaton, automaton_file)

    logging.info("Updated automaton under path '{}'.".format(automaton_filename))
    return automaton


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("zip_filepath")
    parser.add_argument("--concepts-filename", default="CONCEPT.csv")
    parser.add_argument("--synonyms-filename", default="CONCEPT_SYNONYM.csv")
    parser.add_argument("--seperator", default="\t")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    folder_name = prepare_data(args.zip_filepath)

    dataframe = pd.read_csv(
        path.join(folder_name, args.concepts_filename), sep=args.seperator
    ).dropna(subset=["concept_name"])

    # Assert we have the same amount of concept names and ids.
    assert len(dataframe["concept_name"] == dataframe["concept_id"])

    update_automaton(dataframe)

    synonyms_dataframe = pd.read_csv(
        path.join(folder_name, args.synonyms_filename), sep=args.seperator
    ).dropna(subset=["concept_synonym_name"])

    update_automaton(synonyms_dataframe, name_column="concept_synonym_name")


if __name__ == "__main__":
    main()
