#! /usr/bin/env python

import struct
import logging

import utili

logging.basicConfig(
    filename='diario.log',
    level=logging.DEBUG,
    format='%(asctime)s %(message)s')

# Per prima la tabella delle interruzioni
DIM_TAB_IRQ = 428

# Poi il descrittore: 4 dword con firma, id, versione, dimensione
DIM_DESC = 4 * 4

FIRMA = 0x2607C324

lista_id = [0x43d3212d, 0x927ba45b, 0x55a682cc, 0x65e57c04]


class MANIPOLA(object):

    def __init__(self, padre):
        self.padre = padre

        # Salvo il descrittore per rigenerarlo
        self.imgId = None
        self.imgVer = None
        self.imgDim = None

        try:
            filePadre = open(padre, "rb")

            with filePadre:
                filePadre.seek(0, 2)
                dim = filePadre.tell()

                if dim < DIM_TAB_IRQ + DIM_DESC:
                    logging.critical(
                        'Troppo piccolo: %d < %d',
                        dim,
                        DIM_TAB_IRQ + DIM_DESC)
                    raise utili.problema('Troppo piccolo')

                while True:
                    # Salto le interruzioni
                    filePadre.seek(DIM_TAB_IRQ)

                    # Descrittore
                    desc = filePadre.read(DIM_DESC)
                    if len(desc) != DIM_DESC:
                        logging.critical('Errore leggendo il descrittore')
                        break

                    desc = struct.unpack('<4I', desc)
                    if desc[0] != FIRMA:
                        logging.critical(
                            'Errore: firma %08X != %08X', desc[0], FIRMA)
                        break

                    valido = False
                    try:
                        valido = desc[1] in lista_id
                    except:
                        logging.critical(
                            'Errore: id %08X non valido', desc[1])
                        break

                    # Tutto bene, salvo
                    self.imgId = desc[1]
                    self.imgVer = desc[2]
                    self.imgDim = dim

                    break

                filePadre.close()
        except:
            logging.critical('Il file <%s> non esiste', padre)

    def aPosto(self):
        return self.imgVer is not None

    def Salva(self, figlio):
        esito = False

        if self.imgVer is not None:
            with open(self.padre, "rb") as filePadre:
                with open(figlio, "wb") as fileFiglio:

                    # Interruzioni
                    irq = filePadre.read(DIM_TAB_IRQ)
                    if len(irq) != DIM_TAB_IRQ:
                        raise utili.problema('Errore in lettura')
                    else:
                        fileFiglio.write(irq)
                    crc = utili.crcSTM32(irq)

                    # Descrittore
                    filePadre.seek(DIM_DESC, 1)

                    x = struct.pack('<I', FIRMA)
                    fileFiglio.write(x)
                    crc = utili.crcSTM32(x, crc)

                    x = struct.pack('<I', self.imgId)
                    fileFiglio.write(x)
                    crc = utili.crcSTM32(x, crc)

                    x = struct.pack('<I', self.imgVer)
                    fileFiglio.write(x)
                    crc = utili.crcSTM32(x, crc)
                    # Aggiungo il crc
                    dim = self.imgDim + 4
                    coda = dim % 4
                    dim += coda
                    self.imgDim = dim // 4
                    x = struct.pack('<I', self.imgDim)
                    fileFiglio.write(x)
                    crc = utili.crcSTM32(x, crc)

                    # Codice
                    while True:
                        x = filePadre.read(1024)
                        if 0 == len(x):
                            break
                        else:
                            fileFiglio.write(x)
                            crc = utili.crcSTM32(x, crc)

                    # Coda
                    x = struct.pack('<B', 255)
                    while coda > 0:
                        fileFiglio.write(x)
                        crc = utili.crcSTM32(x, crc)
                        coda -= 1

                    # Crc
                    x = struct.pack('<I', crc)
                    fileFiglio.write(x)

                    fileFiglio.close()
                    esito = True

                filePadre.close()

        return esito


import sys

if __name__ == '__main__':
    if 3 == len(sys.argv):
        logging.info('converto %s in %s', sys.argv[1], sys.argv[2])
        manipola = MANIPOLA(sys.argv[1])

        if manipola.aPosto():
            if manipola.Salva(sys.argv[2]):
                logging.info('OK')
            else:
                logging.critical('Errore in scrittura')
    else:
        logging.critical(
            'Passare il file di ingresso seguito da quello di uscita')
