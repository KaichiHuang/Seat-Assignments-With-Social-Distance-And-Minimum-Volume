# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 21:39:38 2022

@author: JEAN
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os as os



data_file="SEAT_OUTPUT_with_Audio.xlsx"
coordinates = pd.read_excel(data_file)

filename = data_file[:-5] #從哪裡擷取到哪裡 負值代表由後往前
# coordinates=coordinates.iloc[:,:2]#砍掉多餘的後兩欄

#DataFrame.loc屬性可返回“行”標簽對應的“名稱”列中顯示的值
seats = np.array(coordinates)   
seat_loc_all      = np.array(coordinates.loc[coordinates['Feature'] != 'selected_seat', ['X', 'Y']])  #此為顯示x,y列中的值
seat_loc_selected = np.array(coordinates.loc[coordinates['Feature'] == 'selected_seat', ['X', 'Y']])
teacher= np.array(coordinates.loc[coordinates['Feature'] == 'teacher', ['X', 'Y']])
audio= np.array(coordinates.loc[coordinates['Feature'] == 'audio', ['X', 'Y']])



## create matplotlib figure.
fig, axs = plt.subplots() #建立多個子圖表
axs.set_aspect('equal')  #x, y 為相同scaling
fig.set_figheight(15) #設定 Matplotlib 中的圖形大小
fig.set_figwidth(15) #設定 Matplotlib 中的圖形大小
axs.invert_yaxis() #反轉y軸
axs.invert_xaxis() #反轉x軸

    
#tick_params 參數刻度線樣式設置
plt.tick_params(
    axis='both',  # changes apply to the x-axis
    which='both',  # both major and minor ticks are affected
    bottom=False,  # ticks along the bottom edge are off
    left=False,  # ticks along the left edge are off
    labelbottom=False,  # labels along the bottom edge are off
    labelleft=False)  # labels along the left edge are off

legend_objects = []
legend_labels = []

## plot seats and selected seats.
#折線圖
#X[:,0]就是取所有行的第0個數據, X[:,1] 就是取所有行的第1個數據
s0, = axs.plot(seat_loc_all[:, 0], seat_loc_all[:, 1], "s", markersize=15, fillstyle='none', color='black')
s1, = axs.plot(seat_loc_selected[:, 0], seat_loc_selected[:, 1], "s", markersize=15, fillstyle='full')
stu, = axs.plot(audio[:, 0], audio[:, 1], "s", markersize=15, fillstyle='full', color='orange')
t, = axs.plot(teacher[:, 0], teacher[:, 1], "s", markersize=15, fillstyle='full', color='gold')


legend_objects.append(s1)
legend_labels.append('Selected seats')
legend_objects.append(s0)
legend_labels.append('Unselected seats')
legend_objects.append(stu)
legend_labels.append('Audio')
legend_objects.append(t)
legend_labels.append('Teacher')

## add legend.
#.legend()來顯示數據的名稱; loc='lower center'為下方中間; ncol為圖例擁有的列數; bbox_to_anchor=(x, y)用於指定圖例的座標
plt.legend(legend_objects, legend_labels, loc='lower center', ncol=len(legend_objects), bbox_to_anchor=(0.5, -0.1))

## save output file.
plt.savefig(filename + ".pdf", dpi=300) #儲存圖片為pdf檔案