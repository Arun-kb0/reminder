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
        h1 = t1/60
        m1 =t1 % 60
        hour = timedelta(hours=int(h1), minutes=m1)
        return hour

def create_reminder():
    rtime = "13:50"#in 24 clock
    reminder_name = "workout"
    remarks = "do 100 pushups"

    if len(reminder_name) >0 and len(rtime)>0:
        time_now_tmp = datetime.now()
        #print(time_now_tmp)
        time_now= re.search(r" (.*:.*):",str(time_now_tmp))
        h,m= rtime.split(":")
        if time_now.group(1) > rtime: 
            diff = convert(time_now.group(1)) - convert(rtime)
        else:
            diff = convert(rtime) - convert(time_now.group(1))
        diff=convert(diff)
        print(f"{diff} remaining")

        remind = {reminder_name:{rtime:remarks}}
        return remind

def add_to_db(remind):
    c.execute("DROP TABLE if exists reminder ")
    c.execute('''CREATE TABLE reminder(remider_name varchar(255) NOT NULL,time varcher(255) NOT NULL,remarks varchar(255) )''')
    for k,v in remind.items():
        for k1,v1 in v.items():
            print(k,k1,v1)
            table = '''INSERT INTO reminder (remainder_name,time,remarks) VALUES ()'''

            
remind = create_reminder()
add_to_db(remind)