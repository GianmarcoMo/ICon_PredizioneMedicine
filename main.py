import json
import operator
f=open("res/datasetSymptomsIT.json")
y =f.read()

datasint = json.loads(y)


sintomi = {}
contatoresintomi = 0;

for sintomo in datasint:
    sintomi[sintomo["url"]] = sintomo["name"]
    contatoresintomi += 1;
f.close()


listaSintomiUtente = ["http://www.symcat.com/symptoms/skin-lesion",
                      "http://www.symcat.com/symptoms/skin-on-leg-or-foot-looks-infected",
                      "http://www.symcat.com/symptoms/skin-pain"]


f=open("res/datasetConditionsFinaliCodiceMalattia.json")

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
        risultati[malattia["Manufacturer"]] = probabilita/(denominatore + contatoresintomi)
        


maxProbability = max(risultati, key=risultati.get)  # Just use 'min' instead of 'max' for minimum.

print(maxProbability)


z=open("res/datasetMedicinaliFinalilower.json")

h =z.read()

dataMedicinali = json.loads(h)

dictMedicinali = {}

for medicina in dataMedicinali:
    if (medicina["Manufacturer"])== maxProbability:
        prezzomrp = {}
        prezzomrp["Price"] = medicina["Best Price"]
        prezzomrp["MRP"] = medicina["MRP"]
        dictMedicinali[medicina["Medicine Name"]] = prezzomrp

             


        
maxMRP = 0





