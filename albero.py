class StrutturaMappa():
    def __init__(self):
        self.mappa = dict()
    
    def aggiungiVia(self, viaInput):
        # inserisce nodo senza collegamento e senza peso
        self.mappa.update({viaInput : {'':0}})
    
    def aggiungiCollegamento(self, viaPartenza, viaArrivo, pesoArco):
        # Aggiorna il nodo con il valore uguale a viaPartenza
        # se non esiste, ne crea uno nuovo
        self.mappa.update({viaPartenza: {viaArrivo : pesoArco}})
    
    def visualizzaMappa(self):
        for strade in self.mappa:
            print(strade)

mappa = StrutturaMappa()
mappa.aggiungiVia("Via matteo renato")
mappa.aggiungiVia("Via Lussemburgo")
mappa.aggiungiVia("Via degli Aviatori")

mappa.visualizzaMappa()