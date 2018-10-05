#!/usr/bin/env python

"""
    Varie
"""
from __future__ import print_function

import binascii
import threading
import struct
import os

import crcmod


def validaStringa(x, dimmin=None, dimmax=None):
    """
        Usata sui campi testo per validare che la
        lunghezza sia fra un minimo e un massimo
    """
    esito = False

    if x is None:
        pass
    elif dimmin is None:
        if dimmax is None:
            # Accetto qls dimensione
            esito = True
        elif len(x) > dimmax:
            pass
        else:
            esito = True
    elif len(x) < dimmin:
        pass
    elif dimmax is None:
        esito = True
    elif len(x) > dimmax:
        pass
    else:
        esito = True

    return esito


def validaCampo(x, mini=None, maxi=None):
    """
        Se la stringa x e' un intero, controlla
        che sia tra i due estremi inclusi
    """
    esito = False
    val = None
    while True:
        if x is None:
            break

        if 0 == len(x):
            break

        try:
            val = int(x)
        except ValueError:
            try:
                val = int(x, 16)
            except ValueError:
                pass

        if val is None:
            break

        # Entro i limiti?
        if mini is None:
            pass
        elif val < mini:
            break
        else:
            pass

        if maxi is None:
            pass
        elif val > maxi:
            break
        else:
            pass

        esito = True
        break

    return esito, val


def strVer(v):
    """
        Converte la versione del fw in stringa
    """
    ver = ""

    if v == 0:
        ver = '???'
    else:
        if v & 0x80000000:
            ver += "(dbg) "
            v = ~v
            v &= 0xFFFFFFFF

        vmag = v >> 24
        vmin = v & 0xFFFFFF

        ver += str(vmag)
        ver += "."
        ver += str(vmin)

    return ver


def verStr(v):
    """
        Converte una stringa x.y nella versione del fw
    """
    magg, dummy, mino = v.partition('.')

    esito, ver = validaCampo(magg, 0, 255)

    if not esito:
        return False, 0

    esito, v2 = validaCampo(mino, 0, 0xFFFFFF)
    if not esito:
        return False, 0

    ver <<= 24
    ver += v2

    return True, ver


def intEsa(val, cifre=8):
    """
        Converte un valore in stringa esadecimale senza 0x iniziale
    """
    x = hex(val)
    s = x[2:]
    ver = ""
    dim = len(s)
    while dim < cifre:
        ver += "0"
        dim += 1

    ver += s.upper()

    return ver


def StampaEsa(cosa, titolo=''):
    """
        Stampa un dato binario
    """
    if cosa is None:
        print('<vuoto>')
    else:
        print(titolo, binascii.hexlify(cosa))
        # print ''.join('{:02X.}'.format(x) for x in cosa)


def gomsm(conv, div):
    """
        Converte un tempo in millisecondi in una stringa
    """
    if conv[-1] < div[0]:
        return conv
    else:
        r = conv[-1] % div[0]
        v = conv[-1] // div[0]

        conv = conv[:len(conv) - 1]
        conv = conv + (r, v)

        div = div[1:]

        if len(div):
            return gomsm(conv, div)
        else:
            return conv


def stampaDurata(milli):
    """
        Converte un numero di millisecondi in una stringa
        (giorni, ore, minuti, secondi millisecondi)
    """
    x = gomsm((milli,), (1000, 60, 60, 24))
    u = ('ms', 's', 'm', 'o', 'g')

    durata = ""
    for i in range(0, len(x)):
        if len(durata):
            durata = ' ' + durata
        durata = str(x[i]) + u[i] + durata
    return durata


def baMac(mac):
    """
        Converte da mac a bytearray
    """
    componenti = mac.split(':')
    if len(componenti) != 6:
        return None
    else:
        mac = bytearray()
        for elem in componenti:
            esito, val = validaCampo('0x' + elem, 0, 255)
            if esito:
                mac += bytearray([val])
            else:
                mac = None
                break

        return mac


class problema(Exception):

    def __init__(self, msg):
        Exception.__init__(self)
        self.msg = msg

    def __str__(self):
        return self.msg


class periodico(threading.Thread):

    def __init__(self, funzione, param=None):
        threading.Thread.__init__(self)

        self.secondi = None
        self.funzione = funzione
        self.param = param

        self.evento = threading.Event()

    def run(self):
        while True:
            esci = self.evento.wait(self.secondi)
            if esci:
                break

            if self.param is not None:
                self.funzione(self.param)
            else:
                self.funzione()

    def avvia(self, secondi):
        if self.secondi is None:
            self.secondi = secondi
            self.start()

    def termina(self):
        if self.secondi is not None:
            self.evento.set()
            self.join()
            self.secondi = None

    def attivo(self):
        return self.secondi is not None


def crcSTM32(dati, crc=0xFFFFFFFF):
    """
        Calcola il crc come il processore
    """
    calcola = crcmod.mkCrcFun(0x104C11DB7, 0xFFFFFFFF, False)

    while len(dati):
        gira = struct.unpack('>I', dati[0:4])[0]
        dati = dati[4:]
        girati = struct.pack('<I', gira)
        crc = calcola(girati, crc)

    return crc


def stampaTabulare(pos, dati, prec=4):
    """
        Stampa il bytearray dati incolonnando per 16
        prec e' il numero di cifre di pos
    """
    testa_riga = '%0' + str(prec) + 'X '

    print('00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F'.rjust(prec + (3 * 16)))
    primo = pos & 0xFFFFFFF0

    bianchi = pos & 0x0000000F
    riga = testa_riga % primo
    while bianchi:
        riga += '   '
        bianchi -= 1

    conta = pos & 0x0000000F
    for x in dati:
        riga += '%02X ' % (x)
        conta += 1
        if conta == 16:
            print(riga)
            primo += 16
            riga = testa_riga % primo
            conta = 0
    if len(riga) > 4:
        print(riga)


def converti_ba(ba):
    """
        Converte un bytearray in un long
    """
    x = int(0)
    for idx in range(0, len(ba)):
        elem = len(ba) - 1 - idx
        x <<= 8
        x += ba[elem]

    return x


def gira_ba(ba):
    """
        Inverte i byte: gli ultimi saranno i primi
    """
    girato = bytearray()

    for idx in range(0, len(ba)):
        elem = len(ba) - 1 - idx
        girato.append(ba[elem])

    return girato


def converti_long(l):
    """
        Converte un long in un bytearray
    """
    x = bytearray()

    while l:
        x.append(l & 0xFF)
        l >>= 8

    return x


def elimina_estensione(completo):
    path, nomest = os.path.split(completo)
    nome, est = os.path.splitext(nomest)
    return os.path.join(path, nome)


if __name__ == '__main__':
    vettore = (
        0xCC,
        0xF4,
        0x82,
        0x65,
        0x6A,
        0x9E,
        0x7B,
        0xD1,
        0x31,
        0x9F,
        0x40,
        0x31,
        0x7D,
        0x61,
        0x10,
        0x55,
        0xB2,
        0x48,
        0xF3,
        0xD5,
        0x70,
        0x0F,
        0x2D,
        0xEB,
        0xFC,
        0x79,
        0x53,
        0x17,
        0xBF,
        0xCA,
        0xCD,
        0x82,
        0x3E,
        0x06,
        0x92,
        0x3A,
        0xB4,
        0xED,
        0x8C,
        0xA5,
        0xAA,
        0xA9,
        0x12,
        0x9D,
        0x1B,
        0xB4,
        0x0C,
        0x15,
        0x23,
        0xB9,
        0x16,
        0xC3,
        0xC1,
        0xB9,
        0xF8,
        0x24,
        0x1D,
        0x26,
        0xC3,
        0xAE,
        0x77,
        0x2E,
        0x3F,
        0x22,
        0x8C,
        0x77,
        0x83,
        0xBD,
        0x59,
        0x6D,
        0xFA,
        0xC2,
        0xB5,
        0xE5,
        0x45,
        0x5E,
        0xF8,
        0x8C,
        0xD7,
        0xF2,
        0xD6,
        0x56,
        0x16,
        0x35,
        0xDE,
        0xA2,
        0x0A,
        0x34,
        0x60,
        0x18,
        0xCF,
        0x55,
        0x57,
        0x02,
        0xFD,
        0x5D,
        0x90,
        0x98,
        0x06,
        0xD9,
        0x39,
        0x27,
        0x2A,
        0x6E,
        0x3D,
        0x59,
        0xDE,
        0x7B,
        0xC2,
        0xD6,
        0xAA,
        0x16,
        0x29,
        0x3F,
        0x00,
        0x72,
        0x79,
        0x6F,
        0x98,
        0x49,
        0xFC,
        0x94,
        0x3F,
        0x5D,
        0x82,
        0x8D,
        0x60,
        0x5A,
    )

    stampaTabulare(0, vettore)
    vettore_long = converti_ba(vettore)
    print(vettore_long)

    vettore2 = converti_long(vettore_long)
    stampaTabulare(0, vettore2)
