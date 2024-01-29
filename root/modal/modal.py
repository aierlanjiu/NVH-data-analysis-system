import matplotlib.pyplot as plt
import numpy as np
import math
plt.rcParams['font.sans-serif'] = 'Simsun'

def plot(ax,orders,type):
    ax.set_xlim([0, 6000])
    
    
    ax.set_ylim([0, 14000])
    
    for order in orders:
        (plot1,)=ax.plot([(speed * order / 60) for speed in input_speed], input_speed,label=f"{type}{order}",clip_on=False)
    return (plot1,)

# 定义输入轴转速范围
input_speed = list(range(100, 13501))

# 定义阶次数据
bearing_orders = [4.94, 3.06, 4.03, 4.59, 3.6, 2.85, 1.36, 1.07, 0.88]
gear_orders = [9.62, 19.24, 28.86, 26, 52, 78]
frequency_modal = [510.93,676.89,1149.5,1246.6,1496.69,1663.8,1891.8,2115.7]
# 计算频率数据
bearing_frequencies = [(speed * order / 60) for speed in input_speed for order in bearing_orders]
gear_frequencies = [(speed * order / 60) for speed in input_speed for order in gear_orders]
# 绘制图形
plt.figure(figsize=(10, 6))
ax = plt.subplot(111)

def plot(ax, orders, type):
    ax.set_xlim([0, 2000])
    ax.set_ylim([0, 14000])
    
    # 创建一个空列表，用于存储每次循环的plot1结果
    plot1_list = []

    for order in sorted(orders):
        plot1, = ax.plot([(speed * order / 60) for speed in input_speed], input_speed, label=f"{type}{order}", clip_on=False)
        
        # 将当前循环的plot1添加到列表
        plot1_list.append(plot1)
    
    # 返回包含所有plot1的列表
    return plot1_list



plot_b = plot(ax,bearing_orders,'轴承')
plot_g = plot(ax,gear_orders,'齿轮')


# 添加标签和标题
plt.ylabel('输入轴转速')
plt.xlabel('频率')
plt.title('阶次频率图')

# 设置x轴范围
plt.xlim(0, 2000)
plt.ylim(0, 14000)
# 显示图形
plt.grid()

# 添加标签
for i,order in enumerate(sorted(bearing_orders)):
    ax.text((8000+i*500)*order/60, (8000+i*500), f" {order}", family="Simsun", 
             size="medium", bbox=dict(facecolor="white", edgecolor="None", alpha=0.85),
               color=plot_b[i].get_color(), ha="center", va="center", rotation=math.atan(60/order)/np.pi*90)
    
for i,order in enumerate(sorted(gear_orders)):
    ax.text((500+100*i), ((500+100*i)*60/order), f" {order}", family="Simsun", size="medium",
              bbox=dict(facecolor="white", edgecolor="None", alpha=0.85), 
              color=plot_g[i].get_color(), ha="center", va="center", rotation=math.atan(60/order)/np.pi*90)


# 计算频率数据
for modal in frequency_modal:
    modal_frequencies = [(1 * modal) for speed in input_speed]

    # 绘制 modal_frequencies 的曲线
    ax.plot(modal_frequencies, input_speed, label='Modal Frequencies', linestyle='-', color='black')

for modal in frequency_modal:
    low_value = modal -5
    ax.axvline(low_value, linestyle='--', color='red',alpha=0.5)
    high_value = modal +5
    ax.axvline(high_value, linestyle='--', color='red',alpha=0.5)
    ax.text(modal,0, f"modal", family="Simsun", size="small",
            bbox=dict(facecolor="white", edgecolor="None", alpha=0.85), 
            color='black', ha="center", va="center", rotation=0)
plt.show()