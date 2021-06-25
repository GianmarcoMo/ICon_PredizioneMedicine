# ICon_PredizioneMedicine

![https://www.uniba.it/bibliotechecentri/farmacia/Logo%20Uniba%20Aldo%20Moro.jpg](https://www.uniba.it/bibliotechecentri/farmacia/Logo%20Uniba%20Aldo%20Moro.jpg)

# Indice
1. [Introduzione](#Introduzione)
2. [Requisiti specifici](#Requisiti-specifici)
3. [System Design](#System-Design)
4. [Esempio pratico](#Esempio-pratico)

# Introduzione

**ProgettoIConBot** è un chatbot progettato per l'assistenza sanitaria agli anzini e non, per aiutare l'utente ad individuare, sulla base dei sintomi risontrati, la più probabile malattia **associata** ai sintomi. 

Il progetto è stato sviluppato da 3 ragazzi del terzo anno di **"Informatica" dell'Università degli studi di Bari Aldo Moro** durante **l'A.A. 2020/21**

- Gaetano Dibenedetto
- Mauro Andretta
- Gianmarco Moresi

# Requisiti specifici

## Requisiti per l'utente

- Un account **Telegram**
- Digitare `@ProgettoIConBot` nella barra di ricerca e avviare il bot

## Requisiti per lo sviluppatore

- Account **Telegram** per il testing
- Token per l'accesso HTTP API generato da **BotFather**
- Python 3 e repository GitHub

## Librerie utilizzate

- **python-telegram-bot**
- **telegram** (InlineKeyboardButton, InlineKeyboardMarkup)
- **telegram.ext** (*Updater, CommandHandler, MessageHandler, Filters*)
- **nltk.tokenize** (*word_tokenize*)
- **json**

# System Design

## Server Telegram Python

Il lato server per l'acquisizione dei sintomi e l'avvio del bot è gestito dal codice scritto in Python.

### Avvio chatbot

L'avvio viene eseguito tramite **l'inserimento del token** generato tramite **BotFather su Telegram** dopo aver creato il "profilo" del bot su telegram stesso, registrando il nome.

### Acquisizone sintomi

L'utente, avvia la chat con il bot tramite il pulsante grafico predisposto da telegram stesso o tramite il comando "/start", successivamente dovrà scegliere che tipo di predizione delle malattie vorrà utlizzare, qui abbiamo due scelte tra cui "Avvia predizione tramite metodo Bayesiano" ed "Avvia predizione tramite ricerca ad albero". Quando si seleziona uno dei due pulsanti verrà chiesta un ulteriore conferma per la scelta del metodo che è possibile effettuare interagendo con il bot. Come suggerito dal bot è sempre possibile, anche in questa fase di conferma, il riavvio del bot attraverso il comando "/restart".

Dopodichè i sintomi vengono gestiti tramite un algoritmo che processa i sintomi prima effettuando la tokenizzazione della frase scritta dall'utente e poi avviene la ricerca all'interno del dataset, dopo aver trovato il sintomo nel dataset, viene creato un oggetto contenente tutti i dettagli di quel sintomo.

### Predizione malattia metodo Bayesiano

Dopo aver indicato tutti i sintomi da parte dell'utente, viene effettuata la predizione tramite il **metodo Bayesiano** sul dataset presente nel progetto. Dopo aver eseguito il calcolo, il chatbot restituisce la malattia predetta.

### Predizione malattia tramite ricerca su albero

Dopo aver indicato tutti i sintomi da parte dell'utente, viene effettuata la predizione tramite una **struttura ad albero**, infatti partendo dal dataset iniziale delle malattia questo verrà di volta in volta ridotto in base ai sintomi selezionati. Una volta arrivato ad un nodo foglia avremo l'output. Potrebbe capitare che l'albero di decisione non porti a nessun output, in tal caso viene mostrato la predizione utilizzando il metodo Bayesiano

# Esempio pratico

## Esempio 1

<img src="documentazioneMedia/35739CE8-BF14-42E1-8FEE-9B4811669F12.jpeg" alt="drawing" width="400"/>

## Esempio 2

<img src="documentazioneMedia/9807754B-1DA4-49EA-99E9-0EB425CF4A2C.jpeg" alt="drawing" width="400"/>

## Esempio 3

<img src="documentazioneMedia/B2AF7AFD-D75A-4E13-A834-2CB254EF9159.jpeg" alt="drawing" width="400"/>
<img src="documentazioneMedia/B2AF7AFD-D75A-4E13-A834-2CB254EF9159part2.jpeg" alt="drawing" width="400"/>
