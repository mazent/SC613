#! /usr/bin/env python
#
# GUI module generated by PAGE version 4.5
# In conjunction with Tcl version 8.6
#    Oct 04, 2018 03:38:00 PM
import sys

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

import gui_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = Tk()
    root.title('New_Toplevel_1')
    geom = "603x581+285+127"
    root.geometry(geom)
    gui_support.set_Tk_var()
    w = New_Toplevel_1 (root)
    gui_support.init(root, w)
    root.mainloop()

w = None
def create_New_Toplevel_1(root, param=None):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = Toplevel (root)
    w.title('New_Toplevel_1')
    geom = "603x581+285+127"
    w.geometry(geom)
    gui_support.set_Tk_var()
    w_win = New_Toplevel_1 (w)
    gui_support.init(w, w_win, param)
    return w_win

def destroy_New_Toplevel_1():
    global w
    w.destroy()
    w = None


class New_Toplevel_1:
    def __init__(self, master=None):
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85' 
        _ana2color = '#d9d9d9' # X11 color: 'gray85' 
        font11 = "-family {Courier New} -size 10 -weight normal -slant"  \
            " roman -underline 0 -overstrike 0"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])
        master.configure(background="#d9d9d9")
        master.configure(highlightbackground="#d9d9d9")
        master.configure(highlightcolor="black")


        self.style.configure('TNotebook.Tab', background=_bgcolor)
        self.style.configure('TNotebook.Tab', foreground=_fgcolor)
        self.style.map('TNotebook.Tab', background=
            [('selected', _compcolor), ('active',_ana2color)])
        self.TNotebook1 = ttk.Notebook(master)
        self.TNotebook1.place(relx=0.02, rely=0.08, relheight=0.87
                , relwidth=0.94)
        self.TNotebook1.configure(width=569)
        self.TNotebook1.configure(takefocus="")
        self.TNotebook1_pg0 = ttk.Frame(self.TNotebook1)
        self.TNotebook1.add(self.TNotebook1_pg0, padding=3)
        self.TNotebook1.tab(0, text="Seriale",underline="-1",)
        self.TNotebook1_pg1 = ttk.Frame(self.TNotebook1)
        self.TNotebook1.add(self.TNotebook1_pg1, padding=3)
        self.TNotebook1.tab(1, text="Varie",underline="-1",)
        self.TNotebook1_pg2 = ttk.Frame(self.TNotebook1)
        self.TNotebook1.add(self.TNotebook1_pg2, padding=3)
        self.TNotebook1.tab(2, text="Parametri",underline="-1",)

        self.Entry1 = Entry(self.TNotebook1_pg0)
        self.Entry1.place(relx=0.23, rely=0.23, relheight=0.05, relwidth=0.69)
        self.Entry1.configure(background="white")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font=font11)
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(highlightbackground="#d9d9d9")
        self.Entry1.configure(highlightcolor="black")
        self.Entry1.configure(insertbackground="black")
        self.Entry1.configure(justify=CENTER)
        self.Entry1.configure(selectbackground="#c4c4c4")
        self.Entry1.configure(selectforeground="black")
        self.Entry1.configure(textvariable=gui_support.portaSeriale)

        self.Button1 = Button(self.TNotebook1_pg0)
        self.Button1.place(relx=0.05, rely=0.23, height=25, width=80)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background=_bgcolor)
        self.Button1.configure(command=self.apriSeriale)
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Usa questa''')

        self.Button47 = Button(self.TNotebook1_pg0)
        self.Button47.place(relx=0.05, rely=0.34, height=25, width=80)
        self.Button47.configure(activebackground="#d9d9d9")
        self.Button47.configure(activeforeground="#000000")
        self.Button47.configure(background=_bgcolor)
        self.Button47.configure(command=self.apriFTDI)
        self.Button47.configure(disabledforeground="#a3a3a3")
        self.Button47.configure(foreground="#000000")
        self.Button47.configure(highlightbackground="#d9d9d9")
        self.Button47.configure(highlightcolor="black")
        self.Button47.configure(pady="0")
        self.Button47.configure(text='''Usa FTDI''')

        self.Button2 = Button(self.TNotebook1_pg1)
        self.Button2.place(relx=0.05, rely=0.05, height=25, width=50)
        self.Button2.configure(activebackground="#d9d9d9")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background=_bgcolor)
        self.Button2.configure(command=self.Eco)
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''Eco''')

        self.TLabelframe1 = ttk.Labelframe(self.TNotebook1_pg1)
        self.TLabelframe1.place(relx=0.18, rely=0.02, relheight=0.24
                , relwidth=0.41)
        self.TLabelframe1.configure(text='''Prova''')
        self.TLabelframe1.configure(width=230)

        self.Label2 = Label(self.TLabelframe1)
        self.Label2.place(relx=0.09, rely=0.22, height=25, width=39)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(background=_bgcolor)
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(text='''Invia''')

        self.Entry2 = Entry(self.TLabelframe1)
        self.Entry2.place(relx=0.33, rely=0.22, relheight=0.22, relwidth=0.3)
        self.Entry2.configure(background="white")
        self.Entry2.configure(disabledforeground="#a3a3a3")
        self.Entry2.configure(font=font11)
        self.Entry2.configure(foreground="#000000")
        self.Entry2.configure(highlightbackground="#d9d9d9")
        self.Entry2.configure(highlightcolor="black")
        self.Entry2.configure(insertbackground="black")
        self.Entry2.configure(justify=CENTER)
        self.Entry2.configure(selectbackground="#c4c4c4")
        self.Entry2.configure(selectforeground="black")
        self.Entry2.configure(textvariable=gui_support.numEco)

        self.Button3 = Button(self.TLabelframe1)
        self.Button3.place(relx=0.7, rely=0.22, height=25, width=50)
        self.Button3.configure(activebackground="#d9d9d9")
        self.Button3.configure(activeforeground="#000000")
        self.Button3.configure(background=_bgcolor)
        self.Button3.configure(disabledforeground="#a3a3a3")
        self.Button3.configure(foreground="#000000")
        self.Button3.configure(highlightbackground="#d9d9d9")
        self.Button3.configure(highlightcolor="black")
        self.Button3.configure(pady="0")
        self.Button3.configure(text='''Eco''')
        self.Button3.bind('<ButtonRelease-1>',self.ecoProva)

        self.TProgressbar1 = ttk.Progressbar(self.TLabelframe1)
        self.TProgressbar1.place(relx=0.13, rely=0.57, relwidth=0.78
                , relheight=0.0, height=22)
        self.TProgressbar1.configure(mode="indeterminate")

        self.TLabelframe2 = ttk.Labelframe(self.TNotebook1_pg1)
        self.TLabelframe2.place(relx=0.02, rely=0.27, relheight=0.15
                , relwidth=0.45)
        self.TLabelframe2.configure(text='''Versione''')
        self.TLabelframe2.configure(width=257)

        self.Button4 = Button(self.TLabelframe2)
        self.Button4.place(relx=0.1, rely=0.37, height=25, width=70)
        self.Button4.configure(activebackground="#d9d9d9")
        self.Button4.configure(activeforeground="#000000")
        self.Button4.configure(background=_bgcolor)
        self.Button4.configure(command=self.revisione)
        self.Button4.configure(disabledforeground="#a3a3a3")
        self.Button4.configure(foreground="#000000")
        self.Button4.configure(highlightbackground="#d9d9d9")
        self.Button4.configure(highlightcolor="black")
        self.Button4.configure(pady="0")
        self.Button4.configure(text='''Revisione''')

        self.Entry3 = Entry(self.TLabelframe2)
        self.Entry3.place(relx=0.47, rely=0.32, relheight=0.34, relwidth=0.39)
        self.Entry3.configure(background="white")
        self.Entry3.configure(disabledforeground="#a3a3a3")
        self.Entry3.configure(font=font11)
        self.Entry3.configure(foreground="#000000")
        self.Entry3.configure(highlightbackground="#d9d9d9")
        self.Entry3.configure(highlightcolor="black")
        self.Entry3.configure(insertbackground="black")
        self.Entry3.configure(justify=CENTER)
        self.Entry3.configure(selectbackground="#c4c4c4")
        self.Entry3.configure(selectforeground="black")
        READONLY = 'readonly'
        self.Entry3.configure(state=READONLY)
        self.Entry3.configure(textvariable=gui_support.revisione)

        self.TLabelframe8 = ttk.Labelframe(self.TNotebook1_pg1)
        self.TLabelframe8.place(relx=0.05, rely=0.69, relheight=0.23
                , relwidth=0.32)
        self.TLabelframe8.configure(text='''Led''')
        self.TLabelframe8.configure(width=178)

        self.Checkbutton1 = Checkbutton(self.TLabelframe8)
        self.Checkbutton1.place(relx=0.11, rely=0.25, relheight=0.23
                , relwidth=0.33)
        self.Checkbutton1.configure(activebackground="#d9d9d9")
        self.Checkbutton1.configure(activeforeground="#000000")
        self.Checkbutton1.configure(background=_bgcolor)
        self.Checkbutton1.configure(disabledforeground="#a3a3a3")
        self.Checkbutton1.configure(foreground="#000000")
        self.Checkbutton1.configure(highlightbackground="#d9d9d9")
        self.Checkbutton1.configure(highlightcolor="black")
        self.Checkbutton1.configure(justify=LEFT)
        self.Checkbutton1.configure(text='''Rosso''')
        self.Checkbutton1.configure(variable=gui_support.rosso)

        self.Checkbutton2 = Checkbutton(self.TLabelframe8)
        self.Checkbutton2.place(relx=0.11, rely=0.55, relheight=0.23
                , relwidth=0.33)
        self.Checkbutton2.configure(activebackground="#d9d9d9")
        self.Checkbutton2.configure(activeforeground="#000000")
        self.Checkbutton2.configure(background=_bgcolor)
        self.Checkbutton2.configure(disabledforeground="#a3a3a3")
        self.Checkbutton2.configure(foreground="#000000")
        self.Checkbutton2.configure(highlightbackground="#d9d9d9")
        self.Checkbutton2.configure(highlightcolor="black")
        self.Checkbutton2.configure(justify=LEFT)
        self.Checkbutton2.configure(text='''Verde''')
        self.Checkbutton2.configure(variable=gui_support.verde)

        self.Button14 = Button(self.TLabelframe8)
        self.Button14.place(relx=0.53, rely=0.3, height=50, width=47)
        self.Button14.configure(activebackground="#d9d9d9")
        self.Button14.configure(activeforeground="#000000")
        self.Button14.configure(background=_bgcolor)
        self.Button14.configure(command=self.led)
        self.Button14.configure(disabledforeground="#a3a3a3")
        self.Button14.configure(foreground="#000000")
        self.Button14.configure(highlightbackground="#d9d9d9")
        self.Button14.configure(highlightcolor="black")
        self.Button14.configure(pady="0")
        self.Button14.configure(text='''Scrivi''')
        self.Button14.configure(width=47)

        self.TLabelframe10 = ttk.Labelframe(self.TNotebook1_pg1)
        self.TLabelframe10.place(relx=0.02, rely=0.47, relheight=0.16
                , relwidth=0.48)
        self.TLabelframe10.configure(text='''Cicalino''')
        self.TLabelframe10.configure(width=270)

        self.Label18 = Label(self.TLabelframe10)
        self.Label18.place(relx=0.06, rely=0.4, height=21, width=60)
        self.Label18.configure(activebackground="#f9f9f9")
        self.Label18.configure(activeforeground="black")
        self.Label18.configure(background=_bgcolor)
        self.Label18.configure(disabledforeground="#a3a3a3")
        self.Label18.configure(foreground="#000000")
        self.Label18.configure(highlightbackground="#d9d9d9")
        self.Label18.configure(highlightcolor="black")
        self.Label18.configure(text='''Frequenza''')

        self.Entry22 = Entry(self.TLabelframe10)
        self.Entry22.place(relx=0.33, rely=0.35, relheight=0.32, relwidth=0.22)
        self.Entry22.configure(background="white")
        self.Entry22.configure(disabledforeground="#a3a3a3")
        self.Entry22.configure(font=font11)
        self.Entry22.configure(foreground="#000000")
        self.Entry22.configure(highlightbackground="#d9d9d9")
        self.Entry22.configure(highlightcolor="black")
        self.Entry22.configure(insertbackground="black")
        self.Entry22.configure(justify=CENTER)
        self.Entry22.configure(selectbackground="#c4c4c4")
        self.Entry22.configure(selectforeground="black")
        self.Entry22.configure(textvariable=gui_support.cicalino)

        self.Label19 = Label(self.TLabelframe10)
        self.Label19.place(relx=0.61, rely=0.39, height=21, width=20)
        self.Label19.configure(activebackground="#f9f9f9")
        self.Label19.configure(activeforeground="black")
        self.Label19.configure(background=_bgcolor)
        self.Label19.configure(disabledforeground="#a3a3a3")
        self.Label19.configure(foreground="#000000")
        self.Label19.configure(highlightbackground="#d9d9d9")
        self.Label19.configure(highlightcolor="black")
        self.Label19.configure(text='''Hz''')

        self.Button19 = Button(self.TLabelframe10)
        self.Button19.place(relx=0.74, rely=0.39, height=25, width=50)
        self.Button19.configure(activebackground="#d9d9d9")
        self.Button19.configure(activeforeground="#000000")
        self.Button19.configure(background=_bgcolor)
        self.Button19.configure(command=self.cicalino)
        self.Button19.configure(disabledforeground="#a3a3a3")
        self.Button19.configure(foreground="#000000")
        self.Button19.configure(highlightbackground="#d9d9d9")
        self.Button19.configure(highlightcolor="black")
        self.Button19.configure(pady="0")
        self.Button19.configure(text='''Scrivi''')

        self.TLabelframe11 = ttk.Labelframe(self.TNotebook1_pg2)
        self.TLabelframe11.place(relx=0.04, rely=0.04, relheight=0.26
                , relwidth=0.74)
        self.TLabelframe11.configure(text='''Matricola''')
        self.TLabelframe11.configure(width=418)

        self.Button33 = Button(self.TLabelframe11)
        self.Button33.place(relx=0.06, rely=0.3, height=25, width=50)
        self.Button33.configure(activebackground="#d9d9d9")
        self.Button33.configure(activeforeground="#000000")
        self.Button33.configure(background=_bgcolor)
        self.Button33.configure(command=self.matLeggi)
        self.Button33.configure(disabledforeground="#a3a3a3")
        self.Button33.configure(foreground="#000000")
        self.Button33.configure(highlightbackground="#d9d9d9")
        self.Button33.configure(highlightcolor="black")
        self.Button33.configure(pady="0")
        self.Button33.configure(text='''Leggi''')

        self.Button34 = Button(self.TLabelframe11)
        self.Button34.place(relx=0.79, rely=0.31, height=25, width=50)
        self.Button34.configure(activebackground="#d9d9d9")
        self.Button34.configure(activeforeground="#000000")
        self.Button34.configure(background=_bgcolor)
        self.Button34.configure(command=self.matScrivi)
        self.Button34.configure(disabledforeground="#a3a3a3")
        self.Button34.configure(foreground="#000000")
        self.Button34.configure(highlightbackground="#d9d9d9")
        self.Button34.configure(highlightcolor="black")
        self.Button34.configure(pady="0")
        self.Button34.configure(text='''Scrivi''')

        self.Entry31 = Entry(self.TLabelframe11)
        self.Entry31.place(relx=0.22, rely=0.32, relheight=0.2, relwidth=0.54)
        self.Entry31.configure(background="white")
        self.Entry31.configure(disabledforeground="#a3a3a3")
        self.Entry31.configure(font=font11)
        self.Entry31.configure(foreground="#000000")
        self.Entry31.configure(highlightbackground="#d9d9d9")
        self.Entry31.configure(highlightcolor="black")
        self.Entry31.configure(insertbackground="black")
        self.Entry31.configure(justify=CENTER)
        self.Entry31.configure(selectbackground="#c4c4c4")
        self.Entry31.configure(selectforeground="black")
        self.Entry31.configure(textvariable=gui_support.matricola)

        self.Button37 = Button(self.TLabelframe11)
        self.Button37.place(relx=0.41, rely=0.63, height=25, width=50)
        self.Button37.configure(activebackground="#d9d9d9")
        self.Button37.configure(activeforeground="#000000")
        self.Button37.configure(background=_bgcolor)
        self.Button37.configure(command=self.matCrea)
        self.Button37.configure(disabledforeground="#a3a3a3")
        self.Button37.configure(foreground="#000000")
        self.Button37.configure(highlightbackground="#d9d9d9")
        self.Button37.configure(highlightcolor="black")
        self.Button37.configure(pady="0")
        self.Button37.configure(text='''Crea''')

        self.TLabelframe12 = ttk.Labelframe(self.TNotebook1_pg2)
        self.TLabelframe12.place(relx=0.04, rely=0.34, relheight=0.28
                , relwidth=0.74)
        self.TLabelframe12.configure(text='''Scheda''')
        self.TLabelframe12.configure(width=418)

        self.Button35 = Button(self.TLabelframe12)
        self.Button35.place(relx=0.06, rely=0.29, height=25, width=50)
        self.Button35.configure(activebackground="#d9d9d9")
        self.Button35.configure(activeforeground="#000000")
        self.Button35.configure(background=_bgcolor)
        self.Button35.configure(command=self.schLeggi)
        self.Button35.configure(disabledforeground="#a3a3a3")
        self.Button35.configure(foreground="#000000")
        self.Button35.configure(highlightbackground="#d9d9d9")
        self.Button35.configure(highlightcolor="black")
        self.Button35.configure(pady="0")
        self.Button35.configure(text='''Leggi''')

        self.Button36 = Button(self.TLabelframe12)
        self.Button36.place(relx=0.79, rely=0.3, height=25, width=50)
        self.Button36.configure(activebackground="#d9d9d9")
        self.Button36.configure(activeforeground="#000000")
        self.Button36.configure(background=_bgcolor)
        self.Button36.configure(command=self.schScrivi)
        self.Button36.configure(disabledforeground="#a3a3a3")
        self.Button36.configure(foreground="#000000")
        self.Button36.configure(highlightbackground="#d9d9d9")
        self.Button36.configure(highlightcolor="black")
        self.Button36.configure(pady="0")
        self.Button36.configure(text='''Scrivi''')

        self.Entry32 = Entry(self.TLabelframe12)
        self.Entry32.place(relx=0.22, rely=0.3, relheight=0.19, relwidth=0.54)
        self.Entry32.configure(background="white")
        self.Entry32.configure(disabledforeground="#a3a3a3")
        self.Entry32.configure(font=font11)
        self.Entry32.configure(foreground="#000000")
        self.Entry32.configure(highlightbackground="#d9d9d9")
        self.Entry32.configure(highlightcolor="black")
        self.Entry32.configure(insertbackground="black")
        self.Entry32.configure(justify=CENTER)
        self.Entry32.configure(selectbackground="#c4c4c4")
        self.Entry32.configure(selectforeground="black")
        self.Entry32.configure(textvariable=gui_support.scheda)

        self.Button38 = Button(self.TLabelframe12)
        self.Button38.place(relx=0.42, rely=0.64, height=25, width=50)
        self.Button38.configure(activebackground="#d9d9d9")
        self.Button38.configure(activeforeground="#000000")
        self.Button38.configure(background=_bgcolor)
        self.Button38.configure(command=self.schCrea)
        self.Button38.configure(disabledforeground="#a3a3a3")
        self.Button38.configure(foreground="#000000")
        self.Button38.configure(highlightbackground="#d9d9d9")
        self.Button38.configure(highlightcolor="black")
        self.Button38.configure(pady="0")
        self.Button38.configure(text='''Crea''')

        self.Label1 = Label(master)
        self.Label1.place(relx=0.03, rely=0.02, height=21, width=559)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background=_bgcolor)
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(textvariable=gui_support.Messaggio)



    def Eco(self):
            print('self.Eco')
            sys.stdout.flush()

    def apriFTDI(self):
            print('self.apriFTDI')
            sys.stdout.flush()

    def apriSeriale(self):
            print('self.apriSeriale')
            sys.stdout.flush()

    def cicalino(self):
            print('self.cicalino')
            sys.stdout.flush()

    def ecoProva(self,p1):
            print('self.ecoProva')
            sys.stdout.flush()

    def led(self):
            print('self.led')
            sys.stdout.flush()

    def matCrea(self):
            print('self.matCrea')
            sys.stdout.flush()

    def matLeggi(self):
            print('self.matLeggi')
            sys.stdout.flush()

    def matScrivi(self):
            print('self.matScrivi')
            sys.stdout.flush()

    def revisione(self):
            print('self.revisione')
            sys.stdout.flush()

    def schCrea(self):
            print('self.schCrea')
            sys.stdout.flush()

    def schLeggi(self):
            print('self.schLeggi')
            sys.stdout.flush()

    def schScrivi(self):
            print('self.schScrivi')
            sys.stdout.flush()





if __name__ == '__main__':
    vp_start_gui()


