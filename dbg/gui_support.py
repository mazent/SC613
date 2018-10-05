#! /usr/bin/env python
#
# Support module generated by PAGE version 4.5
# In conjunction with Tcl version 8.6
#    Oct 04, 2018 03:37:55 PM


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

def set_Tk_var():
    # These are Tk variables used passed to Tkinter and must be
    # defined before the widgets using them are created.
    global portaSeriale
    portaSeriale = StringVar()

    global numEco
    numEco = StringVar()

    global revisione
    revisione = StringVar()

    global rosso
    rosso = StringVar()

    global verde
    verde = StringVar()

    global cicalino
    cicalino = StringVar()

    global matricola
    matricola = StringVar()

    global scheda
    scheda = StringVar()

    global Messaggio
    Messaggio = StringVar()


def init(top, gui, arg=None):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

