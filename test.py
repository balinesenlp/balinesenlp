from BahasBali.NER import Name,Time,Location
import
import unidecode
import os

sentence = []
with open('text.txt', encoding='utf8') as f:
  for line in f:
    if line.strip() != '':
      sentence.append(line.strip())

sentence = " ".join(sentence)
print(sentence)
tokoh = Name.ner_name(sentence)
print(tokoh)
time = Time.ner_time(sentence.lower())
print(time)
loc = Location.ner_location(sentence)
print(loc)


# sentence = ""