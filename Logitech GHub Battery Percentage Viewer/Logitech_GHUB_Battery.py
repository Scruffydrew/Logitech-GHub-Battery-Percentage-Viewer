import re
import sys
import os
import time
import json
import tkinter as tk
from tkinter import Label, Frame
from threading import Thread
from pystray import Menu, MenuItem as item
import pystray
from PIL import Image, ImageTk
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
# Stop the print command from showing up in the console
def blockPrint():
    sys.stdout = open(os.devnull, 'w')
# Allow the print command to show up in console again
def enablePrint():
    sys.stdout = sys.__stdout__
# Activates the print block function
#blockPrint()
Chargestatus = []
Chargestatus.append("0")
Chargestatus.append("0")
def Background_stuff():
    global quitmain
    a_file = str(os.path.expandvars('%LOCALAPPDATA%'))+ "/LGHUB/settings.db"
    print(a_file)
    percentage = str("percentage")
    G502 = str("battery/g502wireless/percentage")
    G915 = str("battery/g915/percentage")
    millivolts = str("millivolts")
    timeline = "time"
    charging = "isCharging"
    listhide = "999"
    file_path = os.path.realpath(__file__)
    file = resource_path('listfile.txt')
    Chargestatus[0] = "0"
    Chargestatus[1] = "0"
    while True:
        if quitmain == True:
            sys.exit()
        list = []
        NEWlist = []
        Chargestatus[0] = "0"
        Chargestatus[1] = "0"
        Charging_Found = False
        f = open(a_file, errors="ignore")
        for line in f:
            if G502 in line:
                print(line)
                line = re.findall(r'\d+', line)
                line = str(line); line = line[2:]; line = line[:-2]
                list.append(line)
                for i in range(3):
                    followline = next(f)
                    if timeline in followline:
                        followline = listhide
                    else:
                        print(followline)
                        if charging in followline:
                            del Chargestatus[0]
                            Chargestatus.insert(0, '1')
                            followline = listhide
                    followline = re.findall(r'\d+', followline)
                    followline = str(followline); followline = followline[2:]; followline = followline[:-2]
                    list.append(followline)
            if G915 in line:
                print(line)
                line = re.findall(r'\d+', line)
                line = str(line); line = line[2:]; line = line[:-2]
                list.append(line)
                for i in range(3):
                    followline = next(f)
                    if timeline in followline:
                        followline = listhide
                    else:
                        print(followline)
                        if charging in followline:
                            del Chargestatus[1]
                            Chargestatus.append("1")
                            followline = listhide
                    followline = re.findall(r'\d+', followline)
                    followline = str(followline); followline = followline[2:]; followline = followline[:-2]
                    list.append(followline)
        if not list:
            print("List is empty")
            with open(resource_path('listfile.txt'), 'r') as filehandle:
                TEMPlist = json.load(filehandle)
            TEMPlist = NEWlist
            print(TEMPlist)
            print(NEWlist)
        else:
            print("List is not Empty")
            print(list)            
            NEWlist = [x for x in list if int(x) <= 915]
            print(NEWlist)
            G502_Found = 0
            G915_Found = 0
            G502_Check = NEWlist[0]
            G915_Check = NEWlist[0]
            if G502_Check == str(502):
                print("G502 Check")
                list.remove(listhide)
                G502_Found = 1
            else:
                if G915_Check == str(915):
                    print("G915 Check")
                    list.remove(listhide)
                    G915_Found = 1
            if G502_Found == 1:
                print("G502 Found")
                if len(NEWlist) == 4:
                    print("NEWlist = 4")
                    #list.remove(listhide)
                    if NEWlist[-2] == str(915):
                        with open(resource_path('listfile.txt'), 'w') as filehandle:
                            json.dump(NEWlist, filehandle)
                    else:
                        def swapPositions(list, pos1, pos2):
                            get = NEWlist[pos1], NEWlist[pos2]
                            NEWlist[pos2], NEWlist[pos1] = get
                            return NEWlist
                        pos1, pos2 = -1, -2
                        swapPositions(NEWlist, pos1=1, pos2=1)
                else:
                    print("NEWlist = 2")
                    with open(resource_path('listfile.txt'), 'r') as filehandle:
                        TEMPlist = json.load(filehandle)
                    NEWlist.append(TEMPlist[-2])
                    NEWlist.append(TEMPlist[-1])
                    print(NEWlist)
                    if NEWlist[-1] == str(915):
                        print("Rearranging")
                        def swapPositions(list, pos1, pos2):
                            get = NEWlist[pos1], NEWlist[pos2]
                            NEWlist[pos2], NEWlist[pos1] = get
                            return NEWlist
                        pos1, pos2 = -1, -2
                        swapPositions(NEWlist, pos1=1, pos2=1)
                    print(NEWlist)
                    with open(resource_path('listfile.txt'), 'w') as filehandle:
                        json.dump(NEWlist, filehandle)
            else:
                if G915_Found == 1:
                    print("G915 Found")
                    if len(NEWlist) == 2:
                        with open(resource_path('listfile.txt'), 'r') as filehandle:
                            TEMPlist = json.load(filehandle)
                    NEWlist.insert(0, TEMPlist[1])
                    NEWlist.insert(0, TEMPlist[0])
                    print(NEWlist)
                    with open(resource_path('listfile.txt'), 'w') as filehandle:
                        json.dump(NEWlist, filehandle)
            #enablePrint()
            print(NEWlist)
            with open(resource_path('listfile.txt'), 'w') as filehandle:
                json.dump(NEWlist, filehandle)
            with open(resource_path('Current_Percentage.txt'), 'w') as filehandle:
                json.dump(NEWlist, filehandle)
            with open(resource_path('Current_Charge.txt'), 'w') as c:
                json.dump(Chargestatus, c)           
            time.sleep(1)
def GUI_stuff():
    global hideshow
    global quitmain
    global loc
    def Draw():
        global G915
        global G502
        frame=tk.Frame(root,width=100,height=100,relief='solid',bd=0, bg="grey")
        frame.place(x=10,y=10)
        G915=tk.Label(frame,text=CURRENTPERCENTAGES, bg="grey", fg="white")
        G915.pack()
        G502=tk.Label(frame,text=CURRENTPERCENTAGES, bg="grey", fg="white")
        G502.pack()
    def Refresher():
        global showhidestate
        global hideshow
        global quitmain
        global loc
        global G915
        global G502
        if hideshow == 0:
            print("root.withdraw()")
            root.withdraw()
            showhidestate = 1
        if hideshow == 1:
            print("root.update()")
            root.update()
            root.deiconify()
            showhidestate = 0
        if quitmain == True:
            sys.exit()
        def show():
            root.update()
            root.deiconify()
        def hide():
            root.withdraw()
        with open(resource_path('Current_Percentage.txt'), 'r') as filehandle:
            CURRENTPERCENTAGES = json.load(filehandle)
        with open(resource_path('Current_Charge.txt'), 'r') as c:
            CurrentCharge = json.load(c)
        print(CurrentCharge)
        print(CURRENTPERCENTAGES)
        charge502 = "    "
        charge915 = "    "
        print(CurrentCharge[0] +" 0")
        print(CurrentCharge[1] +" 1")
        if CurrentCharge[0] == "1":
            print(1)
            charge502 = "🗲"
        if CurrentCharge[1] == "1":
            print(2)
            charge915 = "🗲"
        if loc == "150x150-1839+999":
            G502.configure(text="G"+CURRENTPERCENTAGES[0] + " :"+ charge502 + CURRENTPERCENTAGES[1] + "%", font=("Segoe UI", 7))
            G915.configure(text="G"+CURRENTPERCENTAGES[-2] + " :"+ charge915 + CURRENTPERCENTAGES[-1] + "%", font=("Segoe UI", 7))
        else:
            if loc == "150x150-3697+999":
                G502.configure(text="G"+CURRENTPERCENTAGES[0] + " :"+ charge502 + CURRENTPERCENTAGES[1] + "%", font=("Segoe UI", 7))
                G915.configure(text="G"+CURRENTPERCENTAGES[-2] + " :"+ charge915 + CURRENTPERCENTAGES[-1] + "%", font=("Segoe UI", 7))
            else:
                if loc == "150x150-1930+1029":
                    G502.configure(text="G"+CURRENTPERCENTAGES[0] + " :"+ charge502 + CURRENTPERCENTAGES[1] + "%", font=("Segoe UI", 9))
                    G915.configure(text="G"+CURRENTPERCENTAGES[-2] + " :"+ charge915 + CURRENTPERCENTAGES[-1] + "%", font=("Segoe UI", 9))
                else:
                    if loc == "150x150-1930-941":
                        G502.configure(text="G"+CURRENTPERCENTAGES[0] + " :"+ charge502 + CURRENTPERCENTAGES[1] + "%", font=("Segoe UI", 9))
                        G915.configure(text="G"+CURRENTPERCENTAGES[-2] + " :"+ charge915 + CURRENTPERCENTAGES[-1] + "%", font=("Segoe UI", 9))
        root.geometry(loc) # Sets the size of the window
        root.after(1000, Refresher) # every second...
    CURRENTPERCENTAGES = []
    root = tk.Tk()
    root.title("Logitech GHub Battery Viewer")# Names the Tk root window
    root.geometry("150x150-1930+1029") # Sets the size of the window
    root.overrideredirect(1) # Removes title bar from window
    root.configure(bg='grey') # Makes backgroud fo window grey
    root.wm_attributes("-topmost", True) # Makes the window always stay on top
    root.wm_attributes("-transparentcolor", "grey") # Makes the window background transparent
    with open(resource_path('Current_Percentage.txt'), 'r') as filehandle:
        CURRENTPERCENTAGES = json.load(filehandle)
    with open(resource_path('Current_Charge.txt'), 'r') as filehandle:
        CurrentCharge = json.load(filehandle)
    Draw()
    Refresher()
    root.mainloop()
def Tray_stuff():
    global hideshow
    global showhidestate
    global quitmain
    global loc
    win=tk.Tk()
    def showhide():
        global hideshow
        global showhidestate
        if showhidestate == 1:
            print("hideshow = 1")
            hideshow = 1
        if showhidestate == 0:
            print("hideshow = 0")
            hideshow = 0
    def quit_window(icon, item):
        global quitmain
        quitmain = True
        icon.stop()
        win.destroy()
        os._exit()
    def loc1():
        global loc
        loc = "150x150-1930+1029"
    def loc2():
        global loc
        loc = "150x150-1930-941"
    def loc3():
        global loc
        loc = "150x150-3697+999"
    def loc4():
        global loc
        loc = "150x150-1839+999"
    def hide_window():
        win.withdraw()
        image=Image.open(resource_path('battery.ico'))
        menu=(item('Quit', quit_window), item("Location:", Menu(item('Bottom', loc1), item('Top', loc2), item('Left', loc3), item('Right', loc4))), item('Show/Hide', showhide))
        icon=pystray.Icon("name", image, "Battery Viewer", menu)
        icon.run()
    win.protocol('WM_DELETE_WINDOW', hide_window)
    hide_window()
    win.mainloop()
hideshow = 1
showhidestate = 1
quitmain = False
if quitmain == True:
    sys.exit()
loc = "150x150-1930+1029"
Thread(target = Background_stuff).start() 
Thread(target = GUI_stuff).start()
Thread(target = Tray_stuff).start()