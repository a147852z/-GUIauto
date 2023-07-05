import tkinter as tk
from pynput import keyboard, mouse
from pynput.mouse import Controller as MouseController
import time
from datetime import datetime
import pprint
import json
import random
from tkinter import *
import pyautogui
from pynput.keyboard import Controller
import os
from PIL import Image
import pytesseract
import pyscreenshot as ImageGrab
import cv2
mouse_positions = {}
counter = 1
randomlist = [0,0,0,0]
word = []
wordtime = []
record_text_start = 0 
red = 0
Mtime = []#滑鼠記錄時間
Mred = {}
Ktime = []#鍵盤記錄時間
Kred = []
km = []
def on_press(key):
    global mouseXY, record_text_start, red, km
    try:
        if key == keyboard.Key.f2:
            record_coordinate()
        elif isinstance(key, keyboard.KeyCode):
            if red == 1:
                Kred.append(key.char)
                Ktime.append(float(time.time()))
                km.append("K")
            if record_text_start == 1:
                print(key.char)
                word.append(key.char)
                wordtime.append(float(time.time()))
            else:
                record_text_start = 0
        elif key == keyboard.Key.f1:   
            detection()
            mouseXY = mouse_controller.position
            textXY["text"] = f"對輸入框按shift來選定位置X:{mouseXY[0]} Y:{mouseXY[1]}"
        else:
            if red == 1:
                Kred.append(key.name)
                Ktime.append(float(time.time()))
                km.append("K")
    except AttributeError:
        pass

num = 0
def on_click(x, y, button, pressed):
    global red, Mtime, Mred, num, km
    if pressed:
        if red == 1:
            km.append("M")
            Mred[num] = {
                "x" : x,
                "y" : y
            }
            Mtime.append(float(time.time()))
            num +=1
            print(f"座標：({x}, {y})，按鍵：{button}")
            # 在这里执行你想要的操作

mouse_listener = mouse.Listener(on_click=on_click)
mouse_listener.start()

def record_coordinate():
    global counter, interval
    mouse_position = mouse_controller.position
    timestamp = datetime.now()
    timestamp_str = str(timestamp)
    if mouse_positions == {}:
        interval = []
    interval.append(float(time.time()))
    mouse_positions[counter] = (mouse_position[0], mouse_position[1], timestamp_str)
    coordinate_label["text"] = f"滑鼠座標：X={mouse_position[0]}, Y={mouse_position[1]}, 時間={timestamp}"
    counter += 1

def reset_coordinates():
    global counter  
    coordinate_label["text"] = "滑鼠座標："
    mouse_positions.clear()
    counter = 1
    print(interval)

def get_random1():
    random_x = random.randrange(0, 1919)
    randomlist[0] = random_x
    random_y = random.randrange(0, 1079)
    randomlist[1] = random_y
    getrandom1["text"] = f"亂數座標：X={random_x}, Y={random_y}"

def get_random2():
    random_x = random.randrange(0, 1919)
    randomlist[2] = random_x
    random_y = random.randrange(0, 1079)
    randomlist[3] = random_y
    getrandom2["text"] = f"亂數座標：X={random_x}, Y={random_y}"

def execute_actions():
    i = 0
    for key, value in mouse_positions.items():
        x, y, timestamp = value[0], value[1], value[2]
        mouse_controller.position = (x, y)
        mouse_controller.click(mouse.Button.left, 1)
        if i<len(interval)-1:
            time.sleep(interval[i+1]-interval[i])
            i+=1

def output_actions():
    with open("data.json", "w") as json_file:
        json.dump(mouse_positions, json_file)

def src():
    pyautogui.hotkey('win', 'shift', "s") 
    time.sleep(1)
    pyautogui.moveTo(randomlist[0], randomlist[1], duration = 0.5)
    pyautogui.dragTo(randomlist[2], randomlist[3], duration = 0.5, button='right') 
    try:
        time.sleep(1)
        pyautogui.moveTo(1690, 832)
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(1010, 151)
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(596, 115)
        pyautogui.click()
        time.sleep(1)
        tt = list(str(datetime.now()))
        for i in range(10):    
            pyautogui.typewrite(tt[i])
        pyautogui.typewrite(".png")
        time.sleep(1)
        pyautogui.moveTo(998, 597)
        pyautogui.click()
    except:
        pass



def record_text():
    global record_text_start
    if record_text_start == 0:
        record_text_start_button["text"] = f"記錄文字開關，目前為：開啟"
        record_text_start = 1
    elif record_text_start == 1:
        record_text_start_button["text"] = f"記錄文字開關，目前為：關閉，已重設"
        record_text_start = 0

def textstart():
    pyautogui.moveTo(mouseXY[0], mouseXY[1], duration = 0.5)
    pyautogui.click()
    for i in range(len(word)):   
        if i >= 1:
            time.sleep(wordtime[i] - wordtime[i - 1])
        pyautogui.typewrite(word[i])

def search_script():
    global filelist
    filelist = []
    for file_name in os.listdir('.'):  # 搜尋當前資料夾
        if file_name.endswith('.json'):  # 只處理以 .json 結尾的檔案
            filelist.append(file_name)
    searchs_text["text"] = f"{filelist}"

iii = 0
current_f = 0
current_file = ""
def select_script():
    global iii, current_file, current_f
    if iii >= len(filelist):
        iii = 0
    selects_text["text"] = f"當前為：{filelist[iii]}"
    current_file = filelist[iii]
    current_f = iii
    iii += 1

def generate_script():
    data = {"Kred": Kred, 
            "Ktime": Ktime, 
            "Mred": Mred, 
            "Mtime": Mtime, 
            "km": km}
    name = str(gs_text.get()) + ".json"
    print(name)
    with open(name, "w") as json_file:
        json.dump(data, json_file)
def execute_script():
    with open(filelist[current_f], "r") as json_file:
        data = json.load(json_file)
        Kred1 = data["Kred"]
        Ktime1 = data[ "Ktime"]
        Mred1 = data[ "Mred"]
        Mtime1 = data[ "Mtime"]
        km1 = data[ "km"]
        ki = 0
        mi = 0
        timef = Ktime1[0]
        for i in range(len(km1)):
            if km1[i] == "K":
                if ('0' <= Kred1[ki] <= '9') or ('A' <= Kred1[ki] <= 'Z') or ('a' <= Kred1[ki] <= 'z' and len(Kred1[ki]) == 1):
                    time.sleep(Ktime1[ki+1]-timef)
                    pyautogui.typewrite(Kred1[ki])
                else:
                    pyautogui.press(Kred1[ki])
                ki += 1
                timef = Ktime1[ki]
            if km1[i] == "M":
                time.sleep(Mtime1[mi+1]-timef)
                pyautogui.moveTo(Mred1[str(mi)]["x"], Mred1[str(mi)]["y"])
                pyautogui.click()
                mi += 1
                timef = Mtime1[mi]


def start():
    global red
    red = 1
    Mtime.append(float(time.time()))
    Ktime.append(float(time.time()))
    try:
        pass
    except:
        pass

def stop():
    global red
    red = 0
    del Mred[len(Mtime)-2]
    Mtime.pop()
    km.pop()
    print(Mred)
    print(Mtime)
    print(km)

def detection():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    #指定tesseract.exe執行檔位置
    mousXY = mouse_controller.position
    img = ImageGrab.grab(bbox=(mousXY[0]-50, mousXY[1]-50, mousXY[0]+50, mousXY[1]+50))  # X1, Y1, X2, Y2
    img.save('image.jpg', 'JPEG')
    img1 = cv2.imread("image.jpg")
    ret, img1 = cv2.threshold(img1, 127, 255, cv2.THRESH_BINARY)  #二值化
    cv2.imshow("1",img1)
    cv2.waitKey(0)
    #text = pytesseract.image_to_string(img) #讀英文
    #text = pytesseract.image_to_string(img, lang='chi_sim') #簡體中文
    text = pytesseract.image_to_string(img, lang='chi_tra+eng') #繁體中文
    print(text)

def script():
    pass
# 創建主視窗
window = tk.Tk()
window.title("圖形化界面")
window.geometry("600x600")

# 創建按鈕
record_button = tk.Button(window, text="記錄座標", command=record_coordinate)
record_button.pack(side=tk.TOP)

coordinate_label = tk.Label(window, text="滑鼠座標：")
coordinate_label.pack()
reset_button = tk.Button(window, text="重設", command=reset_coordinates)
reset_button.pack(side=tk.TOP)

execute_button = tk.Button(window, text="執行", command=execute_actions)
execute_button.pack(side=tk.TOP) 

output_button = tk.Button(window, text="輸出", command=output_actions)
output_button.pack(side=tk.TOP)


a = LabelFrame(window, height=600, width=200, text='產生亂數')
a.pack(side='top', fill='both', expand=True)
btn1 = Button(a, text='產生亂數1', command=get_random1)
btn1.grid(row=0, column=0)
btn2 = Button(a, text='產生亂數2', command=get_random2)
btn2.grid(row=2, column=0)
btn2 = Button(a, text='截圖', command=src)
btn2.grid(row=4, column=0)


# 滑鼠座標顯示標籤
getrandom1 = tk.Label(a, text="亂數1：")
getrandom1.grid(row=1, column=0)
getrandom2 = tk.Label(a, text="亂數2：")
getrandom2.grid(row=3, column=0)

record_text_start_button = tk.Button(window, text="記錄操作，目前為：關閉", command=record_text)
record_text_start_button.pack(side=tk.TOP)
textXY = tk.Label(window, text="對輸入框按shift來選定位置")
textXY.pack()
text_start = tk.Button(window, text="執行", command=textstart)
text_start.pack(side=tk.TOP)


b = LabelFrame(window, height=200, width=200, text='腳本')
b.pack(side='top', fill='both', expand=True)
startS = Button(b, text='開始錄製', command=start)
startS.grid(row=0, column=0)
stopS = Button(b, text='結束', command=stop)
stopS.grid(row=0, column=1)
searchs = Button(b, text='搜尋腳本', command=search_script)
searchs.grid(row=1, column=0)
searchs_text = tk.Label(b, text="點擊按鈕搜索")
searchs_text.grid(row=1, column=1)
selects = Button(b, text='選擇腳本', command=select_script)
selects.grid(row=2, column=0)
selects_text = tk.Label(b, text="當前為：")
selects_text.grid(row=2, column=1)
Es = Button(b, text='執行腳本', command=execute_script)
Es.grid(row=2, column=2)
gs = Button(b, text='儲存腳本', command=generate_script)
gs.grid(row=3, column=0)
gs1 = tk.Label(b, text="名稱為：")
gs1.grid(row=3, column=1)
gs_text = tk.Entry(b)
gs_text.grid(row=3, column=2)

c = LabelFrame(window, height=200, width=200, text='偵測腳本-Visual Studio Code')
c.pack(side='top', fill='both', expand=True)
button_texts = ['腳本1', '腳本2', '腳本3']
# # 先清除框架中的所有按鈕
# for button in c.winfo_children():
#     button.destroy()
for text in button_texts:
    button = tk.Button(c, text=text)
    button.pack(side='top')
# 設置鍵盤監聽器
listener = keyboard.Listener(
    on_press=on_press,)
    
listener.start()

# 滑鼠控制器
mouse_controller = MouseController()

# 開始主迴圈
window.mainloop()
