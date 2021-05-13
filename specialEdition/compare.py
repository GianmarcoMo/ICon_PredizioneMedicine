import json


y=open('malattie.json')
s= y.read()

datamalattie= json.loads(s)
y.close()


x=open('datasetConditionsIT.json')
z= x.read()
datasintomi= json.loads(z)
x.close()



u=open('Medicine_details.json')
h= u.read()
datamedicinali= json.loads(h)
u.close()

datafinalemalattie = []
datafinalemedicnali = []
datamalattie = []

for malattia in datamalattie:
    for sintomi in datasintomi:
        if ( malattia["Ita"].lower() in sintomi["url"].lower() or 
            malattia["Ita"].lower() in sintomi["name"].lower() or
            malattia["Ita"].lower() in sintomi["senses"].lower() or
            malattia["Eng"].lower() in sintomi["url"].lower() or 
            malattia["Eng"].lower() in sintomi["name"].lower() or
            malattia["Eng"].lower() in sintomi["senses"].lower()):
            datafinalemalattie.append(malattia["Eng"])
            datamalattie.append(sintomi)
            print("WE MAURO")
            
            
            
for medicinale in datamedicinali:
    for malattia in datafinalemalattie:
        if (medicinale["Manufacturer"] == malattia):
            datafinalemedicnali.append(medicinale)

with open("datasetMedicinaliFinali.json", "w") as write_file:
    json.dump(datafinalemedicnali, write_file)

with open("datasetConditionsFinali.json", "w") as write_file:
    json.dump(datamalattie, write_file)