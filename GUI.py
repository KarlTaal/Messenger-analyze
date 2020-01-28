import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from abistajad import *
import analüüs
import json
import os
import shutil
from tkinter import messagebox

def on_entry_click_path(event):
    """function that gets called whenever entry is clicked"""
    if path_to_dir.get() == 'Enter path here...':
       path_to_dir.delete(0, "end") # delete all the text in the entry
       path_to_dir.insert(0, '') #Insert blank for user input
       path_to_dir.config(fg = 'black')
def on_focusout_path(event):
    if path_to_dir.get() == '':
        path_to_dir.insert(0, 'Enter path here...')
        path_to_dir.config(fg = 'grey')

def on_entry_click_fullname(event):
    """function that gets called whenever entry is clicked"""
    if fullname.get() == 'Enter FB file owner full name here...':
       fullname.delete(0, "end") # delete all the text in the entry
       fullname.insert(0, '') #Insert blank for user input
       fullname.config(fg = 'black')
def on_focusout_fullname(event):
    if fullname.get() == '':
        fullname.insert(0, 'Enter FB file owner full name here...')
        fullname.config(fg = 'grey')


def kirjutaTeksti(teks):
    tekst.config(state=NORMAL)
    tekst.insert(INSERT, teks)
    tekst.config(state=DISABLED)

def seisuinfo(txt):
    tööinfo.config(text=txt)
    tööinfo.update()

def korrasta_kaustad():
    cwd = os.getcwd()
    dir = os.path.join(cwd, "results")
    dir2 = os.path.join(cwd, "results\\plots")
    if os.path.exists(dir):
        shutil.rmtree(dir)
    if os.path.exists(dir2):
        shutil.rmtree(dir2)
    if not os.path.exists(dir):
        os.mkdir(dir)
    if not os.path.exists(dir2):
        os.mkdir(dir2)

def käivita():
    korrasta_kaustad()
    kirjutaTeksti("")
    progress["value"] = 0
    seisuinfo("Otsin andmeid...")
    pages = []
    # Reading the jsons as a dict
    i = 1
    while True:
        try:
            with open(str(path_to_dir.get()) + '\message_' + str(i) + '.json') as json_data:
                data = json.load(json_data)
                data["messages"].reverse()
                pages.append(data)
        except:
            break
        i += 1
    pages.reverse()

    if len(pages) == 0:
        messagebox.showinfo("Vale path", "Sisestasid vale pathi...")
        return

    seisuinfo("Töötlen andmeid, palun oota...")

    sõnumid = []
    names = []
    for page in pages:
        for n in page["participants"]:
            name, emojis = parseString(n["name"])
            if name not in names:
                names.append(name)
        messages = page["messages"]
        for msg in messages:
            sõnumid.append(msg)

    OMANIK = fullname.get().strip()
    if OMANIK not in names:
        abistr = ""
        for n in names:
            abistr += n + "\n"
        messagebox.showinfo("Vale nimi", "Sellist nime ei leidnud. Valikud on:\n" + abistr)
        return

    analüüsiinfo = analüüs.analyze(sõnumid, names, progress, tööinfo, OMANIK)
    if var1.get() == 1:
        seisuinfo("Loon pdf'i. If i'm not responding then it doesn't mean i'm dead...")
        #pdflooja.create(analüüsiinfo)
    kirjutaTeksti(analüüsiinfo)
    seisuinfo("Valmis!")






















###################################### GUI ###########################################

root = Tk()
root.title("Facebook chat analyzer")
root.resizable(True, True)
root.geometry("420x300")


customed_style = Style()
customed_style.configure('Custom.TNotebook.Tab', padding=[20, 7], font=('Helvetica', 13))

tabControl = Notebook(root, style='Custom.TNotebook')

tab1 = Frame(tabControl)
tabControl.add(tab1, text="Analyze")
tabControl.pack(expand=1, fill="both")

tab2 = Frame(tabControl)
tabControl.add(tab2, text="Results")
tabControl.pack(expand=1, fill="both")

tab3 = Frame(tabControl)
tabControl.add(tab3, text="How to")
tabControl.pack(expand=1, fill="both")


path_to_dir = tk.Entry(tab1, width=65, justify='center')
path_to_dir.insert(0, 'Enter path here...')
path_to_dir.bind('<FocusIn>', on_entry_click_path)
path_to_dir.bind('<FocusOut>', on_focusout_path)
path_to_dir.config(fg = 'grey')
path_to_dir.pack(pady=7)


fullname = tk.Entry(tab1, width=50, justify='center')
fullname.insert(0, 'Enter FB file owner full name here...')
fullname.bind('<FocusIn>', on_entry_click_fullname)
fullname.bind('<FocusOut>', on_focusout_fullname)
fullname.config(fg = 'grey')
fullname.pack(pady=7)


var1 = IntVar()
pdfcheck = Checkbutton(tab1, text="Kas teen pdf'i ka? See võtab natuke rohkem aega.", variable=var1)
pdfcheck.pack(pady= 7)


nupp = Button(tab1, text="Käivita", command=lambda: käivita())
nupp.pack(pady=7)

tekst = Text(tab2)
tekst.pack()
tekst.config(state=DISABLED)


howto = Text(tab3)
info = "Kopeeri sõnumite kausta full path analyze tab'is sisendi reale. Pastemiseks saad kasutada ctr+v\n\nNäide full pathist: C:\\Users\\Karl\\Documents\\Messenger analyzis\\GoldenTrio_tswwMWYp2w\n\nSeejärel vajuta nuppu ja peale analüüsi tekib tekstilist infot Results tab'ile ja graafikud leiad kaustast results."

howto.insert(INSERT, info)
howto.pack()
howto.config(state=DISABLED)


tööinfo = Label(tab1)
tööinfo.pack()

progress = Progressbar(tab1, orient=HORIZONTAL, length=100, mode='determinate')
progress.pack()



root.mainloop()