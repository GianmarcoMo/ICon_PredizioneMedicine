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
        if ( malattia["Ita"].lower() in sintomi["url"].lower() or 
            malattia["Ita"].lower() in sintomi["name"].lower() or
            malattia["Ita"].lower() in sintomi["senses"] or
            malattia["Eng"].lower() in sintomi["url"].lower() or 
            malattia["Eng"].lower() in sintomi["name"].lower() or
            malattia["Eng"].lower() in sintomi["senses"]):
            sintomi["Manufacturer"] = malattia["Eng"]
            datafinalemalattie.append(sintomi)
            
print(datasintomi[0])


with open("datasetConditionsFinaliCodiceMalattia.json", "w") as write_file:
    json.dump(datafinalemalattie, write_file)