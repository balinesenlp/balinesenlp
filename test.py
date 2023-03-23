from BahasBali.NER import Name,Time,Location
import unidecode
import os
import pandas as pd
import nltk

# sentence = []
# with open('text.txt', encoding='utf8') as f:
#   for line in f:
#     if line.strip() != '':
#       sentence.append(line.strip())

# sentence = " ".join(sentence)
# print(sentence)
# tokoh = Name.ner_name(sentence)
# print(tokoh)
# time = Time.ner_time(sentence.lower())
# print(time)
# loc = Location.ner_location(sentence)
# print(loc)

df = pd.read_excel("data.xlsx")
df['satwa_text'] = df['satwa_text'].apply(unidecode.unidecode)
df['tokoh'] = df['tokoh'].apply(unidecode.unidecode)

readWaktu = lambda x:Time.ner_time(x.lower())
df['ptokoh']  = df['satwa_text'].apply(Name.ner_name)
df['pwaktu']  = df['satwa_text'].apply(readWaktu)
df['plokasi'] = df['satwa_text'].apply(Location.ner_location)

def splitKoma(x):
  try:
    return [a.strip() for a in x.split(",")]
  except:
    pass
df['tokoh']   = df['tokoh'].apply(splitKoma)
df['waktu']   = df['waktu'].apply(splitKoma)
df['lokasi']  = df['lokasi'].apply(splitKoma)

df.to_excel("afterPredict.xlsx",index=False)

TP = 0
TN = 0
FP = 0
FN = 0
lessThan = []
for i in range(len(df)):
  data = df.iloc[i,:]
  TPa = 0
  FPa = 0
  print(data['tokoh'],data['ptokoh'],type(data['ptokoh']))
  for d in data['ptokoh']:
    print(d)
    indexList = [nltk.edit_distance(d.lower(), x.lower().strip()) for x in data['tokoh']]
    print(indexList)
    if 3>min(indexList):
      TPa +=1
    else:
      FPa +=1
  print(i,TPa,FPa)
  if TPa/(TPa+FPa)<0.6:
    lessThan.append(i)
  #print("Akurasi Tokoh",data['satwa_judul'],":",TPa/(TPa+FPa))
  TP += TPa
  FP += FPa

print("Akurasi Tokoh:",(TP+TN)/(TP+TN+FP+FN))
print(lessThan)

TP = 0
TN = 0
FP = 0
FN = 0
for i in range(len(df)):
  data = df.iloc[i,:]
  TPa = 0
  FPa = 0
  for d in data['pwaktu']:
    indexList = [nltk.edit_distance(d.lower(), x.lower().strip()) for x in data['waktu']]
    if 3>min(indexList):
      TPa +=1
    else:
      FPa +=1
  #print("Akurasi Tokoh",data['satwa_judul'],":",TPa/(TPa+FPa))
  TP += TPa
  FP += FPa

print("Akurasi Waktu:",(TP+TN)/(TP+TN+FP+FN))

TP = 0
TN = 0
FP = 0
FN = 0

for i in range(len(df)):
  data = df.iloc[i,:]
  TPa = 0
  FPa = 0
  for d in data['plokasi']:
    indexList = [nltk.edit_distance(d.lower(), x.lower().strip()) for x in data['lokasi']]
    if 3>min(indexList):
      TPa +=1
    else:
      FPa +=1
  #print("Akurasi Tokoh",data['satwa_judul'],":",TPa/(TPa+FPa))
  TP += TPa
  FP += FPa

print("Akurasi Lokasi:",(TP+TN)/(TP+TN+FP+FN))