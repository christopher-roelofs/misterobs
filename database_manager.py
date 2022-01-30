from glob import glob
from tkinter import *           # Python interface to the Tk GUI toolkit
from tkinter import filedialog  # open file
from tkinter import ttk
from tkinter.messagebox import showinfo
import tkinter
import database
import database_tools

selected_uuid = ""

root = Tk()
root.title('Database Manager')

#menu itmes removed for space


root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

frame1 = Frame(root)
frame2 = Frame(root)
frame3 = Frame(root)
scrollbar = Scrollbar(frame1)     # put a scrolbar widget on the right side of the window
scrollbar.pack(side = RIGHT, fill = Y)

# put a treeview widget on the window with stylized column headers and use show="headings" to hide the first hierarchy column
column_headers=['uuid','release_name', 'system', 'region']
style = ttk.Style()
style.configure("Treeview.Heading", font=("Verdana", 11))
tv = ttk.Treeview(frame1, height=30, columns=column_headers, show="headings", yscrollcommand = scrollbar.set) 

def refresh_games(search=""):
    for item in tv.get_children():
        tv.delete(item)
    for game in database.search_roms_by_name(search):
        tv.insert('', tkinter.END, values=(game['uuid'],game['release_name'],game["system"],game["region"]))

tv.pack(side=LEFT, fill=BOTH, expand=TRUE)
scrollbar.config(command = tv.yview)



def search_games(e):
    for item in tv.get_children():
        tv.delete(item)
    for game in database.search_roms_by_name(search_entry.get()):
        tv.insert('', tkinter.END, values=(game['uuid'],game['release_name'],game["system"],game["region"]))

def clear_search():
    search_entry.delete(0, END)
    refresh_games()

clear_search_button = ttk.Button(frame2, text = "Clear", width=15,command=clear_search)
clear_search_button.pack(side = RIGHT, anchor =NE , padx=10, pady=5)

search_label = Label(frame2, text= "Search:")
search_label.pack(side = LEFT, anchor = W, padx=1, pady=1)

search_entry = Entry(frame2,width=60)
search_entry.pack(side = RIGHT, anchor = W, padx=1, pady=1)
search_entry.bind('<KeyRelease>', search_games)



def treeview_sort_column(tv, col, text, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, text=text, command=lambda _col=col: \
                 treeview_sort_column(tv, _col, text,not reverse))
    

tv.heading('uuid', text='UUID')
tv.column('uuid', anchor='w',width=50)

tv.heading('release_name', text='Release Name',command=lambda _col="release_name":treeview_sort_column(tv, _col, 'Release Name', False))
tv.column('release_name', anchor='w', width = 400)

tv.heading('system', text='System',command=lambda _col="system":treeview_sort_column(tv, _col,"System",False))
tv.column('system', anchor='w',width=180)

tv.heading('region', text='Region',command=lambda _col="region":treeview_sort_column(tv, _col,"Region",False))
tv.column('region', anchor='w',width = 90)

for game in database.search_roms_by_name(""):
    tv.insert('', tkinter.END, values=(game['uuid'],game['release_name'],game["system"],game["region"]))


rn_label = Label(frame3, text= "Release Name")
rn_label.pack( anchor = SW,padx=1, pady=1)

rn_entry = Entry(frame3,width=60)
rn_entry.pack( anchor = SW,padx=1, pady=1)

romn_label = Label(frame3, text= "Rom Extensionless File Name")
romn_label.pack( anchor = SW,padx=1, pady=1)

romn_entry = Entry(frame3,width=60)
romn_entry.pack( anchor = SW,padx=1, pady=1)

sha1_label = Label(frame3, text= "SHA1")
sha1_label.pack( anchor = SW,padx=1, pady=1)

sha1_entry = Entry(frame3,width=60)
sha1_entry.pack( anchor = SW,padx=1, pady=1)

developer_label = Label(frame3, text= "Developer")
developer_label.pack( anchor = SW,padx=1, pady=1)

developer_entry = Entry(frame3,width=60)
developer_entry.pack( anchor = SW,padx=1, pady=1)

publisher_label = Label(frame3, text= "Publisher")
publisher_label.pack( anchor = SW,padx=1, pady=1)

publisher_entry = Entry(frame3,width=60)
publisher_entry.pack( anchor = SW,padx=1, pady=1)

genre_label = Label(frame3, text= "Genre")
genre_label.pack( anchor = SW,padx=1, pady=1)

genre_entry = Entry(frame3,width=60)
genre_entry.pack( anchor = SW,padx=1, pady=1)

date_label = Label(frame3, text= "Date")
date_label.pack( anchor = SW,padx=1, pady=1)

date_entry = Entry(frame3,width=60)
date_entry.pack( anchor = SW,padx=1, pady=1)

reference_label = Label(frame3, text= "Reference URL")
reference_label.pack( anchor = SW,padx=1, pady=1)

reference_entry = Entry(frame3,width=60)
reference_entry.pack( anchor = SW,padx=1, pady=1)

manual_label = Label(frame3, text= "Manual URL")
manual_label.pack( anchor = SW,padx=1, pady=1)

manual_entry = Entry(frame3,width=60)
manual_entry.pack( anchor = SW,padx=1, pady=1)

region_label = Label(frame3, text= "Region")
region_label.pack( anchor = SW,padx=1, pady=1)

region_combo = ttk.Combobox(frame3)
region_combo["values"] = database_tools.regions
region_combo.current(1)
region_combo.pack(anchor = SW,padx=1, pady=1)

system_label = Label(frame3, text= "System")
system_label.pack( anchor = SW,padx=1, pady=1)

system_combo = ttk.Combobox(frame3)
system_combo["values"] = database_tools.systems
system_combo.current(1)
system_combo.pack(anchor = SW,padx=1, pady=1)


description_label = Label(frame3, text= "Description")
description_label.pack(anchor = SW,padx=1, pady=1)

description_text = Text(frame3,height=10, width=60)
description_text.pack(anchor = SW,padx=1, pady=1)




def clear():
    global selected_uuid
    selected_uuid = ""
    rn_entry.delete(0, END)
    romn_entry.delete(0, END)
    region_combo.current(1)
    system_combo.current(1)
    developer_entry.delete(0, END)
    sha1_entry.delete(0, END)
    publisher_entry.delete(0, END)
    genre_entry.delete(0, END)
    date_entry.delete(0, END)
    reference_entry.delete(0, END)
    manual_entry.delete(0, END)
    description_text.delete("1.0", END)

def delete():
    if selected_uuid != "":
        MsgBox = tkinter.messagebox.askquestion ('Delete Record','Are you sure you want to delete the record',icon = 'warning')
        if MsgBox == 'yes':
            database.delete_rom(selected_uuid)
            clear()
            refresh_games()



def submit():
    rom = {}
    rom['uuid'] = selected_uuid
    rom["release_name"] = rn_entry.get()
    rom["region"] = region_combo.get()
    rom["system"] = system_combo.get()
    rom['sha1'] = sha1_entry.get().upper()
    rom["rom_extensionless_file_name"] = romn_entry.get()
    rom["publisher"] = publisher_entry.get()
    rom["date"] = date_entry.get()
    rom["developer"] = developer_entry.get()
    rom["genre"] = genre_entry.get()
    rom["description"] = description_text.get("1.0","end")
    rom["reference_url"] = reference_entry.get()
    rom["manual_url"] = manual_entry.get()
    if selected_uuid != "":
        test = database.get_rom_by_uuid(rom["uuid"])
        # rom already exist so we will update
        if len(test) > 0:
            database.update_rom(rom)
            clear()
            refresh_games()
        else:
            if database.is_new_rom(rom):
                database.update_rom(rom)
                clear()
                refresh_games()
            else:
                tkinter.messagebox.showerror(title="Error", message="Either Sha1 or Rom Extensionless File Name need to be unique")
                


def duplicate():
    global selected_uuid
    if selected_uuid != "":
        selected_uuid = database_tools.generate_uuid()
        tkinter.messagebox.showinfo(title="Creating Duplicate", message="You are now edidting a duplicate record \n a new uuid has been generated \n SHA1 AND OR Rom Name should be changed \n submit to add new record")


export_button = ttk.Button(frame3, text = "Submit", width=15,command=submit)
export_button.pack(side = LEFT, anchor = NE, padx=10, pady=5)

duplicate_button = ttk.Button(frame3, text = "Duplicate", width=15,command=duplicate)
duplicate_button.pack(side = LEFT, anchor = NE, padx=10, pady=5)


clear_button = ttk.Button(frame3, text = "Clear", width=15,command=clear)
clear_button.pack(side = LEFT, anchor = NE, padx=10, pady=5)

close_button = ttk.Button(frame3, text = "Delete", width=15,command=delete)
close_button.pack(side = LEFT, anchor = NE, padx=10, pady=5)





frame1.grid(column=0, row=0, sticky="nsew")
frame2.grid(column=0, row=1, sticky="n")
frame3.grid(column=1, row=0, sticky="nsew")
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

def item_selected(event):
    global selected_uuid
    for selected_item in tv.selection():
        item = tv.item(selected_item)
        record = item['values']
        details = database.get_rom_by_uuid(record[0])
        selected_uuid = details["uuid"]
        rn_entry.delete(0, END)
        rn_entry.insert(0, details["release_name"])
        romn_entry.delete(0, END)
        romn_entry.insert(0, details["rom_extensionless_file_name"])
        region_combo.set(details["region"])
        system_combo.set(details["system"])
        developer_entry.delete(0, END)
        developer_entry.insert(0, details["developer"])
        sha1_entry.delete(0, END)
        sha1_entry.insert(0, details["sha1"])
        publisher_entry.delete(0, END)
        publisher_entry.insert(0, details["publisher"])
        genre_entry.delete(0, END)
        genre_entry.insert(0, details["genre"])
        date_entry.delete(0, END)
        date_entry.insert(0, details["date"])
        reference_entry.delete(0, END)
        reference_entry.insert(0, details["reference_url"])
        manual_entry.delete(0, END)
        manual_entry.insert(0, details["manual_url"])
        description_text.delete("1.0", END)
        description_text.insert("1.0", details["description"])


tv.bind('<<TreeviewSelect>>', item_selected)

root.mainloop()