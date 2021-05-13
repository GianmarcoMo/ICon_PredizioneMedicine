import json
f=open("datasetMedicinaliFinali.json")
y =f.read()

datamedicinali = json.loads(y)

medicinali = {}

for medicine in datamedicinali:
    medicinali[medicine["Manufacturer"]] = medicine["Composition"]
    
for medicine in medicinali:
    print ("\n" + medicine)