import struct
import os
import json
import math
import difflib
from collections import defaultdict
from letters import parse
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
        df.seek(pointer)
        return json.loads(df.readline())

def search(query):
    query = remove_punctuation(query)
    query_tokens = simple_tokenizer(query)

    query_tf = defaultdict(int)
    query_df = {}
    doc_tf_idf = defaultdict(lambda: defaultdict(float))

    with open(HASHTABLEFILE, "rb") as hf, open(POSTINGSFILE, "r", encoding="utf-8") as pf:
        for token in query_tokens:
            _, df, offset = find_word(token, hf)
            if offset < 0:
                continue
            query_tf[token] += 1
            query_df[token] = df

            pf.seek(offset)
            term, posting_data = json.loads(pf.readline())
            for doc_id, tf in posting_data:
                doc_tf_idf[doc_id][term] = calculate_tfidf(tf, df)

    query_vector = {term: calculate_tfidf(tf, query_df[term]) for term, tf in query_tf.items()}
    query_norm = math.sqrt(sum(w**2 for w in query_vector.values()))
    entries = []

    for doc_id, vec in doc_tf_idf.items():
        dot = 0.0
        for q_term, q_weight in query_vector.items():
            for d_term, d_weight in vec.items():
                # Exact match
                if q_term == d_term:
                    dot += q_weight * d_weight
                # Fuzzy match
                elif q_term in d_term:
                    similarity = difflib.SequenceMatcher(None, q_term, d_term).ratio()
                    if similarity > 0.7:  # tweakable threshold
                        boost = similarity  # e.g., similarity = 0.8 → boost by 0.8
                        dot += q_weight * d_weight * boost

        doc_norm = math.sqrt(sum(w**2 for w in vec.values()))
        score = dot / (query_norm * doc_norm) if query_norm and doc_norm else 0.0
        entries.append((doc_id, score))
    return sorted(entries, key=lambda x: x[1], reverse=True)

def get_results(query, n=5):
    query_letters = [letter for letter, _, _ in parse(query)]  # parsed spelling letters
    query_text = ''.join(query_letters)  # join back to text for edit distance

    primary_results = search(query)
    results = []

    for ptr, score in primary_results:
        definition = fetch_definitions(ptr)
        headword_letters = definition.get("headword_letters", [])
        headword_text = ''.join(headword_letters)

        # Boost for exact spelling match at start
        if headword_letters[:len(query_letters)] == query_letters:
            score += 1.0
        elif any(q in headword_letters for q in query_letters):
            score += 0.5

        # Bonus: Boost if edit distance is small
        distance = edit_distance(query_text, headword_text[:len(query_text)+2])  # allow slight extra characters
        if distance == 1:
            score += 0.3  # Small typo boost
        elif distance == 2:
            score += 0.1  # Very minor boost

        definition["score"] = score
        results.append(definition)

    # Sort by boosted score
    results = sorted(results, key=lambda r: r["score"], reverse=True)

    return results[:n] if n > 0 else results

results = get_results("computer", 1)
print(results)
