# -*- coding: utf-8 -*-

import json
from nltk.tokenize import word_tokenize
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler
import telegram

def conferma():
    return sintomi.get(test.getStato()[0])
class jsonButton:
    def __init__(self):
        self.stati = list()
    def getStato(self):
        return self.stati
    def nuovoStato(self):
        self.stati = list()
    
class classeSintomo:
    def __init__(self, url, sinonimiInput, nomeIt, descInput, linkWiki):
        self.url = url
        self.sinonimi = sinonimiInput
        self.nomeIT = nomeIt
        self.descrizione = descInput
        self.linkWiki = linkWiki
        
    def setUrl(self, url):
        self.url = url
    def setSinonimi(self, listaSinonimi):
        self.sinonimi = listaSinonimi
    def setNomeIT(self, nomeItaliano):
        self.nomeIT = nomeItaliano
    def setDescrizione(self, descInput):
        self.descrizione = descInput
    
    def getNome(self):
        return self.nomeIT
    def getUrl(self):
        return self.url
    def getSinonimi(self):
        return self.sinonimi
    def getDescrizione(self):
        return self.descrizione
    def getLinkWiki(self):
        return self.linkWiki
 
sw_list = {"ho","mi","sento","oggi","stamattina","prima","avevo","avuto"}

f=open("res/datasetSymptomsIT.json")
y =f.read()

datasint = json.loads(y)

sintomi = {}
contatoresintomi = 0

for sintomo in datasint:
    sintomi[sintomo["url"]] = classeSintomo(sintomo["url"], sintomo['senses'], sintomo['name'], sintomo['descriptions'], sintomo.get('link'))
    contatoresintomi += 1;
f.close()
test = jsonButton()

def buttonCallback(update, context, listaSintomiDefinitiva):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Ho trovato diversi sintomi: ')
    test.nuovoStato()
    keyboard = []
    for sintomo in listaSintomiDefinitiva:
        test.getStato().append(sintomo.getUrl())
        keyboard.append([InlineKeyboardButton(sintomo.getNome(), callback_data = sintomo.getUrl())])
        
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text('Scegli uno tra questi:', reply_markup=reply_markup)


def riconoscimentoSintomo(inputSintomo,update, context, dispatcher, updater):
    inputSintomo = inputSintomo.lower()
    #Tokenize input
    text_tokens = word_tokenize(inputSintomo)
    #Tokenize input ed eliminazione stopwords
    tokens_without_sw = [word for word in text_tokens if not word in sw_list]
    inputSintomo = ''
    #Ricompongo stringa utente stenza sw
    for token in tokens_without_sw:
        inputSintomo += token + ' '
    #elimino spazio finale del for
    inputSintomo = inputSintomo[:-1]
    if (inputSintomo == ''):
         context.bot.send_message(chat_id=update.effective_chat.id, text='Non ho trovato nessun sintomo corrispondente alla tua descrizione. \nPotresti essere più preciso?')
         return '0'
    listaSintomiDefinitiva = list()
    
    for sintomo in sintomi: # per ogni sintomo in malattia
        trovato = False
        if(inputSintomo in sintomi[sintomo].getNome().lower() or inputSintomo == sintomi[sintomo].getUrl().lower()): # Se l'input è nel nome, segnamo il trovato su true.
            trovato = True
        else:
            for sinonimo in sintomi[sintomo].getSinonimi(): # Se l'input non è nel nome, cerchiamo nei sinonimi
                if(inputSintomo in sinonimo.lower()):
                    trovato = True
                    break
            # Se l'input non è nei sinonimi, cerchiamo nella descrizione
            if(trovato == False and inputSintomo in sintomi[sintomo].getDescrizione()):
                trovato = True
            
        # Se il sintomo è stato trovato, inseriamo il vero nome del sintomo in una lista.
        if(trovato):
            listaSintomiDefinitiva.append(sintomi[sintomo])
        
    if(len(listaSintomiDefinitiva) > 1):
            context.bot.send_message(chat_id=update.effective_chat.id, text='/risultato')
            updater.dispatcher.add_handler(CommandHandler('risultato', buttonCallback(update, context, listaSintomiDefinitiva)))
            
            return '0' 
    else:
        if (len(listaSintomiDefinitiva) == 0):
            #print('Non ho trovato nessun sintomo corrispondente alla tua descrizione. \nPotresti essere più preciso?')
            context.bot.send_message(chat_id=update.effective_chat.id, text='Non ho trovato nessun sintomo corrispondente alla tua descrizione. \nPotresti essere più preciso?')
            return '0'
    
    #Quando la lista è formata da solo un sintomo
    return listaSintomiDefinitiva[0]
    
class Malattia:
    def __init__(self, malattiaInput, descInput, linkInput, listaSintomi):
        self.nomeMalattia = malattiaInput
        self.descrizione = descInput
        self.linkWiki = linkInput
        self.sintomi = listaSintomi
        
    def getNome(self):
        return self.nomeMalattia 
    def getDescrizione(self):
        return self.descrizione 
    def getLinkWiki(self):
        return self.linkWiki
    def getListaSintomi(self):
        return self.sintomi

def predizioneMalattiaBayes(listaSintomiUtente):
    f=open("res/datasetConditionsIT.json")
    
    x =f.read()
    
    data = json.loads(x)
    
    listaMalattie = {}
    
    for malattia in data:
        listaMalattie[malattia["name"]] = Malattia(malattia['name'], malattia['descriptions'], malattia.get('wikipedia'), malattia.get('symptoms'))
        
    f.close()

    risultati = {}
    for malattia in data:
        probabilita = 1;
        denominatore = 0;
        sintomimatchati = 0
        
        for sintomoMalattia in malattia["symptoms"]:  
            for sintomoutente in listaSintomiUtente:
                if (sintomoutente.getUrl() == sintomoMalattia["name"]):
                    probabilita = probabilita * sintomoMalattia["probability"] /100 
                    denominatore += probabilita
                    sintomimatchati += 1
                    
        if (denominatore != 0):
            probabilita += sintomimatchati
            risultati[malattia["name"]] = probabilita/(denominatore + contatoresintomi)
            
    maxProbability = max(risultati, key=risultati.get) # Just use 'min' instead of 'max' for minimum.
    
    return listaMalattie.get(maxProbability)

def predizioneMalattiaAlbero(listaSintomiUtente):
    f=open("res/datasetConditionsIT.json")
    
    x =f.read()
    
    dataMalattie = json.loads(x)
    
    listaMalattie = {}
    
    for malattia in dataMalattie:
        listaMalattie[malattia["name"]] = Malattia(malattia['name'], malattia['descriptions'], malattia.get('wikipedia'),  malattia.get('symptoms'))
        
    f.close()
    
    listacopia = listaMalattie.copy()
    dataMalattie = listaMalattie.copy()
    
    for sintomoutente in listaSintomiUtente:
        for malattia in dataMalattie:
            trovato = False
            for sintomo in dataMalattie[malattia].getListaSintomi():
                if sintomo["name"] == sintomoutente.getUrl():
                    trovato = True
            if trovato == False:      
                listacopia.pop(malattia)
        dataMalattie = listacopia.copy()
              
    dictMalattia = {}
            
    for malattia in dataMalattie:
        risultato = 1
        for sintomo in dataMalattie[malattia].getListaSintomi():
            for sintomoUtente in listaSintomiUtente:
                if (sintomo['name'] == sintomoUtente.getUrl()):
                    risultato += sintomo["probability"]
        dictMalattia[dataMalattie[malattia]] = risultato
        
        
    if (len(dictMalattia)==0):
        return 0
    #print(sorted(dictMalattia.items() , key=lambda x: x[1]))
    
    maxProbability = max(dictMalattia, key=dictMalattia.get)
    return maxProbability
