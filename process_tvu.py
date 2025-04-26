import json
from collections import defaultdict
from letters import uyir, aytham, mei, uyirmei, one_letter_words, granda
all_letters = uyir + aytham + mei + uyirmei + granda
all_letters_key = sorted(all_letters.keys(), key=lambda x:len(x), reverse=True)

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
        i = 0
        for letter in all_letters_key:
            if headword[i:].startswith(letter):
                transliteration += all_letters[letter]
                i += len(letter)
                break
        data_list[transliteration] = (headword, definition)

all_dictionary_entries = {}
for i in range(24):
    process_json_source(all_dictionary_entries, f"database/v{i+1:02d}.json")

words = all_dictionary_entries.keys()

bigrams = defaultdict(int)
for word in words:
    for i in range(len(word) - 1):
        bigrams[word[i:i+2]] += 1

print(bigrams)
