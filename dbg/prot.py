'''
    Protocollo di comunicazione col banco di
    taratura della SC524

    Il protocollo e' cosi' composto:
        0x85    Inizio trama
        0xYYYY  Codice comando (little endian)
                Eventuali dati
        0xXX    Il checksum e' il not della somma a 8 bit
                del comando e della parte dati, per cui
                sommando tutto cio' che sta fra inizio
                e fine trama si ottiene 0xFF
        0x82    Fine trama
'''


import struct
import base64

import serial


class PROT(object):
    _BAUD = 115200
    _INIZIO_TRAMA = 0x02
    _FINE_TRAMA = 0x03
    _CS_VALIDO = 0xFF

    def __init__(self, timeout=1, **cosa):
        if 'porta' in cosa:
            # Apro come seriale
            try:
                self.uart = serial.Serial(cosa['porta'],
                                          PROT._BAUD,
                                          serial.EIGHTBITS,
                                          serial.PARITY_NONE,
                                          serial.STOPBITS_ONE,
                                          timeout,
										  rtscts=True)
                self.prm = self.uart.getSettingsDict()
            except serial.SerialException as err:
                print(err)
                self.uart = None
            except ValueError as err:
                print(err)
                self.uart = None
        else:
            # Apro come usb
            try:
                self.uart = serial.serial_for_url(
                    'hwgrep://%s:%s' %
                    (cosa['vid'], cosa['pid']),
                    baudrate=PROT._BAUD,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=timeout,
                    rtscts=True)
                self.prm = self.uart.getSettingsDict()
            except serial.SerialException as err:
                print(err)
                self.uart = None

    def __del__(self):
        self.chiudi()

    def a_posto(self):
        return self.uart is not None

    def chiudi(self):
        if self.uart is not None:
            self.uart.close()
            self.uart = None

    def cambia(self, baud=None, tempo=None):
        imp = self.uart.getSettingsDict()
        if baud is not None:
            imp['baudrate'] = baud
        if tempo is not None:
            imp['timeout'] = tempo
        self.uart.applySettingsDict(imp)

    def ripristina(self):
        self.uart.applySettingsDict(self.prm)

    # ============================================
    # Spedisce il messaggio aggiungendo la parte mancante
    # ============================================

    def _trasmetti(self, msg):
        # Aggiungo il checksum
        cs = 0
        for x in msg:
            cs += x

        cs = (~cs) & 0xFF
        msg.append(cs)

        try:
            # Compongo il pacchetto
            pkt = bytearray()

            pkt.append(PROT._INIZIO_TRAMA)

            # codifico
            pkt += base64.standard_b64encode(msg)

            pkt.append(PROT._FINE_TRAMA)

            # Trasmetto
            self.uart.flushInput()
            self.uart.write(pkt)

            return True
        except binascii.Error:
            return False

    # ============================================
    # Restituisce il messaggio ricevuto o un bytearray vuoto
    # ============================================

    def _ricevi(self):
        pkt = bytearray()
        trovato = False
        # Mi aspetto almeno: inizio + comando[2] + cs + fine
        daLeggere = 5
        while not trovato:
            letti = bytearray(self.uart.read(daLeggere))
            if 0 == len(letti):
                break
            for rx in letti:
                if PROT._INIZIO_TRAMA == rx:
                    pkt = bytearray()
                elif PROT._FINE_TRAMA == rx:
                    if len(pkt) >= 3:
                        trovato = True
                else:
                    pkt.append(rx)
            daLeggere = self.uart.inWaiting()
            if 0 == daLeggere:
                daLeggere = 1

        if not trovato:
            pkt = bytearray()
        else:
            try:
                x = base64.standard_b64decode(pkt)
                cs = 0
                for i in x:
                    cs += i
                if (cs & 0xFF) != PROT._CS_VALIDO:
                    pkt = bytearray()
                else:
                    pkt = bytearray(x[:len(x)-1])
            except binascii.Error:
                pkt = bytearray()

        return pkt

    def _risposta_void(self, cmd):
        rsp = self._ricevi()
        if len(rsp) != 2:
            return False
        elif rsp[0] != cmd[0]:
            return False
        elif rsp[1] == cmd[1] | 0x80:
            return True
        else:
            return False

    # ============================================
    # Comando senza parametri e senza risposta
    # ============================================

    def cmdVoidVoid(self, cmd):
        tx = bytearray(struct.pack('<H', cmd))

        if not self._trasmetti(tx):
            return False
        else:
            return self._risposta_void(tx)

    # ============================================
    # Comando con parametri e senza risposta
    # ============================================

    def cmdPrmVoid(self, cmd, prm):
        tx = bytearray(struct.pack('<H', cmd))
        tx += prm
        if not self._trasmetti(tx):
            return False
        else:
            return self._risposta_void(tx)

    # ============================================
    # Comando senza parametri ma con risposta
    # ============================================

    def cmdVoidRsp(self, cmd, dim=None):
        rsp = None

        tx = bytearray(struct.pack('<H', cmd))
        if not self._trasmetti(tx):
            pass
        else:
            tmp = self._ricevi()
            if len(tmp) < 2:
                pass
            elif tmp[0] != tx[0]:
                pass
            elif tmp[1] != tx[1] | 0x80:
                pass
            elif dim is None:
                rsp = tmp[2:]
            elif len(tmp) != 2 + dim:
                pass
            else:
                rsp = tmp[2:]

        return rsp

    # ============================================
    # Comando con parametri e risposta
    # ============================================

    def cmdPrmRsp(self, cmd, prm, dim=None):
        rsp = None

        tx = struct.pack('<I', cmd)
        tx = tx[:2]
        tx = bytearray(tx)
        tx += prm

        if not self._trasmetti(tx):
            pass
        else:
            tmp = self._ricevi()
            if len(tmp) < 2:
                pass
            elif tmp[0] != tx[0]:
                pass
            elif tmp[1] != tx[1] | 0xC0:
                pass
            elif dim is None:
                rsp = tmp[2:]
            elif len(tmp) != 2 + dim:
                pass
            else:
                rsp = tmp[2:]

        return rsp

    # senza protocollo

    def ricevi(self, dim):
        pkt = bytearray()
        while True:
            daLeggere = min(dim, 1000)

            letti = bytearray(self.uart.read(daLeggere))
            if 0 == len(letti):
                break

            pkt += letti
            if len(pkt) >= dim:
                break

        return pkt

