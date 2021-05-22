# -*- coding: utf-8 -*-
import json
f=open("res/datasetSymptomsIT.json")
y =f.read()

datasint = json.loads(y)


sintomi = {}
contatoresintomi = 0;

for sintomo in datasint:
    sintomi[sintomo["url"]] = sintomo["name"]
    contatoresintomi += 1;
f.close()


listaSintomiUtente = ["http://www.symcat.com/symptoms/sharp-abdominal-pain",
                      "http://www.symcat.com/symptoms/groin-mass",
                      "http://www.symcat.com/symptoms/ache-all-over"]


f=open("res/datasetConditionsIT.json")

x =f.read()

dataMalattie = json.loads(x)


listaMalattie = []
print(len(dataMalattie))

for sintomo in listaSintomiUtente:
    for malattia in dataMalattie:
        contatore = 0
        trovato = False
        for contatore in range(len(malattia['symptoms'])):
            if(sintomo == malattia['symptoms'][contatore]['name']):
                trovato = True
        if(trovato == False):
            dataMalattie.remove(malattia)
         
                

print(len(dataMalattie))
for malattia in dataMalattie:
    print(malattia['url'])
        