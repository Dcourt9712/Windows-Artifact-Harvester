
import os
import sqlite3




"""
Chrome must be closed when running this script otherwise it cannot access the database
"""

def main():
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

  

if __name__ == "__main__":
    main()