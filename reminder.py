import sqlite3
import re  
from datetime import date, datetime,timedelta
from time import time



def convert(t1):
    try: 
        h,m = t1.split(":")
        min = (int(h)*60)+int(m)
        print(min,h)
        return min
    except:
        hour = timedelta( minutes=t1)
        return hour

def create_reminder(rtime,reminder_name,remarks):
    #rtime = "17:43"#in 24 clock
    #reminder_name = "workout"
    #remarks = "do 100 pushups"

    if len(reminder_name) >0 and len(rtime)>0:
        time_now_tmp = datetime.now()
        #print(time_now_tmp)
        time_now= re.search(r" (.*:.*):",str(time_now_tmp))
        h1,m1= rtime.split(":")

        y= time_now_tmp.year
        m= time_now_tmp.month
        d= time_now_tmp.day
        t1 = datetime(y,m,d,int(h1),int(m1),0)
        diff = t1 - datetime.now()
        #print(diff)
        try:
            time_left = re.search(r", (.*):(.*):(.*)",str(diff))
            h2,m2,s2 = time_left.group(1),time_left.group(2),time_left.group(3)
        except:
            time_left = re.search(r"(.*):(.*):(.*)",str(diff))
            h2,m2,s2 = time_left.group(1),time_left.group(2),time_left.group(3)
        
        if alarm_bit:
            print("")
        
        elif int(h2)>0:
            print(f"{h2} hours and {m2} minutes left")
        elif int(h2) == 0 and m>0:
            print(f"{m2} minutes left")
      
        else:
            print("less than 1 minute left")

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
            print(f"time : {d[1]}\nreminder: {d[0]}\ngoal: {d[2]}")
            c.execute(f"DELETE FROM reminder where time = '{time_now}'")
            alarm_bit = True
    conn.commit()
    return alarm_bit

if __name__ == "__main__" :
    conn = sqlite3.connect("remiders.db")
    c = conn.cursor()
    remind,time_now = create_reminder("21:10","workout","100 pushups")
    add_to_db(remind)
    #show_reminder()
    alarm_bit = alarm(time_now)
    conn.close()