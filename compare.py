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

datafinalemalattie= []
datafinalemedicnali=[]


for malattia in datamalattie:
    for sintomi in datasintomi:
        if ( malattia["Ita"].lower() in sintomi["url"] or 
            malattia["Ita"].lower() in sintomi["name"] or
            malattia["Ita"].lower() in sintomi["senses"] or
            malattia["Eng"].lower() in sintomi["url"] or 
            malattia["Eng"].lower() in sintomi["name"] or
            malattia["Eng"].lower() in sintomi["senses"]):
            datafinalemalattie.append(malattia["Eng"])
            
for medicinale in datamedicinali:
    for malattia in datafinalemalattie:
        if (medicinale["Manufacturer"] == malattia):
            datafinalemedicnali.append(medicinale)

with open("datasetMedicinaliFinali.json", "w") as write_file:
    json.dump(datafinalemedicnali, write_file)

