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

sentence = " ".join(sentence)
print(sentence)
tokoh = Name.ner_name(sentence)
print(tokoh)
time = Time.ner_time(sentence.lower())
print(time)
loc = Location.ner_location(sentence)
print(loc)

df = pd.read_excel("data.xlsx")
df['satwa_text'] = df['satwa_text'].apply(unidecode.unidecode)

readWaktu = lambda x:Time.ner_time(x.lower())
df['ptokoh']  = df['satwa_text'].apply(Name.ner_name)
df['pwaktu']  = df['satwa_text'].apply(readWaktu)
df['plokasi'] = df['satwa_text'].apply(Location.ner_location)

splitKoma = lambda x:x.split(",")
df['tokoh']   = df['tokoh'].apply(splitKoma)
df['waktu']   = df['waktu'].apply(splitKoma)
df['lokasi']  = df['lokasi'].apply(splitKoma)

df.to_excel("afterPredict.xlsx",index=False)

TP = 0
TN = 0
FP = 0
FN = 0
for i in range(len(df)):
  data = df.iloc[i,:]
  TPa = 0
  FPa = 0
  for d in data['ptokoh']:
    indexList = [nltk.edit_distance(d.lower(), x.lower().strip()) for x in data['tokoh']]
    if 3>min(indexList):
      TPa +=1
    else:
      FPa +=1
  #print("Akurasi Tokoh",data['satwa_judul'],":",TPa/(TPa+FPa))
  TP += TPa
  FP += FPa
  TPa = 0
  FPa = 0
  
  for d in data['pwaktu']:
    indexList = [nltk.edit_distance(d.lower(), x.lower().strip()) for x in data['waktu']]
    if 3>min(indexList):
      TPa +=1
    else:
      FPa +=1
  #print("Akurasi Waktu",data['satwa_judul'],":",TPa/(TPa+FPa))
  TP += TPa
  FP += FPa
  TPa = 0
  FPa = 0

  for d in data['plokasi']:
    indexList = [nltk.edit_distance(d.lower(), x.lower().strip()) for x in data['lokasi']]
    if 3>min(indexList):
      TPa +=1
    else:
      FPa +=1
  #print("Akurasi Lokasi",data['satwa_judul'],":",TPa/(TPa+FPa))
  TP += TPa
  FP += FPa
  #input()

print("Akurasi:",(TP+TN)/(TP+TN+FP+FN))