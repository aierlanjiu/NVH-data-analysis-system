import os
import pandas as pd
import numpy as np
from tqdm import tqdm
import time
import concurrent.futures
import ast
import re
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


def condition_processing(condition):
    # 分割字符串为多个部分
    runup_rundown = condition.split('/')

    # 初始化变量并设置默认值
    runup_data = "N/A"
    rundown_data = "N/A"
    constant_data = "N/A"

    if len(runup_rundown) == 3:
        try:
            runup_data = runup_rundown[0].split(':')[1]
            rundown_data = runup_rundown[1].split(':')[1]
            constant_data = runup_rundown[2].split(':')[1]
        except IndexError:
            pass


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

    # 转换constant的数据为字典
    constant_values = constant_data.split(',')
    curve_characters_torque_650rpm = {}

    for item in constant_values:
        parts = item.split(' ')
        curve_characters_torque_650rpm[item] = parts[-1]
    
    return curve_characters_torque_runup,curve_characters_torque_rundown,curve_characters_torque_650rpm

def serial_processing(serial):
    # 提取serial的数据并转换为字典格式
    serial_values = serial.split(',')
    curve_characters_serial = {}
    for item in serial_values:
        curve_characters_serial[item]=item
    return curve_characters_serial


def testp_processing(testp):
    # 检查testp中是否存在逗号分隔符
    if ',' in testp:
        testp_values = testp.split(',')
    else:
        # 使用正则表达式匹配键值对
        testp_values = re.findall(r'(\w+):(\w+)', testp)

    curve_characters_testp = {}

    for item in testp_values:
        if isinstance(item, tuple):  # 如果使用正则表达式匹配到了键值对
            key = item[0]
            value = item[1]
        else:  # 如果使用逗号分隔符提取数据
            key = item
            value = re.sub(r'[^\w\s]', '', item).replace("_Shaft", "")
        curve_characters_testp[key] = value

    return curve_characters_testp

# order_characters = {"Overall level":"OA",
#                     "Order 26.00":"26 order primary gear",
#                     "Order 9.62":"9.62 order secondary gear",
#                     "Order 19.24":"19.24 order 2xprimary gear",
#                     "Order 28.86":"28.86 order 3xprimary gear",
#                     "Order 52.00":"52 order 2xsecondary gear",
#                     "Order 78.00":"78 order 3xsecondary gear",
#                     "Order 4.94":"4.94 order input bearing inner ring",
#                     "Order 3.06":"3.06 order input bearing outer ring",
#                     "Order 4.03":"4.03 order input bearing rolling",
#                     "Order 4.59":"4.59 order middle bearing inner ring",
#                     "Order 3.60":"3.6 order middle bearing outer ring",
#                     "Order 2.85":"2.85 order middle bearing rolling",
#                     "Order 1.36":"1.36 order differential bearing inner ring",
#                     "Order 1.07":"1.07 order differential bearing outer ring",
#                     "Order 0.88":"0.88 order differential bearing rolling"}

# curve_characters_torque_runup = {"LOOP1 20Nm":"20Nm",
#                                  "LOOP2 50Nm 1":"50Nm",
#                                  "LOOP4 93Nm":"93Nm", 
#                                  "LOOP5 160Nm":"160Nm", 
#                                  "LOOP7 310Nm":"310Nm"}

# curve_characters_torque_rundown = {"LOOP1 20Nm":"-20Nm",
#                                    "LOOP2 50Nm 1":"-50Nm",
#                                    "LOOP5 160Nm":"-152Nm", 
#                                    "LOOP7 310Nm":"-5Nm"}
# curve_characters_torque_650rpm = {"650rpm 2Nm":"2Nm"}

# curve_characters_testpoint = {"Middle_Shaft:+Z":"MiddleZ",
#                               "Middle_Shaft:-X":"MiddleX",
#                               "Middle_Shaft:-Y":"MiddleY"}

# curve_characters_serial = {
#                            "2310020011":"2310020011",
#                            "2309050023":"2309050023",
#                            "2309060034":"2309060034",
#                            "2309060060":"2309060060",
#                            "2309260052":"2309260052",
#                            "2310020011":"2310020011",
#                            "2310030010":"2310030010",
#                            "2310160001":"2310160001",
#                            "2310170081":"2310170081",
#                            "2310190109":"2310190109",
#                            "2310190114":"2310190114",
#                            "2310220062":"2310220062"                          
#                            }

def eol_processing(file_path, order, condition, testp, serial):
    # 设置要处理的文件名
    file_name = file_path
    order_characters=serial_processing(order)
    curve_characters_torque_runup, curve_characters_torque_rundown,curve_characters_torque_650rpm = condition_processing(condition)
    curve_characters_serial = serial_processing(serial)
    curve_characters_testpoint = testp_processing(testp)
   
    def process_curve(i, df, curve_characters_torque_dict, order_characters, curve_characters_testpoint, curve_characters_serial):
        curve_type = None
        order = None
        torque = None
        testpoint = None
        serial = None
        
        speed_col = df.iloc[:, i]  # 当前曲线的转速列
        vibration_col = df.iloc[:, i + 1]  # 当前曲线的振动幅值列

        def check_vibration_col(vibration_col, text):
            for data in vibration_col:
                if not isinstance(data, (int, float)):
                    if text in str(data):
                        return True
            return False

        order_found = False
        curve_type_found = False
        torque_found = False
        testpoint_found = False
        serial_found = False

        for text in ["Running Up", "Running Down","650rpm"]:
            if check_vibration_col(vibration_col, text):
                curve_type = text
                curve_type_found = True
            
        for key in order_characters:
            if check_vibration_col(vibration_col, key):
                order = order_characters[key]
                order_found = True

        for key in curve_characters_torque_dict[curve_type]:
            if check_vibration_col(vibration_col, key):
                torque = curve_characters_torque_dict[curve_type][key]
                torque_found = True
            
        for key in curve_characters_testpoint:
            if check_vibration_col(vibration_col, key):
                testpoint = curve_characters_testpoint[key]
                testpoint_found = True

        for key in curve_characters_serial:
            if check_vibration_col(vibration_col, key):
                serial = curve_characters_serial[key]
                serial_found = True


        if order_found and curve_type_found and torque_found and testpoint_found and serial_found:
            # 转换为纯数字类型的数据
            
            speed_col = pd.to_numeric(speed_col, errors='coerce')
            vibration_col = pd.to_numeric(vibration_col, errors='coerce')
            
            a_data_list = []

            for j in range(len(speed_col)):
                speed = speed_col[j]
                slope = curve_type
                vibration = vibration_col[j]
                new_data = {
                    "order": order,
                    "slope": slope,
                    "Test Point": testpoint,
                    "Torque": torque,
                    "Serial": serial,
                    "Speed": speed,
                    "vibration": vibration,
                    
                }
                a_data_list.append(new_data)
                
            return a_data_list


    def process_excel_file(file_path: str):
        # 读取Excel数据
        sheets = pd.read_excel(file_path, sheet_name=None)
        df = pd.concat([pd.read_excel(file_path, sheet_name=sheet) for sheet in sheets.keys()], axis=1)
        
        a_data_list = []
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            
            curve_characters_torque_dict = {
                "Running Up": curve_characters_torque_runup,
                "Running Down": curve_characters_torque_rundown,
                "650rpm": curve_characters_torque_650rpm,
                
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

    all_data = df.sort_values(by=["order", "slope","Serial", "Test Point", "Torque", "Speed"])

    all_data = all_data.dropna()
    merged_data = all_data.drop_duplicates()
    merged_data.to_csv(os.path.join('', f"{os.path.splitext(file_name)[0]}_done.csv"), index=False)


    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    messagebox.showinfo("提示", "NVH_processing运行已完成")


    root.destroy()  # 销毁主窗口