# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
import telegram
import logging

import riconoscimentoSintomi
import aStarMatrice

# Lettura file per token
f = open("token", "r")

tokenFile = f.read()

f.close()

class Sistema:
    def __init__(self):
        self.statoSistema = 0
    def setBayes(self):
        self.statoSistema = 1
    def setAlbero(self):
        self.statoSistema = 2
    def getStato(self):
        return self.statoSistema
    def reset(self):
        self.statoSistema = 0

class Persona:
    def __init__(self):
        self.statoSintomi = False
        self.nome = ''
        self.cognome = ''
        self.eta = 0
        self.sintomi = list()
        self.riconocimento = '0'
        
    def cambiaStatoSintomi(self):
        if(self.statoSintomi):
            # Si attiva l'acquisizione dei sintomi
            self.statoSintomi = False
        else: 
            # Si disattiva l'acquisizione dei sintomi
            self.sintomi = list()
            self.statoSintomi = True

    def inserisciNome(self, nome):
        self.nome = nome

    def inserisciCognome(self, cognome):
        self.cognome = cognome
        
    def inserisciEta(self, eta):
        self.eta = eta
    
    def getStato(self):
        return self.statoSintomi

    def getSintomi(self):
        return self.sintomi
    
    def getRiconoscimento(self):
        return self.riconocimento
    
    def SetRiconoscimento(self,inpututente):
        self.riconocimento = inpututente
   

def echo(update, context):
    messaggioUtente = update.message.text
    
    if(sistema.getStato() != 0):  
        if("mostra" in messaggioUtente.lower() and "sintomi" in messaggioUtente.lower()):
            if (len(utente.getSintomi())!=0):
                mostraChatSintomiAcquisiti(update, context)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Scusami, non ho ancora compreso nessun sintomo")
        
        elif(messaggioUtente.lower() == 'no' or messaggioUtente.lower() == 'stop' or messaggioUtente.lower()=="non ho altri sintomi"):
            #se abbiamo acquisito sintomi
            if (len(utente.getSintomi())!=0):
                
                mostraChatSintomiAcquisiti(update, context)
                context.bot.send_message(chat_id=update.effective_chat.id, text="Ora controllo cosa hai...")
                
                # predizione malattia
                if(sistema.getStato() == 1):
                    risultato = riconoscimentoSintomi.predizioneMalattiaBayes(utente.getSintomi())
                elif(sistema.getStato() == 2):
                    risultato = riconoscimentoSintomi.predizioneMalattiaAlbero(utente.getSintomi())
                    
                if (risultato == 0)    :
                    context.bot.send_message(chat_id=update.effective_chat.id, text="Con i dati che mi hai fornito con il sistema ad albero non sono riuscito a trovare una malattia nel database")
                    context.bot.send_message(chat_id=update.effective_chat.id, text="Effettuo comunque una predizione con il metodo Bayesiano")
                    risultato = riconoscimentoSintomi.predizioneMalattiaBayes(utente.getSintomi())

                context.bot.send_message(chat_id=update.effective_chat.id, text=f"Secondo i dati che miei fornito potresti avere: *{risultato.getNome()}*", parse_mode=telegram.ParseMode.MARKDOWN)
                # Fine predizione 
                
                if (risultato.getLinkWiki()!=None):
                    context.bot.send_message(chat_id=update.effective_chat.id, text=risultato.getLinkWiki())
                else:
                     context.bot.send_message(chat_id=update.effective_chat.id, text=risultato.getDescrizione()[0])
                
                context.bot.send_message(chat_id=update.effective_chat.id, text="Predizione conclusa, digita o premi */restart* per riavviare", parse_mode=telegram.ParseMode.MARKDOWN)
                context.bot.send_message(chat_id=update.effective_chat.id, text="Oppure se vuoi avere info sull'ambulanza digita o premi /chiediAmbulanza", parse_mode=telegram.ParseMode.MARKDOWN)

                # Reset lista sintomi acquisita e cambio stato
                utente.cambiaStatoSintomi()
            else:
                #se abbiamo acquisito sintomi
                context.bot.send_message(chat_id=update.effective_chat.id, text="Scusami, non ho ancora compreso nessun sintomo, non posso avviare la predizione della malattia. \nQuale sintomo credi di avere?")
                utente.SetRiconoscimento('0')
    
        else:
            if(messaggioUtente.lower() == 'si'):
                 context.bot.send_message(chat_id=update.effective_chat.id, text="Cos'altro credi di avere?")
                 utente.SetRiconoscimento('0')
            elif(messaggioUtente.lower() == 'conferma'):
                utente.getSintomi().append(riconoscimentoSintomi.conferma())
                                
                context.bot.send_message(chat_id=update.effective_chat.id, text="Sintomo acquisito correttamente.\nHai altri sintomi?")
                utente.SetRiconoscimento('0')
            else:
                utente.SetRiconoscimento(riconoscimentoSintomi.riconoscimentoSintomo(messaggioUtente,update, context, dispatcher, updater))
                if (utente.getRiconoscimento() != '0'):
                    if(utente.getRiconoscimento() in utente.getSintomi()):
                         context.bot.send_message(chat_id=update.effective_chat.id, text="Sintomo già acquisito in precedenza, inserire un *nuovo sintomo* o digitare *stop*",parse_mode=telegram.ParseMode.MARKDOWN)
                    else:
                        
                        utente.getSintomi().append(utente.getRiconoscimento())
                        context.bot.send_message(chat_id=update.effective_chat.id, text="Sintomo acquisito correttamente.\nHai altri sintomi?")
                    utente.SetRiconoscimento('0')
      

def mostraChatSintomiAcquisiti(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Per adesso i sintomi che ho inserito sono:")
    for sintomo in utente.getSintomi():
         context.bot.send_message(chat_id=update.effective_chat.id, text=f"- {sintomo.getNome()}")    

def gestoreMessaggi():     
    # Comandi sconosciuti
    unknown_handler = MessageHandler(Filters.text & Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)
        
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)   

def start(update, context):
    sistema.reset()
    utente.sintomi = list()
    
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ciao sono il bot per predire malattie in base ai tuoi sintomi.")
    
    keyboard = []
    keyboard.append([InlineKeyboardButton("Avvia predizione tramite metodo Bayesiano", callback_data = "/bayes_method")])
    keyboard.append([InlineKeyboardButton("Avvia predizione tramite ricerca ad albero", callback_data = "/ricerca_albero")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text("Scegli un'opzione tra queste:", reply_markup=reply_markup)
    

def bayes_method(update, context):
    sistema.setBayes()
    context.bot.send_message(chat_id=update.effective_chat.id, text="Dimmi quale sintomo credi di avere")

def ricerca_albero(update, context):
    sistema.setAlbero()
    context.bot.send_message(chat_id=update.effective_chat.id, text="Dimmi quale sintomo credi di avere")
    
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Utilizza solo pulsanti o comandi indicati dal bot.")

def stop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ciao ciao")
    updater.stop()

def chiediAmbulanza(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Vorresti chiamare l'ambulanza?")
    
    keyboard = []
    keyboard.append([InlineKeyboardButton("SI!", callback_data = "si_chiama")])
    keyboard.append([InlineKeyboardButton("NO!", callback_data = "no_chiama")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text("Scegli un'opzione tra queste:", reply_markup=reply_markup)

def risultatoCallBack(update, context):
    cqd = update.callback_query.data
    query = update.callback_query
    query.answer()
    
    if(cqd == "/bayes_method" or cqd == "/ricerca_albero"):
        query.edit_message_text(text="Clicca per confermare: "+ query.data)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Oppure clicca qui per restartare: /restart")
    elif(cqd == "si_chiama"):
        aStarMatrice.ambulanza(update, context)
    elif(cqd == "no_chiama"):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Clicca o digita /restart per confermare")
    else:
        query.edit_message_text(text=f"Digita *{query.data}* per confermare il sintomo", parse_mode=telegram.ParseMode.MARKDOWN)

         
# -------------------------------------------
sistema = Sistema()
utente = Persona()

updater = Updater(token=tokenFile, use_context=True)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('restart', start))
updater.dispatcher.add_handler(CallbackQueryHandler(risultatoCallBack))

updater.dispatcher.add_handler(CommandHandler('chiediAmbulanza', chiediAmbulanza))

updater.dispatcher.add_handler(CommandHandler('bayes_method', bayes_method))
updater.dispatcher.add_handler(CommandHandler('ricerca_albero', ricerca_albero))
updater.dispatcher.add_handler(CommandHandler('stop', stop))

updater.start_polling()

gestoreMessaggi()




