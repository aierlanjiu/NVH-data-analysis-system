# 导入必要的库
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from tqdm import tqdm
import ast
from openpyxl import Workbook
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
def eol_plot(data_path,target_path,target_path_poly,order_info,m_order,mode):

    order_characters=ast.literal_eval(order_info)
    
    gear_order=m_order[0].split(",")
    gear_multiple_order=m_order[1].split(",")
    input_bearing_order=m_order[2].split(",")
    middle_bearing_order=m_order[3].split(",")
    differential_bearing_order=m_order[4].split(",")
    order_dict = {"gear":gear_order,
                "gear multiple":gear_multiple_order,
                "input bearing":input_bearing_order,
                "middle bearing":middle_bearing_order,
                "differential bearing":differential_bearing_order}
    print(order_dict)
    print(order_characters)
    raw_file = os.path.join('', f"{os.path.splitext(data_path)[0]}_done.csv")
    df = pd.read_csv(raw_file,low_memory=False)

    if mode == "2":
        target_file = target_path
    elif mode == "1":
        target_file = target_path_poly

    for slope in df["slope"].unique():
        slope_data = df[df["slope"] == slope]
        
        for testpoint in slope_data["Test Point"].unique():
        # for testpoint in ['MiddleY']:
            testpoint_data = slope_data[slope_data["Test Point"] == testpoint]
            
            for torque in testpoint_data["Torque"].unique():
                torque_data = testpoint_data[testpoint_data["Torque"] == torque]
                for key in order_dict.keys():
                    if key == "gear multiple":
                        nrows = 2
                    else:
                        nrows = 1
                    fig, axs = plt.subplots(nrows, ncols=len(order_dict[key])//nrows, figsize=(16, 9))
                    axs = axs.reshape(-1)

                    for i,order in enumerate(order_dict[key]):
                        
                        
                        order_data = torque_data[torque_data["order"]==order]
                        print(order)
                        filename = ' '+slope +' '+ torque + order + testpoint
                        
                        try:
                            target = pd.read_excel(target_file, sheet_name=f'{slope}{torque}{testpoint}{order}')
                            
                            sns.lineplot(data=target, x=target.iloc[:, 0], y=target.iloc[:, 2], ax=axs[i],color = 'black',label = 'target',linewidth=2)
                        
                        except:
                            pass

                        
                        sns.lineplot(data=order_data, x=order_data["Speed"], y=order_data["vibration"], hue=order_data["Serial"], palette="Set1",linewidth=0.8, ax=axs[i])

                        print(order_characters[order])
                        
                        axs[i].set_title(f"{order_characters[order]} ", fontdict={'fontsize': 10})
                        axs[i].set_title(f"{order}", fontdict={'fontsize': 10})
                        axs[i].set_xlabel("Speed", fontdict={'fontsize': 8})
                        axs[i].set_ylabel(f"{order} dB[g]", fontdict={'fontsize': 8})
                        #axs[i].set_xlim(0, max(order_data["Speed"])+1)
                        #axs[i].set_xticks(np.arange(0, max(order_data["Speed"])+1, 1000))
                        if torque == "2Nm":
                            axs[i].set_ylim(60, 150)
                            axs[i].set_yticks(np.arange(60, 150, 10))
                        axs[i].grid(alpha=0.5)
                        axs[i].tick_params(labelsize=8)
                        axs[i].legend(loc='upper left', bbox_to_anchor=(1, 1))
                    fig.suptitle(f"{slope} {torque} {key} order {testpoint} ",fontsize=12)
                    plt.tight_layout()
                    plt.savefig(os.path.join('data\\Project\\ProcessedData\\EOL Data\\EOL plot', f"{slope} {torque} {key} order {testpoint}.jpg"), dpi=400)
                    plt.close()







    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    messagebox.showinfo("提示", "图像已绘制完成")


    root.destroy()  # 销毁主窗口

