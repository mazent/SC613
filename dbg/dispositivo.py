import struct

import prot


class DISPOSITIVO(object):

    def __init__(self, **argo):
        self.coda = None
        try:
            self.prot = prot.PROT(porta=argo['uart'])
        except KeyError:
            try:
                self.prot = prot.PROT(vid=argo['vid'], pid=argo['pid'])
            except KeyError:
                self.prot = None

    def __del__(self):
        del self.prot

    def aPosto(self):
        # Controllo una sola volta
        if self.prot is None:
            return False
        else:
            return self.prot.a_posto()

    def Chiudi(self):
        if self.prot is not None:
            self.prot.chiudi()
            del self.prot
            self.prot = None

    def Cambia(self, baud=None, tempo=None):
        if self.prot is not None:
            self.prot.cambia(baud, tempo)

    def Ripristina(self):
        if self.prot is not None:
            self.prot.ripristina()

    # ============================================
    # Varie
    # ============================================

    def Eco(self, dati=None):
        if dati is None:
            dati = struct.pack('<I', 0xDEADBEEF)

        eco = self.prot.cmdPrmRsp(0x0000, dati, len(dati))
        if eco is None:
            return False
        else:
            return eco == dati

    def Ping(self):
        return self.prot.cmdVoidVoid(0x0000)

    # def Revisione(self):
    #     rsp = self.prot.cmdVoidRspBA(0x0001, 4)
    #     if rsp is None:
    #         return None
    #     else:
    #         rsp = struct.unpack('<I', rsp)
    #         return rsp[0]
    # 
    # def Led(self, rosso, verde, blu):
    #     led = 0
    #     if rosso:
    #         led += 1 << 0
    #     if verde:
    #         led += 1 << 1
    #     if blu:
    #         led += 1 << 2
    #     prm = struct.pack('<B', led)
    #     return self.prot.cmdPrmVoid(0x0004, prm)
    # 
    # def Cicalino(self, hertz):
    #     prm = struct.pack('<H', hertz)
    #     return self.prot.cmdPrmVoid(0x0005, prm)
    # 
    # def tasto(self):
    #     rsp = self.prot.cmdVoidRspBA(0x0006, 1)
    #     if rsp is None:
    #         return None
    #     else:
    #         return rsp[0]
    # 
    # def gg_leggi(self, reg):
    #     prm = struct.pack('<B', reg)
    #     val = self.prot.cmdPrmRsp(0x0007, prm, 2)
    #     if val is None:
    #         return None
    #     else:
    #         return struct.unpack('<H', val)[0]
    # 
    # def gg_scrivi(self, reg, val):
    #     prm = struct.pack('<BH', reg, val)
    #     return self.prot.cmdPrmVoid(0x0008, prm)
    # 
    # # ============================================
    # # Memorie
    # # ============================================
    # 
    # def provaRam(self):
    #     rsp = self.prot.cmdVoidRspBA(0x0100, 5)
    #     if rsp is None:
    #         return None
    #     else:
    #         return struct.unpack('<BI', rsp)
    # 
    # def norCaratteristiche(self):
    #     rsp = self.prot.cmdVoidRspBA(0x0180, 2 * 2)
    #     if rsp is None:
    #         return None
    #     else:
    #         return struct.unpack('<2H', rsp)
    # 
    # def norCancella(self, blocco):
    #     prm = struct.pack('<H', blocco)
    #     return self.prot.cmdPrmVoid(0x0181, prm)
    # 
    # def norLeggi(self, blocco, posizione, dimensione):
    #     prm = struct.pack('<3H', blocco, posizione, dimensione)
    #     return self.prot.cmdPrmRsp(0x0182, prm, 2 * dimensione)
    # 
    # def norScrivi(self, blocco, posizione, dati):
    #     prm = bytearray(struct.pack('<2H', blocco, posizione))
    #     prm += dati
    #     return self.prot.cmdPrmVoid(0x0183, prm)
    # 
    # # ============================================
    # # Ottica
    # # ============================================
    # 
    # def laserI(self):
    #     return self.prot.cmdVoidVoid(0x0200)
    # 
    # def laserF(self):
    #     return self.prot.cmdVoidVoid(0x0201)
    # 
    # def laserA(self, perc):
    #     prm = struct.pack('<B', perc)
    #     return self.prot.cmdPrmVoid(0x0202, prm)
    # 
    # def cameraI(self):
    #     return self.prot.cmdVoidVoid(0x0203)
    # 
    # def cameraF(self):
    #     return self.prot.cmdVoidVoid(0x0204)
    # 
    # def cameraL(self, reg):
    #     prm = struct.pack('<B', reg)
    # 
    #     x = self.prot.cmdPrmRsp(0x0205, prm, 1)
    #     if x is not None:
    #         x = struct.unpack('<B', x)[0]
    # 
    #     return x
    # 
    # def cameraS(self, reg, val):
    #     prm = struct.pack('<2B', reg, val)
    # 
    #     return self.prot.cmdPrmVoid(0x0206, prm)
    # 
    # def cameraPrmL(self, prm):
    #     prm = struct.pack('<B', prm)
    # 
    #     x = self.prot.cmdPrmRsp(0x0207, prm, 2)
    #     if x is not None:
    #         x = struct.unpack('<H', x)[0]
    # 
    #     return x
    # 
    # def cameraPrmS(self, prm, val):
    #     prm = struct.pack('<BH', prm, val)
    # 
    #     return self.prot.cmdPrmVoid(0x0208, prm)
    # 
    # def cameraFoto(self):
    #     self.prot.cambia(tempo=2)
    #     esito = self.prot.cmdVoidVoid(0x0209)
    #     self.prot.ripristina()
    #     return esito
    # 
    # def cameraLeggi(self, posizione, dimensione=0):
    #     prm = struct.pack('<IB', posizione, dimensione)
    #     if 0 == dimensione:
    #         return self.prot.cmdPrmRsp(0x020A, prm)
    #     else:
    #         return self.prot.cmdPrmRsp(0x020A, prm, dimensione)
    # 
    # def cameraX(self):
    #     if self.prot.cmdVoidVoid(0x020D):
    #         return self.prot.ricevi(1280 * 800)
    #     else:
    #         return None
    # 
    # def LaserFoto(self, perc):
    #     prm = struct.pack('<B', perc)
    #     return self.prot.cmdPrmVoid(0x020B, prm)
    # 
    # def Misura(self):
    #     return self.prot.cmdVoidVoid(0x020C)
    # 
    # # ============================================
    # # Bluetooth
    # # ============================================
    # 
    # def btAccendi(self, baud):
    #     prm = struct.pack('<I', baud)
    # 
    #     return self.prot.cmdPrmVoid(0x0300, prm)
    # 
    # def btSpegni(self):
    #     return self.prot.cmdVoidVoid(0x0302)
    # 
    # def btStato(self):
    #     x = self.prot.cmdVoidRspBA(0x0301, 1)
    #     if x is not None:
    #         x = struct.unpack('<B', x)[0]
    # 
    #     return x
    # 
    # def btTx(self, cmd):
    #     dati = bytearray(cmd.encode('ascii'))
    #     return self.prot.cmdPrmVoid(0x0303, dati)
    # 
    # def btRx(self):
    #     x = self.prot.cmdVoidRspBA(0x0304)
    #     if x is not None:
    #         try:
    #             x = x.decode('ascii')
    #         except:
    #             x = None
    #     return x
    # 
    # # ============================================
    # # Aggiornamento
    # # ============================================
    # 
    # def aggChiSei(self):
    #     x = self.prot.cmdVoidRspBA(0x0A02, 4)
    #     if x is None:
    #         return x
    #     else:
    #         return struct.unpack('<I', x)[0]
    # 
    # def aggVersioni(self):
    #     x = self.prot.cmdVoidRspBA(0x0A00, 4 * 4)
    #     if x is None:
    #         return x
    #     else:
    #         return struct.unpack('<4I', x)
    # 
    # def aggInfo(self):
    #     x = self.prot.cmdVoidRspBA(0x0A01, 4 * 4)
    #     if x is None:
    #         return x
    #     else:
    #         return struct.unpack('<4I', x)
    # 
    # def aggReset(self, chi):
    #     prm = bytearray(struct.pack('<B', chi))
    # 
    #     return self.prot.cmdPrmVoid(0x0A03, prm)
    # 
    # def aggInizia(self, dim):
    #     prm = bytearray(struct.pack('<I', dim))
    # 
    #     return self.prot.cmdPrmVoid(0x0A10, prm)
    # 
    # def aggScrivi(self, pos, dati):
    #     prm = bytearray(struct.pack('<I', pos))
    #     prm += dati
    # 
    #     return self.prot.cmdPrmVoid(0x0A11, prm)
    # 
    # def aggFine(self):
    #     return self.prot.cmdVoidVoid(0x0A12)
    # 
    # def aggApplica(self):
    #     return self.prot.cmdVoidVoid(0x0A13)
    # 
    # # ============================================
    # # Parametri
    # # ============================================
    # 
    # def leggiMatr(self):
    #     x = self.prot.cmdVoidRspBA(0x0400)
    #     if x is not None:
    #         x = x.decode('ascii')
    #     return x
    # 
    # def scriviMatr(self, matr):
    #     matr = bytearray(matr.encode('ascii'))
    #     return self.prot.cmdPrmVoid(0x0401, matr)
    # 
    # def leggiScheda(self):
    #     x = self.prot.cmdVoidRspBA(0x0402)
    #     if x is not None:
    #         x = x.decode('ascii')
    #     return x
    # 
    # def scriviScheda(self, matr):
    #     matr = bytearray(matr.encode('ascii'))
    #     return self.prot.cmdPrmVoid(0x0403, matr)
    # 
    # def leggiBTbaud(self):
    #     baud = self.prot.cmdVoidRspBA(0x0480)
    #     if baud is not None:
    #         baud = struct.unpack('<I', baud)[0]
    # 
    #     return baud
    # 
    # def scriviBTbaud(self, baud):
    #     prm = bytearray(struct.pack('<I', baud))
    # 
    #     return self.prot.cmdPrmVoid(0x0481, prm)
