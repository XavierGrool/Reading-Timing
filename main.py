from tkinter import *
from tkinter import ttk
from tkinter import font
import time
import threading
from datetime import date
import os

switch = False
thread_exist = False
total_time = 0

def timing():
    while True:
        time.sleep(1)
        if switch == True:
            global total_time
            total_time += 1

            if total_time % 60 == 0:
                f = open("record.txt", "w")
                f.write(date.today().isoformat() + " " + str(total_time))
                f.close()
            hour = (total_time % 216000) // 3600
            minute = (total_time % 3600) // 60
            second = total_time % 60
            show_time.set(str(hour).zfill(2) + " : " + str(minute).zfill(2) + " : " + str(second).zfill(2))

def start_or_stop():
    global switch
    global thread_exist

    if btn_text.get() == "开始":
        switch = True
        t = threading.Thread(target=timing)
        thread_exist = True
        t.start()
        btn_text.set("暂停")
    elif btn_text.get() == "继续":
        switch = True
        if thread_exist == False:
            t = threading.Thread(target=timing)
            thread_exist = True
            t.start()
        btn_text.set("暂停")
    else:
        switch = False
        btn_text.set("继续")

root = Tk()
root.title("英语上80了吗？")
root.geometry('400x100-50+50')

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

show_time = StringVar()
btn_text = StringVar()

if os.path.exists("./record.txt"): # 记录文件存在 判断日期是否有效 有效的话就直接显示累计时长 无效则重置
    f = open("record.txt", "r")
    record = f.read().split()
    if record[0] == date.today().isoformat():
        total_time = int(record[1])
        hour = (total_time % 216000) // 3600
        minute = (total_time % 3600) // 60
        second = total_time % 60
        show_time.set(str(hour).zfill(2) + " : " + str(minute).zfill(2) + " : " + str(second).zfill(2))
        btn_text.set("继续")
        f.close()
    else:
        show_time.set("00 : 00 : 00")
        btn_text.set("开始")
        f.close()
        f = open("record.txt", "w")
        f.write(date.today().isoformat() + " 0")
        f.close()
else: # 记录文件不存在
    show_time.set("00 : 00 : 00")
    btn_text.set("开始")
    f = open("record.txt", "w")
    f.write(date.today().isoformat() + " 0")
    f.close()

appHighlightFont = font.Font(family='Helvetica', size=24, weight='bold')
ttk.Label(mainframe, textvariable=show_time, font=appHighlightFont).grid(column=1, row=1, padx=40, pady=20)

ttk.Button(mainframe, textvariable=btn_text, command=start_or_stop).grid(column=2, row=1, padx=20, pady=20)

root.mainloop()