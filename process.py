import json 
import re 
import csv
from collections import defaultdict
from letters import parse, tamil_stopwords

CLEANR = re.compile('<.*?>') 
STOPWORDS = set(['a', 'an', 'the', 'is', 'in', 'and', 'of', 'to', 'for', 'with', 'by'])
STOPWORDS.update(tamil_stopwords)
STOPWORDS.update(['', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])

def cleanhtml(raw_html):
    """Removes HTML tags from text."""
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext

def process_json_source(data_list, filename):
    data = {}
    with open(filename, 'r', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
    for headword_key, definition_value in data.items():
        headword = str(headword_key).strip()
        definition = str(definition_value).strip()
        if not headword:
            continue
        parsed = parse(headword)
        headword_list = []
        transliteration = ""
        for letter, _, translit in parsed:
            headword_list.append(letter)
            transliteration += translit
        data_list[headword] = (headword_list, transliteration, definition)


collections = {
    "./database/Fabricius Dictionary.csv": ["headword", "ignore_0?", "definition", "ignore_1", "ignore_2"],
    "./database/Kadirvelu Dictionary.csv": ["headword", "definition", "ignore_1", "ignore_2"],
    "./database/lddttam.csv": ["headword", "definition", "ignore_1", "ignore_2"],
    "./database/McAlpin Dictionary.csv": ["headword", "definition", "ignore_1", "ignore_2"],
    "./database/Tamil Terminology by TVA.csv": ["definition", "headword", "definition_2"],
    "./database/Winslow.csv": ["definition", "headword", "definition_2"],

}

all_dictionary_entries = {}
for i in range(24):
    process_json_source(all_dictionary_entries, f"database/v{i+1:02d}.json")
words = all_dictionary_entries.keys()

# ----
def generate_ngrams(n=2):
    if n <= 0:
        return []
    bigram = defaultdict(int)
    for word in words:
        letters = ["^"] + all_dictionary_entries[word][0] + ["$"]
        for i in range(len(letters) - n + 1):
            bigram["".join(letters[i:i+n])] += 1
    return [(k,bigram[k]) for k in sorted(bigram, key=lambda x:bigram[x], reverse=True)]


def generate_top10_ngrams():
    with open("ngrams_top10.txt", "w", encoding="utf-8") as f:
        for i in range(30):
            grams = generate_ngrams(i)
            f.write(f"n:{i}, length:{len(grams)}, top10:{grams[:10]}\n")
# ----


print(all_dictionary_entries["மற்றும்"])
