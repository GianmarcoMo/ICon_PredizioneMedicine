import json
f=open("Medicine_details.json")
y =f.read()

datasint = json.loads(y)


sintomi = {}
contatoresintomi = 0;

for sintomo in datasint:
    sintomi[sintomo["Medicine Name"]] = sintomo["Composition"]
    contatoresintomi += 1;
print(contatoresintomi)
f.close()
