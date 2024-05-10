import tkinter as tk                     
from tkinter import ttk 
import csv
from tkinter import filedialog
from tkinter import *
import platform
import winreg as wrg
import os.path
import socket
import re
import uuid
import json
import psutil
import logging
import cpuinfo
import wmi
import math



def open_csv_file():
    global file_path
    file_path = filedialog.askopenfilename(title="Open CSV File", filetypes=[("CSV files", "*.csv")])
    if file_path:
        display_csv_data(file_path)
    
    return file_path

def display_csv_data(file_path):
    try:
        with open(file_path, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  
            tree.delete(*tree.get_children())  

            tree["columns"] = header
            for col in header:
                tree.heading(col, text=col)
                tree.column(col, width=100)

            for row in csv_reader:
                tree.insert("", "end", values=row)

            status_label.config(text=f"CSV file loaded: {file_path}")

    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")


def search_csv_data():
    query = user_input.get()
    print(query)
    try:
        with open(file_path, 'r', newline='') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  
            tree.delete(*tree.get_children())

            tree["columns"] = header
            for col in header:
                tree.heading(col, text=col)
                tree.column(col, width=100)

            for row in csv_reader:
                    for items in row:
                        if query in items:
                            tree.insert("", "end", values=row)

            status_label.config(text=f"CSV file loaded: {file_path}")

    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")

def reset():
    display_csv_data(file_path)


root = tk.Tk() 
root.title("Windows Artifact Harvester") 
root.geometry("1200x600")
customed_style = ttk.Style()

tabControl = ttk.Notebook(root) 
  
tab1 = ttk.Frame(tabControl) 
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)

open_button = tk.Button(tab3, text="Open CSV File", command=open_csv_file)
open_button.pack(padx=20, pady=10)

tabControl.add(tab1, text ='Data collection scripts') 
tabControl.add(tab2, text ='PC Specs')
tabControl.add(tab3, text ='Data Reader') 
tabControl.pack(expand = 1, fill ="both") 

tree = ttk.Treeview(tab3, show="headings")
tree.pack(padx=20, pady=20, fill="both", expand=True)

status_label = tk.Label(tab3, text="", padx=20, pady=10)
status_label.pack()
#tab1
def script_clicked():
    if chrome_clicked.get():
        os.system(" python3 chrome.py")

    if app_clicked.get():
        os.system(" python3 InstalledApps.py")
    

    if MRU_clicked.get():
        os.system(" python3 MRU.py")

    if network_clicked.get():
        os.system(" python3 Networks.py")
        


var = IntVar()
welcome_label =tk.Label(tab1,text="Welcome to Windows-Artifact-Harvester",font=("Helvetica 12",30))
welcome_label.place(x=240, y=0)

chrome_clicked = tk.IntVar()
chrome_check = Checkbutton(tab1, text="Chrome", variable=chrome_clicked)
chrome_check.place(x = 0, y = 60)

app_clicked = tk.IntVar()
Installed_apps_check = Checkbutton(tab1, text="Installed_Apps", variable=app_clicked)
Installed_apps_check.place(x = 0, y = 90)

MRU_clicked = tk.IntVar()
MRU_check = Checkbutton(tab1, text="MRU(Most Recently viewed)",variable=MRU_clicked)
MRU_check.place(x = 0, y = 120)

network_clicked = tk.IntVar()
Networks_check = Checkbutton(tab1, text="Network information", variable=network_clicked)
Networks_check.place(x = 0, y = 150)


run_scripts_button = tk.Button(tab1, text="Run Scripts", command= script_clicked)
run_scripts_button.place(x=0,y=180)

#tab2
operating_system=tk.Label(tab2,text="Operating system: " + str(platform.system()),font=("Helvetica 12",10))
operating_system.place(x=0,y=0)

computer_name=tk.Label(tab2,text="Computer name: " + str(socket.gethostname()),font=("Helvetica 12",10))
computer_name.place(x=0,y=30)

user=tk.Label(tab2,text="Connected User: " + str(os.getlogin()),font=("Helvetica 12",10))
user.place(x=0,y=60)

ip_address=tk.Label(tab2,text="Ip_address: " + str(socket.gethostbyname(socket.gethostname())),font=("Helvetica 12",10))
ip_address.place(x=0,y=90)

mac_address=tk.Label(tab2,text="MAC_address: " + str(':'.join(re.findall('..', '%012x' % uuid.getnode()))),font=("Helvetica 12",10))
mac_address.place(x=0,y=120)

processor=tk.Label(tab2,text="Processor: " + str(cpuinfo.get_cpu_info()['brand_raw']),font=("Helvetica 12",10))
processor.place(x=0,y=150)

memory=tk.Label(tab2,text="Memory: " + str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB",font=("Helvetica 12",10))
memory.place(x=0,y=180)

partitions = psutil.disk_partitions()

partition_info=tk.Label(tab2,text="Partion info: " + str(partitions[0]),font=("Helvetica 12",10))
partition_info.place(x=0,y=210)

hard_drive_info = psutil.disk_usage('/')
hardrive_total=tk.Label(tab2,text="Hard disk total memory: " + str(math.trunc((hard_drive_info[0] / (2**30)))) + " GBS",font=("Helvetica 12",10))
hardrive_total.place(x=0,y=240)
hardrive_total=tk.Label(tab2,text="Hard disk used memory: " + str(math.trunc((hard_drive_info[1] / (2**30)))) + " GBS",font=("Helvetica 12",10))
hardrive_total.place(x=0,y=270)
hardrive_total=tk.Label(tab2,text="Hard disk free memory: " + str(math.trunc((hard_drive_info[2] / (2**30)))) + " GBS",font=("Helvetica 12",10))
hardrive_total.place(x=0,y=300)

controllers = wmi.WMI().Win32_VideoController()
graphics_card = "" 
for controller in controllers:
    graphics_card = str( controller.wmi_property('Name').value)

GPU=tk.Label(tab2,text="Graphics Card: " + str(graphics_card),font=("Helvetica 12",10))
GPU.place(x=0,y=330)





# tab3 
user_input = StringVar()
label1=tk.Label(tab3,text="By Title:",font="Helvetica 12")
label1.pack()
search1=tk.Entry(tab3,textvariable=user_input)
search1.pack()


search_button = tk.Button(tab3, text="Search", command=search_csv_data)
search_button.pack()
reset_button = tk.Button(tab3, text="Reset", command=reset)
reset_button.pack()


  
root.mainloop()   