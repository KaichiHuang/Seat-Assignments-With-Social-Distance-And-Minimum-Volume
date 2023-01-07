# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 13:22:21 2022

@author: JEAN
"""


from gurobipy import *
import numpy as np
import pandas as pd
import sys
import os as os
import math

#初始音量，先設置為60
volume_first=float(60.0)

#讀取座位
coordinates = pd.read_excel("layout.xlsx") 

#老師座標設置為(75,160)
teacher=[75,160]

#把輸入座位轉成nparray
seat_loc    = np.array(coordinates)

#計算座位數量
seat_number = [i for i in range(len(seat_loc))]

#算a對b-z&b對a-z.....
pair_set = [] 
for s1 in range(len(seat_number) - 1):
    for s2 in range(s1 + 1, len(seat_number)):
        pair_set.append((seat_number[s1], seat_number[s2]))

#設置模型
model=Model('indivual seats layout')


#設置Gurobi參數
#setParam（參數名稱，新值） False
model.setParam('OutputFlag', False)  

x = model.addVars(seat_number, vtype = GRB.BINARY)

#計算距離
distance = {} 
for pair in pair_set:
    xa = np.abs(seat_loc[pair[0]][0] - seat_loc[pair[1]][0])
    yb = np.abs(seat_loc[pair[0]][1] - seat_loc[pair[1]][1])
    distance[pair] = np.sqrt(xa **2 + yb **2)


distance_for_volume=[]
volume = []
 

for i in range(len(seat_loc)):
        xx = np.abs(seat_loc[i][0] - teacher[0])
        yy = np.abs(seat_loc[i][1] - teacher[1])
        distance_for_volume=np.sqrt(xx **2  + yy **2)
        volume.append(volume_first + 10*(math.log10((10/distance_for_volume)**2)))
    


for pair in pair_set:
    if distance[pair] < 20 :
        #addConstr增加限制式
        model.addConstr(x[pair[0]] + x[pair[1]] <= 1) 
    

for i in seat_number:
    if volume[i]<40:
        model.addConstr(x[i] == 0)


# set objective function: maximize number of students
model.setObjective(quicksum(x[s] for s in seat_number), GRB.MAXIMIZE)

# optimize the model
model.optimize()



## print and return the result
status_code = {1:'LOADED', 2:'OPTIMAL', 3:'INFEASIBLE', 4:'INF_OR_UNBD', 5:'UNBOUNDED'}
status = model.status
print('The optimization status is {}'.format(status_code[status]) + "<br>")
if status == 2:
    
    # Retrieve objective value
    print('Optimal objective value: {}'.format(model.objVal) + " occupied seats <br>")
    
    # Retrieve variable value and record selected seats' index and coordinates.
    seat_loc_selected = []
    seat_selected = []
    for s in seat_number:
        if x[s].x > 0:
            seat_loc_selected.append(seat_loc[s])
            seat_selected.append(s)
            coordinates = coordinates.append(pd.DataFrame([['selected_seat', seat_loc[s][0], seat_loc[s][1]]],
                                                          columns=['Feature', 'X', 'Y']))
            
    coordinates = coordinates.append(pd.DataFrame([['teacher', teacher[0], teacher[1]]],columns=['Feature', 'X', 'Y']))

# save the output file.
coordinates.to_excel("seat.xlsx",sheet_name='sheet1')














