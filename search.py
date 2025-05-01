import struct
import os
import json
import math
from collections import defaultdict
from letters import parse, get_readable_transliteration
from utils import remove_punctuation, simple_tokenizer, get_hash, HEADER_SIZE, HEADER, STRUCTURE_SIZE, STRUCTURE, HASHTABLEFILE, POSTINGSFILE, DATAFILE

N = struct.unpack(HEADER, open(HASHTABLEFILE, "rb").read(HEADER_SIZE))[0]
HASH_N = os.path.getsize(HASHTABLEFILE) // STRUCTURE_SIZE

def prettify_definition(entry):
    """Prettifies the dictionary output from fetch_definitions."""
    print("Entry:")
    for key, value in entry.items():
        print(f"* **{key.replace('_', ' ').title()}**: {value}")

def edit_distance(s1, s2):
    seq = difflib.SequenceMatcher(None, s1, s2)
    ratio = seq.ratio()  # 1.0 = identical, closer to 0 = very different
    distance = int((1 - ratio) * max(len(s1), len(s2)))
    return distance

def calculate_tfidf(tf, df):
    """Calculates TF-IDF score."""
    idf = math.log(N / (df + 1)) # Add 1 to df to avoid log(0) if a term is in all documents
    return tf * idf


def find_word(word, fp):
    search_hash = get_hash(word)
    low_index = 0
    high_index = HASH_N - 1
    while low_index <= high_index:
        mid_index = (low_index + high_index) // 2
        mid_offset = HEADER_SIZE + mid_index * STRUCTURE_SIZE
        fp.seek(mid_offset)

        entry_data = fp.read(STRUCTURE_SIZE)
        stored_hash, df, postings_offset = struct.unpack(STRUCTURE, entry_data)
        if search_hash == stored_hash:
            return (stored_hash, df, postings_offset)
        elif search_hash < stored_hash:
            high_index = mid_index - 1
        else: 
            low_index = mid_index + 1
    # If the loop finishes, the word was not found
    return (b'0', 0, -1)

        
def fetch_definitions(pointer):
    with open(DATAFILE, "r", encoding="utf-8") as df:
        try:
            df.seek(pointer)
            return json.loads(df.readline())
        except BaseException:
            return {}

EXACT_HEADWORD_BONUS = 100.0  # Large bonus for exact match
PREFIX_HEADWORD_BONUS = 50.0  # Medium bonus for prefix match

def search(query):
    processed_query = remove_punctuation(query.strip())
    query_tokens = simple_tokenizer(processed_query)

    query_tf = defaultdict(int)
    doc_term_tf = defaultdict(lambda: defaultdict(float))
    term_df = {}

    with open(HASHTABLEFILE, "rb") as hf, open(POSTINGSFILE, "r", encoding="utf-8") as pf:
        for token in query_tokens:
            _, df, offset = find_word(token, hf)
            if offset < 0:
                continue
            query_tf[token] += 1
            if token not in term_df:
                term_df[token] = df

            pf.seek(offset)
            term_in_postings, posting_data = json.loads(pf.readline())
            if term_in_postings != token:
                print(f"Warning: Hash collision suspected or index error for '{token}'")
                continue

            for doc_id, tf in posting_data:
                doc_term_tf[doc_id][token] = tf

    query_vector = {}
    for term, tf in query_tf.items():
        if term in term_df:
            query_vector[term] = calculate_tfidf(tf, term_df[term])
    query_norm = math.sqrt(sum(w**2 for w in query_vector.values()))


    entries = []
    for doc_id, term_tf_map in doc_term_tf.items():
        doc_vector = {}
        dot_product = 0.0
        for term, tf in term_tf_map.items():
            if term in term_df:
                df = term_df[term]
                doc_vector[term] = calculate_tfidf(tf, df)
                if term in query_vector:
                    dot_product += query_vector[term] * doc_vector[term]

        doc_norm = math.sqrt(sum(w**2 for w in doc_vector.values()))
        tfidf_score = dot_product / (query_norm * doc_norm) if query_norm and doc_norm else 0.0

        match_bonus = 0.0
        entry_data = fetch_definitions(doc_id)
        headword = entry_data.get("headword", "")
        cleaned_headword = remove_punctuation(headword.strip())
        if cleaned_headword == processed_query:
            match_bonus = EXACT_HEADWORD_BONUS
        elif cleaned_headword.startswith(processed_query):
            match_bonus = PREFIX_HEADWORD_BONUS
        final_score = match_bonus + tfidf_score
        entries.append((doc_id, final_score))

    return sorted(entries, key=lambda x: x[1], reverse=True)

def get_results(query, n=5):
    primary_results = search(query)
    num_results_to_fetch = n if n > 0 else len(primary_results)
    top_results_pointers = primary_results[:num_results_to_fetch]
    formatted_results = []

    for ptr, score in top_results_pointers:
        definition_data = fetch_definitions(ptr)
        definition_data["score"] = score
        headword_letters = definition_data.get("headword_letters", [])
        definition_data["transliteration"] = get_readable_transliteration(headword_letters)
        if isinstance(definition_data.get("definition"), str):
             definition_data["definition"] = definition_data["definition"].split(";")
        formatted_results.append(definition_data)
    return formatted_results



if __name__ == "__main__":
    for x in get_results("wall", 1):
        print(prettify_definition(x))
