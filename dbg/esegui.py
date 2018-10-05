#! /usr/bin/env python

"""
    Per non bloccare la grafica viene creato un task
    che aspetta i comandi e li esegue
"""

from __future__ import print_function

import threading
import math
import time

import cv2
import numpy as np

import gui_support
import utili


IDENT_S = {
    0x43D3212D: 'uLDR',
    0x927BA45B: 'CLDE',
    0x55A682CC: 'CLDF',
    0x65E57C04: 'APPL'
}

IDENT_I = {
    0x43D3212D: '0',
    0x927BA45B: '1',
    0x55A682CC: '2',
    0x65E57C04: '3'
}

def identifica_s(cosa):
    id = None
    try:
        id = IDENT_S[cosa]
    except KeyError:
        if cosa == 0:
            id = '???'
        else:
            id = '%08X' % cosa

    return id

def identifica_i(cosa):
    id = None
    try:
        id = IDENT_I[cosa]
    except KeyError:
        # Esce dall'intervallo della radio
        id = '1000'

    return id


class taskEsecutore(threading.Thread):

    def __init__(self, codaEXE, codaGUI):
        threading.Thread.__init__(self)

        self.coda_exe = codaEXE
        self.coda_gui = codaGUI

        self.dispo = None

        self.comando = {
            'eco': self._eco,
            'revisione': self._revisione,
            'led': self._led,
            'cicalino': self._cicalino,
            'tasto': self._tasto,
            'batLeggi': self._gg_leggi,
            'batScrivi': self._gg_scrivi,
            'reset': self._reset,

            'ecoFinito': self._eco_limite,
            'ecoInfinito': self._eco_8,
            'ecoFinePerErrore': self._eco_fine_x_errore,

            'provaRam': self._provaRam,
            'norCar': self._nor_crt,
            'norCan': self._nor_cancella,
            'norLeggi': self._nor_leggi,
            'norScrivi': self._nor_scrivi,

            'laserI': self._laserI,
            'laserF': self._laserF,
            'laserA': self._laserA,
            'camI': self._camI,
            'camF': self._camF,
            'camL': self._camL,
            'camS': self._camS,
            'camC': self._foto,
            'camPL': self._cam_prm_leggi,
            'camPS': self._cam_prm_scrivi,
            'leggiFoto': self._leggi_foto,
            'las_foto': self._lasera_fotografa,
            'misura': self._misura,

            'btAccendi': self._bt_accendi,
            'btAccendiAuto': self._bt_accendi_auto,
            'btSpegni': self._bt_spegni,
            'btCmd': self._bt_cmd,
            'btFile': self._bt_file,
            'btRic': self._bt_rx,

            'aggSituazione': self._agg_situazione,
            'Aggiorna': self._agg_scrivi,
            'Applica': self._agg_applica,

            'matLeggi': self._matricola_leggi,
            'matScrivi': self._matricola_scrivi,
            'schLeggi': self._scheda_leggi,
            'schScrivi': self._scheda_scrivi,
            'btbaud_l': self._leggi_bt_baud,
            'btbaud_s': self._scrivi_bt_baud
        }

    def run(self):
        while True:
            lavoro = self.coda_exe.get()
            if "esci" == lavoro[0]:
                break
            elif "Dispositivo" == lavoro[0]:
                self.dispo = lavoro[1]
            elif not lavoro[0] in self.comando:
                pass
            else:
                self.comando[lavoro[0]](lavoro)

    def _manda_alla_grafica(self, x, y=None):
        if y is None:
            self.coda_gui.put((x))
        else:
            self.coda_gui.put((x, y))

    # Invocati dall'eco
    def _eco_8(self, prm):
        prm[1].ecoInfinito(self.dispo)

    def _eco_limite(self, prm):
        prm[1].ecoFinito(prm[2], self.dispo)

    def _eco_fine_x_errore(self, prm):
        prm[1].ecoFinePerErrore(prm[2], self.dispo)

    ########### VARIE ########################################################

    def _eco(self, dummy):
        if self.dispo.Eco():
            gui_support.Messaggio.set("Eco: OK")
        else:
            gui_support.Messaggio.set("Eco: ERRORE")

    def _revisione(self, dummy):
        gui_support.revisione.set('-')

        x = self.dispo.Revisione()
        if x is None:
            gui_support.Messaggio.set("Revisione: ERRORE")
        else:
            gui_support.revisione.set('%d' % x)
            gui_support.Messaggio.set("Revisione: OK")

    def _led(self, prm):
        if self.dispo.Led(int(prm[1]), int(prm[2]), int(prm[3])):
            gui_support.Messaggio.set("Led: OK")
        else:
            gui_support.Messaggio.set("Led: ERRORE")

    def _cicalino(self, prm):
        if self.dispo.Cicalino(prm[1]):
            gui_support.Messaggio.set("Cicalino: OK")
        else:
            gui_support.Messaggio.set("Cicalino: ERRORE")

    def _tasto(self, dummy):
        t = self.dispo.tasto()
        if t is None:
            gui_support.Messaggio.set("Tasto: ERRORE")
        else:
            gui_support.sttTasto.set(t != 0)
            gui_support.Messaggio.set("Tasto: OK")

    def _gg_leggi(self, prm):
        reg = self.dispo.gg_leggi(prm[1])
        if reg is None:
            gui_support.Messaggio.set("Gas gauge: ERRORE")
        else:
            gui_support.Messaggio.set("Gas gauge: OK")
            gui_support.batVal.set('%d = %04X' % (reg, reg))

    def _gg_scrivi(self, prm):
        if self.dispo.gg_scrivi(prm[1], prm[2]):
            gui_support.Messaggio.set("Gas gauge: OK")
        else:
            gui_support.Messaggio.set("Gas gauge: ERRORE")

    def _reset(self, prm):
        if self.dispo.aggReset(prm[1]):
            gui_support.Messaggio.set("Reset: OK")
        else:
            gui_support.Messaggio.set("Reset: ERRORE")

    ########### MEMORIE ######################################################

    def _provaRam(self, dummy):
        gui_support.provaRam.set('-')

        x = self.dispo.provaRam()
        if x is None:
            gui_support.Messaggio.set("Ram: ERRORE")
        else:
            esito = x[0]
            errore = x[1]
            if 0 == esito:
                gui_support.provaRam.set('OK')
            else:
                err = {
                    1: 'Address walking 1',
                    2: 'Address walking 0',
                    3: 'Data walking 0/1'
                }
                gui_support.provaRam.set(
                    '%s: 0x%08X = %d' %
                    (err[esito], errore, int(
                        math.log(
                            errore, 2))))

            gui_support.Messaggio.set("Ram: OK")

    def _nor_crt(self, dummy):
        gui_support.norNumBlk.set('-')
        gui_support.norDimBlk.set('-')

        x = self.dispo.norCaratteristiche()
        if x is None:
            gui_support.Messaggio.set("Nor: ERRORE")
        else:
            gui_support.norNumBlk.set(x[0])
            gui_support.norDimBlk.set(x[1])
            gui_support.Messaggio.set("Nor: OK")

    def _nor_cancella(self, prm):
        if self.dispo.norCancella(prm[1]):
            gui_support.Messaggio.set("Nor: OK")
        else:
            gui_support.Messaggio.set("Nor: ERRORE")

    def _nor_leggi(self, prm):
        x = self.dispo.norLeggi(prm[1], prm[2], prm[3])
        if x is None:
            gui_support.Messaggio.set("Nor: ERRORE")
        else:
            print('Blocco %d' % prm[1])
            utili.stampaTabulare(prm[2], x)
            gui_support.Messaggio.set("Nor: OK")

    def _nor_scrivi(self, prm):
        blk = prm[1]
        pos = prm[2]
        dim = prm[3]
        val = prm[4]
        dati = bytearray()
        for _ in range(dim):
            dati.append(val)
            dati.append(val)
        if self.dispo.norScrivi(blk, pos, dati):
            gui_support.Messaggio.set("Nor: OK")
        else:
            gui_support.Messaggio.set("Nor: ERRORE")

    ########### OTTICA #######################################################

    def _laserI(self, dummy):
        if self.dispo.laserI():
            gui_support.Messaggio.set("Laser: OK")
        else:
            gui_support.Messaggio.set("Laser: ERRORE")

    def _laserF(self, dummy):
        if self.dispo.laserF():
            gui_support.Messaggio.set("Laser: OK")
        else:
            gui_support.Messaggio.set("Laser: ERRORE")

    def _laserA(self, prm):
        if self.dispo.laserA(prm[1]):
            gui_support.Messaggio.set("Laser: OK")
        else:
            gui_support.Messaggio.set("Laser: ERRORE")

    def _camI(self, dummy):
        if self.dispo.cameraI():
            gui_support.Messaggio.set("Camera: OK")
        else:
            gui_support.Messaggio.set("Camera: ERRORE")

    def _camF(self, dummy):
        if self.dispo.cameraF():
            gui_support.Messaggio.set("Camera: OK")
        else:
            gui_support.Messaggio.set("Camera: ERRORE")

    def _camL(self, prm):
        val = self.dispo.cameraL(prm[1])
        if val is None:
            gui_support.Messaggio.set("Camera: ERRORE")
        else:
            gui_support.camRegL.set('0x%02X' % val)
            gui_support.Messaggio.set("Camera: OK")

    def _camS(self, prm):
        if self.dispo.cameraS(prm[1], prm[2]):
            gui_support.Messaggio.set("Camera: OK")
        else:
            gui_support.Messaggio.set("Camera: ERRORE")

    def _foto(self, dummy):
        if self.dispo.cameraFoto():
            gui_support.Messaggio.set("Camera: OK")
        else:
            gui_support.Messaggio.set("Camera: ERRORE")

    def _cam_prm_leggi(self, prm):
        val = self.dispo.cameraPrmL(prm[1])
        if val is None:
            gui_support.Messaggio.set("Camera: ERRORE")
        else:
            gui_support.camPrmL.set(val)
            gui_support.Messaggio.set("Camera: OK")

    def _cam_prm_scrivi(self, prm):
        if self.dispo.cameraPrmS(prm[1], prm[2]):
            gui_support.Messaggio.set("Camera: OK")
        else:
            gui_support.Messaggio.set("Camera: ERRORE")

    def _riprova_bayer(self, pos, dim):
        letti = None

        riprova = 0
        TENTATIVI = 3
        daleggere = min(dim, 190)

        while True:
            print('Provo con', daleggere)

            dati = self.dispo.cameraLeggi(pos, daleggere)
            if dati is None:
                riprova += 1
                if riprova == TENTATIVI:
                    break
                else:
                    daleggere -= 20
                    if daleggere <= 0:
                        break
            else:
                letti = dati
                break

        return letti

    def _leggi_bayer(self, dim, inizio=0):
        bayer = bytearray()

        self.dispo.Cambia(tempo=.1)

        # cinema
        gui_support.leggiFoto.set(0)
        tinizio = time.clock()

        DIM_TOT = dim

        while dim:
            dati = self.dispo.cameraLeggi(len(bayer) + inizio)
            if dati is None:
                dati = self._riprova_bayer(len(bayer) + inizio, dim)
                if dati is None:
                    bayer = None
                    break

            letti = len(dati)
            if letti == 0:
                bayer = None
                break
            if letti > dim:
                dati = dati[:dim]

            bayer += dati
            dim -= len(dati)
            gui_support.leggiFoto.set(100 * len(bayer) / DIM_TOT)

        # cinema
        durata = time.clock() - tinizio
        sdurata = utili.stampaDurata(int(round(durata * 1000.0, 0)))
        kib = round(DIM_TOT / (durata * 1024), 1)
        print("%d B in %s = %d KiB/s" % (DIM_TOT, sdurata, kib))

        self.dispo.Ripristina()

        return bayer

    def _leggi_foto_(self, dummy):
        colonne = 1280
        righe = 800

        tinizio = time.clock()
        bayer = self.dispo.cameraX()
        durata = time.clock() - tinizio

        if bayer is None:
            gui_support.Messaggio.set("Camera: ERRORE")
        elif len(bayer) != righe * colonne:
            gui_support.Messaggio.set("Camera: ERRORE (dati)")
        else:
            sdurata = utili.stampaDurata(int(round(durata * 1000.0, 0)))
            kib = round(len(bayer) / (durata * 1024), 1)
            print("%d B in %s = %d KiB/s" % (len(bayer), sdurata, kib))

            img = np.ndarray((righe, colonne), dtype='uint8', buffer=bayer)

            rgb = cv2.cvtColor(img, cv2.COLOR_BayerBG2RGB)
            nomefoto = 'pippo.png'
            cv2.imwrite(nomefoto, rgb)

            # Mostro
            cv2.namedWindow('foto', cv2.WINDOW_NORMAL)
            cv2.imshow('foto', rgb)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            gui_support.Messaggio.set("Camera: OK (" + nomefoto + ")")


    def _leggi_foto(self, prm):
        while True:
            # Tolgo l'estensione perche' metto io quella giusta
            nomefile = utili.elimina_estensione(prm[1])
            nomefoto = nomefile

            colonne = 1280
            righe = 800
            inizio = 0

            if '1' == prm[2]:
                inizio += 0x00100000
                colonne /= 2
                righe /= 2

            dim = colonne * righe

            bayer = self._leggi_bayer(dim, inizio)
            if bayer is None:
                gui_support.Messaggio.set("Camera: ERRORE")
                break

            img = np.ndarray((righe, colonne), dtype='uint8', buffer=bayer)
            if '1' == prm[2]:
                rgb = img
                nomefoto = nomefile + '.pgm'
                cv2.imwrite(nomefoto, img)
            else:
                # La documentazione e' sbagliata: secondo lei dovrei mettere
                # cv2.COLOR_BayerRG2RGB
                rgb = cv2.cvtColor(img, cv2.COLOR_BayerBG2RGB)
                nomefoto = nomefile + '.png'
                cv2.imwrite(nomefoto, rgb)

            # Mostro
            cv2.namedWindow('foto', cv2.WINDOW_NORMAL)
            cv2.imshow('foto', rgb)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            if True and '0' == prm[2]:
                # Scompongo
                blu = img[::2, ::2]
                cv2.imwrite(nomefile + '.blu.pgm', blu)

                verde_blu = img[::2, 1::2]
                cv2.imwrite(nomefile + '.verde_blu.pgm', verde_blu)

                rosso = img[1::2, 1::2]
                cv2.imwrite(nomefile + '.rosso.pgm', rosso)

                verde_rosso = img[1::2, ::2]
                cv2.imwrite(nomefile + '.verde_rosso.pgm', verde_rosso)

            gui_support.Messaggio.set("Camera: OK (" + nomefoto + ")")

            break

    def _lasera_fotografa(self, prm):
        if self.dispo.LaserFoto(prm[1]):
            gui_support.Messaggio.set("Camera: OK")
        else:
            gui_support.Messaggio.set("Camera: ERRORE")

    def _misura(self, dummy):
        if self.dispo.Misura():
            gui_support.Messaggio.set("Misura: OK")
        else:
            gui_support.Messaggio.set("Misura: ERRORE")

    ########### BLUETOOTH ####################################################

    def _bt_accendi_baud(self, baud):
        esito = False

        if self.dispo.btAccendi(baud):
            time.sleep(.5)

            riprova = 0
            conta = 0

            while True:
                stt = self.dispo.btStato()
                if stt is None:
                    riprova += 1
                    if 3 == riprova:
                        break
                else:
                    conta += 1
                    riprova = 0
                    if 3 == stt:
                        break
                    elif 2 == stt:
                        esito = True
                        break
                    elif conta == 20:
                        break

                time.sleep(.5)

        return esito

    def _bt_accendi(self, prm):
        if self._bt_accendi_baud(prm[1]):
            gui_support.Messaggio.set("Bluetooth: acceso")
        else:
            gui_support.Messaggio.set("Bluetooth: ERRORE")

    def _bt_accendi_auto(self, prm):
        """
            Usata quando la velocita' della seriale non e' nota:
            le prova tutte
        """
        esito = False

        BT_BAUD = prm[1]

        chiavi = sorted(BT_BAUD.keys())
        for elem in chiavi:
            baud = BT_BAUD[elem]
            if 0 == baud:
                continue

            gui_support.Messaggio.set("Bluetooth: provo " + str(baud))
            if not self._bt_accendi_baud(baud):
                break
            else:
                # Aspetto che si assesti
                time.sleep(.5)

                # Invio un comando
                if not self.dispo.btTx("info\r\n"):
                    break

                # Aspetto la risposta
                time.sleep(.5)

                # Ricevo la risposta
                risp = bytearray()
                while True:
                    tmp = self.dispo.btRx()
                    if tmp is None:
                        break
                    elif len(tmp) > 0:
                        risp += tmp
                    else:
                        break

                # La risposta deve essere giusta
                if len(risp) > 4:
                    risp = str(risp)
                    if 'WRAP' in risp:
                        # Ottimo
                        esito = True
                        break
                    elif 'Bluegiga' in risp:
                        # Buono (ho perso la prima parte)
                        esito = True
                        break
                    else:
                        # Schifo
                        pass

                if self.dispo.btSpegni():
                    # Aspetto che si assesti
                    time.sleep(.5)
                else:
                    break

        if esito:
            gui_support.Messaggio.set("Bluetooth: OK")
        else:
            gui_support.Messaggio.set("Bluetooth: ERRORE")

    def _bt_spegni(self, dummy):
        if self.dispo.btSpegni():
            gui_support.Messaggio.set("Bluetooth: spento")
        else:
            gui_support.Messaggio.set("Bluetooth: ERRORE")

    def _bt_cmd(self, prm):
        if self.dispo.btTx(prm[1]):
            tot = 0
            zero = False

            # Aspetto che arrivi qualcosa
            time.sleep(.1)

            while True:
                rsp = self.dispo.btRx()
                if rsp is None:
                    break
                elif len(rsp) > 0:
                    self._manda_alla_grafica('btrx', rsp)
                    zero = False
                    tot += len(rsp)
                elif zero:
                    break
                else:
                    time.sleep(.05)
                    zero = True

            if tot:
                gui_support.Messaggio.set("Bluetooth: OK")
            else:
                gui_support.Messaggio.set("Bluetooth: NESSUN DATO")
        else:
            gui_support.Messaggio.set("Bluetooth: ERRORE")

    def _esegui_cmd_bt(self, cmd):
        rsp = b''
        if self.dispo.btTx(cmd):
            # Aspetto che arrivi qualcosa
            time.sleep(.1)

            zero = False
            while True:
                tmp = self.dispo.btRx()
                if tmp is None:
                    break
                elif len(tmp) > 0:
                    rsp += tmp
                elif zero:
                    break
                else:
                    time.sleep(.05)
                    zero = True

        return rsp

    def _bt_file(self, prm):
        righe = None
        with open(prm[1], "rt") as comandi:
            righe = comandi.read().splitlines()

        conta = 0
        for cmd in righe:
            if len(cmd) < 2:
                pass
            elif cmd[0] == '#':
                pass
            else:
                conta += 1
                cmd += '\n'
                self._manda_alla_grafica('btrx', cmd)

                r = self._esegui_cmd_bt(cmd)

                if len(r):
                    self._manda_alla_grafica('btrx', r + '\n')
                else:
                    self._manda_alla_grafica('btrx', 'No risp\n')
                time.sleep(1.0)

        if conta:
            gui_support.Messaggio.set("Inviati %d comandi" % conta)
        else:
            gui_support.Messaggio.set("Nessun comando inviato")

    def _bt_rx(self, dummy):
        rsp = self.dispo.btRx()
        if rsp is None:
            gui_support.Messaggio.set("Bluetooth: ERRORE")
        else:
            self._manda_alla_grafica('btrx', rsp)
            gui_support.Messaggio.set("Bluetooth: OK")

    ########### AGGIORNA ###################################################

    def _agg_situazione(self, dummy):
        # preparo esito negativo
        gui_support.verUL.set('-')
        gui_support.verCE.set('-')
        gui_support.verAPP.set('-')
        gui_support.verPAR.set('-')
        gui_support.idUL.set('-')
        gui_support.idCE.set('-')
        gui_support.idAPP.set('-')
        gui_support.idPAR.set('-')
        gui_support.identCorr.set(10)

        while True:
            cs = self.dispo.aggChiSei()
            if cs is None:
                gui_support.Messaggio.set("Non so chi e'")
                break

            gui_support.identCorr.set(identifica_i(cs))

            ver = self.dispo.aggVersioni()
            if ver is None:
                gui_support.Messaggio.set("Versioni: ERRORE")
                break

            gui_support.verUL.set(utili.strVer(ver[0]))
            gui_support.verCE.set(utili.strVer(ver[1]))
            gui_support.verAPP.set(utili.strVer(ver[2]))
            gui_support.verPAR.set(utili.strVer(ver[3]))

            ident = self.dispo.aggInfo()
            if ident is None:
                gui_support.Messaggio.set("Identificativo: ERRORE")
                break

            gui_support.idUL.set(identifica_s(ident[0]))
            gui_support.idCE.set(identifica_s(ident[1]))
            gui_support.idAPP.set(identifica_s(ident[2]))
            gui_support.idPAR.set(identifica_s(ident[3]))

            gui_support.Messaggio.set("Situazione: OK")
            break

    def _agg_scrivi(self, prm):
        aposto = False
        msg = None

        with open(prm[1], "rb") as fileBIN:
            fileBIN.seek(0, 2)
            dim = fileBIN.tell()
            fileBIN.seek(0, 0)

            # Un secondo per KiB
            self.dispo.Cambia(tempo=dim / 1024)

            if not self.dispo.aggInizia(dim):
                msg = "Aggiorna: ERRORE aggInizia"
            else:
                #DIM_PACC = 2 * 1496 <- dimensione massima ammessa dal protocollo
                # Per non andare a cavallo di due settori:
                DIM_PACC = 2 * 1024
                # cinema
                prog = 0.0
                gui_support.aggProg.set(int(prog))

                pos = 0
                mancano = dim
                while pos < dim:
                    leggi = DIM_PACC
                    if leggi > mancano:
                        leggi = mancano
                    dati = fileBIN.read(leggi)

                    if self.dispo.aggScrivi(pos, dati):
                        pos += leggi
                        mancano -= leggi

                        # cinema
                        prog = pos * 100.0 / dim
                        gui_support.aggProg.set(int(prog))
                    else:
                        break

                if pos != dim:
                    msg = "Aggiorna: ERRORE aggScrivi"
                elif not self.dispo.aggFine():
                    msg = "Aggiorna: ERRORE aggFine"
                else:
                    aposto = True

        self.dispo.Ripristina()

        if aposto:
            gui_support.Messaggio.set("Aggiorna: OK")
        elif msg is None:
            gui_support.Messaggio.set("Aggiorna: ERRORE su file")
        else:
            gui_support.Messaggio.set(msg)

    def _agg_applica(self, dummy):
        if self.dispo.aggApplica():
            gui_support.Messaggio.set("Applica: OK")
        else:
            gui_support.Messaggio.set("Applica: ERRORE")

    ########### PARAMETRI ###################################################

    def _matricola_leggi(self, dummy):
        gui_support.matricola.set('-')
        x = self.dispo.leggiMatr()
        if x is None:
            gui_support.Messaggio.set("Matricola: ERRORE")
        else:
            gui_support.matricola.set(x)
            gui_support.Messaggio.set("Matricola: OK")

    def _matricola_scrivi(self, prm):
        if self.dispo.scriviMatr(prm[1]):
            gui_support.Messaggio.set("Matricola: OK")
        else:
            gui_support.Messaggio.set("Matricola: ERRORE")

    def _scheda_leggi(self, dummy):
        gui_support.scheda.set('-')
        x = self.dispo.leggiScheda()
        if x is None:
            gui_support.Messaggio.set("Scheda: ERRORE")
        else:
            gui_support.scheda.set(x)
            gui_support.Messaggio.set("Scheda: OK")

    def _scheda_scrivi(self, prm):
        if self.dispo.scriviScheda(prm[1]):
            gui_support.Messaggio.set("Scheda: OK")
        else:
            gui_support.Messaggio.set("Scheda: ERRORE")

    def _leggi_bt_baud(self, dummy):
        gui_support.baudBT.set('-')
        x = self.dispo.leggiBTbaud()
        if x is None:
            gui_support.Messaggio.set("Baud: ERRORE")
        else:
            gui_support.baudBT.set(str(x))
            gui_support.Messaggio.set("Baud: OK")

    def _scrivi_bt_baud(self, prm):
        if self.dispo.scriviBTbaud(prm[1]):
            gui_support.Messaggio.set("Baud: OK")
        else:
            gui_support.Messaggio.set("Baud: ERRORE")
