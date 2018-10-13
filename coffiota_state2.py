# Import the requests library to send http request to coinbase.com
import requests

#import math
import math

# Import json library for reading json data returned by the http request
import json 

# Import pynput library to register input activity
import pynput
from pynput import mouse

# Import the configparser library used for reading and writing to let_there_be_light.ini 
import configparser

# Import some funtions from TkInter
from tkinter import Tk, Label, Button, Frame, HORIZONTAL
import tkinter.font
import tkinter.ttk
from tkinter.ttk import Progressbar

#import gif stuff
from itertools import count, cycle
#from AnimatedGIF import *
from AnimatedGIF2 import *

# Import some functions from Pillow
from PIL import ImageTk, Image

# Import the PyQRCode library
import pyqrcode

# Imports some Python Date/Time functions
import time
import datetime

# Imports the PyOTA library
import iota
from iota import Iota
from iota import Address

# Abstract methods
from abc import ABCMeta, abstractmethod

import random

import sys

# Define the Exit function
    
def exitGUI():
    root.destroy()
    print('gui ended')
    

def generateNewAddress(addrIndexCount):
    result = api.get_new_addresses(index=addrIndexCount, count=1, security_level=2)
    addresses = result['addresses']
    address = [addresses[0]]
    return(address)

# Define function for checking address balance on the IOTA tangle. 
def checkbalance(_addr):
    gb_result = api.get_balances(_addr)
    balance = gb_result['balances']
    return (balance[0])

# Define function to check for existing address transactions
def getTransExist(addr):
        result = api.find_transactions(addresses=addr)
        myhashes = result['hashes']
        if len(myhashes) > 0:
            transFound = True
        else:
            transFound = False
        return(transFound)

# Define function for reading and storing address indexes

def getNewIndex():
    config = configparser.ConfigParser()
    config.read('coffiota.ini')
    oldIndex = config.getint('IndexCounter', 'addrIndexCount')
    newIndex = oldIndex +1
    config.set('IndexCounter', 'addrIndexCount', str(newIndex))
    with open('coffiota.ini', 'w') as configfile:
        config.write(configfile)
    return(newIndex)

def getEuroRateIOTA():
    r = requests.get('https://api.coinmarketcap.com/v1/ticker/iota')
    for coin in r.json():
        fprice = float(coin["price_usd"])
        IOTA_price = EUR_price/fprice
        return (IOTA_price*1000000)

class Splash_GUI():

    def __init__(self, master):
        print("Splash GUI initiated")
        self._click = False
        self.master = master
        master.configure(background="black",cursor='none')
        master.title("Coffiota")
        #self.label = Label(master, text="Coffiota System")
        #self.label.pack()
        
        
        #self.close_button = Button(master, text="Close", command=exitGUI)
        #self.close_button.pack()
        
        
        self.loadgif = AnimatedGIF(master, 'iota_load2.gif')  # (tkinter.parent, filename, delay between frames)
        self.loadgif.pack()# Packing the label with the animated gif (grid works just as well)
        self.w = Label(master, text="Touch to Activate Coffiota", font=("Helvetica", 30),bg='black',fg='white')
        self.w.pack()
        root.bind("<Button-1>",self.exitSplash)# Shows gif at first frame and we are ready to go
    def exitSplash(self, _click):
        #root.destroy()
        self._click = True
        #remove current widgets
        self.loadgif.destroy()
        self.w.destroy()
    
    def greet(self):
        print("Greetings!")

class Selection_GUI:

    def __init__(self, master):
        print("Selection GUI initiated")
        self.USD_price = 0
        self.master = master
        self._selected = False
        master.configure(background="white",cursor='none')
        master.title("Coffiota")
        #coffee image
        self.mainframe = Frame(master, bg='white')
        self.mainframe.pack()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
        self.photo1 = PhotoImage(file="cup_americano.png")
        self.photo2 = PhotoImage(file="cup_espresso.png")
        self.photo3 = PhotoImage(file="cup_capucino.png")
        self.photo4 = PhotoImage(file="cup_machiato.png")
        #big buttons:
        self.b_a = Button(self.mainframe,text='Americano' ,image=self.photo1, bg='white',activebackground='white',width=225,height=225,command =lambda: self.setPrice(1))
        self.b_a.grid(row=0,column=0)
        self.b_e = Button(self.mainframe,text='Espresso' ,image=self.photo2,bg='white',activebackground='white', width=225,height=225,command =lambda: self.setPrice(2))
        self.b_e.grid(row=1,column=0)
        self.b_c = Button(self.mainframe,text='Cappuccino' ,image=self.photo3,bg='white',activebackground='white', width=225,height=225,command =lambda: self.setPrice(3))
        self.b_c.grid(row=0,column=1)
        self.b_m = Button(self.mainframe,text='Macchiato' ,image=self.photo4,bg='white',activebackground='white', width=225,height=225,command =lambda: self.setPrice(4))
        self.b_m.grid(row=1,column=1)
        self.b_exit = Button(self.mainframe,text='EXIT',bg='white',activebackground='white',command=self.exitgui)
        self.b_exit.grid(row=2,column=0,columnspan=2)
        
        
    def exitSelection(self):
        self.mainframe.destroy()
    def exitgui(self):
        root.destroy()
    def setPrice(self, selection):
        self._selected = True
        if selection == 1:
            self.USD_price=2 #USD
            print('USD price is now 2')
        elif selection == 2:
            self.USD_price=2
        elif selection == 3:
            self.USD_price=2.5
        elif selection == 4:
            self.USD_price=3
    #def toPayment(self):
       
class Payment_GUI():
    
    def __init__(self, master):
        print("Payment GUI initiated")
        self.master = master
        master.configure(background="white",cursor='none')
        master.title("Coffiota")
        #create frame
        self.topframe = Frame(master, bg='white')
        self.topframe.pack()
        #create and render QR code and price text
        self.qrframe = Frame(self.topframe)
        self.qrframe.pack()
        
        self.code = pyqrcode.create('')
        self.code_xbm = self.code.xbm(scale=3)
        self.code_bmp = tkinter.BitmapImage(data=self.code_xbm)
        self.code_bmp.config(background="white")
        
        self.qrcode = tkinter.Label(self.qrframe, image=self.code_bmp, borderwidth = 0)
        self.qrcode.pack()
        
        #progress bar
        
        self.progressFrame = Frame(self.topframe)
        self.progressFrame.pack()
        self.progress=Progressbar(self.progressFrame,orient=HORIZONTAL,length=100,mode='determinate')
        self.progress.pack()
        
        self.paymentStatusFrame = Frame(self.topframe)
        self.paymentStatusFrame.pack()
        self.paymentState = Label(self.paymentStatusFrame,text=paymentStatusText, font=("Helvetica", 9))
        self.paymentState.pack()
        
        self.close_button = Button(self.topframe, text="Close", command=exitGUI)
        self.close_button.pack()
        #create and render transaction status
        
    def updateQRcode(self,_price,_address):
        self.QRaddr = '{"address":"%s","amount":%d,"message":"","tag":"COFFIOTA"}' % (_address,_price)
        self.code = pyqrcode.create(self.QRaddr)
        self.code_xbm = self.code.xbm(scale=3)
        self.code_bmp = tkinter.BitmapImage(data=self.code_xbm)
        self.code_bmp.config(background="white")
        self.qrcode.configure(image=self.code_bmp)
        self.qrcode.image = self.code_bmp
        
    #def progress(self,_status):
        #status looking for transaction
        
        #status pending transaction
        
        #status transaction complete or appropiate balance
                    
    def exitPayment(self):
        self.topframe.destroy()
    def exitGUI(self):
        root.destroy()
    

# Seed used for generating addresses and collecting funds.
# IMPORTANT!!! Replace with your own seed
MySeed = b"YJVSZKQTPILUSPAEDBJXM9QAPQUVRALGBYMBENUEYBGXYDMQVILPHQJYZGUJAMMHMGUNPC9YKYVHOHRYT"


# URL to IOTA fullnode used when checking balance
iotaNode = "https://field.deviota.com:443"

# Create an IOTA object
api = Iota(iotaNode, MySeed)

root = Tk()


# Set the form background to black#
root.config(background="black")

# TkInter font to be used in GUI
myFont = tkinter.font.Font(family = 'Helvetica', size = 20, weight = "bold")

# Set main form to full screen
root.overrideredirect(True)

root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
"""
root.focus_set()  # <-- move focus to this widget
root.bind('<Escape>', lambda e: e.widget.quit())# Define main form as root 

"""

#coffiota_state.py

from machine_states import Splash_state, Payment_state, Brewing_state,\
    Selection_state

class Coffiota(object):
    """ 
    A simple state machine that mimics the functionality of a device from a 
    high level.
    """

    def __init__(self):
        """ Initialize the components. """

        # Start with a default state.
        self.state = Splash_state()

    def on_event(self, event):
        """
        This is the bread and butter of the state machine. Incoming events are
        delegated to the given states which then handle the event. The result is
        then assigned as the new state.
        """

        # The next state will be the result of the on_event function.
        self.state = self.state.on_event(event)
        
        
addrIndex = getNewIndex()

addr = generateNewAddress(addrIndex)

device = Coffiota()
    
while True:
    print("Program has started")
    print(device.state)
    price = 0
    EUR_price = 0
    IOTA_price = 0
    root.update_idletasks()
    root.update()
    #initialise splashscreen
    #create and render
    IOTA_address = 'EYHDTODCIUBEDIBVZRZRHHBQVFUUMSLHLFAVQDWCHBWRMA9AYEZKT9NPRQHKEONGRQCBERZRNRHESSBGDEOENAJUNX'
    splash_frame = Splash_GUI(root)
    
    while device.state.splash:
        root.update_idletasks()
        root.update()
        if splash_frame._click:
            device.on_event("To selection")
            break
        time.sleep(0.01)
            
    #clear frames and initialise new frame for selection state
    #create and render 4 big buttons for coffee, espresso, Cappucino and Latte macchiato, bind them to mouse click event
    selection_frame = Selection_GUI(root)
    print(device.state)
    count=0
    while device.state.selection:
        root.update_idletasks()
        root.update()
        time.sleep(0.01)
        count = count+1
        if count > 2000:
            print(count)
            selection_frame.exitSelection()
            device.on_event("To splash")
            break
        if selection_frame._selected:
            price = selection_frame.USD_price
            selection_frame.exitSelection()
            device.on_event("To payment")
            break
        
    paymentStatusText = 'Waiting for Transactions'
    payment_frame = Payment_GUI(root)
    EUR_price = price #EUR/USD conversion
    IOTA_price = math.floor(getEuroRateIOTA())
    payment_frame.updateQRcode(IOTA_price, addr)
    print(device.state)
    count=0
    
    while device.state.payment:
        root.update_idletasks()
        root.update()
        time.sleep(0.01)
        count = count+1
        if count > 2000:
            print(count)
            payment_frame.exitPayment()
            device.on_event("To splash")
            break
        if checkbalance(addr)>= IOTA_price:
            #send all addr balance to different account (main account)
            device.on_event("To brewing")
            break
        
    while device.state.brewing:
        root.update_idletasks()
        root.update()
        time.sleep(0.01)
        count = count+1
    
    """
    while device.state == Selection_state():
        if :#coffee icon is pressed
            price = 2 #USD
            device.on_event("selection made")
            break
        elif :#espresso icon is pressed
            price = 1.8 #USD
            device.on_event("selection_made")
            break
        elif :#cappucino icon is pressed
            price = 2.5 #USD
            device.on_event("selection made")
            break
        elif :#latte icon is pressed
            price = 2.8 #USD
            device.on_event("selection made")
            break
        else: #if idle for 60 seconds go back to splash screen
            device.on_event("back to splash")
            break
    #clear selection frame and initialise new frame for payment state
    mainframe.pack_forget()
    while device.state == Payment_state():
        if :#balance is high enough to match price of item
            #do something with the iota's
            device.on_event("payment confirmed")
            break
        else:
            print("Balance is not high enough yet")
            # ask if user wants to cancel and then break
            time.sleep(5)
            break
        
    #clear payment frame and initialise brewing frame
    mainframe.pack_forget()
    while device.state == Brewing_state():
        if :#user clicked return to home
            device.on_event("return home")
            break    
        else: #break after 60 idle seconds back to selection menu
    mainframe.pack_forget()
    """
    print("end of main loop")
    print(device.state)
    time.sleep(2)
    

print("program ended")