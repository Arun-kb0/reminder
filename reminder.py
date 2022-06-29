from cProfile import label
from ctypes import alignment
from lib2to3.pgen2.token import RIGHTSHIFTEQUAL
import sqlite3
import re  
from datetime import date, datetime,timedelta
from time import time
from tkinter import *
import tkinter

def in_min(t1):
    h,m = t1.split(":")
    min = (int(h)*60)+int(m)
    #print(h,min)
    return min

def create_reminder(reminder_name, rtime, remarks):
   
   # reminder_name = str(input("enter reminder name : "))
    #rtime =str(input("enter time in 24 hour clock : "))
    #remarks = str(input("enter remarks : "))
    
    if len(reminder_name) >0 and len(rtime)>0:   
        remind = {reminder_name:{rtime:remarks}}
        return remind
             
def add_to_db(remind):
    #c.execute("DROP TABLE IF EXISTS reminder")
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
    

def alarm(select):

    alarm_bit=False
    c.execute("SELECT * FROM reminder")
    data = c.fetchall()

    while alarm_bit ==False:
        time_now_tmp = datetime.now()
        #print(time_now_tmp)
        time_now_tmp2= re.search(r" (.*:.*):",str(time_now_tmp))
        time_now =  time_now_tmp2.group(1)

        for d in data:
            #print(f"alarm at{time_now}")
            if time_now in d :
                print("_"*20+"ALARM"+"_"*20)
                print(f"time : {d[1]}\nreminder: {d[0]}\ngoal: {d[2]}")
                c.execute(f"DELETE FROM reminder where time = '{time_now}'")
                alarm_bit = True
                break 
        conn.commit()
    
        if alarm_bit == False :
            if select:
                rtime = data[-1][1]
                print_details(rtime)    
        
            else:
                r={}
                diff_sorted=[]
                t2 = in_min(str(time_now))
                for row in data:
                    t1 = in_min(str(row[1]))
                    diff = t1 - t2
                    if diff < 0:
                        diff +=1444
                    r[diff]=row[1]           
                print(r)
                for k in sorted(r.keys()):
                    diff_sorted.append(r[k])
                    #print(k)
                print_details(diff_sorted[0])
                #print(r,"\n",diff_sorted)
                

def print_details(rtime):
    #prints start time and time left for reminder

    time_now_tmp = datetime.now()
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
        
        
    if int(h2)>0:
            print(f"{h2} hours and {m2} minutes left")
    elif int(h2) == 0 and m>0:
        print(f"{m2} minutes left")
      
    else:
        print("less than 1 minute left")


if __name__ == "__main__" :
    root = tkinter.Tk()
    root.title("Reminder")
    root.geometry("600x400")
 
    conn = sqlite3.connect("remiders.db")
    c = conn.cursor()

    def submit(): 
        reminder_name = rn.get()
        rtime = rt.get()
        remarks = rr.get()

        remind = create_reminder(reminder_name, rtime, remarks)
        add_to_db(remind)
        #show_reminder()
        alarm_bit = alarm(True) 
        conn.close()     

    def check():
        show_reminder() 
        #alarm(False)

    rn = StringVar()
    rt =StringVar()
    rr = StringVar()


    l1 = Label(root,text="enter reminder name :")
    l2 = Label(root,text ="enter time :")
    l3 = Label(root,text="enter remarks :")


    
    e1 = Entry(root, textvariable=rn)
    e2 = Entry(root,textvariable=rt)
    e3 = Entry(root,textvariable=rr)

    btn1 = Button(root,text="create reminder",command=submit)
    btn2 = Button(root,text="check reminders",command= check)

    l1.grid(row=0,column=0)
    e1.grid(row=0,column=1,columnspan=5, pady=10)
    l2.grid(row=1,column=0)
    e2.grid(row=1,column=1,columnspan=5,pady=10)
    l3.grid(row=2,column=0,)
    e3.grid(row=2,column=1,columnspan=5,pady=10)

    btn1.grid(row=3,column=1,columnspan=5,pady=15)
    btn2.grid(row=4,column=1, columnspan=5,pady=15)

    root.mainloop()