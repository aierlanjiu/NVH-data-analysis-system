import sys
import os
sys.path.append('D:\\NVH data analysis system_modified\\root')

import tkinter as tk
from tkinter import ttk
from datetime import datetime
from PIL import ImageTk, Image
import time
from tkinter import filedialog
import os
from data_management.data_loader import dataloader
import pygame
from pygame import mixer

def update_time(label):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    label.config(text=current_time)
    label.after(1100, update_time, label)
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')




def change_theme(choose):
    themes = {
        "green": [29, "#030b0d", "#05090a", "black"],
        "black": [30, "#05090a", "#0c1616", "black"],
        "blue": [28, "#205bc2", "#85abc2", "#205bc2"],
        "red":[33, "#9a192d", "#ab5970", "black"]
    }
    return themes.get(choose, [29, "#030b0d", "#05090a", "black"])



class MainWindow(ttk.Frame):
    
    def __init__(self, parent, controller,theme):
        super().__init__(parent)
        self.controller = controller
        self.theme = theme
        self.update_theme(theme)
        self.data_loader = dataloader()
    def update_theme(self, new_theme):
        
        self.theme = new_theme

        image_number = self.theme[0]
        bg = self.theme[1]
        bg_t = self.theme[2]
        fg = self.theme[3]

        img_path = "gui\\MicrosoftTeams-image ({image_number}).png".format(image_number=image_number)


        img = Image.open(img_path)
        img = img.resize((600, 500))
        bg_img = ImageTk.PhotoImage(img)
        self.background_label = ttk.Label(self, image=bg_img)
        self.background_label.image = bg_img
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)  # 使用place方法设置图片位置
        self.username_label = ttk.Label(self, text="用户:",font=("Arial", 11),background=bg,foreground="white")
        self.username_label.place(x=20, y=200)
        self.username_combobox = ttk.Combobox(self, values=["NVH user1","NVH user2"],font=("Arial", 11),state="readonly")

        self.username_combobox.current(0) 
        self.username_combobox.place(x=20, y=230)
        self.username = self.username_combobox.get()
        user = self.username_combobox.get()
        self.style = ttk.Style()
        self.style.configure('Large.TButton', font=('Microsoft YaHei', 20), padding=5)
        # 创建各类型数据按钮，并为每个按钮绑定打开新窗口的命令
        self.nvh_button = ttk.Button(self, text="NVH半消声数据", command=lambda: self.open_new_window("NVH"))
        self.eol_button = ttk.Button(self, text="EOL数据", command=lambda: self.open_new_window("EOL"))
        self.vehicle_noise_button = ttk.Button(self, text="整车噪声数据", command=lambda: self.open_new_window("整车噪声"))
        self.efficiency_button = ttk.Button(self, text="效率数据", command=lambda: self.open_new_window("效率"))

        self.nvh_button.place(x=20, y=420)  # 设置按钮位置
        self.eol_button.place(x=180, y=420)
        self.vehicle_noise_button.place(x=340, y=420)
        self.efficiency_button.place(x=500, y=420)

        # 创建当前日期时间标签
        self.current_time_label = ttk.Label(self, text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),font=("Pristina",11),background=bg_t,foreground="white",borderwidth=0)
        self.current_time_label.place(x=20, y=20)  # 设置标签位置
        update_time(self.current_time_label)
        self.engine_label = ttk.Label(self, text="Engnied By Generative Macrolanguage Model",font=("Pristina",11),background=bg_t,foreground="white",borderwidth=0)
        self.engine_label.place(x=360, y=20)  # 设置标签位置
        # 创建项目名称输入框
        self.project_name_hint_label = ttk.Label(self, text="请输入项目名称:",font=("Arial", 11),background=bg,foreground="white",borderwidth=0)
        self.project_name_hint_label.place(x=20, y=280)  # 设置标签位置
        self.project_name_var = tk.StringVar()
        self.project_name_entry = ttk.Entry(self, textvariable=self.project_name_var, style="Custom.TEntry",font=("Arial", 11),background=bg,foreground=fg)
        self.project_name_entry.place(x=20, y=311)  # 设置输入框位置
        

        self.project_name_var.set(f"Hello {user}!")

        self.project_name_varvalue = self.project_name_var.get()





    def open_new_window(self,data_type):
        
        root.withdraw()  # 隐藏母窗口
        new_window = tk.Toplevel(self)
        new_window.title(data_type)
        new_window.geometry("200x124")
        center_window(new_window, 200, 124)
        def update_static_text():
            info_label.config(text="确认以下信息：", font=("Arial", 12),background='yellow')
            new_window.after(1000, update_dynamic_text)

        def update_dynamic_text():
            info_label.config(text="🔥确认以下信息：", font=("Arial", 11))
            new_window.after(1000, update_static_text)



        def play_sound():
            pygame.mixer.init()
            pygame.mixer.music.load("gui//sound.wav")
            pygame.mixer.music.play()

        info_label = ttk.Label(new_window, text="加载数据并确认以下信息：", font=("Arial", 11), borderwidth=0)
        info_label.pack()
        info_label.place(x=220, y=20)


        def close_new_window():
            
            new_window.destroy()
            root.deiconify()  # 重新显示母窗口

        menubar = tk.Menu(new_window)
        new_window.config(menu=menubar) 

        menu1 = tk.Menu(menubar, tearoff=False)
        # 初始调用
        update_static_text()
        update_dynamic_text()
        play_sound()  # 播放音效
        for item in ['💻文件加载','📈目标加载','👈返回']:
            if item == '👈返回':

                menu1.add_separator()
                menu1.add_command(label=item, command=close_new_window)
            elif item == '📈目标加载':
                menu1.add_command(label=item, command=lambda: dataloader.open_file(self.data_loader,data_type))

            else:
                menu1.add_command(label=item, command=lambda: dataloader.load_and_update_data(self.data_loader,new_window,data_type))

        menubar.add_cascade(label='数据📁', menu=menu1)

        new_window.protocol("WM_DELETE_WINDOW", close_new_window)

        new_window.mainloop()

        time.sleep(1) 


def create_main_window(root, app_controller,theme):
    
    return MainWindow(root, app_controller,theme)
class AppController:
    def __init__(self):
        # 在这里初始化一些数据或状态
        pass

    def method_a(self, arg1, arg2):
        # 在这里实现一个方法，该方法接受两个参数，并执行一些操作
        pass

    def method_b(self, arg1):
        # 在这里实现另一个方法，该方法接受一个参数，并执行一些操作
        pass

    # 您可以在这里定义其他方法


if __name__ == "__main__":
    root = tk.Tk()

    root.style = ttk.Style()
    initial_theme = change_theme("green")
    root.style.theme_use("clam")

    
    app_controller = AppController()
    root.geometry("600x500")

    
    menubar = tk.Menu(root)
    root.config(menu=menubar) 
    menu0= tk.Menu(menubar, tearoff=False)
    main_window = create_main_window(root, app_controller,initial_theme)
    
    for item in ['green','black','blue','red','退出']:
        if item == '退出':

            menu0.add_separator()
            menu0.add_command(label=item, command=root.destroy)
        else:
            
            menu0.add_command(label=item, command=lambda item=item: main_window.update_theme(change_theme(item)))

    menubar.add_cascade(label='主题', menu=menu0)
    main_window.pack(fill=tk.BOTH, expand=True)
    center_window(root, 600, 500)  # 设置主窗口位置
    root.title("NVH DATA ANALYSIS SYSTEM")
    root.mainloop()

