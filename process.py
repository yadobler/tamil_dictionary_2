import json 
import os
import csv
import struct
from letters import parse
from collections import defaultdict
from utils import remove_punctuation, simple_tokenizer, get_hash, cleanhtml, STRUCTURE, HEADER, HASHTABLEFILE, POSTINGSFILE, DATAFILE

entries_no = 0

def process_json_source(filename):
    data_list = []
    data = {}
    global entries_no
    with open(filename, 'r', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
    for headword_key, definition_value in data.items():
        headword = remove_punctuation(str(headword_key).strip())
        definition = str(definition_value).strip()
        if not headword:
            continue
        entries_no += 1
        parsed = parse(headword)
        headword_list = []
        transliteration = ""
        for letter, _, translit in parsed:
            headword_list.append(letter)
            transliteration += translit
        data_list.append({
            "headword": headword,
            "headword_letters": headword_list, 
            "transliteration": transliteration, 
            "definition": definition,
            "source": "TVU"
        })
    return data_list

def process_csv_source(filepath, header):
    all_dictionary_entries = []
    global entries_no
    with open(filepath, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        has_optional_header = "ignore_0?" in header
        expected_cols_max = len(header)
        expected_cols_min = expected_cols_max - 1 if has_optional_header else expected_cols_max
        line_num = 0
        for row in csv_reader:
            line_num += 1
            num_columns_found = len(row)
            entry_data = {
                'source': os.path.basename(filepath), # Store the filename as source
                'headword': None,
                'definition': None,
                # 'raw_row': row # Keep the original row for debugging if needed
            }
            if has_optional_header:
                # This logic specifically handles the "ignore_0?" case
                if num_columns_found == expected_cols_max: # 5 columns
                    # ["headword", "ignore_0?", "definition", "ignore_1", "ignore_2"]
                    entry_data['headword'] = remove_punctuation(row[0])
                    entry_data['definition'] = row[2]
                elif num_columns_found == expected_cols_min: # 4 columns
                    entry_data['headword'] = remove_punctuation(row[0])
                    entry_data['definition'] = row[1]
            else:
                assert num_columns_found == expected_cols_max
                row_dict = dict(zip(header, row))
                entry_data['headword'] = remove_punctuation(row_dict.get('headword'))
                entry_data['definition'] = row_dict.get('definition')
                # Handle special cases like 'definition_2' if needed
                if 'definition_2' in row_dict and row_dict['definition_2']:
                    # Append to main definition
                    if entry_data['definition']:
                         entry_data['definition'] += f" ({row_dict['definition_2']})"
                    else:
                         entry_data['definition'] = row_dict['definition_2']
            if entry_data['headword'] or entry_data['definition']:
                entries_no += 1
                parsed = parse(entry_data['headword'])
                headword_list = []
                transliteration = ""
                for letter, _, translit in parsed:
                    headword_list.append(letter)
                    transliteration += translit
                entry_data["headword_letters"] = headword_list
                entry_data["transliteration"] = transliteration
                entry_data['definition'] = cleanhtml(entry_data['definition'])
                all_dictionary_entries.append(entry_data)
    return all_dictionary_entries

csv_collections = {
    "./database/Fabricius Dictionary.csv": ["headword", "ignore_0?", "definition", "ignore_1", "ignore_2"],
    "./database/Kadirvelu Dictionary.csv": ["headword", "definition", "ignore_1", "ignore_2"],
    "./database/lddttam.csv": ["headword", "definition", "ignore_1", "ignore_2"],
    "./database/McAlpin Dictionary.csv": ["headword", "definition", "ignore_1", "ignore_2"],
    "./database/Tamil Terminology by TVA.csv": ["definition", "headword", "definition_2"],
    # "./database/Winslow.csv": [],
}

all_dictionary_entries = []
for i in range(24):
    all_dictionary_entries += process_json_source(f"database/v{i+1:02d}.json")
for filename, header in csv_collections.items():
    all_dictionary_entries += process_csv_source(filename, header)
inverted_index = defaultdict(list)

with open(DATAFILE, "w", encoding="utf-8") as f:
    for e in all_dictionary_entries:
        for i in range(len(e["headword"])):
            inverted_index[e["headword"][:i]].append(f.tell())
        tokens = simple_tokenizer(e["definition"])
        for word in tokens:
            inverted_index[word].append(f.tell())
        f.write(f"{json.dumps(e, ensure_ascii=False)}\n")

inverted_index_keys = sorted(inverted_index.keys(), key=lambda x: get_hash(x))

hash_table = []
with open(POSTINGSFILE, "w", encoding='utf-8') as f:
    for word in inverted_index_keys:
        postings = inverted_index[word]
        term_freq = defaultdict(int)
        for p in postings:
            term_freq[p] += 1 
        df = len(term_freq.keys())
        hash_table.append((get_hash(word), df, f.tell()))
        f.write(f"{json.dumps((word, [(k,v) for k,v in sorted(term_freq.items(), key=lambda x: x[0])]), ensure_ascii=False)}\n")

with open(HASHTABLEFILE, "wb") as f:
    f.write(struct.pack(HEADER, entries_no))
    for e in hash_table:
        f.write(struct.pack(STRUCTURE, *e))
