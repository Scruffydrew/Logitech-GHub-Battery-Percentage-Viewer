import re, sys, os, time, json, pystray, tkinter as tk
from tkinter import Label, Frame
from threading import Thread
from pystray import Menu, MenuItem as item
from PIL import Image, ImageTk
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
Background_stuff_DEBUG = False    # Debug for Background_stuff thread, set to True to make all print functions in Background_stuff print to console, set to False if you dont want it to print to console
GUI_stuff_DEBUG = True           # Debug for GUI_stuff thread, set to True to make all print functions in Background_stuff print to console, set to False if you dont want it to print to console
Tray_stuff_DEBUG = False          # Debug for Tray_stuff thread, set to True to make all print functions in Background_stuff print to console, set to False if you dont want it to print to console

Chargestatus = []   # Create list called Chargestatus
Chargestatus.append("0")    # set first item in list to 0
Chargestatus.append("0")    # set second item in list to 0
def Background_stuff():
    global Background_stuff_DEBUG
    global quitmain
    def log(s):
        if Background_stuff_DEBUG == True:
            print(s)
    a_file = str(os.path.expandvars('%LOCALAPPDATA%'))+ "/LGHUB/settings.db"    # Gets the filepath for the Logitech GHub settings which contains the values for the battery percentages
    log(a_file)
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
    counter = 1
    def looper():
        global Background_stuff_DEBUG
        global quitmain
        def log(s):
            if Background_stuff_DEBUG == True:
                print(s)
        counter = counter + 1
        runcount = 'Counter: ', counter
        log(runcount)
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
                log(line)
                line = re.findall(r'\d+', line)
                line = str(line); line = line[2:]; line = line[:-2]
                list.append(line)
                for i in range(3):
                    followline = next(f)
                    if timeline in followline:
                        followline = listhide
                    else:
                        log(followline)
                        if charging in followline:
                            del Chargestatus[0]
                            Chargestatus.insert(0, '1')
                            followline = listhide
                    followline = re.findall(r'\d+', followline)
                    followline = str(followline); followline = followline[2:]; followline = followline[:-2]
                    list.append(followline)
            if G915 in line:
                log(line)
                line = re.findall(r'\d+', line)
                line = str(line); line = line[2:]; line = line[:-2]
                list.append(line)
                for i in range(3):
                    followline = next(f)
                    if timeline in followline:
                        followline = listhide
                    else:
                        log(followline)
                        if charging in followline:
                            del Chargestatus[1]
                            Chargestatus.append("1")
                            followline = listhide
                    followline = re.findall(r'\d+', followline)
                    followline = str(followline); followline = followline[2:]; followline = followline[:-2]
                    list.append(followline)
        if not list:
            log("List is empty")
            with open(resource_path('listfile.txt'), 'r') as filehandle:
                TEMPlist = json.load(filehandle)
            TEMPlist = NEWlist
            log(TEMPlist)
            log(NEWlist)
        else:
            log("List is not Empty")
            log(list)            
            NEWlist = [x for x in list if int(x) <= 915]
            log(NEWlist)
            G502_Found = 0
            G915_Found = 0
            G502_Check = NEWlist[0]
            G915_Check = NEWlist[0]
            if G502_Check == str(502):
                log("G502 Check")
                list.remove(listhide)
                G502_Found = 1
            else:
                if G915_Check == str(915):
                    log("G915 Check")
                    list.remove(listhide)
                    G915_Found = 1
            if G502_Found == 1:
                log("G502 Found")
                if len(NEWlist) == 4:
                    log("NEWlist = 4")
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
                    log("NEWlist = 2")
                    with open(resource_path('listfile.txt'), 'r') as filehandle:
                        TEMPlist = json.load(filehandle)
                    NEWlist.append(TEMPlist[-2])
                    NEWlist.append(TEMPlist[-1])
                    log(NEWlist)
                    if NEWlist[-1] == str(915):
                        log("Rearranging")
                        def swapPositions(list, pos1, pos2):
                            get = NEWlist[pos1], NEWlist[pos2]
                            NEWlist[pos2], NEWlist[pos1] = get
                            return NEWlist
                        pos1, pos2 = -1, -2
                        swapPositions(NEWlist, pos1=1, pos2=1)
                    log(NEWlist)
                    with open(resource_path('listfile.txt'), 'w') as filehandle:
                        json.dump(NEWlist, filehandle)
            else:
                if G915_Found == 1:
                    log("G915 Found")
                    if len(NEWlist) == 2:
                        with open(resource_path('listfile.txt'), 'r') as filehandle:
                            TEMPlist = json.load(filehandle)
                    NEWlist.insert(0, TEMPlist[1])
                    NEWlist.insert(0, TEMPlist[0])
                    log(NEWlist)
                    with open(resource_path('listfile.txt'), 'w') as filehandle:
                        json.dump(NEWlist, filehandle)
            log(NEWlist)
            with open(resource_path('listfile.txt'), 'w') as filehandle:
                json.dump(NEWlist, filehandle)
            with open(resource_path('Current_Percentage.txt'), 'w') as filehandle:
                json.dump(NEWlist, filehandle)
            with open(resource_path('Current_Charge.txt'), 'w') as c:
                json.dump(Chargestatus, c)           
            time.sleep(10)
            looper()
def GUI_stuff():
    global counter
    global GUI_stuff_DEBUG
    global showhidestate
    global hideshow
    global quitmain
    global loc
    counter = 1
    def log(s):
        if GUI_stuff_DEBUG == True:
            print(s)
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
        global counter
        global showhidestate
        global hideshow
        global quitmain
        global loc
        global G915
        global G502
        if hideshow == 0:
            log("root.withdraw()")
            root.withdraw()
            showhidestate = 1
        if hideshow == 1:
            log("root.update()")
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
        with open(resource_path('Current_Charge.txt'), 'r') as filehandle:
            CurrentCharge = json.load(filehandle)
        log(CurrentCharge)
        log(CURRENTPERCENTAGES)
        charge502 = "    "
        charge915 = "    "
        log(CurrentCharge[0] +" 0")
        log(CurrentCharge[1] +" 1")
        if CurrentCharge[0] == "1":
            log("G502: " + charge502)
            charge502 = "🗲"
        if CurrentCharge[1] == "1":
            log("G915: " + charge915)
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
        counter = counter + 1
        runcount = 'Counter: ', counter
        log(runcount)
        root.after(1000, Refresher) # every second it reruns the code in the Refresher
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
    global Tray_stuff_DEBUG
    global hideshow
    global showhidestate
    global quitmain
    global loc
    def log(s):
        if Tray_stuff_DEBUG == True:
            print(s)
    win=tk.Tk()
    def showhide():
        global hideshow
        global showhidestate
        if showhidestate == 1:
            log("hideshow = 1  ,  Window is now Visible")
            hideshow = 1
        if showhidestate == 0:
            log("hideshow = 0  ,  Window is now Hidden")
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
        global visibility
        win.withdraw()
        image=Image.open(resource_path('battery.ico'))
        menu=(item('Quit', quit_window), item("Location:", Menu(item('Bottom', loc1), item('Top', loc2), item('Left', loc3), item('Right', loc4))), item('Hide/Show', showhide))
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