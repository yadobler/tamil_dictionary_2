import json
from collections import defaultdict
from letters import uyir, aytham, mei, uyirmei, one_letter_words, granda
all_letters = uyir | aytham | mei | uyirmei | granda
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
        while (i < len(headword)):
            for letter in all_letters_key:
                if headword[i:].startswith(letter):
                    transliteration += all_letters[letter]
                    i += len(letter) - 1
                    break
            i += 1
                
        data_list[transliteration] = (headword, definition)

all_dictionary_entries = {}
for i in range(24):
    process_json_source(all_dictionary_entries, f"database/v{i+1:02d}.json")

words = all_dictionary_entries.keys()
bigram = defaultdict(int)
for word in words:
    for i in range(len(word) - 2):
        bigram[word[i:i+3]] += 1

print([(k,bigram[k]) for k in sorted(bigram, key=lambda x:bigram[x], reverse=True)])
