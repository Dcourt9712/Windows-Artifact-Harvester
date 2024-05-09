import winreg as wrg
import binascii
import re
import csv
import chardet

import struct
from binascii import unhexlify
from datetime import datetime, timedelta
networks_list = []

def get_previous_networks(g_key):
    net = ""
    location = wrg.HKEY_LOCAL_MACHINE

    Key = wrg.OpenKeyEx(location,g_key)

    network_name = ""
    date_created = ""
  
    try:
        network_name = wrg.QueryValueEx(Key,"ProfileName")
        net = net + str(network_name[0])
    except WindowsError as e:
        pass

    try:
        
        date_created = wrg.QueryValueEx(Key,"DateCreated")
        raw = date_created[0].hex()
      
        year = int(str(raw[2:4] + raw[0:2]),16)
        month = int(str(raw[7:8] + raw[5:6]),16)
        day_number =int(str(raw[15:16] + raw[13:14]),16)

        hour = str(int(str(raw[19:20] + raw[17:18]),16))
        if(len(hour) < 2):
            hour = "0" + str(hour)
        
        minute = str(int(str(raw[23:24] + raw[21:22]),16))
        if(len(minute) < 2):
            minute = "0" + str(minute)

        seconds = str(int(str(raw[27:28] + raw[25:26]),16))

        if(len(seconds) < 2):
            seconds = "0" + str(seconds)

        date = str(year) + "-" + str(month) + "-" + str(day_number) + " "+ str(hour) + ":" + str(minute) + ":" + str(seconds)

        net = net + " ," + date
    except WindowsError as e:
        pass


    try:
        
        date_last_connected = wrg.QueryValueEx(Key,"DateLastConnected")
        raw = date_last_connected[0].hex()
      
        year = int(str(raw[2:4] + raw[0:2]),16)
        month = int(str(raw[7:8] + raw[5:6]),16)
        day_number =int(str(raw[15:16] + raw[13:14]),16)

        hour = str(int(str(raw[19:20] + raw[17:18]),16))
        if(len(hour) < 2):
            hour = "0" + str(hour)
        
        minute = str(int(str(raw[23:24] + raw[21:22]),16))
        if(len(minute) < 2):
            minute = "0" + str(minute)

        seconds = str(int(str(raw[27:28] + raw[25:26]),16))

        if(len(seconds) < 2):
            seconds = "0" + str(seconds)

        date = str(year) + "-" + str(month) + "-" + str(day_number) + " "+ str(hour) + ":" + str(minute) + ":" + str(seconds)

        net = net + " ," + date
    except WindowsError as e:
        pass
   
    
    networks_list.append(net.split(','))

    if Key:
        wrg.CloseKey(Key)


key_list = []
count = 0
location = wrg.HKEY_LOCAL_MACHINE
reg_key =r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\NetworkList\Profiles"
key = wrg.OpenKeyEx(location,reg_key,0,wrg.KEY_READ)
for i in range(1024):
    try:
        subkey = wrg.EnumKey(key, i)
    
        val =( str(reg_key) + '\\' +str(subkey))
        key_list.insert(i,val)
    
    except WindowsError as e:
        break    

for i in range(0,len(key_list)):
    get_previous_networks(key_list[i])


with open('PreviousNetworks.csv','w',newline='',encoding='utf-8') as myfile:
    wr = csv.writer(myfile, escapechar = '\\')
    wr.writerow((["Names","DateCreated", "DateLastConnected" ]))
    for row in range(0,len(networks_list)):
        wr.writerow(networks_list[row])
  

        
myfile.close()