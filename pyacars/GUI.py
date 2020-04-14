from tkinter import *

class Flight():
    def __init__(self):
        self.number = ''

class MyFirstGUI:
    def __init__(self, master):
        self.flight = Flight()

        self.master = master
        master.title("pyACARS")

        self.topFrame = Frame(master)
        self.topFrame.pack()

        self.bottomFrame = Frame(master)
        self.bottomFrame.pack()
        
        self.leftFrame = Frame(self.topFrame)
        self.leftFrame.pack(side = LEFT)
        self.centerFrame = Frame(self.topFrame)
        self.centerFrame.pack(side = LEFT)
        self.rightFrame = Frame(self.topFrame)
        self.rightFrame.pack(side = LEFT)

        self.label = Label(self.leftFrame, text="Flight Number")
        self.label.pack()
        self.inputFlightNumber = Entry(self.leftFrame)
        self.inputFlightNumber.pack()

        self.label = Label(self.leftFrame, text="Origin (ICAO)")
        self.label.pack()
        self.inputOrigin = Entry(self.leftFrame)
        self.inputOrigin.pack()

        self.label = Label(self.leftFrame, text="Destination (ICAO)")
        self.label.pack()
        self.inputDestination = Entry(self.leftFrame)
        self.inputDestination.pack()

        self.label = Label(self.leftFrame, text="Alternate (ICAO)")
        self.label.pack()
        self.inputAlternate = Entry(self.leftFrame)
        self.inputAlternate.pack()

        self.label = Label(self.leftFrame, text="Route")
        self.label.pack()
        self.inputRoute = Entry(self.leftFrame)
        self.inputRoute.pack()

        self.label = Label(self.leftFrame, text="Remarks")
        self.label.pack()
        self.inputRemarks = Entry(self.leftFrame)
        self.inputRemarks.pack()

        self.buttonReset = Button(self.bottomFrame, text="Reset", command=self.greet)
        self.buttonReset.pack()


        self.label = Label(self.centerFrame, text="Aircraft")
        self.label.pack()
        self.inputAircraft = Entry(self.centerFrame)
        self.inputAircraft.pack()

        self.label = Label(self.centerFrame, text="Cruise Altitude")
        self.label.pack()
        self.inputAltitude = Entry(self.centerFrame)
        self.inputAltitude.pack()

        self.label = Label(self.centerFrame, text="PAX")
        self.label.pack()
        self.inputPax = Entry(self.centerFrame)
        self.inputPax.pack()

        self.label = Label(self.centerFrame, text="Cargo (kg)")
        self.label.pack()
        self.inputCargoKg = Entry(self.centerFrame)
        self.inputCargoKg.pack()

        self.label = Label(self.centerFrame, text="Type of Flight")
        self.label.pack()
        self.listRules = Listbox(self.centerFrame, selectmode=SINGLE, height=2)
        self.listRules.insert(END, 'VFR')
        self.listRules.insert(END, 'IFR')
        self.listRules.pack()

        self.label = Label(self.centerFrame, text="Network")
        self.label.pack()
        self.listOnline = Listbox(self.centerFrame, selectmode=SINGLE, height=3)
        self.listOnline.insert(END, 'Offline')
        self.listOnline.insert(END, 'VATSIM')
        self.listOnline.insert(END, 'IVAO')
        self.listOnline.pack()



        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
        print("Greetings: %s" % self.inputFlightNumber.get())

root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()

