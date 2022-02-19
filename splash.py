# Importing application:
from grape import application_

# ImportLibraryHere
from tkinter import *

# SplashScreen


sroot = Tk()
sroot.overrideredirect(1)

sroot.minsize(height=417, width=600)

sroot.title("Splash window")

sroot.configure()

spath = 'Images\\grape.png'

simg = PhotoImage(file=spath)

my = Label(sroot, image=simg)

my.image = simg

my.place(x=-2, y=-1.5)

Frame(sroot, height=500, width=900, bg='black').place(x=520, y=500)


# MainScreen


def mainroot():
    application_()


# calling the main window here


def call_mainroot():
    sroot.destroy()

    mainroot()


sroot.after(3000, call_mainroot)  # TimeOfSplashScreen

mainloop()
