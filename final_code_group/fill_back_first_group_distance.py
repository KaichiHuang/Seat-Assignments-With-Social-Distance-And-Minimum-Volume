#group
import numpy as np
import pandas as pd
import sys
import os as os
import math


coordinates = pd.read_excel("G:\我的雲端硬碟\ORA\seat assignment\input\hall_layout.xlsx")
# coordinates = pd.read_excel("G:\我的雲端硬碟\ORA\seat assignment\input\Auditorium_layout.xlsx")
print("coordinates=\n",coordinates)

coordinates = coordinates.sort_values(by=['Y','X'], ascending=False) #fill in seats from left to right, back to front  #遞減
coordinates=coordinates.iloc[:,:2]#砍掉多餘的後兩欄

seat_loc    = np.array(coordinates)

print("seat_loc=\n",seat_loc)
groups = pd.read_excel("G:\我的雲端硬碟\ORA\seat assignment\input\classroom_groups.xlsx")

groups = groups.sort_values(by=['GroupId'], ascending=True) #sort groups by GroupID   #遞增
groups = np.array(groups)
# print("groups=\n",groups)

seat_set = [i for i in range(len(seat_loc))]


pair_set = []  # define a set of seat index pair (s1, s2) for all s1 != s2.  #座位組合
for s1 in range(len(seat_set) - 1):
    for s2 in range(s1 + 1, len(seat_set)):
        pair_set.append((seat_set[s1], seat_set[s2]))
        # print(pair_set)


distance = {}  # compute distance between each pair of seats (s1, s2) for all s1 != s2.
for pair in pair_set:
    x = np.abs(seat_loc[pair[0]][0] - seat_loc[pair[1]][0])
    y = np.abs(seat_loc[pair[0]][1] - seat_loc[pair[1]][1])
    # z = np.abs(seat_loc[pair[0]][2] - seat_loc[pair[1]][2])
    distance[pair] = np.sqrt(x * x + y * y )
    # print(x,y,distance[pair])  #兩個位子之間的距離


current_seat = 0 # current seat to be assigned in the for loop
seating_plan = [0]*len(seat_loc) # final seating plan; array initialized with zeros  [0,0,...,0] 共100個0

#初始音量，先設置為60
volume_first=float(60.0)

for group_index in range(len(groups)): #for each group

    group_seats = [] #seats occupied by the group
    g_list=[]#用於紀錄該group所有成員位置
    for person in range(groups[group_index,1]): #for each person in the group  group[group_index,1]=組人數


        for seat in range (current_seat, len(seat_loc)): # for each unchecked seat range(start, stop)
            if seating_plan[current_seat] == 0: #if seat is available
                seating_plan[current_seat] = groups[group_index,0] #assign a group number(ID) to the seat   將0改成groupID

                group_seats.append(current_seat) #add seat to the group of seats occupied by the group
                g_list.append(current_seat)
                current_seat = current_seat + 1
                break
            else: #if seat is unavailable because of social distance constraints
                current_seat = current_seat + 1
    print("GGG",g_list)


    #for each unchecked seat, define the seat as unavailable if the distance between
    #the seat and one of the seats occupied by the group is greater than the social distance threshold
    for i in range(current_seat, len(seat_loc)):

        for j in group_seats:  #已有group佔據
            if distance[j,i] < 20:
                seating_plan[i] = -1


# print(seat_loc)
# save the output file.
coordinates["SeatingPlan"] = seating_plan

coordinates.to_excel("G:\我的雲端硬碟\ORA\seat assignment\output\hall_group_result_distance.xlsx", index=False)

#how many seats are occupied
print(str(sum(coordinates["SeatingPlan"] > -1)) + " occupied seats ")

