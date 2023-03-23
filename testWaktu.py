from BahasBali.NER import Name,Time,Location
import unidecode
import os
import pandas as pd
import nltk

sentence = []
with open('text.txt', encoding='utf8') as f:
  for line in f:
    if line.strip() != '':
      sentence.append(line.strip())

sentence = unidecode.unidecode(" ".join(sentence))

time = Time.ner_time(sentence.lower())
print(time)