import winreg as wrg
import binascii
import re
import csv

networks_list = []

def get_previous_networks(g_key):
    net = ""
    location = wrg.HKEY_LOCAL_MACHINE

    Key = wrg.OpenKeyEx(location,g_key)

    network_name = ""
  
    try:
        network_name = wrg.QueryValueEx(Key,"ProfileName")
        net = net + str(network_name[0])
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
    wr = csv.writer(myfile)
    wr.writerow((["Names"]))
    for row in range(0,len(networks_list)):
        wr.writerow(networks_list[row])
  

        
myfile.close()