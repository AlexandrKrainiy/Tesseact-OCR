import Tkinter as tk
from Tkinter import *
from Tkinter import Label, Canvas
import tkMessageBox
from PIL import Image,ImageTk
from pathlib import Path
import pickle
import numpy as np
from pypdfocr import pypdfocr_gs as pdfImg
from pypdfocr import pypdfocr_tesseract
from tkFileDialog import askopenfile # Will be used to open the file from the user
from pytesseract import image_to_string
import pytesseract
import imutils
import ttk
import cv2
import os
import pytesser
import pygame
import matplotlib.pyplot as plt


class template:
    name=""
    itemsname=[]
    itemstype=[]
    itemfposx=[]
    itemfposy=[]
    itemsposx = []
    itemsposy = []
    itemcount=0

    def __init__(self):
        self.name=""
        self.itemfposx=[]
        self.itemfposy=[]
        self.itemstype=[]
        self.itemsposx = []
        self.itemsposy = []
        self.itemcount=0
    def itemADD(self,type,fposx,fposy,sposx,sposy):
        self.itemstype.append(type)
        self.itemfposx.append(fposx)
        self.itemfposy.append(fposy)
        self.itemsposx.append(sposx)
        self.itemsposy.append(sposy)
        self.itemcount =self.itemcount+1
    def itemChange(self, index,type,fposx,fposy,sposx,sposy):
        self.itemstype[index]=type
        self.itemfposx[index]=fposx
        self.itemfposy[index]=fposy
        self.itemsposx[index]=sposx
        self.itemsposy[index]=sposy
    def itemDEL(self, index):
        self.itemstype = self.itemstype[:index] + self.itemstype[index + 1:]
        self.itemfposx = self.itemfposx[:index] + self.itemfposx[index + 1:]
        self.itemfposy = self.itemfposy[:index] + self.itemfposy[index + 1:]
        self.itemsposx = self.itemsposx[:index] + self.itemsposx[index + 1:]
        self.itemsposy = self.itemsposy[:index] + self.itemsposy[index + 1:]
        self.itemcount =self.itemcount-1
def ADD_Template(temp, Ntemplate):
    global Comboldinxex, Combcurrentindex,Ntemp
    if(Ntemplate.name=="\n" or Ntemplate.name==""):
        tkMessageBox.showerror("Error", "Please input Template name")
        return temp
    else:
        if(len(temp)>0):
            for i in range(len(temp)):
                if(temp[i].name==Ntemplate.name):
                    tkMessageBox.showerror("Error", "Please input Other Template name")
                    return temp
        if(Ntemplate.itemcount<=0):
            tkMessageBox.showerror("Error", "This template doesn't have any items, Please add item in this template!")
            return temp
        else:
            tkMessageBox.showinfo("Sucsess!", "Added Successfully!")
            temp.append(Ntemplate)
            Additem['values'] = []
            Addname.delete(1.0, END)
            AddComb.current(0)
            Additem.set('')
            # add template part
            str1 = Comb['values']
            cstr = []
            for i in range(len(str1)):
                cstr.append(str1[i])
            cstr.append(Ntemplate.name)
            Comb['values'] = cstr
            Combcurrentindex=len(cstr) - 1
            Comb.current(len(cstr) - 1)
            item_initial([])
            Ntemp = template()

            return temp
def DEL_Template(template, index):
    if(index==-1):
        return template
    template=template[:index]+template[index+1 :]
    return template


pressedflag=0
# create button function
def tkButtonCreate(text, command):
    tk.Button(window, text = text, command = command).pack()

# Draws window, opens picture selected by user, packs the canvas
def drawWindow():
    window = tk.Tk()
    window.title("OCR Form") # sets the window title to the

    window.geometry("%dx%d+0+0" % (750, 700))
    window.resizable(0, 0)
    return window

def Open_pdf():
    global Oimg,img
    global canvas
    global W,H
    global openflag,filename
    global PAGE
    W=500;H=600
    directory = askopenfile()
    filename=directory.name
    if(".pdf" in filename):
        tex.delete(1.0, END)
        tex.insert(tk.END,filename)

        pdf = file(filename, "rb").read()
        startmark = "\xff\xd8"
        startfix = 0
        endmark = "\xff\xd9"
        endfix = 2
        istream = pdf.find("stream", 0)
        openflag=0
        if(istream>=0):
            istart = pdf.find(startmark, istream, istream + 20)
            iend = pdf.find("endstream", istart)
            if iend < 0:
                raise Exception("Didn't find end of stream!")
            iend = pdf.find(endmark, iend - 20)
            if iend < 0:
                raise Exception("Didn't find end of JPG!")
            openflag=1
            istart += startfix
            iend += endfix
            jpg = pdf[istart:iend]
            jpgfile = file("jpg1.jpg", "wb")
            jpgfile.write(jpg)
            jpgfile.close()
            Oimg=cv2.imread("jpg1.jpg")
            Oimg1=cv2.resize(Oimg,(W,H))
            #os.remove("jpg1.jpg")
            img = cv2.cvtColor(Oimg1, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img=ImageTk.PhotoImage(img)
            panelA = Label(image=img)
            panelA.image = img
            panelA.place(x=10, y=50)
            os.remove("jpg1.jpg")
            canvas = tk.Canvas(window,width=W, height=H)
            canvas.create_image(0, 0, image=img, anchor = NW)
            canvas.place(x=10, y=50)
            canvas.bind('<Button-1>', onPress)
            canvas.bind('<Motion>', motion)
            canvas.bind(' <ButtonRelease-1>', Released)

            PAGE.delete(1.0, END)
            PAGE.insert(tk.END, "1")
            PAGE.tag_configure("center", justify='center')
            PAGE.tag_add("center", "1.0", "end")
            Rotate.delete(1.0, END)
            Rotate.insert(tk.END, "0.0")
            Rotate.tag_configure("center", justify='center')
            Rotate.tag_add("center", "1.0", "end")
            global Additemoldindex1, Additemcurrentindex1
            index1 = Combcurrentindex
            Additemoldindex1=-1
            Additemcurrentindex1 = ItemComb.current()
            Item_changed(index1)
        else:
            openflag=0

        #line = canvas.create_line(10, 10, 100, 35, fill="red")


def onPress(event):
    global cfpx,cfpy,pressedflag,rectflag
    rectflag=1
    cfpx=event.x
    cfpy=event.y
    pressedflag=1
    #print(cfpx,cfpy)
def motion(event):
    global cspx,cspy
    if(pressedflag==1):
        cspx, cspy = event.x, event.y
        if (cfpy > 0 and cfpx > 0):
            W = cspx - cfpx
            H = cspy - cfpy
            canvas_clean()
            if (W > 0 and H > 0):
                canvas.create_rectangle(cfpx, cfpy, cspx, cspy)
    #global cfpx,cfpy
def canvas_clean():
    canvas.delete("all")
    canvas.create_image(0, 0, image=img, anchor=NW)

def Released(event):
    global pressedflag, rectflag

    pressedflag=0
    if (cfpy > 0 and cfpx > 0):
        W = cspx - cfpx
        H = cspy - cfpy
        canvas_clean()
        if(W>10 and H>5):
            rectflag = 0
            canvas.create_rectangle(cfpx, cfpy, cspx, cspy)
    #print('{}, {}'.format(x, y))
def del_template():
    global Temps,CTemps,Combcurrentindex,Comboldinxex,Additemcurrentindex1,Additemoldindex1
    index = Comb.current()
    Temps = DEL_Template(Temps, index)
    CTemps=Temps
    L=len(CTemps)
    Comboldinxex=-1
    Combcurrentindex=L-1
    cstr = []
    for i in range(L):
        cstr.append(CTemps[i].name)
    Comb['values'] = cstr
    if(L>0):

        Comb.current(L-1)
        Comb_indexChanged()
    else:
        Comb.set('')
        canvas_clean()
        ItemComb['values'] =[]
        ItemComb.set('')
        Additemoldindex1=-1
        Additemcurrentindex1=-1


def item_initial(cstr):
    global cspx, cspy, cfpx, cfpy
    Additem['values'] = cstr
    if(len(cstr)>0):
        Additem.current(len(cstr)-1)
        canvas_clean()
        cfpx = 0
        cfpy = 0
        cspx = 0
        cspy = 0


def Change():
    global cspx, cspy, cfpx, cfpy
    index=Comb.current()
    if(index>-1 and cspx>cfpx and cspy>cfpy):
        index1=ItemComb.current()
        if(index1>-1):
            CTemps[index].itemfposx[index1] = cfpx
            CTemps[index].itemfposy[index1] = cfpy
            CTemps[index].itemsposx[index1] = cspx
            CTemps[index].itemsposy[index1] = cspy
            tkMessageBox.showinfo("Chnage!", "Changed Item!")
            canvas_clean()
            cfpx = 0
            cfpy = 0
            cspx = 0
            cspy = 0
            fpx = CTemps[index].itemfposx[index1]
            fpy = CTemps[index].itemfposy[index1]
            spx = CTemps[index].itemsposx[index1]
            spy = CTemps[index].itemsposy[index1]
            canvas.create_rectangle(fpx, fpy, spx, spy)

def AdditemComb(event):
    global Additemoldindex, Additemcurrentindex
    Additemcurrentindex=Additem.current()
    Additemindex_changed()


def Additemindex_changed():
    global Additemoldindex, Additemcurrentindex
    if(Additemoldindex!=Additemcurrentindex):
        if(Additemcurrentindex!=-1):
            index=Additemcurrentindex
            fpx=Ntemp.itemfposx[index]
            fpy=Ntemp.itemfposy[index]
            spx = Ntemp.itemsposx[index]
            spy = Ntemp.itemsposy[index]
            num=Ntemp.itemstype[index]
            AddComb.current(num)
            canvas_clean()
            canvas.create_rectangle(fpx, fpy, spx, spy)
        else:
            canvas_clean()
            AddComb.current(0)
            Additem.set('')
        Additemoldindex=Additemcurrentindex

def Additem_func():
    global cspx,cspy,cfpx,cfpy,rectflag,Additemcurrentindex
    if(rectflag==0):
        type=AddComb.current()
        Ntemp.itemADD(type,cfpx,cfpy,cspx,cspy)
        str1=Additem['values']
        cstr=[]
        for i in range(len(str1)):
            cstr.append(str1[i])
        cstr.append("item"+str(Ntemp.itemcount))
        item_initial(cstr)
        rectflag=1
        Additemcurrentindex=len(cstr)-1
        Additemindex_changed()

def DeleteItem_func():
    global Additemcurrentindex,Additemoldindex
    index=Additem.current()
    if(index>=0):
        cstr = []
        num=0
        for i in range(Ntemp.itemcount):
            if(index==i):
                continue
            num+=1
            cstr.append("item"+str(num))
        item_initial(cstr)
        Additemoldindex=-1
        Additemcurrentindex = len(cstr) - 1
        Ntemp.itemDEL(index)
        Additemindex_changed()


def Save_func():
    global Temps,CTemps,Ntemp
    Name = Addname.get('0.0', END)
    Ntemp.name=Name
    Temps=ADD_Template(Temps, Ntemp)
    CTemps=Temps
    Comb_indexChanged()

    #clearing Adding part
def Comb_selecindex(event):
    if(openflag==1):
        global Combcurrentindex
        Combcurrentindex=Comb.current()
        Comb_indexChanged()

def Item_selectindex(event):
    global Additemcurrentindex1
    index1 = Combcurrentindex
    Additemcurrentindex1=ItemComb.current()
    Item_changed(index1)

def Item_changed(index1):
    global Additemoldindex1, Additemcurrentindex1
    if (Additemoldindex1 != Additemcurrentindex1 and index1>-1):
        if (Additemcurrentindex1 != -1):
            index = Additemcurrentindex1
            fpx = CTemps[index1].itemfposx[index]
            fpy =  CTemps[index1].itemfposy[index]
            spx =  CTemps[index1].itemsposx[index]
            spy =  CTemps[index1].itemsposy[index]
            canvas_clean()
            canvas.create_rectangle(fpx, fpy, spx, spy)
        else:
            canvas_clean()
            ItemComb.set('')
        Additemoldindex1 = Additemcurrentindex1

def Comb_indexChanged():
    global Comboldinxex, Combcurrentindex,Additemcurrentindex1,Additemoldindex1
    if (Comboldinxex != Combcurrentindex):
        if (Combcurrentindex != -1):
            index = Combcurrentindex
            cstr = []
            for i in range(CTemps[index].itemcount):
                cstr.append("item" + str(i+1))
            ItemComb['values'] = cstr
            ItemComb.current(0)
            Additemcurrentindex1=0
            Additemoldindex1=-1
            Item_changed(index)
        else:
            canvas_clean()
            Comb.set('')
            ItemComb.set('')
        Comboldinxex = Combcurrentindex
def Page_select():
    global Oimg,filename
    global canvas
    global W, H
    global img, openflag
    global PAGE
    Npage= int(PAGE.get('0.0', END))
    pdf = file(filename, "rb").read()
    startmark = "\xff\xd8"
    startfix = 0
    endmark = "\xff\xd9"
    endfix = 2
    i = 0
    njpg = 0
    flag=0
    if(Npage>0):
        while njpg<=Npage+1:
            istream = pdf.find("stream", i)
            if istream < 0:
                break
            istart = pdf.find(startmark, istream, istream + 20)
            if istart < 0:
                i = istream + 20
                continue
            iend = pdf.find("endstream", istart)
            if iend < 0:
                raise Exception("Didn't find end of stream!")
            iend = pdf.find(endmark, iend - 20)
            if iend < 0:
                raise Exception("Didn't find end of JPG!")

            istart += startfix
            iend += endfix
            if(njpg==Npage):
                jpg = pdf[istart:iend]
                jpgfile = file("jpg1.jpg", "wb")
                jpgfile.write(jpg)
                jpgfile.close()
                openflag = 1
                flag=1
            njpg += 1
            i = iend
        if(flag==0):
            istream = pdf.find("stream", 0)
            if (istream >= 0):
                istart = pdf.find(startmark, istream, istream + 20)
                iend = pdf.find("endstream", istart)
                if iend < 0:
                    raise Exception("Didn't find end of stream!")
                iend = pdf.find(endmark, iend - 20)
                if iend < 0:
                    raise Exception("Didn't find end of JPG!")
                openflag = 1
                istart += startfix
                iend += endfix
                jpg = pdf[istart:iend]
                jpgfile = file("jpg1.jpg", "wb")
                jpgfile.write(jpg)
                jpgfile.close()
                flag=1
                njpg=1
            else:
                openflag=0
        if(flag==1):
            Oimg = cv2.imread("jpg1.jpg")
            Oimg1 = cv2.resize(Oimg, (W, H))
            # os.remove("jpg1.jpg")
            img = cv2.cvtColor(Oimg1, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(img)
            panelA = Label(image=img)
            panelA.image = img
            panelA.place(x=10, y=50)
            os.remove("jpg1.jpg")
            canvas = tk.Canvas(window, width=W, height=H)
            canvas.create_image(0, 0, image=img, anchor=NW)
            canvas.place(x=10, y=50)
            canvas.bind('<Button-1>', onPress)
            canvas.bind('<Motion>', motion)
            canvas.bind(' <ButtonRelease-1>', Released)

            PAGE.delete(1.0, END)
            PAGE.insert(tk.END, str(njpg))
            PAGE.tag_configure("center", justify='center')
            PAGE.tag_add("center", "1.0", "end")
            Rotate.delete(1.0, END)
            Rotate.insert(tk.END, "0.0")
            Rotate.tag_configure("center", justify='center')
            Rotate.tag_add("center", "1.0", "end")
        else:
            openflag = 0




def Rotation():
    global Oimg, img
    global Angle
    global rotated_img
    Angle = float(Rotate.get('0.0', END))
    if(openflag==1):
        Oimg1 = cv2.resize(Oimg, (W, H))
        rotated_img=imutils.rotate(Oimg, Angle)
        rotated = imutils.rotate(Oimg1, Angle)
        # os.remove("jpg1.jpg")
        img = cv2.cvtColor(rotated, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        canvas.delete("all")
        canvas.create_image(0, 0, image=img, anchor=NW)
def image_smoothening(img):
    ret1, th1 = cv2.threshold(img, 180, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (3, 3), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3


def remove_noise_and_smooth(img):
    #filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41, 3)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = image_smoothening(img)
    or_image = cv2.bitwise_or(img, closing)
    return or_image
def AI_string(nstr, type):
    pstr=""
    flag=0
    for i in range (len(nstr)):
        if(flag==1):
            flag=0
            continue
        if(type==1 or type==2):
            if(nstr[i]=='i' or nstr[i] == 'l'):
                pstr+='1'
            elif(nstr[i]=='I'):
                pstr+='/'
            elif (nstr[i] == 'Q'  or nstr[i] == 'O'  or nstr[i]=='o'   or nstr[i] == 'C'  or nstr[i]=='c'):
                pstr += '0'
            elif (nstr[i] == 'Z'  or nstr[i]=='z'):
                pstr += '2'
            elif ((nstr[i] == 'g' and i>0 and nstr[i-1]!='K')  or nstr[i] == 'f'  or nstr[i]=='t'):
                pstr += ','
            elif (nstr[i] == 'S'  or nstr[i]=='s'):
                pstr += '5'
            elif(nstr[i]=='1' and i>0 ):
                if(nstr[i-1]=='D'):
                    pstr += '/'
                elif(nstr[i-1]=='e'):
                    pstr += 'l'
                else:pstr+=nstr[i]

            elif(nstr[i]=="\\" or nstr[i]=="'" or nstr[i]=='*' or nstr[i]=='^' or nstr[i]=='}' or nstr[i]=='{' or nstr[i]==')' or nstr[i]=='('):
                continue
            else:
                pstr+=nstr[i]
        if(type==0):
            if(nstr[i]=='!'):
                pstr+='I'
            elif(nstr[i]=='1' and (i>0 and nstr[i-1].isdigit()==False)):
                pstr+='I'
            elif(nstr[i]=='/'):
                pstr+='V'
                flag=1
            else:
                pstr += nstr[i]
    if(type==2):
        num=0
        nstr=pstr
        pstr=""
        for i in range(len(nstr)):
            if('-' in nstr):
                if(nstr[i]==' '):
                    continue
                elif(nstr[i]=='~'):
                    pstr +='-'
                else:
                    pstr += nstr[i]
            else:
                if (nstr[i] == '1' and i > 0 and nstr[i - 1] == 'e'):
                    pstr += 'l'
                elif(nstr[i].isdigit()==False and nstr[i]!='/'):
                    pstr+=nstr[i]
                else:
                    num=num+1
                    if(num==3):
                        pstr+='/'
                        num=0
                    else:
                        pstr += nstr[i]
    if(type==1):
        nstr = pstr
        pstr = ""
        for i in range(len(nstr)):
            if(nstr[i]==' '):
                continue
            if(nstr[i]=='1' and i>0 and nstr[i-1]=='D'):
                pstr += '/'
            else:
                pstr += nstr[i]
        L=len(pstr)
        if(L>5 and pstr[L-2]=='K' and pstr[L-1]=='g'):
            nstr = pstr
            pstr = ""
            for i in range(len(nstr)):
                if (i==L-5):
                    pstr += ','
                else:
                    pstr += nstr[i]


    return pstr
def OCR():
    index=Comb.current()
    if(index>-1):
        OCRtemp=CTemps[index]
        result = ""
        for i in range(OCRtemp.itemcount):
            type=OCRtemp.itemstype[i]
            p1=OCRtemp.itemfposx[i]
            p2=OCRtemp.itemfposy[i]
            q1=OCRtemp.itemsposx[i]
            q2=OCRtemp.itemsposy[i]
            if(type<3):
                fpx,fpy,spx,spy=real_point(p1,p2,q1,q2)
                if(abs(Angle)>0):
                    OCRimage = rotated_img[fpy:spy, fpx:spx]
                else:
                    OCRimage=Oimg[fpy:spy,fpx:spx]

                gray=cv2.cvtColor(OCRimage,cv2.COLOR_RGB2GRAY)
                OCRimage=remove_noise_and_smooth(gray)
                #OCRimage = cv2.morphologyEx(OCRimage, cv2.MORPH_CLOSE, kernel)
                #BW=cv2.Canny(gray, 180, 150, apertureSize=3)
                #BW=cv2.cvtColor(BW,cv2.COLOR_GRAY2RGB)
                cv2.imshow('contrast', OCRimage)
                cv2.imwrite("test.png", OCRimage)
                cv2.waitKey(0)
                """""
                #cv2.imwrite("test.png",OCRimage)
                #imghsv = cv2.cvtColor(OCRimage, cv2.COLOR_BGR2HSV)

                #imghsv[:, :, 2] = [[max(pixel - 50, 0) if pixel < 180 else min(pixel + 70, 255) for pixel in row] for
                 #                  row in imghsv[:, :, 2]]
                #newimg=cv2.cvtColor(imghsv, cv2.COLOR_HSV2BGR)
                #newimg = cv2.GaussianBlur(newimg,(5,5),0)
                kernel = np.ones((2, 2), np.uint8)
                erosion = cv2.dilate(BW, kernel, iterations=1)
                erosion = cv2.GaussianBlur(erosion, (3, 3), 0)
                erosion = cv2.erode(erosion, kernel, iterations=1)
                #cv2.imwrite("test.png", erosion)
                cv2.imshow('contrast', erosion)
                #gray=remove_noise_and_smooth(OCRimage)
                #cv2.imshow('gray', gray)
                cv2.waitKey(0)
                #img = cv2.cvtColor(OCRimage, cv2.COLOR_BGR2RGB)
                #img = Image.fromarray(img)
                """
                result +="item"+str(i+1)+"-\n"
                pstr=image_to_string(Image.open('test.png'))
                pstr=AI_string(pstr,type)
                result+="\t"+pstr+"\n"

                """""
                gray = cv2.cvtColor(OCRimage, cv2.COLOR_BGR2GRAY)
                cv2.imshow("Line Detection", gray)
                cv2.waitKey(0)
                linek = np.zeros((11, 11), dtype=np.uint8)
                linek[5, ...] = 1
                x = cv2.morphologyEx(gray, cv2.MORPH_OPEN, linek, iterations=0)
                gray -= x
                cv2.imshow('gray', gray)
                cv2.waitKey(0)
                """
        resultTxt.delete(1.0, END)
        resultTxt.insert(tk.END, result)

def real_point(fpx,fpy,spx,spy):
    height, width = Oimg.shape[:2]
    ws=float(width)/W;hs=float(height)/H
    nfpx=int(fpx*ws)
    nfpy=int(fpy*hs)
    nspx = int(spx * ws)
    nspy = int(spy * hs)
    return nfpx,nfpy,nspx,nspy
def Closing():
    pickle.dump(Temps, open("save", "wb"))
    window.destroy()
# Global variables for window and canvas
window = drawWindow()

def main():
    global tex
    global openflag
    global Comb
    global ItemComb
    global resultTxt
    global Comboldinxex,Combcurrentindex, Additemoldindex,Additemcurrentindex,Additemoldindex1, Additemcurrentindex1
    global PAGE,PageBtn,Rotate,RBtn
    global Angle
    Angle=0.0
    openflag=0
    Comboldinxex=-1
    Combcurrentindex=-1
    Additemoldindex=-1
    Additemcurrentindex=-1
    Additemoldindex1 = -1
    Additemcurrentindex1 = -1

    tex=tk.Text(window, height=1, width=60,font=('comicsans', 9))
    tex.place(x=15, y=15)
#here are the buttons
    OpenBtn = tk.Button(window, width=5,text='Open', fg='white',   bg='purple', font=('comicsans', 10), command=Open_pdf)
    OpenBtn.place(x=460,y=10)

# Page and Rotation part
    PAGE = tk.Text(window, height=1, width=6)
    PAGE.place(x=550, y=20)
    PAGE.insert(tk.END, "0")
    PAGE.tag_configure("center", justify='center')
    PAGE.tag_add("center", "1.0", "end")
    PageBtn = tk.Button(window, width=4, text='Page', fg='white', bg='purple', font=('comicsans', 8),
                       command=Page_select)
    PageBtn.place(x=610, y=17)

    Rotate = tk.Text(window, height=1, width=6)
    Rotate.place(x=650, y=20)
    Rotate.insert(tk.END, "0.0")
    Rotate.tag_configure("center", justify='center')
    Rotate.tag_add("center", "1.0", "end")
    RBtn = tk.Button(window, width=4, text='R', fg='white', bg='purple', font=('comicsans', 8),
                        command=Rotation)
    RBtn.place(x=710, y=17)


# OCR part
#combobox creation
    lab = Label(window, text="Selection template type and OCR", font=('comicsans', 10))
    lab.place(x=550, y=50)
    Comb=ttk.Combobox(window)
    Comb.place(x=600,y=80)
    Comb.bind("<<ComboboxSelected>>", Comb_selecindex)
    lab=Label(window, text="Type")
    lab.place(x=550,y=80)
    lab = Label(window, text="Items")
    lab.place(x=550, y=110)
    ItemComb = ttk.Combobox(window)
    ItemComb.place(x=600, y=110)
    ItemComb.bind("<<ComboboxSelected>>", Item_selectindex)
    DelBtn = tk.Button(window, width=6, text='Delete', fg='white', bg='purple', font=('comicsans', 9),
                        command=del_template)
    DelBtn.place(x=550, y=145)
    ChangeBtn = tk.Button(window, width=6, text='Change', fg='white', bg='purple', font=('comicsans', 9),
                       command=Change)
    ChangeBtn.place(x=620, y=145)
    OCRBtn = tk.Button(window, width=6, text='OCR', fg='white', bg='purple', font=('comicsans', 9),
                       command=OCR)
    OCRBtn.place(x=690, y=145)

    resultTxt = tk.Text(window, height=20, width=23)
    resultTxt.place(x=550, y=180)

    global Addname
    global AddComb
    global Additem


    lab = Label(window, text="Adding new template", font=('comicsans', 11))
    lab.place(x=550, y=500)
    lab = Label(window, text="Template Name", font=('comicsans', 10))
    lab.place(x=550, y=530)

    Addname = tk.Text(window, height=1, width=11)
    Addname.place(x=650, y=530)


    lab = Label(window, text="OCR type", font=('comicsans', 10))
    lab.place(x=550, y=560)

    items = ('Text','Numbers', 'Date', 'Barcode')
    AddComb = ttk.Combobox(window,values=items,width=12)
    AddComb.current(0)
    AddComb.place(x=650, y=560)

# adding new template
    lab = Label(window, text="Added Item", font=('comicsans', 10))
    lab.place(x=550, y=590)

    Additem = ttk.Combobox(window, width=12)
    Additem.place(x=650, y=590)
    Additem.bind("<<ComboboxSelected>>", AdditemComb)


    AdditemBtn = tk.Button(window, width=5, text='Add', fg='white', bg='purple', font=('comicsans', 9),
                       command=Additem_func)
    AdditemBtn.place(x=550, y=620)

    DelitemBtn = tk.Button(window, width=5, text='Delete', fg='white', bg='purple', font=('comicsans', 9),
                       command=DeleteItem_func)
    DelitemBtn.place(x=625, y=620)

    SaveBtn = tk.Button(window, width=5, text='Save', fg='white', bg='purple', font=('comicsans', 9),
                           command=Save_func)
    SaveBtn.place(x=700, y=620)

   #main part
    global Ntemp,Temps,CTemps
    global cfpx, cfpy, cspx, cspy
    cfpx=0;cfpy=0;cspx=0;cspy=0
    Ntemp=template()
    Sfile=Path("save")
    if(Sfile.exists()):
        Temps=pickle.load(open("save", "rb"))
        CTemps = Temps
        L = len(CTemps)
        Comboldinxex = -1
        Combcurrentindex = L - 1
        cstr = []
        for i in range(L):
            cstr.append(CTemps[i].name)
        Comb['values'] = cstr
    else:
        Temps=[]
    window.protocol('WM_DELETE_WINDOW', Closing)  # root is your root window


    window.mainloop()

main()