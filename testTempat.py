from BahasBali.NER import Name,Time,Location
from BahasBali.Stemmer.StemmerFactory import StemmerFactory
import unidecode
import os
import pandas as pd
import nltk

stem = StemmerFactory().create_stemmer()

sentence = []
with open('text.txt', encoding='utf8') as f:
  for line in f:
    if line.strip() != '':
      sentence.append(line.strip())

sentence = unidecode.unidecode(" ".join(sentence))

loc = Location.ner_location(sentence)
print(loc)