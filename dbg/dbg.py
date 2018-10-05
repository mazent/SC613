#! /usr/bin/env python

"""
    Implementa i metodi ereditati dalla grafica
"""

import sys
import random

try:
    import Queue as coda
    import tkFileDialog as dialogo
except ModuleNotFoundError:
    import queue as coda
    import tkinter.filedialog as dialogo

import gui
import gui_support

import esegui
import eco
import dispositivo
import utili

NOME_UART = None
if sys.platform.startswith("win32"):
    NOME_UART = "COM"
else:
    NOME_UART = "/dev/tty"

TAB_CHIUSA = {1: False, 2: False }
TAB_APERTA = {1: True, 2: True }

CAM_PRM = {
    'Colonne': 0,
    'Righe': 1,
    'Prima riga': 2,
    'Prima colonna': 3,
    'Esposizione': 0x40
}

"""
    Velocita' (da quella predefinita in meglio) prese da:
        WT12
        DATA SHEET
        Wednesday, 09 April 2014
        Version 3.1
"""

BT_BAUD = {
    '   trovala   ': 0,
    '    115200   ': 115200,
    '    230400   ': 230400,
    '    256000   ': 256000,	
    '    460800   ': 460800,
    '    921600   ': 921600,
    '   1382400   ': 1382400,
    '   1800000   ': 1800000,	
    '   1843200   ': 1843200,
    '   2765800   ': 2765800
}

# Registri del gas-gauge

GG_REG = {
    #        1111111111222222222223
    #123456789012345678901234567890
    '          Status            ': 0x00,
    '          Control           ': 0x01,
    '     Accumulated Charge     ': 0x02,
    '    Charge Threshold High   ': 0x04,
    '    Charge Threshold Low    ': 0x06,
    '         Voltage            ': 0x08,
    '   Voltage Threshold High   ': 0x0A,
    '   Voltage Threshold Low    ': 0x0C,
    '          Current           ': 0x0E,
    '   Current Threshold High   ': 0x10,
    '   Current Threshold Low    ': 0x12,
    '        Temperature         ': 0x14,
    ' Temperature Threshold High ': 0x16,
    ' Temperature Threshold Low  ': 0x18,
}


class GUI_DBG(gui.New_Toplevel_1):
    def __init__(self, master=None):
        self.master = master
        gui.New_Toplevel_1.__init__(self, master)

        gui_support.portaSeriale.set(NOME_UART)

        self._imposta_tab(TAB_CHIUSA)

        self.dispo = None

        # Code per la comunicazione fra grafica e ciccia
        self.codaEXE = coda.Queue()
        self.codaGUI = coda.Queue()

        self.task = esegui.taskEsecutore(self.codaEXE, self.codaGUI)
        self.task.start()

        self.eco = eco.ECO(self.Button3,
                           gui_support.numEco,
                           gui_support.Messaggio,
                           self.TProgressbar1,
                           self.codaEXE)

        # Comandi dall'esecutore
        self.cmd = {
        }
        self._esegui_GUI()

    def __del__(self):
        pass

    def chiudi(self):
        self.codaEXE.put(("esci",))
        self.task.join()

        if self.dispo is not None:
            self.dispo.Chiudi()
            self.dispo = None

    def _imposta_tab(self, lista):
        for tab in lista:
            stato = 'disabled'
            if lista[tab]:
                stato = 'normal'

            self.TNotebook1.tab(tab, state=stato)

    def _esegui_GUI(self):
        try:
            msg = self.codaGUI.get(0)

            if msg[0] in self.cmd:
                if 2 == len(msg):
                    self.cmd[msg[0]](msg[1])
                else:
                    self.cmd[msg[0]]()
        except coda.Empty:
            pass

        self.master.after(300, self._esegui_GUI)

    ########### SERIALE ######################################################

    def apriFTDI(self):
        if self.dispo is None:
            self.dispo = dispositivo.DISPOSITIVO(vid='0483', pid='5740')
            if not self.dispo.aPosto():
                del self.dispo
                self.dispo = None
            else:
                self.codaEXE.put(("Dispositivo", self.dispo))

                self.Button47['text'] = 'Mollala'
                self.Entry1['state'] = 'readonly'
                self.Button1['state'] = 'disabled'

                self._imposta_tab(TAB_APERTA)
        else:
            self.dispo.Chiudi()
            self.dispo = None
            self.codaEXE.put(("Dispositivo", self.dispo))

            self.Button47['text'] = 'Usa FTDI'
            self.Button1['state'] = 'normal'
            self.Entry1['state'] = 'normal'
            
            self._imposta_tab(TAB_CHIUSA)

    def apriSeriale(self):
        if self.dispo is None:
            porta = gui_support.portaSeriale.get()
            if porta is None:
                gui_support.portaSeriale.set(NOME_UART)
            elif 0 == len(porta):
                gui_support.portaSeriale.set(NOME_UART)
            else:
                self.dispo = dispositivo.DISPOSITIVO(uart=porta)
                if not self.dispo.aPosto():
                    del self.dispo
                    self.dispo = None
                    gui_support.portaSeriale.set(NOME_UART)
                else:
                    self.codaEXE.put(("Dispositivo", self.dispo))

                    self.Entry1['state'] = 'readonly'
                    self.Button1['text'] = 'Mollala'
                    self.Button47['state'] = 'disabled'

                    self._imposta_tab(TAB_APERTA)
        else:
            self.dispo.Chiudi()
            self.dispo = None
            self.codaEXE.put(("Dispositivo", self.dispo))

            self.Button1['text'] = 'Usa questa'
            self.Entry1['state'] = 'normal'
            self.Button47['state'] = 'normal'

            gui_support.portaSeriale.set(NOME_UART)
            self._imposta_tab(TAB_CHIUSA)

    ########### VARIE ########################################################

    def Eco(self):
        gui_support.Messaggio.set("Aspetta ...")
        self.codaEXE.put(("eco",))

    def ecoProva(self, dummy):
        self.eco.Bottone()

    # def revisione(self):
    #     gui_support.Messaggio.set("Aspetta ...")
    #     self.codaEXE.put(("revisione",))
    #
    # def led(self):
    #     gui_support.Messaggio.set("Aspetta ...")
    #     self.codaEXE.put(
    #         ("led",
    #          gui_support.rosso.get(),
    #          gui_support.verde.get(),
    #          gui_support.blu.get()))
    #
    # def cicalino(self):
    #     esito, hz = utili.validaCampo(
    #         gui_support.cicalino.get(), mini=0, maxi=0xFFFF)
    #     if esito:
    #         gui_support.Messaggio.set("Aspetta ...")
    #         self.codaEXE.put(("cicalino", hz))
    #     else:
    #         gui_support.Messaggio.set("? frequenza ?")
    #
    # def tasto(self):
    #     gui_support.Messaggio.set("Aspetta ...")
    #     self.codaEXE.put(("tasto",))
    #
    # def batLeggi(self):
    #     sel = self.Listbox3.curselection()
    #     if sel is None:
    #         gui_support.Messaggio.set("? registro ?")
    #     elif 0 == len(sel):
    #         gui_support.Messaggio.set("? registro ?")
    #     else:
    #         nome = self.Listbox3.get(sel[0])
    #         reg = GG_REG[nome]
    #
    #         gui_support.batVal.set('---')
    #         gui_support.Messaggio.set("Aspetta ...")
    #         self.codaEXE.put(("batLeggi", reg))
    #
    # def batScrivi(self):
    #     sel = self.Listbox3.curselection()
    #     if sel is None:
    #         gui_support.Messaggio.set("? registro ?")
    #     elif 0 == len(sel):
    #         gui_support.Messaggio.set("? registro ?")
    #     else:
    #         nome = self.Listbox3.get(sel[0])
    #         reg = GG_REG[nome]
    #
    #         esito, val = utili.validaCampo(gui_support.batVal.get(), 0, 0xFFFF)
    #         if not esito:
    #             gui_support.Messaggio.set("? valore ?")
    #         else:
    #             gui_support.Messaggio.set("Aspetta ...")
    #             self.codaEXE.put(("batScrivi", reg, val))
    #
    # def reset(self):
    #     gui_support.Messaggio.set("Aspetta ...")
    #     self.codaEXE.put(("reset", int(gui_support.reset.get())))
    #
    # ########### MEMORIE ######################################################
    #
    # def provaRam(self):
    #     gui_support.Messaggio.set("Aspetta ...")
    #     self.codaEXE.put(("provaRam",))
    #
    # def norCar(self):
    #     gui_support.Messaggio.set("Aspetta ...")
    #     self.codaEXE.put(("norCar",))
    #
    # def norCan(self):
    #     esito, blk = utili.validaCampo(gui_support.norBlk.get(), 0, 0xFFFF)
    #     if not esito:
    #         gui_support.Messaggio.set("? blocco ?")
    #     else:
    #         gui_support.Messaggio.set("Aspetta ...")
    #         self.codaEXE.put(("norCan", blk))
    #
    # def norLeggi(self):
    #     try:
    #         esito, blk = utili.validaCampo(gui_support.norBlk.get(), 0, 0xFFFF)
    #         if not esito:
    #             raise utili.problema('? blocco ?')
    #
    #         esito, pos = utili.validaCampo(gui_support.norPos.get(), 0, 0xFFFF)
    #         if not esito:
    #             raise utili.problema('? posizione ?')
    #
    #         esito, dim = utili.validaCampo(gui_support.norDim.get(), 1, 0xFFFF)
    #         if not esito:
    #             raise utili.problema('? dimensione ?')
    #
    #         gui_support.Messaggio.set("Aspetta ...")
    #         self.codaEXE.put(("norLeggi", blk, pos, dim))
    #
    #     except utili.problema as err:
    #         gui_support.Messaggio.set(err)
    #
    # def norScrivi(self):
    #     try:
    #         esito, blk = utili.validaCampo(gui_support.norBlk.get(), 0, 0xFFFF)
    #         if not esito:
    #             raise utili.problema('? blocco ?')
    #
    #         esito, pos = utili.validaCampo(gui_support.norPos.get(), 0, 0xFFFF)
    #         if not esito:
    #             raise utili.problema('? posizione ?')
    #
    #         esito, dim = utili.validaCampo(gui_support.norDim.get(), 1, 0xFFFF)
    #         if not esito:
    #             raise utili.problema('? dimensione ?')
    #
    #         esito, val = utili.validaCampo(gui_support.norVal.get(), 0, 0xFF)
    #         if not esito:
    #             raise utili.problema('? dimensione ?')
    #
    #         gui_support.Messaggio.set("Aspetta ...")
    #         self.codaEXE.put(("norScrivi", blk, pos, dim, val))
    #
    #     except utili.problema as err:
    #         gui_support.Messaggio.set(err)
    #
    # ########### OTTICA #######################################################
    #
    # def laserI(self):
    #     gui_support.Messaggio.set("Aspetta ...")
    #     self.codaEXE.put(("laserI",))
    #
    # def laserF(self):
    #     gui_support.Messaggio.set("Aspetta ...")
    #     self.codaEXE.put(("laserF",))
    #
    # def laserA(self):
    #     esito, pot = utili.validaCampo(
    #         gui_support.laserA.get(), mini=0, maxi=100)
    #     if not esito:
    #         gui_support.Messaggio.set("? potenza ?")
    #     else:
    #         gui_support.Messaggio.set("Aspetta ...")
    #         self.codaEXE.put(("laserA", pot))
    #
    # def camI(self):
    #     gui_support.Messaggio.set("Aspetta ...")
    #     self.codaEXE.put(("camI",))
    #
    # def camF(self):
    #     gui_support.Messaggio.set("Aspetta ...")
    #     self.codaEXE.put(("camF",))
    #
    # def camL(self):
    #     esito, reg = utili.validaCampo(
    #         gui_support.camReg.get(), mini=0, maxi=255)
    #     if esito:
    #         gui_support.Messaggio.set("Aspetta ...")
    #         self.codaEXE.put(("camL", reg))
    #     else:
    #         gui_support.Messaggio.set("? registro ?")
    #
    # def camS(self):
    #     esito, reg = utili.validaCampo(
    #         gui_support.camReg.get(), mini=0, maxi=255)
    #     if esito:
    #         esito, val = utili.validaCampo(
    #             gui_support.camRegS.get(), mini=0, maxi=255)
    #         if esito:
    #             gui_support.Messaggio.set("Aspetta ...")
    #             self.codaEXE.put(("camS", reg, val))
    #         else:
    #             gui_support.Messaggio.set("? valore ?")
    #     else:
    #         gui_support.Messaggio.set("? registro ?")
    #
    # def camPL(self):
    #     sel = self.Listbox2.curselection()
    #     if sel is None:
    #         gui_support.Messaggio.set("? parametro ?")
    #     elif 0 == len(sel):
    #         gui_support.Messaggio.set("? parametro ?")
    #     else:
    #         prm = self.Listbox2.get(sel[0])
    #         prm = CAM_PRM[prm]
    #
    #         gui_support.Messaggio.set("Aspetta ...")
    #         self.codaEXE.put(("camPL", prm))
    #
    # def camPS(self):
    #     sel = self.Listbox2.curselection()
    #     if sel is None:
    #         gui_support.Messaggio.set("? parametro ?")
    #     elif 0 == len(sel):
    #         gui_support.Messaggio.set("? parametro ?")
    #     else:
    #         prm = self.Listbox2.get(sel[0])
    #         prm = CAM_PRM[prm]
    #
    #         esito, val = utili.validaCampo(
    #             gui_support.camPrmS.get(), mini=0, maxi=65535)
    #         if not esito:
    #             gui_support.Messaggio.set("? valore ?")
    #         else:
    #             gui_support.Messaggio.set("Aspetta ...")
    #             self.codaEXE.put(("camPS", prm, val))
    #
    # def foto(self):
    #     gui_support.Messaggio.set("Aspetta ...")
    #     self.codaEXE.put(("camC",))
    #
    # def leggiFoto(self):
    #     defe = '.png'
    #     tipo = [('Colori', defe)]
    #     if '1' == gui_support.qualeFoto.get():
    #         defe = '.pgm'
    #         tipo = [('B/N', defe)]
    #
    #     opzioni = {
    #         'parent': self.master,
    #         'filetypes': tipo,
    #         # 'filetypes': [('Colori', '.png'), ('B/N', '.pgm')],
    #         'title': 'Scegli il file',
    #         # 'defaultextension': '.png'
    #         'defaultextension': defe
    #     }
    #     filename = dialogo.asksaveasfilename(**opzioni)
    #
    #     if filename is None:
    #         gui_support.Messaggio.set("Hai cambiato idea?")
    #     elif 0 == len(filename):
    #         gui_support.Messaggio.set("Hai cambiato idea?")
    #     else:
    #         gui_support.Messaggio.set("Aspetta ...")
    #         self.codaEXE.put(
    #             ("leggiFoto", filename, gui_support.qualeFoto.get()))
    #
    # def las_foto(self):
    #     esito, pot = utili.validaCampo(
    #         gui_support.laserA.get(), mini=0, maxi=100)
    #     if not esito:
    #         gui_support.Messaggio.set("? potenza ?")
    #     elif 0 == pot:
    #         gui_support.Messaggio.set("? potenza 0 ?")
    #     else:
    #         gui_support.Messaggio.set("Aspetta ...")
    #         self.codaEXE.put(("las_foto", pot))
    #
    # def misura(self):
    #     gui_support.Messaggio.set("Aspetta ...")
    #     self.codaEXE.put(("misura",))
    #
    # ########### BLUETOOTH ####################################################
    #
    # def btAccendi(self):
    #     sel = self.Listbox1.curselection()
    #     if sel is None:
    #         gui_support.Messaggio.set("? baud ?")
    #     elif 0 == len(sel):
    #         gui_support.Messaggio.set("? baud ?")
    #     else:
    #         prm = self.Listbox1.get(sel[0])
    #         prm = BT_BAUD[prm]
    #
    #         gui_support.Messaggio.set("Aspetta ...")
    #         if 0 == prm:
    #             self.codaEXE.put(("btAccendiAuto", BT_BAUD))
    #         else:
    #             self.codaEXE.put(("btAccendi", prm))
    #
    # def btSpegni(self):
    #     gui_support.Messaggio.set("Aspetta ...")
    #     self.codaEXE.put(("btSpegni",))
    #
    # def _bt_rx(self, prm):
    #     self.Text1.insert('end', prm)
    #
    # def btCmd(self):
    #     cmd = gui_support.btCmd.get()
    #     if cmd is None:
    #         gui_support.Messaggio.set("? comando ?")
    #     elif len(cmd) == 0:
    #         gui_support.Messaggio.set("? comando ?")
    #     else:
    #         self.Text1.delete(1.0, 'end')
    #         gui_support.Messaggio.set("Aspetta ...")
    #         self.codaEXE.put(("btCmd", cmd + '\r\n'))
    #
    # def btFile(self):
    #     opzioni = {
    #         'parent': self.master,
    #         'filetypes': [('Comandi iwrap', '.txt')],
    #         'title': 'Scegli il file',
    #         'defaultextension': '.txt'
    #     }
    #     filename = dialogo.askopenfilename(**opzioni)
    #
    #     if filename is None:
    #         gui_support.Messaggio.set("Hai cambiato idea?")
    #     elif 0 == len(filename):
    #         gui_support.Messaggio.set("Hai cambiato idea?")
    #     else:
    #         self.Text1.delete(1.0, 'end')
    #         gui_support.Messaggio.set("Aspetta ...")
    #         self.codaEXE.put(("btFile", filename))
    #
    # def btRic(self):
    #     gui_support.Messaggio.set("Aspetta ...")
    #     self.codaEXE.put(("btRic",))
    #
    # ########### AGGIORNA ####################################################
    #
    # def aggSituazione(self):
    #     gui_support.Messaggio.set("Aspetta ...")
    #     self.codaEXE.put(("aggSituazione",))
    #
    # def Aggiorna(self):
    #     opzioni = {
    #         'parent': self.master,
    #         'filetypes': [('Applicazione', '.bin')],
    #         'title': 'Scegli il file'
    #     }
    #     filename = dialogo.askopenfilename(**opzioni)
    #     if filename is None:
    #         gui_support.Messaggio.set("Hai cambiato idea?")
    #     elif 0 == len(filename):
    #         gui_support.Messaggio.set("Hai cambiato idea?")
    #     else:
    #         gui_support.Messaggio.set("Aspetta ...")
    #         self.codaEXE.put(("Aggiorna", filename))
    #
    # def Applica(self):
    #     gui_support.Messaggio.set("Aspetta ...")
    #     self.codaEXE.put(("Applica", ))
    #
    # ########### PARAMETRI ###################################################
    #
    # def matLeggi(self):
    #     gui_support.Messaggio.set("Aspetta ...")
    #     self.codaEXE.put(("matLeggi",))
    #
    # def matScrivi(self):
    #     x = gui_support.matricola.get()
    #     if x is None:
    #         gui_support.Messaggio.set("? cosa scrivo ?")
    #     elif len(x) == 0:
    #         gui_support.Messaggio.set("? cosa scrivo ?")
    #     else:
    #         gui_support.Messaggio.set("Aspetta ...")
    #         self.codaEXE.put(("matScrivi", x))
    #
    # def matCrea(self):
    #     mat = 'LSGxy%06d' % (random.randint(0, 999999))
    #     gui_support.matricola.set(mat)
    #
    # def schLeggi(self):
    #     gui_support.Messaggio.set("Aspetta ...")
    #     self.codaEXE.put(("schLeggi",))
    #
    # def schScrivi(self):
    #     x = gui_support.scheda.get()
    #     if x is None:
    #         gui_support.Messaggio.set("? cosa scrivo ?")
    #     elif len(x) == 0:
    #         gui_support.Messaggio.set("? cosa scrivo ?")
    #     else:
    #         gui_support.Messaggio.set("Aspetta ...")
    #         self.codaEXE.put(("schScrivi", x))
    #
    # def schCrea(self):
    #     mat = '%08X' % (random.randint(0, 0xFFFFFFFFFFFF))
    #     gui_support.scheda.set(mat)
    #
    # def btbaud_l(self):
    #     gui_support.Messaggio.set("Aspetta ...")
    #     self.codaEXE.put(("btbaud_l",))
    #
    # def btbaud_s(self):
    #     esito, baud = utili.validaCampo(gui_support.baudBT.get(), 0, 2765800)
    #     if not esito:
    #         gui_support.Messaggio.set("? baud ?")
    #     else:
    #         gui_support.Messaggio.set("Aspetta ...")
    #         self.codaEXE.put(("btbaud_s", baud))


if __name__ == '__main__':
    ROOT = gui.Tk()
    ROOT.title('Debug scaldabagno')
    ROOT.geometry("603x581+285+127")

    gui_support.set_Tk_var()

    gui_support.Messaggio.set("Nessun errore")


    FINESTRA = GUI_DBG(ROOT)
    gui_support.init(ROOT, FINESTRA)
    ROOT.mainloop()

    FINESTRA.chiudi()
