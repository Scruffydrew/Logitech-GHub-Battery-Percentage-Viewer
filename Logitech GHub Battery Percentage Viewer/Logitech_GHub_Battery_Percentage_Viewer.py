import re

#a_file = "C:/Users/scruf/AppData/Local/LGHUB/settings.db"
a_file = "C:/Users/scruf/AppData/Local/LGHUB/settings - Copy.db"
#a_file = "C:/Users/scruf/AppData/Local/LGHUB/settings - Copy (G915).db"
#a_file = "C:/Users/scruf/AppData/Local/LGHUB/settings - Copy (G502).db"





percentage = str("percentage")

G502 = str("battery/g502wireless/percentage")
G915 = str("battery/g915/percentage")

millivolts = str("millivolts")

time = "time"

charging = "isCharging"

listhide = "999999999"

f = open(a_file, errors="ignore")

list = []

for line in f:
        
    if G502 in line:
        
        print(line)
        
        line = re.findall(r'\d+', line)
        
        line = str(line); line = line[2:]; line = line[:-2]

        list.append(line)

        for i in range(3):
            
            followline = next(f)

            if time in followline:
                followline = listhide

            else:
                
                print(followline)

                if charging in followline:
                    print(followline)
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
            
            if time in followline:
                followline = listhide

            else:
                
                print(followline)

                if charging in followline:
                    print(followline)
                    followline = listhide
                
            followline = re.findall(r'\d+', followline)
            
            followline = str(followline); followline = followline[2:]; followline = followline[:-2]
            
            list.append(followline)
            

list.remove(listhide)
list.remove(listhide)



print(list)

import json

# open output file for writing
with open('listfile.txt', 'w') as filehandle:
    json.dump(list, filehandle)

