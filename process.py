import json 
import re 
import os
import csv
import string
from collections import defaultdict
from letters import parse, tamil_stopwords

CLEANR = re.compile('<.*?>') 
ALLOWED_CHARS = set(string.ascii_letters + string.digits + ' ')
TAMIL_START = 0x0B80
TAMIL_END = 0x0BFF
for code_point in range(TAMIL_START, TAMIL_END + 1):
  ALLOWED_CHARS.add(chr(code_point))

STOPWORDS = set(['a', 'an', 'the', 'is', 'in', 'and', 'of', 'to', 'for', 'with', 'by'])
STOPWORDS.update(tamil_stopwords)
STOPWORDS.update(['', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])

def cleanhtml(raw_html):
    """Removes HTML tags from text."""
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext

def remove_punctuation(text):
    cleaned_text_list = [char for char in text.strip() if char in ALLOWED_CHARS]
    cleaned_text = "".join(cleaned_text_list)
    return cleaned_text

def process_json_source(filename):
    data_list = []
    data = {}
    with open(filename, 'r', encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
    for headword_key, definition_value in data.items():
        headword = remove_punctuation(str(headword_key).strip())
        definition = str(definition_value).strip()
        if not headword:
            continue
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
                'raw_row': row # Keep the original row for debugging if needed
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

sorted_dictionary = sorted(all_dictionary_entries, key=lambda x: x["headword"])
print(sorted_dictionary[:5])


