import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from matplotlib.font_manager import FontProperties
import sys
import traceback
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, filedialog,ttk
import traceback
def calculate_efficiency(data_path, new_window):
    try:
        sub_directory = "data"
        new_path = os.path.join(data_path, sub_directory)
        current_directory = new_path
        
        def contourplot(data_path,folder_path_raw,thold):
            
            font = FontProperties(fname="C:\\WINDOWS\\FONTS\\SIMSUN.TTC")
            file_path=data_path
            # Verify if the target is valid
            valid_targets = {"01": "电机效率", "02": "系统效率", "03": "控制器效率"}
            for key in valid_targets:

                sheet_name_read = valid_targets[key]
                dfs = pd.read_excel(file_path, sheet_name=sheet_name_read, header=None)
                dfs.columns = dfs.iloc[0]
                dfs = dfs.drop(dfs.index[0])
                dfs = pd.DataFrame(dfs)
                
                for voltage in dfs['voltage'].unique():
                    data=dfs[dfs['voltage']==voltage]

                    speed = data.columns[2:len(data.columns)].values
                    
                    torque = data['转矩'].values
                    
                    efficiency_raw = data.iloc[:, 2:].values
                    
                    df = pd.DataFrame(efficiency_raw)
                    df = df.fillna(efficiency_raw.min())
                    efficiency = df.values
                    # 计算最小间隔
                    min_interval = 1

                    # 将最小间隔作为分割数量
                    num_splits = int((speed.max() - speed.min()) / min_interval)


                    # 使用插值函数来生成新的efficiency值
                    new_speed = np.linspace(speed[0], speed[-1], num_splits)  # 创建新速度点
                    new_efficiency = np.zeros((len(torque), num_splits))

                    for i in range(len(torque)):
                        f = interp1d(speed, efficiency[i, :], kind='linear', fill_value='extrapolate')
                        new_efficiency[i, :] = f(new_speed)
                    y = np.linspace(torque.max(), torque.min(), num=len(torque))
                    # 重新创建Speed和Torque
                    Speed, Torque = np.meshgrid(new_speed, y)
                    
                    # 计算大于85%的数据数量
                    high_efficiency_count = np.sum(new_efficiency > thold)

                    # 计算非空数据的数量
                    total_data_count = np.sum(new_efficiency > 0)

                    # 计算高效区间的百分比
                    high_efficiency_percentage = (high_efficiency_count / total_data_count) * 100

                    figure=plt.figure('contour',facecolor='white')
                    if voltage == 410:
                        plt.title(f"{sheet_name_read} {voltage}V（发电）效率图 {thold:.2f}%高效区间占比: {high_efficiency_percentage:.2f}%", fontsize=12, fontproperties=font)
                    else:
                        plt.title(f"{sheet_name_read} {voltage}V效率图 {thold:.2f}%高效区间占比: {high_efficiency_percentage:.2f}%", fontsize=12, fontproperties=font)
                    
                    


                    plt.xlabel('Speed', fontsize=12)
                    plt.ylabel('Torque', fontsize=12)

                    # 指定等高线的分割值
                    levels = np.linspace(60, 100, 17)  
                    print(levels)
                    # 创建等高线图
                    cntr = plt.contour(Speed, Torque, new_efficiency, levels=levels, colors='black', linewidths=0.2, vmin=50, vmax=100)

                    plt.clabel(cntr, fmt='%.2f', fontsize=8,manual=False) 

                    cntrf = plt.contourf(Speed, Torque, new_efficiency, levels=levels,cmap='hsv_r',alpha=1,vmin=50,vmax=100) 
                    # 获取等高线的等高线值
                    contour_levels = cntr.levels

                    # 找到等于thold的等高线索引
                    highlight_index = np.where(contour_levels == thold)

                    # 标记等于thold的等高线
                    cntr.collections[int(highlight_index[0])].set_linewidth(1) 
                    plt.colorbar()
                    folder_path =f"{folder_path_raw}_{thold:.2f}%"

                    if folder_path_raw == f"":
                        folder_path = f"{datetime.now().strftime('%Y%m%d')}_{thold:.2f}%" # 获取当前日期，格式为'YYYYMMDD'

                    if not os.path.exists(f"{folder_path}"):
                        os.makedirs(f"{folder_path}")

                    if voltage == 410:
                        # 保存图像
                        plt.savefig(f"{folder_path}//{sheet_name_read} {voltage}V（发电）效率图.png", dpi=600)
                    else:
                        plt.savefig(f"{folder_path}//{sheet_name_read} {voltage}V 效率图.png", dpi=600)


                    plt.close()
            print('Done!')






        def run_program(folder_path_raw):
            try:
                
                thold_options = {"80%": 80, "85%": 85, "90%": 90, "95%": 95, "97.5%": 97.5}
                thold_option = thold_var.get()
                thold = thold_options[thold_option]
                contourplot(data_path,folder_path_raw,thold)
                messagebox.showinfo("Done", "效率图绘制完成！")
                root.destroy()
                
            except Exception as e:
                error_message = traceback.format_exc()
                messagebox.showerror("Error", f"An error occurred:\n{error_message}")
                sys.exit(1)






        root = tk.Tk()
        root.title("绘制效率map")
        thold_var = tk.StringVar(root)
        thold_var.set("80%")  # 默认选择80%



        label1 = tk.Label(root, text="效率map存放文件夹名称(默认为当前日期)：")
        label1.grid(row=0, column=1, sticky="n", padx=10, pady=10)

        entry1 = tk.Entry(root)
        entry1.grid(row=1, column=1, sticky="n", padx=10, pady=10)
        entry1.insert(0,data_path)
        label2 = tk.Label(root, text="请选择高效区间阈值：")
        label2.grid(row=2, column=1, sticky="n", padx=10, pady=10)
        options = ["80%","85%","90%","95%","97.5%"]
        thold_combobox = ttk.Combobox(root, textvariable=thold_var, values=options)
        thold_combobox.grid(row=3, column=1, sticky="n", padx=10, pady=10)

        btn = tk.Button(root, text="RUN", command=lambda:run_program(entry1.get()))
        btn.grid(row=4, column=1, sticky="n", padx=10, pady=10)

        root.mainloop()
    except Exception as e:
        print(f"An error occurred during shape deletion: {e}")