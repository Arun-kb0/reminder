import sqlite3
import re  
from datetime import date, datetime,timedelta
from time import time
from tkinter import *
import tkinter
from tkinter.font import Font
from turtle import bgcolor, color
from PIL import Image,ImageTk



root = tkinter.Tk()

#convert data to minutes
def in_min(t1):
    h,m = t1.split(":")
    min = (int(h)*60)+int(m)
    #print(h,min)
    return min

#creates reminder
def create_reminder(reminder_name, rtime, remarks):
   
    if len(reminder_name) >0 and len(rtime)>0:   
        remind = {reminder_name:{rtime:remarks}}
        return remind
             
#add data to DB
def add_to_db(remind):
    #c.execute("DROP TABLE IF EXISTS reminder")
    #c.execute('''CREATE TABLE if not exists reminder ( reminder_name varchar(255) NOT NULL,time varchar(255) NOT NULL,remarks varchar(255) )''')
    for k,v in remind.items():
        for k1,v1 in v.items():
            k3,k2,v2 = "'"+str(k)+"'","'"+str(k1)+"'","'"+str(v1)+"'"
            table = f'''INSERT INTO reminder(reminder_name,time,remarks) VALUES({k3},{k2},{v2})'''
            c.execute(table)
    conn.commit()

#shows all reminders
def show_reminder():
    #print("all reminders")

    new_window = Toplevel(root)
    new_window.geometry("400x300")
    new_window.title("all reminders ")

    

    c.execute("SELECT * FROM reminder ")
    data = c.fetchall()

    db_data = Text(new_window,width=70 ,height=20)
    db_data.grid(row=0,column=0)


    for d in data:
        #print(d)
        db_data.insert(END, str(d).strip("()") + "\n")
    conn.commit()
    
#shows alarm on time
def alarm(select):

    alarm_bit=False
    c.execute("SELECT * FROM reminder")
    data = c.fetchall()

    while alarm_bit ==False:

        #print("in alarm")
        time_now_tmp = datetime.now()
        #print(time_now_tmp)
        time_now_tmp2= re.search(r" (.*:.*):",str(time_now_tmp))
        time_now =  time_now_tmp2.group(1)

        for d in data:
            #print(f"alarm at{time_now}")
            if time_now in d :

                alarm_on = Label(frame1,text=f"Reminder : {d[0]} \nTime : {d[1]}\nGoal: {d[2]}",
                font=font_airal3, foreground= "blue" )
                alarm_on.grid(row=1,column=0)

                c.execute(f"DELETE FROM reminder where time = '{time_now}'")
                alarm_bit = True
                root.bell()
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
                #print(r)
                for k in sorted(r.keys()):
                    diff_sorted.append(r[k])
                    #print(k)
                print_details(diff_sorted[0])
                #print(r,"\n",diff_sorted)
                
#covert data from alarm to format for printing
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
        #print(f"{h2} hours and {m2} minutes left")

        t_count= f"reminder in {h2} hours and {m2} minutes"
        time_count = Label(frame1,text=t_count,width=40,font= font_airal2)
        time_count.grid(row=0,column=0,pady=10)
        root.update()

    elif int(h2) == 0 and m>0:
        #print(f"{m2} minutes left")

        t_count = f"reminder in {m2} minutes" 
        time_count = Label(frame1,text=t_count,width=40,font= font_airal2)
        time_count.grid(row=0,column=0,pady=10)
        root.update()

    else:
        #print("less than 1 minute left")

        t_count =  "reminder in less than 1 minute"
        time_count = Label(frame1,text=t_count,width=40,font= font_airal2)
        time_count.grid(row=0,column=0, pady=10)
        root.update()

#main 
if __name__ == "__main__" :
   
    root.title("Reminder")
    root.geometry("700x400")
 
    #creating DB
    conn = sqlite3.connect("remiders.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE if not exists reminder ( reminder_name varchar(255) NOT NULL,time varchar(255) NOT NULL,remarks varchar(255) )''')
    
    #for creating reminder 
    def submit():

        reminder_name = rn.get()
        rtime = rt.get()
        remarks = rr.get()

        remind = create_reminder(reminder_name, rtime, remarks)
        add_to_db(remind)
        #show_reminder()
        alarm(True)

    #shows all db contents in app
    def check():

        show_reminder() 
        alarm(True)

    
    #fonts
    font_airal = Font(family="Arial", size ="15", weight="bold")
    font_airal2 = Font(family="Arial", size ="10")
    font_airal3 = Font(family="Arial", size ="10")

    #tkinter variables
    rn = StringVar()
    rt =StringVar()
    rr = StringVar()

    #labelsv for entry
    l1 = Label(root,text="enter reminder name :",font= font_airal2)
    l2 = Label(root,text ="enter time :",font= font_airal2)
    l3 = Label(root,text="enter remarks :",font= font_airal2)

    #for entering data
    e1 = Entry(root, textvariable=rn,font= font_airal2 )
    e2 = Entry(root,textvariable=rt, font= font_airal2 )
    e3 = Entry(root,textvariable=rr, font= font_airal2)

    #buttons
    btn1 = Button(root,text="create reminder",font= font_airal2, command=submit)
    btn2 = Button(root,text="check reminders",font= font_airal2, command= check)

    #placing labels,buttons and entry
    l1.grid(row=0,column=0)
    e1.grid(row=0,column=1,columnspan=5, pady=10)
    l2.grid(row=1,column=0)
    e2.grid(row=1,column=1,columnspan=5,pady=10)
    l3.grid(row=2,column=0,)
    e3.grid(row=2,column=1,columnspan=5,pady=10)

    btn1.grid(row=3,column=1,columnspan=5,pady=15)
    btn2.grid(row=4,column=1, columnspan=5,pady=15)
    
    #creating frame
    frame1 = LabelFrame(root,text = "alarm details",width=5,height=30, font=font_airal ,
        foreground="gray")
    frame1.grid(row=0,column=7,padx=35)

    c.execute("SELECT * FROM reminder ")
    data1 = c.fetchall()
    if len(data1) !=0 :
        alarm(True)

    root.mainloop()
    conn.close()  