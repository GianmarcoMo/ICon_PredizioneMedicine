import json
f=open("res/datasetSymptomsIT.json")
y =f.read()

datasint = json.loads(y)


sintomi = {}
contatoresintomi = 0;

for sintomo in datasint:
    sintomi[sintomo["url"]] = sintomo["name"]
    contatoresintomi += 1;
print(contatoresintomi)
f.close()


listaSintomiUtente = ["http://www.symcat.com/symptoms/skin-lesion",
                      "http://www.symcat.com/symptoms/skin-on-leg-or-foot-looks-infected",
                      "http://www.symcat.com/symptoms/skin-pain"]


f=open("datasetConditionsIT.json")

x =f.read()

data = json.loads(x)


risultati = {}
for malattia in data:
    probabilita = 1;
    denominatore = 0;
    sintomimatchati = 0
    
    for sintomo in malattia["symptoms"]:  
        for sintomoutente in listaSintomiUtente:
            if (sintomoutente == sintomo["name"]):
                probabilita = probabilita * sintomo["probability"] /100 
                denominatore += probabilita
                sintomimatchati += 1
                
    if (denominatore != 0):
        probabilita += sintomimatchati
        risultati[malattia["name"]] = probabilita/(denominatore + contatoresintomi)


print({k: v for k, v in sorted(risultati.items(), key=lambda item: item[1])})

