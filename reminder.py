import sqlite3
import re 

conn = sqlite3.connect("remiders.db")
c = conn.cursor()

def create_reminder():
    time = "06:30"#in 24 clock
    reminder_name = "workout"
    remarks = "do 100 pushups"

    
def create_db():
    c.execute("DROP TABLE if exists reminder ")
    c.execute('''CREATE TABLE reminder(time varcher(255) NOT NULL,remider_name varchar(255) NOT NULL,remarks varchar(255) )''')
