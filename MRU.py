import winreg as wrg
import binascii
import re
import csv

MRU_list = []

def get_mru(reg_key):
    location = wrg.HKEY_CURRENT_USER
    Key = wrg.OpenKeyEx(location,reg_key)
    for x in range(0,1024):
        try:
            value = wrg.QueryValueEx(Key,str(x))
            MRU_list.insert(x,re.sub('[^A-z0-9 -.]', '', value[0].decode("unicode-escape")).replace(" ", " "))
        except WindowsError as e:
            break

    if Key:
        wrg.CloseKey(Key)

def main():
    location = wrg.HKEY_CURRENT_USER
    reg_key =r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSavePidlMRU"
    key = wrg.OpenKeyEx(location,reg_key,0,wrg.KEY_READ)
  
    for i in range(200):
        try:
            subkey = wrg.EnumKey(key, i)
            val =( str(reg_key + '\\' +str(subkey)))
            get_mru(val)
        except:
            
            break
    
    get_mru(r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedPidlMRU")
    header = ['item']
    with open('MRU.csv','w',newline='',encoding='utf-8') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(header)
        wr.writerows(zip(MRU_list))
    
    

    myfile.close()
main() 