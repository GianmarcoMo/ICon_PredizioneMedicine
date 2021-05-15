# -*- coding: utf-8 -*-

# Costante per la directory dei dataset
DATASET_PATH = 'dataset/'

# Librerie varie
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix
import seaborn as sns

# df = datasetDisease
# df1 = datasetGravita
# d = datasetCodifica 

# Lettura del dataset
datasetDisease = pd.read_csv( DATASET_PATH + 'datasetEsempi.csv')

# ---------------------------------------------------
# Output dei primi 10 esempi del dataset
#print(datasetDisease.head(10))

# ---------------------------------------------------
# Lettura file gravita' sintomi
datasetGravita = pd.read_csv(DATASET_PATH + 'gravitaSintomi.csv')
#print(datasetGravita.head())

# ---------------------------------------------------
# Rimuovo lo spazio finale dalla colonna dei sintomi
cols = datasetDisease.columns
data = datasetDisease[cols].values.flatten()

s = pd.Series(data)
s = s.str.strip()
s = s.values.reshape(datasetDisease.shape)

datasetDisease = pd.DataFrame(s, columns=datasetDisease.columns)
#print(datasetDisease.head())

# ---------------------------------------------------
# Sostituisco i valore NaN con lo zero
datasetDisease = datasetDisease.fillna(0)
#print(datasetDisease.head())

# ---------------------------------------------------
# Codifica dei sintomi nel dataset con la gravita' dei sintomi
vals = datasetDisease.values
symptoms = datasetGravita['Symptom'].unique()

for i in range(len(symptoms)):
    vals[vals == symptoms[i]] = datasetGravita[datasetGravita['Symptom'] == symptoms[i]]['weight'].values[0]
    
datasetCodifica = pd.DataFrame(vals, columns=cols)
#print(datasetCodifica.head())

# Alcuni sintomi non hanno una gravita',
# quindi andiamo a sostituire il loro valore (stringa) con il numero 0
datasetCodifica = datasetCodifica.replace('dischromic _patches', 0)
datasetCodifica = datasetCodifica.replace('spotting_ urination',0)
datasetDisease = datasetCodifica.replace('foul_smell_of urine',0)
#print(datasetDisease.head())

# ---------------------------------------------------
# Seleziono la gravita' dei sintomi
gravSintomi = datasetDisease.iloc[:,1:].values

# Seleziono le malattie
nomeMalattie = datasetDisease['Disease'].values

# ---------------------------------------------------
# Effettuo divisione dataset per training e test
# Grandezza insieme di training 90
x_train, x_test, y_train, y_test = train_test_split(gravSintomi, nomeMalattie, shuffle=True, train_size = 0.90)
#print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)

gnb = GaussianNB()
gnb.fit(x_train,y_train)

preds = gnb.predict(x_test)
#print(x_test[0])
#print(preds[0])

conf_mat = confusion_matrix(y_test, preds)
df_cm = pd.DataFrame(conf_mat, index=datasetDisease['Disease'].unique(), columns=datasetDisease['Disease'].unique())
print('F1-score% =', f1_score(y_test, preds, average='macro')*100, '|', 'Accuracy% =', accuracy_score(y_test, preds)*100)

sns.heatmap(df_cm)
