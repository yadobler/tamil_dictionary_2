import csv
from collections import defaultdict

with open("./database/train.csv") as f:
    a = csv.DictReader(f)
    b = [x for x in a]

m_count = defaultdict(int)
n = 2
for x in b:
    text_padded = "$" * (n-1) + x["text"]
    for i in range(len(text_padded)):
        m_count[text_padded[i:i+n]] += 1 

m_top = sorted(m_count.keys(), reverse=True)

for i in range(10):
    print(m_top[i], m_count[m_top[i]])
