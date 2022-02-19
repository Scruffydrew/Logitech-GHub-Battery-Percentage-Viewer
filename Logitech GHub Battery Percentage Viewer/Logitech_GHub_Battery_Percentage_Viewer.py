import re
import sys
import os
from os import path
import time

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
blockPrint()

a_file = str(os.path.expandvars('%LOCALAPPDATA%'))+ "/LGHUB/settings.db"

print(a_file)

percentage = str("percentage")

G502 = str("battery/g502wireless/percentage")
G915 = str("battery/g915/percentage")

millivolts = str("millivolts")

timeline = "time"

charging = "isCharging"

listhide = "999"


while True:

    blockPrint()

    list = []
    NEWlist = []

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
                    
                        followline = listhide
                
                followline = re.findall(r'\d+', followline)
            
                followline = str(followline); followline = followline[2:]; followline = followline[:-2]
            
                list.append(followline)

    import json

    if not list:
    
        print("List is empty")
    
        with open('listfile.txt', 'r') as filehandle:
                TEMPlist = json.load(filehandle)

        TEMPlist = NEWlist
        enablePrint()
        print(TEMPlist)
        print(NEWlist)
        blockPrint()

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
                    with open('listfile.txt', 'w') as filehandle:
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
        
                with open('listfile.txt', 'r') as filehandle:
                    TEMPlist = json.load(filehandle)
    
                NEWlist.append(TEMPlist[-1])
                NEWlist.append(TEMPlist[-2])

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

                with open('listfile.txt', 'w') as filehandle:
                    json.dump(NEWlist, filehandle)

        else:

            if G915_Found == 1:

                print("G915 Found")

                if len(NEWlist) == 2:
                
                    with open('listfile.txt', 'r') as filehandle:
                        TEMPlist = json.load(filehandle)
    
                NEWlist.insert(0, TEMPlist[1])
                NEWlist.insert(0, TEMPlist[0])

                print(NEWlist)

                with open('listfile.txt', 'w') as filehandle:
                    json.dump(NEWlist, filehandle)
    
        enablePrint()
        print(NEWlist)
        time.sleep(10)