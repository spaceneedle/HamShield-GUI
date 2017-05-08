import serial
import serial.tools.list_ports
from Tkinter import *
import tkFont
import tkMessageBox
import time

frequency = 146.520
freq = 0
# hamshield = serial.Serial("COM3",9600)

def tx_start(event):
    hamshield.write("XT")
    print "Start transmitting"

def tx_end(event):
    hamshield.write("XO")
    print "Stop transmitting"


def change_freq(val):
    print val

def set_port(val):
    print val
    global hamshield
    val = str(val)
    if(val.find(" ") != -1): val = val.split(" ")[0]
    hamshield = serial.Serial(val,9600)
    global t
    t.destroy()

def pick_port(self):
    if len(list(serial.tools.list_ports.comports())) == 0:
        tkMessageBox.showinfo("Serial Error :(",
""" We were unable to find a connected Arduino.

Please check your connections, power and Arduino serial drivers.
We didn't get to reach the step to detect HamShield or the proper sketch, so don't worry about that just yet.

After you figure out the problem, run this program again.""")
        quit()
    default = StringVar()
    default.set(list(serial.tools.list_ports.comports())[0])
    t = Toplevel(self)
    t.wm_title("Configure Serial Port")
    t.attributes("-topmost", True)
    t.minsize(width=600,height=100)
    t.maxsize(width=600,height=100)
    option = OptionMenu(t,default,*list(serial.tools.list_ports.comports()),command=set_port).grid(sticky=N+S+W+E)
    global t
    t.lift()

def setpower(event):
    global power
    powerlevel = power.get()
    hamshield.write("XA"+chr(powerlevel)+"!")
    print "Power level set to "+str(powerlevel)

def prgfreq(event):
    global freq
    global frequency
    frequency = float(freq.get())
    freq.set(format(float(frequency),'.3f'))
    print "Programming "+str(freq.get())
    hamshield.write("XF"+str(freq.get())+"!")
    print "XF"+str(freq.get())+"!"
    hamshieldgui.focus()


def setpltone(event):
    global pltone
    print pltone.get()
    hamshield.write("XP"+str(pltone.get())+"!")

class Application(Frame):
    def __init__(self,parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
    def initUI(self):

        # Globalizations 

        global frequency
        global freq
        global pltone
        global power

        # GUI String Setup

        freq = StringVar()
        pltone = StringVar(self)
        power = StringVar()

        # Set GUI String Defaults
        
        pltone.set("PL Tone (None)")
        power.set("Power Level (Lowest)")
        freq.set(format(frequency,'.3f'))

        # Create Main Window and configure it
        
        self.parent.title("HamShield Simplex")
        freqfont = tkFont.Font(family="Courier", size=32)
        indfont = tkFont.Font(family="Courier", size=8)

        # Create GUI widgets
        
        freqentry = Entry(self,textvariable=freq,font=freqfont,bg="#000000",bd=0,fg="#00FF00",insertbackground="#00FF00")
        pl_set = OptionMenu(self,pltone,"No PL","67.0","69.3","69.4","71.9","74.4","77.0","79.7","82.5","85.4","88.5","91.5","94.8","97.4","100.0","103.5","107.2","110.9","114.8","118.8","123.0","127.3","131.8","136.5","141.3","146.2","150.0","151.4","156.7","159.8","162.2","165.5","167.9","171.3","173.8","177.3","179.9","183.5","186.2","189.9","192.8","196.6","199.5","203.5","206.5","210.7","213.8","218.1","221.3","225.7","229.1","233.6","237.1","241.8","245.5","250.3","254.1",command=setpltone)
        transmit = Button(self,text="TRANSMIT")
        power_set = OptionMenu(self,power,"Power 0","Power 1","Power 2","Power 3","Power 4","Power 5","Power 6","Power 7","Power 8","Power 9","Power 10","Power 11","Power 12","Power 13","Power 14","Power 15",command=setpower)
        
        #l_tx = Label(self,text="TX",bg="#000000",bd=0,fg="#00FF00",font=indfont)
        #l_tx.pack(side=TOP)
        #l_rx = Label(self,text="RX",bg="#000000",bd=0,fg="#00FF00",font=indfont)
        #l_rx.pack(side=TOP)
        #l_pl = Label(self,text="PL",bg="#000000",bd=0,fg="#00FF00",font=indfont)
        #l_pl.pack(side=TOP)
        
        # Pack things

        pl_set.grid(row=0,column=0,sticky=W+E)
        power_set.grid(row=0,column=1,sticky=W+E)
        transmit.grid(row=2,columnspan=2,sticky=W+E)
        freqentry.grid(row=1,columnspan=2,sticky=W+E)
        self.pack(fill=BOTH, expand=1)
        
        # Create Bindings
        
        freqentry.bind('<Return>',prgfreq)
        transmit.bind('<Button-1>',tx_start)
        transmit.bind('<ButtonRelease-1>',tx_end)
        self.bind('<space>',tx_start)
        self.bind('<KeyRelease-space>',tx_end)


        self.fireOnce()
        self.onUpdate()
    def fireOnce(self):
        pick_port(self)
    def onUpdate(self):
      #global freq
     self.after(1000, self.onUpdate)
      #print "Frequency is "+str(freq.get())

hamshieldgui = Tk()
app = Application(hamshieldgui)
hamshieldgui.mainloop()
