# 导入必要的库
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from tqdm import tqdm
from scipy.stats import norm
import re
from scipy.interpolate import UnivariateSpline
from sklearn.model_selection import KFold
from openpyxl import Workbook
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def eol_target(data_path,target_path):
    #读取文件夹内所有xlsx文件，并生成一个新的xlsx保存目标线
    folder_path = os.path.dirname(data_path)
    xlsx_files = [f for f in os.listdir(folder_path) if f.endswith('_done.csv')]
    workbook = Workbook()
    worksheet = workbook.active
    workbook.save(target_path)

    for filename in tqdm(xlsx_files):
        if filename.endswith(".csv"):

            file_path = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}.csv")
            
            #对数据进行筛选清洗
            dfs = pd.read_csv(file_path, low_memory=False)
            for slope in dfs['slope'].unique():
                dfs_slope = dfs[dfs['slope'] == slope]
                for torque in dfs['Torque'].unique():
                    dfs_torque = dfs_slope[dfs_slope['Torque'] == torque]
                    if "-5Nm" in torque or "310Nm" in torque:
                        boardline = 3000
                        end = 5000
                    elif "2Nm" in torque:
                        boardline = 20
                        end = 28
                    else:
                        boardline = 5000
                        end = 10000
                    for testp in dfs_torque['Test Point'].unique():
                        dfs_testp = dfs_torque[dfs_torque['Test Point'] == testp]
                        
                        
                        for i, order in enumerate(dfs_testp["order"].unique()):
                            order_data = dfs_testp[dfs_testp["order"] == order]
                            
                            df = order_data
                            df_max = df.groupby(['Test Point','Torque','Speed'])['vibration'].max().reset_index()
                            df_max_t = df.groupby(['Torque'])['vibration'].mean().sort_values(ascending=False).head(7).reset_index()
                            df_max_dm = df_max.drop(['vibration', 'Speed'], axis=1)
                            def count_rms_length(x):
                                return len(x)


                            df_rms = df.groupby(["Test Point","Torque","Speed"])["vibration"].agg(
                                    ["mean", "std", lambda x: norm.interval(0.99379, loc=x.mean(), scale=x.std() / np.sqrt(len(x)))[1],
                                    lambda x: norm.interval(0.99379, loc=x.mean(), scale=x.std() / np.sqrt(len(x)))[0],
                                    count_rms_length]
                                ).rename(columns={'count_rms_length': 'RMS Length'})
                        

                            df_rms = df_rms.reset_index()
                            df_rms.columns = ["Test Point", "Torque", "Speed", "Mean RMS", "Standard Deviation", "upper_bound","lower_bound","len"]      

                                    
                            fig, ax = plt.subplots(figsize=(8, 5))
                            plt.rcParams['font.sans-serif'] = ['Simsun']


                            sns.lineplot(data=df_rms, x="Speed", y="Mean RMS", ax=ax, color='green', label='RMS值平均值')
                            # 按照"Max Vibration"列降序排序
                            df_sorted = df_max.sort_values(by="vibration", ascending=False)

                            # 计算保留的较大点数量
                            num_large_points = int(len(df_sorted) * 0.05)

                            # 获取前 num_large_points 个较大的点
                            df_large_points = df_sorted[:num_large_points]

                            # 对剩余的点进行降采样
                            df_sampled = df_sorted[num_large_points:].sample(frac=0.1)

                            # 合并保留的较大点和降采样后的点
                            df_final = pd.concat([df_large_points, df_sampled])

                            # 绘制散点图
                            sns.scatterplot(data=df_final, x="Speed", y="vibration", ax=ax, s=6, marker='o', alpha=0.5, color='gray', label='最大振动值(部分值)')

                            
                            #拟合最大振动及其转速点的趋势线
                            x = df_max['Speed']
                            y = df_max['vibration']
                            # 假设 x 和 y 是你的数据
                            x = df_max['Speed'].values.reshape(-1, 1)
                            y = df_max['vibration'].values

                            # 创建一个函数来执行多项式回归
                            def polynomial_regression(x, y, degree):
                                model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
                                model.fit(x, y)
                                return model

                            # 尝试不同阶数的多项式
                            best_degree = None
                            best_score = -np.inf

                            for degree in range(1, 20):  # 可以根据需要调整阶数的范围
                                model = polynomial_regression(x, y, degree)
                                score = model.score(x, y)
                                
                                if score > best_score:
                                    best_score = score
                                    best_degree = degree

                            # 使用最佳阶数的模型进行拟合
                            best_model = polynomial_regression(x, y, best_degree)

                            # 绘制原始数据和拟合曲线
                            plt.scatter(x, y, label='Original Data')
                            plt.plot(x, best_model.predict(x), color='red', label=f'Polynomial Regression (Degree {best_degree})')
                            plt.legend()
                            # plt.title(f"{slope}{torque}{order}{testp}_polynomial")
                            # plt.savefig(os.path.join('data\\Project\\ProcessedData\\EOL Data\\target', f"{slope}{torque}{testp}{order}Polynomial Regression Degree {best_degree}.png"))

                            
                            
                            x_new = np.concatenate([x])
                            y_new = np.concatenate([y])
                            max_x_new = np.max(x_new)
                            min_x_new = np.min(x_new)
                            max_y_new = np.max(y_new)
                            x_new, indices = np.unique(x_new, return_index=True)
                            y_new = y_new[indices]
                            sort_indices = np.argsort(x_new)
                            x_new, y_new = x_new[sort_indices], y_new[sort_indices]
                            x_new_filtered = x_new
                            y_new_filtered = y_new
                            max_x_new_filtered = np.max(x_new_filtered)
                            
                            new_x = np.linspace(min_x_new, max_x_new, num=len(df_max['vibration']))
                            new_x_filtered = np.linspace(5000, max_x_new_filtered, num=6000)
                            x_new_1 = x_new[x_new < boardline]
                            y_new_1 = y_new[x_new < boardline]
                            x_new_2 = x_new_filtered[x_new_filtered >= boardline]
                            y_new_2 = y_new_filtered[x_new_filtered >= boardline]
                            kf = KFold(n_splits=5, shuffle=True, random_state=42)
                            s_values = np.logspace(10, 60, num=11, base=10.0)
                            best_s_1 = None
                            best_score_1 = None
                            for s in s_values:
                                scores = []
                                for train_index, val_index in kf.split(x_new_1):
                                        f = UnivariateSpline(x_new_1[train_index], y_new_1[train_index], s=s)
                                        y_pred = f(x_new_1[val_index])
                                        score = np.max(np.abs(np.gradient(y_pred)))
                                        scores.append(score)
                                mean_score = np.mean(scores)
                                if best_score_1 is None or mean_score < best_score_1:
                                    best_score_1 = mean_score
                                    best_s_1 = s
                            f_1 = UnivariateSpline(x_new_1, y_new_1, s=best_s_1)
                            best_s_2 = None
                            best_score_2 = None
                            for s in s_values:
                                scores = []
                                for train_index, val_index in kf.split(x_new_2):
                                    f = UnivariateSpline(x_new_2[train_index], y_new_2[train_index], s=s)
                                    y_pred = f(x_new_2[val_index])
                                    score = np.max(np.abs(np.gradient(y_pred)))
                                    scores.append(score)
                                mean_score = np.mean(scores)
                                if best_score_2 is None or mean_score < best_score_2:
                                    best_score_2 = mean_score
                                    best_s_2 = s
                            f_2 = UnivariateSpline(x_new_2, y_new_2, s=best_s_2)
                            new_y_1 = f_1(new_x[new_x < boardline])
                            new_y_2 = f_2(new_x[new_x >= boardline])
                            new_y = np.concatenate([new_y_1, new_y_2])
                            #对拟合后的曲线做修正补偿
                            f = UnivariateSpline(new_x, new_y, s=np.mean([best_s_1,best_s_2]))

                            new_y = f(new_x)
                            diff_values = new_y - df_max["vibration"]

                            max_diff_value = np.max(diff_values)
                            new_y = f(new_x)+max_diff_value

                            #拟合RMS的4σ边界线
                            x2 = df_rms['Speed']
                            y2 = df_rms['upper_bound']
                            max_x2 = np.max(x2)
                            min_x2 = np.min(x2)
                            mean_s = np.mean([best_s_1, best_s_2])
                            new_x2 = np.linspace(min_x2, max_x2, num=len(df_rms['Speed']))
                            
                            f = UnivariateSpline(new_x2 , y2, s=mean_s)
                            new_y2 = f(new_x2)
                            #修正拟合曲线
                            f = UnivariateSpline(new_x2, new_y2, s=mean_s)
                            new_y2 = f(new_x2)
                            diff_values_b = new_y - df_max["vibration"]

                            max_diff_value_b = np.max(diff_values_b)
                            new_y2 = f(new_x2)+ max_diff_value_b

                            difference = np.subtract(new_y2, new_y)

                            # 计算差值的均值
                            mean_difference = np.nanmean(difference)

                            if mean_difference>0 or mean_difference>50:
                                new_y = new_y2+3

                            #保存目标线到excel
                            #targetline = {'input speed': new_x, 'target': new_y,'target+5': new_y+5,'target_RMS': new_y2}
                            targetline = {'input speed': new_x, 'target': new_y,'target+5': new_y+5}
                            df_target = pd.DataFrame(targetline)

                            with pd.ExcelWriter(target_path, mode='a', engine='openpyxl') as writer:
                                df_target.to_excel(writer, sheet_name=f'{slope}{torque}{testp}{order}', index=False)
                            targetline_poly = {'input speed': new_x, 'target': best_model.predict(new_x.reshape(-1,1)),'target+5': best_model.predict(new_x.reshape(-1,1))+5}
                            poly_target = os.path.join("data\\Project\\ProcessedData\\EOL data", f"target_poly.xlsx")
                            print(targetline_poly)
                            df_target_poly = pd.DataFrame(targetline_poly)
                            
                            with pd.ExcelWriter(poly_target, mode='a', engine='openpyxl') as writer:
                                 df_target_poly.to_excel(writer, sheet_name=f'{slope}{torque}{testp}{order}', index=False)
                            
                            #保存预测曲线图
                            sns.lineplot(x=new_x, y=new_y, ax=ax,label='趋势线拟合')
                            sns.lineplot(x=new_x,y=new_y+5,ax=ax,label='目标线', linestyle='--')
                            ax.fill_between(new_x, new_y, new_y+5, color='yellow', alpha=0.2,label='修正值')
                            plt.fill_between(df_rms["Speed"], df_rms["lower_bound"], df_rms["upper_bound"], color='lightgreen', alpha=0.8,label='RMS值 4σ 带')
                            plt.plot(new_x2, new_y2, color='skyblue', linewidth=1,label='上边界')
                            plt.legend(title="Legend", loc="upper left")
                            plt.title(f" {slope}{torque}{testp}{order}")

                            title = ax.get_title()
                            #for pattern, replacement in pattern_dict.items():
                                #title = re.sub(pattern, replacement, title)
                            ax.set_title(title, fontsize=10)
                            plt.xlabel("输入轴转速", fontsize=10)
                            plt.ylabel("壳体振动 dB[g]", fontsize=10)
                            plt.xlim(0, end)
                            plt.xticks(np.arange(0, end+1, 1000), fontsize=8)
                            plt.ylim(60, 166)
                            plt.yticks(np.arange(60, 166, 10), fontsize=8)
                            plt.legend(fontsize= 10)
                            plt.grid(color='#D3D3D3') # 添加透明色网格
                            plt.savefig(os.path.join('data\\Project\\ProcessedData\\EOL Data\\target', f"{slope}{torque}{testp}{order}derivative practice.png"))
                            plt.close()





    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    messagebox.showinfo("提示", "数据拟合完成")


    root.destroy()  # 销毁主窗口

