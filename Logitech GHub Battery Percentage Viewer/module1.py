import json

print("hi")
# open output file for reading
with open('listfile.txt', 'r') as filehandle:
    list = json.load(filehandle)

print(list)
input("Press Enter to continue...")
