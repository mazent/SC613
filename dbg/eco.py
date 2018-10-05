#! /usr/bin/env python

"""
    Racchiude tutto quanto serve per la prova dell'eco
    L'applicazione deve avere:
        *) Un bottone per iniziare e terminare la prova
        *) Una edit col numero di prove
        *) Una etichetta per i messaggi
        *) Una progressbar
        *) Una coda dove inviare i messaggi di aggiornamento grafica ...
        *) ... e le funzioni che gestiscono i messaggi:
              *) ecoFinePerErrore(quanti)
              *) ecoInfinito()
              *) ecoFinito(quanti)
           Queste funzioni devono invocare quelle omonime dell'oggetto passando
           il dispositivo
"""

import threading
import time

import utili


class ECO(object):

    def __init__(self, bottone,
                 numeco,
                 msg,
                 progBar,
                 coda):
        self.bottone = bottone
        self.numEco = numeco
        self.msg = msg
        self.progBar = progBar
        self.coda = coda

        self.continuaEco = False

        self.ecoConta = 0
        self.ecoTot = 0
        self.ecoInizio = 0
        self.ecoMux = threading.Lock()

        self.timerEco = None
        self.durataTimer = None

    def aggiornaEco(self):
        if self.continuaEco:
            self.ecoMux.acquire()
            durata = time.clock() - self.ecoInizio
            self.ecoMux.release()

            self.msg.set(utili.stampaDurata(int(round(durata * 1000.0, 0))))

            self.timerEco = self.bottone.after(
                self.durataTimer, self.aggiornaEco)
        else:
            self.bottone.after_cancel(self.timerEco)

    # GUI

    def Bottone(self):
        if "Basta" == self.bottone["text"]:
            self.continuaEco = False
            self.bottone.after_cancel(self.timerEco)
        else:
            esito, quanti = utili.validaCampo(self.numEco.get(), None, None)
            if esito:
                self.continuaEco = True
                self.bottone["text"] = "Basta"

                self.msg.set("Aspetta ...")

                if quanti < 0:
                    self.coda.put(("ecoFinePerErrore", self, -quanti))
                elif 0 == quanti:
                    self.coda.put(("ecoInfinito", self))
                else:
                    self.coda.put(("ecoFinito", self, quanti))

                # Imposto un timer per le prove lunghe
                self.durataTimer = 60 * 1000
                self.timerEco = self.bottone.after(
                    self.durataTimer, self.aggiornaEco)
            else:
                self.msg.set("Quanti echi ???")

    # Esegui

    def ecoFinePerErrore(self, quanti, dispo):
        self.progBar.start(10)

        self.ecoConta = 0
        self.ecoTot = 0

        self.ecoInizio = time.clock()
        while self.ecoConta < quanti and self.continuaEco:
            self.ecoMux.acquire()
            self.ecoTot += 1

            if not dispo.Eco():
                self.ecoConta += 1
            self.ecoMux.release()

        self.continuaEco = False
        durata = time.clock() - self.ecoInizio
        sdurata = utili.stampaDurata(int(round(durata * 1000.0, 0)))

        if 0 == self.ecoConta:
            milli = round(1000.0 * durata / self.ecoTot, 3)
            self.msg.set(
                "Eco: OK %d in %s (%.3f ms)" %
                (self.ecoTot, sdurata, milli))
        else:
            self.msg.set(
                "Eco: %d errori su %d [%s]" %
                (self.ecoConta, self.ecoTot, sdurata))

        self.progBar.stop()
        self.bottone["text"] = "Eco"

    def ecoInfinito(self, dispo):
        self.progBar.start(10)

        self.ecoConta = 0
        self.ecoTot = 0

        self.ecoInizio = time.clock()
        while self.continuaEco:
            self.ecoMux.acquire()
            self.ecoTot += 1

            if dispo.Eco():
                self.ecoConta += 1
            self.ecoMux.release()

        durata = time.clock() - self.ecoInizio
        sdurata = utili.stampaDurata(int(round(durata * 1000.0, 0)))

        if self.ecoConta == self.ecoTot:
            milli = round(1000.0 * durata / self.ecoConta, 3)
            self.msg.set(
                "Eco: OK %d in %s (%.3f ms)" %
                (self.ecoConta, sdurata, milli))
        elif 0 == self.ecoConta:
            self.msg.set("Eco: ERR %d in %s" % (self.ecoTot, sdurata))
        else:
            self.msg.set(
                "Eco: OK %d / %d in %s" %
                (self.ecoConta, self.ecoTot, sdurata))

        self.progBar.stop()
        self.bottone["text"] = "Eco"

    def ecoFinito(self, quanti, dispo):
        self.progBar.start(10)

        self.ecoConta = 0
        self.ecoTot = 0

        self.ecoInizio = time.clock()
        while self.ecoTot < quanti and self.continuaEco:
            self.ecoMux.acquire()
            self.ecoTot += 1

            if dispo.Eco():
                self.ecoConta += 1
            self.ecoMux.release()

        self.continuaEco = False
        durata = time.clock() - self.ecoInizio
        sdurata = utili.stampaDurata(int(round(durata * 1000.0, 0)))

        if self.ecoConta == self.ecoTot:
            milli = round(1000.0 * durata / self.ecoConta, 3)
            self.msg.set(
                "Eco: OK %d in %s (%.3f ms)" %
                (self.ecoConta, sdurata, milli))
        elif 0 == self.ecoConta:
            self.msg.set("Eco: ERR %d in %s" % (self.ecoTot, sdurata))
        else:
            self.msg.set(
                "Eco: OK %d / %d in %s" %
                (self.ecoConta, self.ecoTot, sdurata))

        self.progBar.stop()
        self.bottone["text"] = "Eco"
