
import os
import sqlite3
import csv



"""
Chrome must be closed when running this script otherwise it cannot access the database
"""

def main():
    columns = ['Urls','Titles','Times']
    name = os.getlogin()
    c =sqlite3.connect('C:\\Users\\'+ name +'\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History')
    cursor = c.cursor()
    cursor.execute('SELECT url FROM urls')
    urls = cursor.fetchall()
    cursor.execute('SELECT title from urls')
    titles = cursor.fetchall()
    cursor.execute('SELECT datetime(last_visit_time/1000000-11644473600, \"unixepoch\") as last_visited, url, title, visit_count FROM urls;')
    times = cursor.fetchall()
    new_times = [i[0] for i in times]

    print(new_times[0])
  

    with open('ChromeHistory.csv','w',newline='',encoding='utf-8') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(("Urls","Titles","Times"))
        wr.writerows(zip(urls,titles,new_times))
      
 
      
    myfile.close()

  

if __name__ == "__main__":
    main()