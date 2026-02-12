import random
import tkinter as tk
import time
import threading
import os
import queue
import signal
score : int = 0
correct = 0
eval_list = ('+','-','*','/')
user_list = ('+','-','x','÷')
fuhao : str | None = None
n1 : int = 0
n2 : int = 0
time_text : str | None = None
add_time = queue.Queue()
now_time = queue.Queue()
def check_add() -> int:
    try:
        return add_time.get(block=False)
    except queue.Empty:
        return 0
def timer(sec : float) -> None:
    def time_down() -> None:
        nonlocal sec
        while sec > 0:
            sec += check_add()
            now_time.put(round(sec,1))
            time.sleep(0.1)
            sec -= 0.1
        os.kill(os.getpid(),signal.SIGINT)
    timet = threading.Thread(target = time_down,daemon = True)
    timet.start()
def tk_window() -> None:
    root = tk.Tk()
    root.geometry("200x80+0+0")
    root.attributes("-alpha",0.5)
    root.attributes("-topmost",True)
    root.overrideredirect(True)
    root.resizable(False,False)
    root.configure(bg = "#39C5BB")
    label = tk.Label(root,text = "not define",fg = "#FF0000",bg = "#39C5BB",font = ("Consolas",28,"bold"))
    label.pack(expand = True)
    def get_time() -> None:
        global time_text
        try:
            time_text = now_time.get(block = False)
            label.config(text = str(time_text))
        except queue.Empty:
            pass
        root.after(50,get_time)
    root.after(50,get_time)
    root.mainloop()
def get_number_1() -> str:
    global n1
    n1 = random.randint(-correct*3-5,correct*3+5)
    return str(n1)
def get_number_2() -> str:
    global n2
    while 1:
        n2 = random.randint(-correct*3-5,correct*3+5)
        if n2:
            break
    return str(n2)
def get_fuhao() -> int:
    global fuhao,tmp
    fuhao = random.randint(0,3)
    tmp = fuhao
    fuhao = eval_list[tmp]
    return tmp
def main(dsec : int) -> None:
    global score,n1,n2,fuhao,correct
    tktk = threading.Thread(target = tk_window,daemon = True)
    timer(dsec)
    tktk.start()
    while True:
        q = get_number_1()
        w = get_fuhao()
        e = get_number_2()
        if w == 3:
            n1 = n1*n2
            q = str(n1)
            e = str(n2)
        if (you_answer := input(f"({q}){user_list[w]}({e})=")) == str(int(eval(f"{n1}{fuhao}{n2}"))):
            print("你答对了")
            correct += 1
            add_time.put(5)
            score += correct
        else:
            print(f"你答错了，正确答案是{eval(f"{n1}{fuhao}{n2}")}")
            add_time.put(-correct)
print("计算游戏ver1.0")
input("按Enter已开始")
try:
    main(10)
except:
    print(f"你获得了{score}分，答对了{correct}题")
