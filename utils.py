import re 
import string
import hashlib
import struct
from letters import tamil_stopwords

CLEANR = re.compile('<.*?>') 
ALLOWED_CHARS = set(string.ascii_letters + string.digits + ' ')
TAMIL_START = 0x0B80
TAMIL_END = 0x0BFF
for code_point in range(TAMIL_START, TAMIL_END + 1):
  ALLOWED_CHARS.add(chr(code_point))

STOPWORDS = set(['a', 'an', 'the', 'is', 'in', 'and', 'of', 'to', 'for', 'with', 'by'])
STOPWORDS.update(tamil_stopwords)
STOPWORDS.update(['', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'])

STRUCTURE = "=32sIQ"
HEADER = "I"
STRUCTURE_SIZE = struct.calcsize(STRUCTURE)
HEADER_SIZE = struct.calcsize(HEADER)
# --- Consistent Hashing Function (Returns bytes) ---
def get_hash(input_string):
     if not isinstance(input_string, str):
        input_string = str(input_string)
     return hashlib.sha256(input_string.encode('utf-8')).digest() 

def cleanhtml(raw_html):
    """Removes HTML tags from text."""
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext

def remove_punctuation(text):
    cleaned_text_list = [char for char in text.strip() if char in ALLOWED_CHARS]
    cleaned_text = "".join(cleaned_text_list)
    return cleaned_text

def simple_tokenizer(text):
    """
    A simple tokenizer that splits text into lowercase alphanumeric tokens.
    Removes common English and Tamil stop words, purely numeric tokens, and tokens shorter than 2 chars.
    """
    if not isinstance(text, str):
        return []
    tokens = re.findall(r'\w+', text.lower())
    tokens = [
        token for token in tokens
        if token not in STOPWORDS # Remove stop words
        and not token.isnumeric() # Remove purely numeric tokens
        and len(token) > 1 # Remove tokens shorter than 2 characters
    ]
    return tokens

