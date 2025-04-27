# from letters import uyir, aytham, uyir_kuril, uyil_nethil, mei, vallinam, mellinam, ithaiyinam, uyirmei, uyirmai_kuril, uyirmai_nethil, kutriyalugaram, uyiralapedai, otralapedai, udambadumei, one_letter_words, suttu_vina, numerals, viyankol, granda

uyir = {u'அ':'a',u'ஆ':'A',u'இ':'i',u'ஈ':'I',u'உ':'u',u'ஊ':'U',u'எ':'e',u'ஏ':'E',u'ஐ':'Y',u'ஒ':'o',u'ஓ':'O',u'ஔ':'V','ஃ':'X'}
mei = {u'க':'k',u'ங':'M',u'ச':'c',u'ஞ':'b',u'ட':'d',u'ண':'N',u'த':'t',u'ந':'w',u'ப':'p',u'ம':'m',u'ய':'y',u'ர':'r',u'ல':'l',u'வ':'v',u'ழ':'z',u'ள':'L',u'ற':'R',u'ன':'n',u'ஶ':'z',u'ஜ':'j',u'ஷ':'S',u'ஸ':'s',u'ஹ':'h',u'க்ஷ':'x'}
uyirmei = {u'்':'',u'ா':'A',u'ி':'i',u'ீ':'I',u'ு':'u',u'ூ':'U',u'ெ':'e',u'ே':'E',u'ை':'Y',u'ொ':'o',u'ோ':'O',u'ௌ':'V'}
tamil_stopwords = [u'ஒரு',u'என்று',u'மற்றும்',u'இந்த',u'இது',u'என்ற',u'கொண்டு',u'என்பது',u'பல',u'ஆகும்',u'அல்லது',u'அவர்',u'நான்',u'உள்ள',u'அந்த',u'இவர்',u'என',u'முதல்',u'என்ன',u'இருந்து',u'சில',u'என்',u'போன்ற',u'வேண்டும்',u'வந்து',u'இதன்',u'அது',u'அவன்',u'தான்',u'பலரும்',u'என்னும்',u'மேலும்',u'பின்னர்',u'கொண்ட',u'இருக்கும்',u'தனது',u'உள்ளது',u'போது',u'என்றும்',u'அதன்',u'தன்',u'பிறகு',u'அவர்கள்',u'வரை',u'அவள்',u'நீ',u'ஆகிய',u'இருந்தது',u'உள்ளன',u'வந்த',u'இருந்த',u'மிகவும்',u'இங்கு',u'மீது',u'ஓர்',u'இவை',u'இந்தக்',u'பற்றி',u'வரும்',u'வேறு',u'இரு',u'இதில்',u'போல்',u'இப்போது',u'அவரது',u'மட்டும்',u'இந்தப்',u'எனும்',u'மேல்',u'பின்',u'சேர்ந்த',u'ஆகியோர்',u'எனக்கு',u'இன்னும்',u'அந்தப்',u'அன்று',u'ஒரே',u'மிக',u'அங்கு',u'பல்வேறு',u'விட்டு',u'பெரும்',u'அதை',u'பற்றிய',u'உன்',u'அதிக',u'அந்தக்',u'பேர்',u'இதனால்',u'அவை',u'அதே',u'ஏன்',u'முறை',u'யார்',u'என்பதை',u'எல்லாம்',u'மட்டுமே',u'இங்கே',u'அங்கே',u'இடம்',u'இடத்தில்',u'அதில்',u'நாம்',u'அதற்கு',u'எனவே',u'பிற',u'சிறு',u'மற்ற',u'விட',u'எந்த',u'எனவும்',u'எனப்படும்',u'எனினும்',u'அடுத்த',u'இதனை',u'இதை',u'கொள்ள',u'இந்தத்',u'இதற்கு',u'அதனால்',u'தவிர',u'போல',u'வரையில்',u'சற்று',u'எனக்']
pulli = u'்'

def parse(text):
    i = 0
    results = []
    while len(text) > i:
        if text[i] in uyir:
            results.append((text[i], 'uyir', uyir[text[i]]))
            i += 1
            continue

        if text[i] in mei:
            if i + 1 >= len(text):
                results.append((text[i], 'uyirmei', mei[text[i]]+'a'))
                i += 1
                continue

            if text[i+1] in uyirmei:
                results.append((text[i] + text[i+1], 'mei' if text[i+1] == pulli else 'uyirmei', mei[text[i]] + uyirmei[text[i+1]]))
                i += 2
                continue
            else:
                results.append((text[i], 'uyirmei', mei[text[i]]+'a'))
                i += 1
                continue
        
        results.append((text[i], 'unknown', text[i]))
        i += 1
    return results

if __name__ == "__main__":
    print(parse("தஞ்சாவூர் தமிழ்  என்பது தமிழகத்தின் மத்திய பகுதிகளான தஞ்சாவூர், திருவாரூர், நாகப்பட்டினம், மயிலாடுதுறை காரைக்கால் மற்றும் திருச்சி மாவட்டங்களில் பேசப்படும் பேச்சு மொழியாகும்"))
