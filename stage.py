import Tkinter as tk
from Tkinter import *
from Tkinter import Label, Canvas
import tkMessageBox
import os
import pickle
import numpy as np
from tkFileDialog import askopenfile,askopenfilename
# create button function
def tkButtonCreate(text, command):
    tk.Button(window, text = text, command = command).pack()
def drawWindow(str):
    window = tk.Tk()
    window.title(str) # sets the window title to the

    window.geometry("%dx%d+0+0" % (600, 300))
    window.resizable(0, 0)
    return window
def SetMapper():
    filename = askopenfilename(filetypes = (("Excel files", "*.xls;*.xlsx")
                                                         ,("All files", "*.*") ))
    if (".xls" in filename or ".xlsx" in filename):
        tex1.delete(1.0, END)
        tex1.insert(tk.END, filename)
        TestFileBtn.configure(state=NORMAL)
    else:
        TestFileBtn.configure(state=DISABLED)
def TestFile():
    Closing_page1()
    main2()
def Continu():
	window.destroy()
def Clear():
	window.destroy()
def Exit_page1():
    Closing_page1()
    main()
def main1():
    global window1
    global tex1, TestFileBtn
    window1 = drawWindow('Page 1')
    tex1 = tk.Text(window1, height=1, width=60, font=('comicsans', 9))
    tex1.place(x=15, y=15)
    SetMapperBtn = tk.Button(window1, width=12, text='Set Mapper', fg='white', bg='purple', font=('comicsans', 10),
                             command=SetMapper)
    SetMapperBtn.place(x=50, y=270)
    TestFileBtn = tk.Button(window1, width=12, text='Test Files', fg='white', bg='purple', font=('comicsans', 10),
                            command=TestFile)
    TestFileBtn.place(x=205, y=270)
    TestFileBtn.configure(state=DISABLED)
    ExitBtn = tk.Button(window1, width=8, text='Exit', fg='white', bg='purple', font=('comicsans', 10),
                        command=Exit_page1)
    ExitBtn.place(x=455, y=270)

    window1.protocol('WM_DELETE_WINDOW', Closing_page1)  # root is your root window

    window1.mainloop()
def Gotopage1():
    Closing()
    main1()
def SetFiles():
    filename = askopenfilename(filetypes=(("DAT files", "*.dat")
                                          , ("All files", "*.*")))
    if (".DAT" in filename):
        tex2.delete(1.0, END)
        tex2.insert(tk.END, filename)
def Back():
    Closing_page2()
    main1()
def RunTest():
    window2.destroy()
def main2():
    global window2
    global tex2
    window2 = drawWindow('Page 2')
    tex2 = tk.Text(window2, height=1, width=60, font=('comicsans', 9))
    tex2.place(x=15, y=15)
    SetFilesBtn = tk.Button(window2, width=12, text='Set Files', fg='white', bg='purple', font=('comicsans', 10),
                            command=SetFiles)
    SetFilesBtn.place(x=50, y=270)
    RntestBtn = tk.Button(window2, width=12, text='Run Test', fg='white', bg='purple', font=('comicsans', 10),
                          command=RunTest)
    RntestBtn.place(x=205, y=270)
    BackBtn = tk.Button(window2, width=8, text='Back To 1', fg='white', bg='purple', font=('comicsans', 10),
                        command=Back)
    BackBtn.place(x=455, y=270)

    window2.protocol('WM_DELETE_WINDOW', Closing_page2)  # root is your root window

    window2.mainloop()
def Gotopage2():
    Closing()
    main2()
def Closing_page2():
    window2.destroy()
def Closing_page1():
    window1.destroy()
def Closing():
    window.destroy()


def main():
    global window
    window = drawWindow("start page")
    GoPage1Btn = tk.Button(window, width=12,text='Go to Page One', fg='white',   bg='purple', font=('comicsans', 10), command=Gotopage1)
    GoPage1Btn.place(x=10,y=270)
    GoPage2Btn = tk.Button(window, width=12,text='Go to Page Two', fg='white',   bg='purple', font=('comicsans', 10), command=Gotopage2)
    GoPage2Btn.place(x=125,y=270)
    ClearBtn = tk.Button(window, width=8, text='Clear', fg='white', bg='purple', font=('comicsans', 10),
                           command=Clear)
    ClearBtn.place(x=355, y=270)
    ContinueBtn = tk.Button(window, width=8, text='Continue', fg='white', bg='purple', font=('comicsans', 10),
                         command=Continu)
    ContinueBtn.place(x=435, y=270)
    ExitBtn = tk.Button(window, width=8, text='Exit', fg='white', bg='purple', font=('comicsans', 10),
                         command=Closing)
    ExitBtn.place(x=515, y=270)
    window.protocol('WM_DELETE_WINDOW', Closing)  # root is your root window


    window.mainloop()
main()