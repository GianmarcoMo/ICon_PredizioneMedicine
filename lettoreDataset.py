# -*- coding: utf-8 -*-
import json

def acquisisciDataset(directoryDataset):
    f = open(directoryDataset)
    
    #   creazione di una lista
    listaMalattie = list()
    
    #   per ogni elemento, crea un elmeneto del dizionario con nome malattia e sintomi.
    for elemento in json.loads(f.read()):
        #   nomeMalattia - [sintomo1,sintomo2,ecc...]
        listaMalattie.append({
            'nomeMalattia':elemento['name'],
            'sintomi':elemento['symptoms']
            })       
    
    #   chiusura del file
    f.close()
    return listaMalattie

def visualizzaMalattie(listaMalattie):
    for malattia in listaMalattie:
        print("NOME MALATTIA: ", malattia['nomeMalattia'])
        print('\nSINTOMI:')
        for sintomi in malattia['sintomi']:
            print(sintomi['name']," - ",sintomi['probability'])
        print('\n\n')
    