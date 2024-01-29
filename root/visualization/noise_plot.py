
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from tqdm import tqdm
import numpy as np
import re
from scipy.interpolate import interp1d
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random
import colorsys
import matplotlib.colors as mcolors
def noise_plot(data_path,target_file,serial_num):
    # 创建一个用于保存输出语句的文件
    output_file = 'data\\Project\\ProcessedData\\result.txt'

    # 将标准输出重定向到文件
    sys.stdout = open(output_file, 'w')

    target_file=pd.read_excel(target_file)
    # 设置要处理的文件名
    raw_file = os.path.join('', f"{os.path.splitext(data_path)[0]}_done.csv")

    raw_data = pd.read_csv(raw_file,low_memory=False)

    df = pd.concat([target_file, raw_data])
    # df = raw_data

        
    serial_values = serial_num.split(',')


    grouped_by_torque = df.groupby("Torque")
    def generate_color():
        hue = random.randint(0, 360)  # 随机选择一个色相
        saturation = random.randint(50, 100)  # 设置饱和度在50-100之间
        lightness = random.randint(50, 80)  # 设置亮度在50-80之间
        r, g, b = colorsys.hls_to_rgb(hue / 360, lightness / 100, saturation / 100)
        color = (r, g, b)
        return mcolors.to_hex(color)

    color_palette = {}
    target_colors = ['black', 'gray']         
    for index, key in enumerate(df["Serial"].unique()):
        if 'target' in key:
            color_palette[key] = target_colors.pop(0)
        else:
            color_palette[key] = generate_color()

    print(color_palette)
    for torque, data in tqdm(grouped_by_torque):


        for slope in data["slope"].unique():


                
            slope_data = data[data["slope"] == slope]
            
            slope_data_single = slope_data.loc[~slope_data['Test Point'].str.contains('avg')].copy()
            slope_data_avg = slope_data.loc[slope_data['Test Point'].str.contains('avg')].copy()
            #color_palette = {'PC027': 'steelblue', 'PC004': 'deepskyblue', 'PC006': 'dodgerblue','T012': 'orange', 'T013': 'darkorange', 'SC026': 'red'}
           
            
            


            for order_s in slope_data_single["order"].unique():
                # 确定布局
                fig = plt.figure(figsize=(9, 9))
                
                order_data_s = slope_data_single[slope_data_single["order"] == order_s]
                num_test_points = len(order_data_s["Test Point"].unique())
                num_cols = min(2, num_test_points)  # 最多2列
                num_rows = (num_test_points + 1) // 2  # 根据测试点数量计算行数
                grid = plt.GridSpec(num_rows, num_cols)

                # 遍历每个测试点
                for index, testpoint_single in enumerate(order_data_s["Test Point"].unique()):
                    row = index // num_cols  # 行索引
                    col = index % num_cols   # 列索引

                    # 创建子图
                    ax = fig.add_subplot(grid[row, col])

     
                    # 根据当前测试点筛选数据
                    testpoint_data_single = order_data_s [order_data_s["Test Point"] == testpoint_single]
                    testpoint_clean_single = re.sub(r'[^\w\s]', '', testpoint_single)

                
                    
                    sns.lineplot(data=testpoint_data_single , x=testpoint_data_single["Input Speed"], y=testpoint_data_single["Average Noise"],
                                hue="Serial", palette=color_palette, ax=ax)
                    
                    ax.set_title(f"{order_s} {slope} for {torque} at {testpoint_clean_single}", fontdict={'fontsize': 12})
                    ax.set_xlabel("Input Speed", fontdict={'fontsize': 8})
                    ax.set_ylabel(f"{testpoint_clean_single} dB[A]", fontdict={'fontsize': 8})
                    ax.set_xlim(0, max(testpoint_data_single["Input Speed"]) + 1)
                    ax.set_xticks(np.arange(0, max(testpoint_data_single["Input Speed"]) + 1, 1000))
                    ax.set_ylim(0, 100)
                    ax.set_yticks(np.arange(0, 100, 10))
                    ax.grid(alpha=0.5)
                    ax.tick_params(labelsize=10)

                # 调整子图之间的间距
                plt.subplots_adjust(hspace=0.4)

                plt.tight_layout()
                plt.savefig(os.path.join('data\\Project\\ProcessedData\\Semi Acoustic Data\\single', f"{order_s} {slope} for {torque}.png"), dpi=500)
                plt.close()

            
            # 创建大图和子图
            fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(9, 9))
            axs = axs.reshape(-1)
            testpoint_data = slope_data_avg
            testpoint = testpoint_data["Test Point"].unique()[0]
            testpoint_clean = re.sub(r'[^\w\s]','',testpoint)
            for i, order in enumerate(slope_data_avg["order"].unique()):
                order_data = testpoint_data[testpoint_data["order"] == order]
                sns.lineplot(data=order_data, x=order_data["Input Speed"], y=order_data["Average Noise"], hue="Serial", palette=color_palette, ax=axs[i])
                min_max_speed = order_data.groupby("Serial")["Input Speed"].max().min() + 1
                axs[i].set_title(f"{order} {slope} for {torque} at {testpoint_clean}", fontdict={'fontsize': 12})
                axs[i].set_xlabel("Input Speed", fontdict={'fontsize': 8})
                axs[i].set_ylabel(f"{testpoint_clean} dB[A]", fontdict={'fontsize': 8})
                axs[i].set_xlim(0, min_max_speed)
                axs[i].set_xticks(np.arange(0, min_max_speed, 1000))
                axs[i].set_ylim(0, 100)
                axs[i].set_yticks(np.arange(0, 100, 10))
                axs[i].grid(alpha=0.5)
                axs[i].tick_params(labelsize=10)

                target_Punch = order_data[order_data["Serial"] == "target_raw"].reset_index()
                
                interpolation_func = interp1d(target_Punch["Input Speed"],target_Punch["Average Noise"])

                for serial in serial_values:
                    
                    serial_data = order_data[order_data["Serial"] == serial]

                    y_values = interpolation_func(serial_data["Input Speed"])

                    # 比较serial_data["noise"]和y_values，找到大于的转速区间
                    intervals = []
                    start_value = None
                    end_value = None
                    for i in range(len(serial_data)):
                        if start_value is None:
                            if serial_data["Average Noise"].iloc[i] > y_values[i]:
                                start_value = i
                        else:
                            if serial_data["Average Noise"].iloc[i] <= y_values[i]:
                                intervals.append((start_value, i-1))
                                start_value = None
                    if start_value is not None:
                        intervals.append((start_value, len(serial_data)-1))


                    if len(intervals)>0:
                        text1 = f"{serial} {order} {slope} for {torque} at {testpoint_clean} speed:"
                        # 输出每个转速区间的初始值和终止值
                        text2_list = []  # 创建一个空列表
                        for interval in intervals:
                            start_index = interval[0]
                            end_index = interval[1]
                            start_value = serial_data["Input Speed"].iloc[start_index]
                            end_value = serial_data["Input Speed"].iloc[end_index]
                            text2 = f"[{start_value}, {end_value}]"
                            text2_list.append(text2)  # 将每个text2添加到列表中

                        combined_text2 = ", ".join(text2_list)  # 使用逗号连接列表中的各个元素
                        text3 = f"exceed target"
                        
                        print(f"{text1}' '{combined_text2}' '{text3}")


                    else:
                        text4 = f"{serial} {order} {slope} for {torque} at {testpoint_clean} is fullfill target"
                        print(f"{text4}")

            plt.tight_layout()
            plt.savefig(os.path.join('data\\Project\\ProcessedData\\Semi Acoustic Data\\avg', f"{slope} for {torque} at {testpoint_clean}.png"), dpi=500)
            plt.close()
    # 恢复标准输出
    sys.stdout.close()
    sys.stdout = sys.__stdout__
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    messagebox.showinfo("提示", "图像已绘制完成")


    root.destroy()  # 销毁主窗口