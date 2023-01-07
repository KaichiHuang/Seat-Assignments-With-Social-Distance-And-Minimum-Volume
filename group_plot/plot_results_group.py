import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os as os
import matplotlib.patches as mpatch


# data_file="G:\我的雲端硬碟\ORA\seat assignment\output\group_layout_result.xlsx"
data_file="G:\我的雲端硬碟\ORA\seat assignment\output\hall_group_result_2.xlsx"
coordinates = pd.read_excel(data_file)
filename = data_file[:-5]  #從哪裡擷取到哪裡 負值代表由後往前

    
seats = np.array(coordinates)

## create matplotlib figure.
fig, axs = plt.subplots()  #建立多個子圖表
axs.set_aspect('equal')  #x, y 為相同scaling
axs.set_xlim((-5, max(seats[:,0]) + 5))  #設定x軸限制  [:,0]取所有行的第0個數據
axs.set_ylim((-5, max(seats[:,1]) + 5))  #設定y軸限制  [:,1]取所有行的第1個數據
axs.invert_yaxis()  #反轉y軸
axs.invert_xaxis()  #反轉x軸
#去除邊框線(上下左右)
axs.spines['top'].set_visible(False)    
axs.spines['right'].set_visible(False)
axs.spines['bottom'].set_visible(False)
axs.spines['left'].set_visible(False)
#tick_params 參數刻度線樣式設置
plt.tick_params(
    axis='both',  # changes apply to the x-axis
    which='both',  # both major and minor ticks are affected
    bottom=False,  # ticks along the bottom edge are off
    left=False,  # ticks along the left edge are off
    labelbottom=False,  # labels along the bottom edge are off
    labelleft=False # labels along the left edge are off
)
# annotate() 方法和 text() 類似，可以在圖表中加入文字
for seat_index in range(len(seats)):    #len(seats)代表座位數   
        
    if int(seats[seat_index,2]) == -1:
        axs.annotate('X', (seats[seat_index,0], seats[seat_index,1]), color='red', weight='bold', fontsize=5, ha='center', va='center')
    elif int(seats[seat_index,2]) == -2:
        axs.annotate('|', (seats[seat_index,0], seats[seat_index,1]), color='black', weight='bold', fontsize=5, ha='center', va='center')
    else:
        axs.annotate(int(seats[seat_index,2]),  (seats[seat_index,0], seats[seat_index,1]), color='b', weight='bold', fontsize=5, ha='center', va='center')

plt.savefig(filename + ".pdf", dpi=300)   #儲存圖片為pdf檔案
   