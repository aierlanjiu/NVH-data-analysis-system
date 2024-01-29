import tkinter as tk
import sys
import os
# sys.path.append('D:\\NVH data analysis system\\root')
sys.path.append(os.path.dirname(__file__))
from data_processing.semiacoustic import NVH_processing
from data_processing.eol_data import eol_processing
from tkinter import ttk
from datetime import datetime
from PIL import ImageTk, Image
import time
from tkinter import filedialog
import os
from tkinter import scrolledtext
from visualization.noise_plot import noise_plot
from data_processing.efficiency_data import calculate_efficiency
from reports.report_generation import generate_report
from reports.report_generation_eol import generate_reporteol
from visualization.eol_plot import eol_plot
from config import Config
from data_processing.fitting_curve import eol_target
from data_processing.noise import noise
import subprocess

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
class dataloader:
    projectPath = os.path.dirname(os.path.abspath(__file__))
    configFile = os.path.join(projectPath,"config.ini")
    print(configFile)
    def __init__(self,profilePath=None):
        
        self.config = Config(self.configFile)


    def open_file(self,data_type):
        if data_type == 'NVH':
            filename = filedialog.askopenfilename(initialdir=self.config.get("NVH","target_path"))
            if filename:
                os.startfile(filename)
        elif data_type == 'EOL':
            filename = filedialog.askopenfilename(initialdir=self.config.get("eol","target_path"))
            if filename:
                os.startfile(filename)
        else:
            print("None Target Load")


    def run_noise(self,data_path):
        subprocess.Popen(["python", "data_processing\\noise.py", "data_path"])
    def ppt_file(self):
        
        ppt_path = filedialog.askopenfilename(initialdir=self.config.get("ppt","template_path"))
        return ppt_path

    def load_data(self,data_type):
        if data_type == "NVH":

            file_path = filedialog.askopenfilename(initialdir=self.config.get("NVH","data_path"))
            
        elif data_type == "EOL":

            file_path = filedialog.askopenfilename(initialdir=self.config.get("eol","data_path"))

        elif data_type == "整车噪声":

            file_path = filedialog.askopenfilename(initialdir=self.config.get("vehicle noise","data_path"))

        elif data_type == "效率":

            file_path = filedialog.askopenfilename(initialdir=self.config.get("efficiency","data_path"))

        print("选择的文件路径:", file_path)
        
        return file_path

    def load_and_update_data(self,new_window, data_type):
        file_path = self.load_data(data_type)
        
        # 在这里添加处理文件的逻辑，例如读取文件内容或执行其他操作
        print("选择的文件路径:", file_path)
        # 进行后续操作，比如更新界面显示等
        data_path = file_path
        if data_type == "NVH":
            new_window.geometry("600x800")
            center_window(new_window, 600, 600)
            img_nvh = Image.open('gui\\MicrosoftTeams-image (44).png')
            img_nvh = img_nvh.resize((600, 600))
            bg_img_nvh = ImageTk.PhotoImage(img_nvh)
            background_label = ttk.Label(new_window, image=bg_img_nvh)
            background_label.image = bg_img_nvh
            background_label.place(x=0, y=0, relwidth=1, relheight=1)  # 使用place方法设置图片位置
            target_path =self.config.get("NVH","target_path")
            pic_path = self.config.get("NVH","pic_path")
            self.nvh_data_input(data_path,target_path,pic_path,new_window)

        elif data_type == "EOL":
            new_window.geometry("600x700")
            center_window(new_window, 600, 700)
            img_eol = Image.open('gui\\MicrosoftTeams-image (45).png')
            img_eol = img_eol.resize((600, 700))
            bg_img_eol = ImageTk.PhotoImage(img_eol)
            background_label = ttk.Label(new_window, image=bg_img_eol)
            background_label.image = bg_img_eol
            background_label.place(x=0, y=0, relwidth=1, relheight=1)  # 使用place方法设置图片位置
            target_path =self.config.get("eol","target_path")
            target_path_poly =self.config.get("eol","target_path_poly")
            pic_path = self.config.get("eol","pic_path")
            self.EOL_data_input(data_path,target_path,target_path_poly,pic_path,new_window)

        elif data_type == "整车噪声":
            new_window.geometry("400x400")
            center_window(new_window, 400, 400)
            img_vehicle = Image.open('gui\\b9009fa4-1795-4429-9be2-819f2ee32ca7.jpg')
            img_vehicle = img_vehicle.resize((400, 400))
            bg_img_vehicle = ImageTk.PhotoImage(img_vehicle)
            background_label = ttk.Label(new_window, image=bg_img_vehicle)
            background_label.image = bg_img_vehicle
            background_label.place(x=0, y=0, relwidth=1, relheight=1)  # 使用place方法设置图片位置
            # 设置计算按钮
            calculate_button = ttk.Button(new_window, text="计算",command=lambda:self.run_noise(data_path))
            calculate_button.pack()
            calculate_button.place(x=270, y=190)

        elif data_type == "效率":
            new_window.geometry("600x400")
            center_window(new_window, 600, 400)
            img_efficiency = Image.open('gui\\MicrosoftTeams-image (43).png')
            img_efficiency = img_efficiency.resize((600, 400))
            bg_img_efficiency = ImageTk.PhotoImage(img_efficiency)
            background_label = ttk.Label(new_window, image=bg_img_efficiency)
            background_label.image = bg_img_efficiency
            background_label.place(x=0, y=0, relwidth=1, relheight=1)  # 使用place方法设置图片位置
            # 设置计算按钮
            calculate_button = ttk.Button(new_window, text="计算",command=lambda:calculate_efficiency(data_path, new_window))
            calculate_button.pack()
            calculate_button.place(x=270, y=190)
    def nvh_data_input(self,data_path,target_path,pic_path,new_window):
        
        data_label = ttk.Label(new_window, text=f"数据：{data_path}", font=("Arial", 11), borderwidth=0, wraplength=300)
        data_label.pack()
        data_label.place(x=20, y=50)
        # NVH测试样件序列号输入
        serial_label = ttk.Label(new_window, text=f"样机编号：",font=("Arial", 11),borderwidth=0)
        
        serial_label.pack()
        serial_label.place(x=320, y=50)
        sample_entry = ttk.Entry(new_window)
        sample_entry.insert(0,self.config.get("NVH","serial"))
        sample_entry.pack()
        sample_entry.place(x=320, y=80)
        
        # NVH测试工况输入
        condition_label = ttk.Label(new_window, text=f"测试工况：",font=("Arial", 11),borderwidth=0)
        condition_label.pack()
        condition_label.place(x=20, y=150)
        condition_entry = scrolledtext.ScrolledText(new_window, wrap=tk.WORD, width=30, height=10)
        condition_entry.pack()
        condition_entry.insert(tk.INSERT,self.config.get("NVH","condition"))
        condition_entry.place(x=20, y=190)
        
        # NVH分析阶次输入
        order_label = ttk.Label(new_window, text=f"分析阶次：",font=("Arial", 11),borderwidth=0)
        order_label.pack()
        order_label.place(x=320, y=150)
        analysis_entry = scrolledtext.ScrolledText(new_window, wrap=tk.WORD, width=30, height=10)
        analysis_entry.pack()
        analysis_entry.insert(tk.INSERT,self.config.get("NVH","order"))
        analysis_entry.place(x=320, y=190)
        
        
        #测点输入
        testp_label = ttk.Label(new_window, text=f"测点位置：",font=("Arial", 11),borderwidth=0)
        testp_label.pack()
        testp_label.place(x=20, y=400)
        testp_entry = scrolledtext.ScrolledText(new_window, wrap=tk.WORD, width=30, height=10)
        testp_entry.pack()
        testp_entry.insert(tk.INSERT,self.config.get("NVH","testp"))
        testp_entry.place(x=20, y=430)
    
        # NVH数据预处理按钮
        def info_update():
            serial=sample_entry.get().strip()
            testp = testp_entry.get("1.0", "end").strip()
            order = analysis_entry.get("1.0", "end").strip()
            condition=condition_entry.get("1.0", "end").strip()
            return order,condition,testp,serial
        
        
        preprocess_button = ttk.Button(new_window, text="NVH数据预处理",command=lambda:NVH_processing(data_path, info_update()[0], info_update()[1], info_update()[2], info_update()[3]))
        preprocess_button.pack()
        preprocess_button.place(x=320, y=430)
        visulation_button = ttk.Button(new_window, text="数据绘图",command=lambda:noise_plot(data_path,target_path,info_update()[3]))
        visulation_button.pack()
        visulation_button.place(x=320, y=480)
        report_button = ttk.Button(new_window, text="生成报告",command=lambda:generate_report(pic_path,self.ppt_file()))
        report_button.pack()
        report_button.place(x=320, y=530)
        

    def EOL_data_input(self,data_path,target_path,target_path_poly,pic_path,new_window):
        data_label = ttk.Label(new_window, text=f"数据：{data_path}", font=("Arial", 11), borderwidth=0, wraplength=300)
        data_label.pack()
        data_label.place(x=20, y=50)
        # NVH测试样件序列号输入
        serial_label = ttk.Label(new_window, text=f"样机编号：",font=("Arial", 11),borderwidth=0)
        
        serial_label.pack()
        serial_label.place(x=320, y=10)
        sample_entry = scrolledtext.ScrolledText(new_window, wrap=tk.WORD, width=30, height=6)
        sample_entry.insert(tk.INSERT,self.config.get('eol','serial'))
        sample_entry.pack()
        sample_entry.place(x=320, y=40)
        
        # NVH测试工况输入
        condition_label = ttk.Label(new_window, text=f"测试工况：",font=("Arial", 11),borderwidth=0)
        condition_label.pack()
        condition_label.place(x=20, y=160)
        condition_entry = scrolledtext.ScrolledText(new_window, wrap=tk.WORD, width=30, height=10)
        condition_entry.pack()
        condition_entry.insert(tk.INSERT,self.config.get('eol','condition'))
        condition_entry.place(x=20, y=190)

        # NVH分析阶次输入
        order_label = ttk.Label(new_window, text=f"分析阶次：",font=("Arial", 11),borderwidth=0)
        order_label.pack()
        order_label.place(x=320, y=160)
        analysis_entry = scrolledtext.ScrolledText(new_window, wrap=tk.WORD, width=30, height=10)
        analysis_entry.pack()
        analysis_entry.insert(tk.INSERT, self.config.get('eol','gear_order')+','+self.config.get('eol','gear_multiple_order')+','+self.config.get('eol','input_bearing_order')+','+self.config.get('eol','middle_bearing_order')+','+self.config.get('eol','differential_bearing_order'))
        analysis_entry.place(x=320, y=190)
        
        #阶次详细信息
        order_info = ttk.Label(new_window, text=f"阶次详细信息：",font=("Arial", 11),borderwidth=0)
        order_info.pack()
        order_info.place(x=320, y=400)
        order_info_entry = scrolledtext.ScrolledText(new_window, wrap=tk.WORD, width=30, height=10)
        order_info_entry.pack()
        order_info_entry.insert(tk.INSERT,self.config.get('eol','order_info'))
        order_info_entry.place(x=320, y=430)
        
        #测点输入
        testp_label = ttk.Label(new_window, text=f"测点位置：",font=("Arial", 11),borderwidth=0)
        testp_label.pack()
        testp_label.place(x=20, y=400)
        testp_entry = scrolledtext.ScrolledText(new_window, wrap=tk.WORD, width=30, height=10)
        testp_entry.pack()
        testp_entry.insert(tk.INSERT,'Middle_Shaft:+Z,Middle_Shaft:-Y,Middle_Shaft:-X')
        testp_entry.place(x=20, y=430)
        
        # NVH数据预处理按钮
        def info_update():
            serial = sample_entry.get("1.0","end").strip()
            testp = testp_entry.get("1.0","end").strip()
            order = analysis_entry.get("1.0","end").strip()
            condition = condition_entry.get("1.0","end").strip()
            order_info = order_info_entry.get("1.0","end").strip()
            return order,condition,testp,serial,order_info
        
        def m_order_get():
            
            gear_order=self.config.get('eol','gear_order')
            gear_multiple_order=self.config.get('eol','gear_multiple_order')
            input_bearing_order=self.config.get('eol','input_bearing_order')
            middle_bearing_order=self.config.get('eol','middle_bearing_order')
            differential_bearing_order=self.config.get('eol','differential_bearing_order')
            return gear_order,gear_multiple_order,input_bearing_order,middle_bearing_order,differential_bearing_order
        mode =self.config.get('eol','mode')
        preprocess_button = ttk.Button(new_window, text="NVH数据预处理",command=lambda:eol_processing(data_path, info_update()[0], info_update()[1], info_update()[2], info_update()[3]))
        preprocess_button.pack()
        preprocess_button.place(x=50, y=650)
        visulation_button = ttk.Button(new_window, text="数据绘图",command=lambda:eol_plot(data_path,target_path,target_path_poly,info_update()[4],m_order_get()[0:5],mode))
        visulation_button.pack()
        visulation_button.place(x=200, y=650)

        target_button = ttk.Button(new_window, text="目标拟合",command=lambda:eol_target(data_path,target_path))
        target_button.pack()
        target_button.place(x=350, y=650)

        report_button = ttk.Button(new_window, text="生成报告",command=lambda:generate_reporteol(pic_path,self.ppt_file()))
        report_button.pack()
        report_button.place(x=500, y=650)
        


