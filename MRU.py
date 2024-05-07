import winreg as wrg
import binascii
import re
import csv

def main():
   

    MRU_list = []
    location = wrg.HKEY_CURRENT_USER
    Key = wrg.OpenKeyEx(location,r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedPidlMRU")
    for x in range(0,1024):
        try:
            value = wrg.QueryValueEx(Key,str(x))
            MRU_list.insert(x,re.sub('[^A-z0-9 -.]', '', value[0].decode("unicode-escape")).replace(" ", " "))
        except WindowsError as e:
            break

    if Key:
        wrg.CloseKey(Key)

   
    for items in range(0,len(MRU_list)):
        print(MRU_list[items])

    header = ['item']
    with open('MRU.csv','w',newline='',encoding='utf-8') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(header)
        wr.writerows(zip(MRU_list))
    
    

    myfile.close()
main() 