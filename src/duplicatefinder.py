import os
import hashlib
from guizero import *
a = App()
screen_width = a.tk.winfo_screenwidth()
screen_height = a.tk.winfo_screenheight()
a.destroy()

#this function returns the md5 hash of the file at a specified path,
#the hashed versions of the files can be compared to see if there are duplicates
def createhash(path):
    hash = hashlib.md5()
    with open(path, "rb") as f:
        for part in iter(lambda: f.read(4096),b""):
            hash.update(part)
    return hash.hexdigest()

#function to combine two dictionaries into one
def joindicts(first, second):
    for key in second.keys():
        if key in first:
            first[key] = first[key] + second[key]
        else:
            first[key] = second[key]
    return first

#walks through all the files/directories within the input directory, creates a dictionary of all file paths with the hashes as keys
def check(folder):
    dups = {}
    for root, dirs, files in os.walk(folder):
        for file in files:
            path = os.path.join(root, file)
            canonical = os.path.realpath(path)
            hashed = createhash(canonical)
            if hashed in dups:
                dups[hashed].append(canonical)
            else:
                dups[hashed] = [canonical]
    return dups

#checks to see which hashes have more than one file path associated with them and returns these as they are duplicates
def find():
    folder1 = input_box1.value
    folder2 = input_box2.value
    if os.path.exists(folder1) and os.path.exists(folder2):
        dups = joindicts(check(folder1),check(folder2))
        aredups = False
        for key in dups:
            if len(dups[key]) > 1:
                aredups = True
                info = "\nDuplicate files found! Names may be different but the content is identical"
                print(info)
                infotext = Text(app, text=info, font="Calibri")
                for item in dups[key]:
                    print(item)
                    itemtext = Text(app, text=item, font="Calibri")
                    #outputs to console and GUI
        if aredups == False:
            info = "\nNo duplicates found"
            print(info)
            infotext = Text(app, text=info, font="Calibri")
    else:
        errortext = Text(app, text="One or both directories do not exist", font="Calibri", color="red")
        print("One or both directories do not exist")

#exit function
def exit():
    app.destroy()

#sets up GUI
app = App(title="Duplicate File Finder", width=screen_width, height=screen_height)
text1 = Text(app, text="Enter first directory *", font="Calibri")
input_box1 = TextBox(app, width=100)
text2 = Text(app, text="Enter second directory *", font="Calibri")
input_box2 = TextBox(app, width=100)
infotext2 = Text(app, text="* indicates required field", font="Calibri")
button = PushButton(app, text="Find Duplicates", command=find)
exitbutton = PushButton(app, text="Exit", command=exit)
app.display()
