from lib2to3.pytree import convert
from math import remainder
import sqlite3
import re  
from datetime import date, datetime,timedelta

conn = sqlite3.connect("remiders.db")
c = conn.cursor()

def convert(t1):
    try: 
        h,m = t1.split(":")
        min = (int(h)*60)+int(m)
        return min
    except:
        hour = timedelta( minutes=t1)
        return hour

def create_reminder():
    rtime = "17:43"#in 24 clock
    reminder_name = "workout"
    remarks = "do 100 pushups"

    if len(reminder_name) >0 and len(rtime)>0:
        time_now_tmp = datetime.now()
        #print(time_now_tmp)
        time_now= re.search(r" (.*:.*):",str(time_now_tmp))
        h,m= rtime.split(":")
        if time_now.group(1) <= rtime:
            diff = convert(time_now.group(1)) - convert(rtime)
            print(diff)
        else:
            diff = (convert(time_now.group(1)) - convert(rtime)) + 1440
            print(diff)
        diff=convert(diff)
        print(f"{diff} remaining")

        remind = {reminder_name:{rtime:remarks}}
        return remind,time_now.group(1)

def add_to_db(remind):
    c.execute("DROP TABLE IF EXISTS reminder")
    c.execute('''CREATE TABLE if not exists reminder ( reminder_name varchar(255) NOT NULL,time varchar(255) NOT NULL,remarks varchar(255) )''')
    for k,v in remind.items():
        for k1,v1 in v.items():
            k3,k2,v2 = "'"+str(k)+"'","'"+str(k1)+"'","'"+str(v1)+"'"
            table = f'''INSERT INTO reminder(reminder_name,time,remarks) VALUES({k3},{k2},{v2})'''
            c.execute(table)
    conn.commit()

def show_reminder():
    print("all reminders")
    c.execute("SELECT * FROM reminder ")
    data = c.fetchall()
    for d in data:
        print(d)
    conn.commit()
    

def alarm(time_now):
    c.execute("SELECT * FROM reminder")
    data = c.fetchall()
    for d in data:
        if time_now in d :
            print("_"*20+"ALARM"+"_"*20)
            print(d)
            c.execute(f"DELETE FROM reminder where time = '{time_now}'")
    show_reminder()
    conn.commit()
    conn.close()


remind,time_now = create_reminder()
add_to_db(remind)
show_reminder()
alarm(time_now)