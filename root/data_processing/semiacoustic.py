import os
import pandas as pd
import numpy as np
from tqdm import tqdm
import time
import concurrent.futures
import re
import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import ast

def order_processing(order):
    order_list = order.replace('order', ' order').split(',')
    order_characters = {}
    for item in order_list:
        value, key = item.strip().split()
        value1 = '{:.2f}'.format(float(value))
        # 保留两位小数
        order_characters["Order " + value1] = value + key
    return order_characters

def condition_processing(condition):
    # 分割字符串为run up和run down两部分
    runup_rundown = condition.split('/')

    # 提取run up和run down的数据
    runup_data = ""
    rundown_data = ""
    if len(runup_rundown) == 2:
        try:
            runup_data = runup_rundown[0].split(':')[1]
            rundown_data = runup_rundown[1].split(':')[1]
        except IndexError:
            pass
    elif len(runup_rundown) == 1:
        if "run up:" in runup_rundown[0]:
            runup_data = runup_rundown[0].split(':')[1]
        elif "run down:" in runup_rundown[0]:
            rundown_data = runup_rundown[0].split(':')[1]

    # 转换run up的数据为字典
    runup_values = runup_data.split(',')
    curve_characters_torque_runup = {}

    for item in runup_values:
        parts = item.split(' ')
        curve_characters_torque_runup[item] = parts[-1]

    # 转换run down的数据为字典
    rundown_values = rundown_data.split(',')
    curve_characters_torque_rundown = {}

    for item in rundown_values:
        parts = item.split(' ')
        curve_characters_torque_rundown[item] = parts[-1]
    return curve_characters_torque_runup, curve_characters_torque_rundown

def serial_processing(serial):
    # 提取serial的数据并转换为字典格式
    serial_values = serial.split(',')
    curve_characters_serial = {}
    for item in serial_values:
        curve_characters_serial[item]=item
    return curve_characters_serial
def testp_processing(testp):
    # 提取testp的数据并转换为字典格式
    testp_values = testp.split(',')
    curve_characters_testp = {}
    for item in testp_values:
        curve_characters_testp[item]=item
    return curve_characters_testp



def NVH_processing(file_path, order, condition, testp, serial):

    order_characters=order_processing(order)
    curve_characters_torque_runup, curve_characters_torque_rundown = condition_processing(condition)
    curve_characters_serial = serial_processing(serial)
    # curve_characters_testpoint = testp_processing(testp)
    curve_characters_testpoint = ast.literal_eval(testp)
    # order_characters = {"Order 26.00":"26order","Order 9.62":"9.62order"}
    # curve_characters_torque_runup = {"200-7000-200rpm 0Nm":"0Nm",
    #                                 "200-7000rpm 0Nm":"0Nm",
    #                                 "200-7000rpm 15Nm":"15Nm",
    #                                 "200-7000rpm 31Nm":"31Nm", 
    #                                 "200-9800rpm 93Nm":"93Nm", 
    #                                 "200-7000rpm 62Nm":"62Nm", 
    #                                 "200-9800rpm 100Nm":"100Nm", 
    #                                 "200-9000rpm 155Nm":"155Nm", 
    #                                 "200-6750rpm 200Nm":"200Nm",
    #                                 "200-6750rpm 217Nm":"217Nm",
    #                                 "200-6000rpm 250Nm":"250Nm",
    #                                 "200-4500rpm 310Nm":"310Nm"}
    # curve_characters_torque_rundown = {"200-7000-200rpm 0Nm":"0Nm",
    #                                 "9000-200rpm -137Nm":"-137Nm",
    #                                 "9800-200rpm -137Nm":"-137Nm",
    #                                 "7000-200rpm 0Nm":"0Nm",
    #                                 "7000-200rpm -15Nm":"-15Nm", 
    #                                 "7000-200rpm -31Nm":"-31Nm", 
    #                                 "7000-200rpm -62Nm":"-62Nm",
    #                                 "9800-200rpm -93Nm":"-93Nm", 
    #                                 "9800-200rpm -100Nm":"-100Nm", 
    #                                 "9000-200rpm -155Nm":"-155Nm", 
    #                                 "6750-200rpm -200Nm":"-200Nm",
    #                                 "6750-200rpm -217Nm":"-217Nm",
    #                                 "6000-200rpm -250Nm":"-250Nm",
    #                                 "4500-200rpm -310Nm":"-310Nm",
    #                                 "9000-200rpm -200Nm":"-200Nm"}
    # curve_characters_testpoint = {"上_50cm":"Top 50cm",
    #                             "左_50cm":"Left 50cm",
    #                             "右_50cm":"Right 50cm",
    #                             "前_50cm":"Front 50cm",
    #                             "后_50cm":"Rear 50cm",
    #                             "Mic_avg":"mic_avg",
    #                             "Poweravg mic":"mic_avg",
    #                             "上50cm":"Top 50cm",
    #                             "左50cm":"Left 50cm",
    #                             "右50cm":"Right 50cm",
    #                             "前50cm":"Front 50cm",
    #                             "后50cm":"Rear 50cm"}

    # curve_characters_serial = {"PC027":"PC027",
    #                         "PC004":"PC004",
    #                         "PC006":"PC006",
    #                         "SC026":"SC026"}



    # 设置要处理的文件名
    file_name = file_path

    def process_curve(i, df, curve_characters_torque_dict, order_characters, curve_characters_testpoint, curve_characters_serial):
        curve_type = None
        order = None
        torque = None
        testpoint = None
        serial = None
        
        speed_col = df.iloc[:, i]  # 当前曲线的转速列
        noise_col = df.iloc[:, i + 1]  # 当前曲线的振动幅值列

        def check_noise_col(noise_col, text):
            for data in noise_col:
                if not isinstance(data, (int, float)):
                    if text in str(data):
                        return True
            return False

        order_found = False
        curve_type_found = False
        torque_found = False
        testpoint_found = False
        serial_found = False

        for text in ["Running Up", "Running Down"]:
            if check_noise_col(noise_col, text):
                curve_type = text
                curve_type_found = True
            
        for key in order_characters:
            if check_noise_col(noise_col, key):
                order = order_characters[key]
                order_found = True

        for key in curve_characters_torque_dict[curve_type]:
            if check_noise_col(noise_col, key):
                torque = curve_characters_torque_dict[curve_type][key]
                torque_found = True
            
        for key in curve_characters_testpoint:
            if check_noise_col(noise_col, key):
                testpoint = curve_characters_testpoint[key]
                testpoint_found = True

        for key in curve_characters_serial:
            if check_noise_col(noise_col, key):
                serial = curve_characters_serial[key]
                serial_found = True

        if order_found and curve_type_found and torque_found and testpoint_found and serial_found:
            # 转换为纯数字类型的数据
            speed_col = pd.to_numeric(speed_col, errors='coerce')
            noise_col = pd.to_numeric(noise_col, errors='coerce')
            
            a_data_list = []

            for j in range(len(speed_col)):
                speed = speed_col[j]
                slope = curve_type
                noise = noise_col[j]
                new_data = {
                    "order": order,
                    "slope": slope,
                    "Test Point": testpoint,
                    "Torque": torque,
                    "Serial": serial,
                    "Input Speed": speed,
                    "noise": noise
                }
                a_data_list.append(new_data)
                
            return a_data_list


    def process_excel_file(file_path: str):
        # 读取Excel数据
        try:
            df = pd.read_csv(file_path,low_memory=False)
            
            sheets = pd.read_excel(file_path, sheet_name=None)
            df = pd.concat([pd.read_excel(file_path, sheet_name=sheet) for sheet in sheets.keys()], axis=1)
        
        except Exception as e:
            pass

        
        a_data_list = []
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            
            curve_characters_torque_dict = {
                "Running Up": curve_characters_torque_runup,
                "Running Down": curve_characters_torque_rundown,
                
            }
            
            for i in tqdm(range(0, len(df.columns), 2)):
                future = executor.submit(process_curve, i, df, curve_characters_torque_dict, order_characters, curve_characters_testpoint, curve_characters_serial)
                futures.append(future)
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    a_data_list.extend(result)
        
        curve_data = pd.DataFrame(a_data_list)
        return curve_data

            
    df = process_excel_file(file_name)



    all_data = df.sort_values(by=["order", "slope","Serial", "Test Point", "Torque", "Input Speed"])
    all_data["noise"] = all_data["noise"].astype(float)
    all_data['Average Noise'] = all_data.groupby(["order", "slope","Serial", "Test Point", "Torque", "Input Speed"])['noise'].transform('mean')
    #all_data.to_csv(os.path.join('', f"{os.path.splitext(file_name)[0]}_raw.csv"), index=False, encoding='utf-8')
    all_data = all_data.drop('noise', axis=1)
    all_data = all_data.dropna()
    merged_data = all_data.drop_duplicates()
    merged_data.to_csv(os.path.join('', f"{os.path.splitext(file_name)[0]}_done.csv"), index=False)


    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    messagebox.showinfo("提示", "NVH_processing运行已完成")


    root.destroy()  # 销毁主窗口