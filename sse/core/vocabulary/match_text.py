import re

WORD_BOUNDARY_REGEX = "\\b{word}\\b".format


def at_word_boundaries(text, offset, word):
    if len(word) >= 3 and (text.lower() == word.lower()):  # handle exact match
        return True

    left_boundary = offset - len(word)
    right_boundary = offset + 2
    text_window = text[left_boundary:right_boundary]
    if len(word) >= 3:
        return re.search(WORD_BOUNDARY_REGEX(word=word), text_window, re.IGNORECASE)
    return re.search(WORD_BOUNDARY_REGEX(word=word), text_window)


def generate_matches(automaton, text):
    for offset, (concept_id, concept_name) in automaton.iter(text):
        if at_word_boundaries(text=text, offset=offset, word=concept_name):
            yield (offset, (concept_id, concept_name))
