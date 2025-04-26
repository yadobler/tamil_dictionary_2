import json
from collections import defaultdict
from letters import uyir, aytham, mei, uyirmai, one_letter_words, granda

def process_json_source(data_list, filename):
    data = {}
    with open(filename, 'r', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
    for headword_key, definition_value in data.items():
        headword = str(headword_key).strip()
        definition = str(definition_value).strip()
        if not headword:
            continue
        transliteration = ""
        data_list[transliteration] = (headword, definition)

all_dictionary_entries = {}
for i in range(24):
    process_json_source(all_dictionary_entries, f"database/v{i+1:02d}.json")

words = all_dictionary_entries.keys()

bigrams = defaultdict(int)
for word in words:
    for i in range(len(word) - 1):
        bigrams[word[i:i+2]] += 1
