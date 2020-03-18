import os
import time
import threading
import Packet
import struct
import calendar
import time
from tkinter import *
from tkinter import Button, Tk, HORIZONTAL
from tkinter.ttk import Progressbar
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

def makeform(root, fields):
    entries = []
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=20, text=field, anchor='w')
        ent = Entry(row)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries.append((field, ent))
    return entries


def processEntry(entries):
    infoDict = {}
    for entry in entries:       
        field = entry[0]
        text  = entry[1].get()
        infoDict[field] = text
        
    return infoDict

def openFile():
    filename = askopenfilename(filetypes = (("BandMaster SM Files","*.sm"),("All files","*.*")))
    if(filename):
        file = open(filename, 'rb')
        file.seek(0)
        filetype = file.read(2)
        if(filetype.decode("ASCII") != "SM"):
            messagebox.showerror('Error', 'The file you choose is not a BandMaster SM file!')        
        else:
            file.read(3) # Don't know what this is
            smVersion = struct.unpack("B", file.read(1))[0]
            file.read(27)
            level = struct.unpack("B", file.read(1))[0]
            ents[3][1].delete(0,END)
            ents[3][1].insert(0,level)
            file.read(2)
            bpm = struct.unpack("B", file.read(1))[0]
            ents[4][1].delete(0,END)
            ents[4][1].insert(0,bpm)
            # ents[4][1].configure(state='disable')
            file.read(3)
            official = struct.unpack("B", file.read(1))[0]
            file.read(19)
            data = file.read(246)
            packet = Packet.Packet(data)
            title = packet.getUnicodeString(82)
            artist = packet.getUnicodeString(82)
            charter = packet.getUnicodeString(82)
            if(official == 15):
                checkButtonVariable.set(1)
            file.read(320)
            bgmData = file.read(82)
            bgmPacket = Packet.Packet(bgmData)
            bgmFile = bgmPacket.getUnicodeString(82)
            ents[0][1].delete(0,END)
            ents[0][1].insert(0,title)
            ents[1][1].delete(0,END)
            ents[1][1].insert(0,artist)
            ents[2][1].delete(0,END)
            ents[2][1].insert(0,charter)
            ents[5][1].delete(0,END)
            ents[5][1].insert(0,bgmFile)
            status['text'] = "Click 'Save' to save your edit..."
            file.close()

def saveFile():
    currentFileName = askopenfilename(filetypes = (("BandMaster SM Files","*.sm"),("All files","*.*")))
    if(currentFileName):
        file = open(currentFileName, 'rb+')
        file.seek(0)
        file.read(12)
        file.write(struct.pack("I", calendar.timegm(time.gmtime())))
        file.read(17)
        file.write(bytes([int(ents[3][1].get())]))
        file.read(2)
        file.write(bytes([int(ents[4][1].get())]))
        file.read(3)
        if(checkButtonVariable.get() == 1):
            file.write(bytes([15]))
        else:
            file.write(bytes([0]))
        file.read(19)
        file.write(ents[0][1].get().encode("utf-16-le"))
        file.write(b'\x00' * (82 - len(ents[0][1].get().encode('utf-16-le'))))
        file.write(ents[1][1].get().encode("utf-16-le"))
        file.write(b'\x00' * (82 - len(ents[1][1].get().encode('utf-16-le'))))
        file.write(ents[2][1].get().encode("utf-16-le"))
        file.write(b'\x00' * (82 - len(ents[2][1].get().encode('utf-16-le'))))
        file.read(320)
        file.write(ents[5][1].get().encode("utf-16-le"))
        file.write(b'\x00' * (82 - len(ents[5][1].get().encode('utf-16-le'))))
        file.close()
        messagebox.showinfo('Successful', 'Write to file successful!')    

root = Tk()
root.title("BandMaster SM Tool")
root.geometry("600x320")

#root.iconbitmap(os.path.join(os.getcwd(), 'favicon.ico'))

fields = 'Title', 'Artist', 'Charter', 'Level', 'BPM', 'BGM File'

ents = makeform(root, fields)
checkButtonVariable = IntVar()

row1 = Frame(root)
officialSongButton = Checkbutton(row1, text="Official SM", variable=checkButtonVariable)
openFileButton = Button(row1, text='Open', command=(openFile))
saveFileButton = Button(row1, text='Save', command=(saveFile))
generateSMPFileButton = Button(row1, text='Generate SMP')
percent = Label(root, text="", anchor=S)
progress = Progressbar(root, length=500, mode='determinate')
status = Label(root, text="Click 'Open' and navigate to SM file..", relief=SUNKEN, anchor=W, bd=2)

# officialSongButton.pack(pady=15, side=LEFT)
row1.pack(side=TOP, fill=X, padx=5, pady=5)
officialSongButton.pack(side=LEFT)
saveFileButton.pack(side=RIGHT)
openFileButton.pack(side=RIGHT, padx=5)
generateSMPFileButton.pack(side=RIGHT)
percent.pack()
progress.pack()
status.pack(side=BOTTOM, fill=X)

root.mainloop()