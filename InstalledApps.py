import winreg as wrg
import binascii
import re
import csv

key_list = []
installed_app  = []

def get_installed_apps(g_key):
    
    location = wrg.HKEY_LOCAL_MACHINE

    Key = wrg.OpenKeyEx(location,g_key)

    display_name = ""
    install_date = ""
    publisher = ""
    install_source = ""
    app = ""
    try:
        display_name = wrg.QueryValueEx(Key,"DisplayName")
        app = app + str(display_name[0])
    except WindowsError as e:
        pass
    
    try:
        install_date = wrg.QueryValueEx(Key,"InstallDate")
        app = app + " ," + str(install_date[0])
    except WindowsError as e:
            pass       
    try:      
        publisher = wrg.QueryValueEx(Key,"Publisher")
        app =  app + " ," + str(publisher[0])
       
    except WindowsError as e:
        pass 
          
    try:    
        install_source = wrg.QueryValueEx(Key,"InstallSource")
        app = app + "," + str(install_source[0])
    except WindowsError as e:
        pass 
  
    installed_app.append(app.split(','))
    if Key:
        wrg.CloseKey(Key)


count = 0
location = wrg.HKEY_LOCAL_MACHINE
reg_key =r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
key = wrg.OpenKeyEx(location,reg_key,0,wrg.KEY_READ)

for i in range(1024):
    try:
        subkey = wrg.EnumKey(key, i)
    
        val =( str(reg_key) + '\\' +str(subkey))
        key_list.insert(i,val)
    
    except WindowsError as e:
        break    

for i in range(0,len(key_list)):
    get_installed_apps(key_list[i])

with open('InstalledApps.csv','w',newline='',encoding='utf-8') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(("DisplayNames","installDates","publishers","install_sources"))
    for row in range(0,len(installed_app)):
        wr.writerow(installed_app[row])
  

        
myfile.close()