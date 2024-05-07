import tkinter as tk                     
from tkinter import ttk 
import csv
from tkinter import filedialog
from tkinter import *



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

#tab2 

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