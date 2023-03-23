from BahasBali.NER import Name,Time,Location
import unidecode
import os
import pandas as pd
import nltk

df = pd.read_excel("data.xlsx")

df['unisatwa_text'] = df['satwa_text'].apply(unidecode.unidecode)
df['unitokoh'] = df['tokoh'].apply(unidecode.unidecode)

df['ptokoh']  = df['unisatwa_text'].apply(Name.ner_name)

def splitKoma(x):
  try:
    return [a.strip() for a in x.split(",")]
  except:
    pass
df['unitokoh']   = df['unitokoh'].apply(splitKoma)

TP = 0
TN = 0
FP = 0
FN = 0
lessThan = []
for i in range(len(df)):
  data = df.iloc[i,:]
  TPa = 0
  FPa = 0

  label = Name.delCommonName(data['unitokoh'])
  pred  = Name.delCommonName(data['ptokoh'])

  for d in pred:
    if d != '':
      indexList = [nltk.edit_distance(d.lower(), x.lower().strip()) for x in label]
      if 3>min(indexList):
        TPa +=1
      else:
        FPa +=1
  
  if TPa/(TPa+FPa)<0.6:
    lessThan.append(i)
    if TPa/(TPa+FPa)<0.5:
      print("==================================")
      print("Data Ke-",i,TPa,FPa)
      print(TPa/(TPa+FPa))
      print(data['unitokoh'])
      print(data['ptokoh'])
      print(label)
      print(pred)
      print("==================================")
  #print("Akurasi Tokoh",data['satwa_judul'],":",TPa/(TPa+FPa))
  TP += TPa
  FP += FPa

print("Akurasi Tokoh:",(TP+TN)/(TP+TN+FP+FN))