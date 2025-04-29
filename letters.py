import re # Needed for splitting words

# --- Dictionaries (mostly unchanged) ---
uyir = {u'அ':'a',u'ஆ':'A',u'இ':'i',u'ஈ':'I',u'உ':'u',u'ஊ':'U',u'எ':'e',u'ஏ':'E',u'ஐ':'Y',u'ஒ':'o',u'ஓ':'O',u'ஔ':'V','ஃ':'X'}
mei = {u'க':'k',u'ங':'M',u'ச':'c',u'ஞ':'b',u'ட':'d',u'ண':'N',u'த':'t',u'ந':'w',u'ப':'p',u'ம':'m',u'ய':'y',u'ர':'r',u'ல':'l',u'வ':'v',u'ழ':'z',u'ள':'L',u'ற':'R',u'ன':'n',u'ஶ':'z',u'ஜ':'j',u'ஷ':'S',u'ஸ':'s',u'ஹ':'h',u'க்ஷ':'x'}
uyirmei = {u'்':'',u'ா':'A',u'ி':'i',u'ீ':'I',u'ு':'u',u'ூ':'U',u'ெ':'e',u'ே':'E',u'ை':'Y',u'ொ':'o',u'ோ':'O',u'ௌ':'V'}
pulli = u'்'

# --- Readable Transliterations ---

readable_uyir = {u'அ':'a',u'ஆ':'aa',u'இ':'i',u'ஈ':'ee',u'உ':'u',u'ஊ':'oo',u'எ':'e',u'ஏ':'ae',u'ஐ':'ai',u'ஒ':'o',u'ஓ':'ou',u'ஔ':'ow','ஃ':'gh'}
readable_mei = {u'க':'k',u'ங':'ng',u'ச':'ch',u'ஞ':'nj',u'ட':'t',u'ண':'n',u'த':'th',u'ந':'n',u'ப':'p',u'ம':'m',u'ய':'y',u'ர':'r',u'ல':'l',u'வ':'v',u'ழ':'lz',u'ள':'l',u'ற':'tr',u'ன':'n',u'ஶ':'z',u'ஜ':'j',u'ஷ':'zh',u'ஸ':'s',u'ஹ':'h',u'க்ஷ':'x'}
readable_uyirmei = {u'்':'',u'ா':'aa',u'ி':'i',u'ீ':'ee',u'ு':'u',u'ூ':'oo',u'ெ':'e',u'ே':'ae',u'ை':'ei',u'ொ':'o',u'ோ':'ou',u'ௌ':'ow'}

def get_readable_transliteration(text_array):
    text = ""
    for x in text_array:
        if len(x) == 2:
            if x[0] in readable_mei and x[1] in readable_uyirmei:
                text += readable_mei[x[0]] + readable_uyirmei[x[1]]
        else:
            if x in readable_uyir:
                text += readable_uyir[x]
            elif x in readable_mei:
                text += readable_mei[x] + 'a'
            else:
                text += x
    return text

# Added more stopwords for better filtering
tamil_stopwords = [u'ஒரு',u'என்று',u'மற்றும்',u'இந்த',u'இது',u'என்ற',u'கொண்டு',u'என்பது',u'பல',u'ஆகும்',u'அல்லது',u'அவர்',u'நான்',u'உள்ள',u'அந்த',u'இவர்',u'என',u'முதல்',u'என்ன',u'இருந்து',u'சில',u'என்',u'போன்ற',u'வேண்டும்',u'வந்து',u'இதன்',u'அது',u'அவன்',u'தான்',u'பலரும்',u'என்னும்',u'மேலும்',u'பின்னர்',u'கொண்ட',u'இருக்கும்',u'தனது',u'உள்ளது',u'போது',u'என்றும்',u'அதன்',u'தன்',u'பிறகு',u'அவர்கள்',u'வரை',u'அவள்',u'நீ',u'ஆகிய',u'இருந்தது',u'உள்ளன',u'வந்த',u'இருந்த',u'மிகவும்',u'இங்கு',u'மீது',u'ஓர்',u'இவை',u'இந்தக்',u'பற்றி',u'வரும்',u'வேறு',u'இரு',u'இதில்',u'போல்',u'இப்போது',u'அவரது',u'மட்டும்',u'இந்தப்',u'எனும்',u'மேல்',u'பின்',u'சேர்ந்த',u'ஆகியோர்',u'எனக்கு',u'இன்னும்',u'அந்தப்',u'அன்று',u'ஒரே',u'மிக',u'அங்கு',u'பல்வேறு',u'விட்டு',u'பெரும்',u'அதை',u'பற்றிய',u'உன்',u'அதிக',u'அந்தக்',u'பேர்',u'இதனால்',u'அவை',u'அதே',u'ஏன்',u'முறை',u'யார்',u'என்பதை',u'எல்லாம்',u'மட்டுமே',u'இங்கே',u'அங்கே',u'இடம்',u'இடத்தில்',u'அதில்',u'நாம்',u'அதற்கு',u'எனவே',u'பிற',u'சிறு',u'மற்ற',u'விட',u'எந்த',u'எனவும்',u'எனப்படும்',u'எனினும்',u'அடுத்த',u'இதனை',u'இதை',u'கொள்ள',u'இந்தத்',u'இதற்கு',u'அதனால்',u'தவிர',u'போல',u'வரையில்',u'சற்று',u'எனக்', u'நான்', u'நீ', u'அவன்', u'அவள்', u'அது', u'நாம்', u'நீங்கள்', u'அவர்கள்', u'அவை']

# --- Suffix Dictionaries (unchanged content, but will be processed) ---
noun_suffix = {
    'Y': 'ACC',         # ஐ
    'Al': "INS",        # ஆல்
    'koNDu': "INS",     # கொண்டு
    'AlkoNDu': "INS",  # ஆல் கொண்டு 
    'AlkkoNdu': "INS",  # ஆல்கொண்டு
    'Odu': "SOC",       # ஓடு
    'udan': "SOC",      # உடன்
    'kku': "DAT",       # க்கு
    'ukku': "DAT",      # உக்கு
    'in poruddu': "DAT",# இன் பொருட்டு
    'inporuddu': "DAT", # இன்்பொருட்டு
    'kkAka': "BEN",     # க்காக
    'ukkAka': "BEN",    # உக்காக
    'iliruwtu': 'ABL',  # இலிருந்து
    'ininRu': 'ABL',    # நின்ற
    'lEliruwtu': 'ABL', # லேலிருந்து
    'idamiruwtu': 'ABL',# இடமிருந்து
    'atu': 'GEN',       # அது
    'udYya': 'GEN',     # உடைய
    'in': 'GEN',        # இன் 
    'il': 'LOC',        # இல்
    'lE': 'LOC',        # லே
    'idam': 'LOC',      # இடம்
    'E': 'VOC',         # ஏ
    'O': 'VOC',         # ஓ
    'A': 'VOC',         # ஆ
    'kaL': 'PL',        # கள் 
    'mAr': 'PLHON',     # மார் 
}

# -m ending nouns (e.g., maram -> maraththu)
noun_m_suffix = {
    'ttY': 'ACC',           # த்தை
    'ttAl': "INS",          # த்தால்
    'ttkoNDu': "INS",       # த்துக்கொண்டு
    'ttAl koNDu': "INS",    # த்தால் கொண்டு
    'ttAlk koNDu': "INS",   # த்தால்க் கொண்டு
    'ttAlkkoNdu': "INS",    # த்தால்க்கொண்டு
    'ttOdu': "SOC",         # த்தோடு
    'ttudan': "SOC",        # த்துடன்
    'ttkku': "DAT",         # த்துக்கு
    'ttukku': "DAT",        # த்துக்கு
    'ttin poruddu': "DAT",  # த்தின் பொருட்டு
    'ttinporuddu': "DAT",   # த்தின்பொருட்டு
    'ttkkAka': "BEN",       # த்துக்காக
    'ttukkAka': "BEN",      # த்துக்காக
    'ttiliruwtu': 'ABL',    # த்திலிருந்து
    'ttininRu': 'ABL',      # த்திலிருந்து
    'ttlEliruwtu': 'ABL',   # த்திலேலிருந்து
    'ttidamiruwtu': 'ABL',  # த்திடமிருந்து
    'ttatu': 'GEN',         # த்தது
    'ttudYya': 'GEN',       # த்துடைய
    'ttin': 'GEN',          # த்தின்
    'ttil': 'LOC',          # த்தில்
    'ttlE': 'LOC',          # த்திலே
    'ttidam': 'LOC',        # த்திடம்
    'mE': 'VOC',            # மே
    'mO': 'VOC',            # மோ
    'mA': 'VOC',            # மா
    'ttukaL': 'PL',         # த்துகள் 
}

noun_m_suffix_sorted = sorted(noun_m_suffix, key=len, reverse=True)
noun_suffix_sorted = sorted(noun_suffix, key=len, reverse=True)


def parse(text):
    i = 0
    results = []
    while len(text) > i:
        if text[i] in uyir:
            results.append((text[i], 'uyir', uyir[text[i]]))
            i += 1
            continue

        if text[i] in mei:
            # Check if it's the last character
            if i + 1 >= len(text):
                results.append((text[i], 'uyirmei', mei[text[i]]+'a')) # Assume 'a' vowel sound
                i += 1
                continue

            # Check if the next character is a vowel modifier
            if text[i+1] in uyirmei:
                # Handle pulli (mei) vs uyirmei
                results.append((text[i] + text[i+1], 'mei' if text[i+1] == pulli else 'uyirmei', mei[text[i]] + uyirmei[text[i+1]]))
                i += 2
                continue
            else:
                # Consonant followed by another consonant or non-modifier - assume 'a' vowel sound
                results.append((text[i], 'uyirmei', mei[text[i]]+'a'))
                i += 1
                continue

        # Handle characters not in the dictionaries (like spaces, punctuation)
        results.append((text[i], 'unknown', text[i]))
        i += 1
    return results

def get_tranliteration(text):
    i = 0
    results = ''
    while len(text) > i:
        if text[i] in uyir:
            results += uyir[text[i]]
            i += 1
            continue

        if text[i] in mei:
            if i + 1 >= len(text):
                results += mei[text[i]]+'a'
                i += 1
                continue

            if text[i+1] in uyirmei:
                results += mei[text[i]] + uyirmei[text[i+1]]
                i += 2
                continue
            else:
                results += mei[text[i]]+'a'
                i += 1
                continue

        # Append unknown characters directly (like spaces, punctuation)
        results += text[i]
        i += 1
    return results


# --- Main Execution Block ---
if __name__ == "__main__":
    # --- Debugging Info ---
    print("--- Character Sets ---")
    print("Uyir:", uyir)
    print("Mei:", mei)
    print("UyirMei Modifiers:", uyirmei)

    # --- Examples ---
    print("\n--- Transliteration Examples ---")
    example_word_1 = "மரத்தின்"
    example_word_2 = "பழங்களை"
    print(f"'{example_word_1}' -> {get_tranliteration(example_word_1)}")
    print(f"'{example_word_2}' -> {get_tranliteration(example_word_2)}")

    long_sentence_tamil = "அவன் இதனால் மாணவர்களோடு  ஆசிரியரின் பொருளை பேருந்திலிருந்து எடுத்து ஓட்டுனரிடம் கொடுத்தான்."
    print("Original Tamil:", long_sentence_tamil)
    transliterated_long = get_tranliteration(long_sentence_tamil)
    print("Transliterated:", transliterated_long)
    
    long_sentence_tamil_parsed = parse(long_sentence_tamil)
    long_sentence_tamil_letters = [x for x,_,_ in long_sentence_tamil_parsed]
    print("Readable Transliteration:",get_readable_transliteration(long_sentence_tamil_letters))

    # print("\n")
    # no_space = re.sub(r"[^a-zA-Z]", '', transliterated_long)
    # i = len(no_space)
    # stack = []
    # old_i = i
    # while i >= 0:
    #     found_suffix = False
    #     for suffix in noun_m_suffix_sorted:
    #         if no_space[:i].endswith(suffix):
    #             stack.append(suffix)
    #             stack.append(no_space[i:old_i])
    #             old_i = i
    #             i -= len(suffix)
    #             found_suffix = True
    #             break
    #     if found_suffix:
    #         continue
    #
    #     for suffix in noun_suffix_sorted:
    #         if no_space[:i].endswith(suffix):
    #             stack.append(suffix)
    #             stack.append(no_space[i:old_i])
    #             old_i = i
    #             i -= len(suffix)
    #             found_suffix = True
    #             break
    #     if found_suffix:
    #         continue
    #     i -= 1
    # stack.reverse()
    # print(stack)
