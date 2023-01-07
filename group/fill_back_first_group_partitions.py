#group
import numpy as np
import pandas as pd
import sys
import os as os
import math


# coordinates = pd.read_excel("G:\我的雲端硬碟\ORA\seat assignment\input\hall_layout.xlsx")
coordinates = pd.read_excel("G:\我的雲端硬碟\ORA\seat assignment\input\hall_layout.xlsx")
# print("coordinates=\n",coordinates)

coordinates = coordinates.sort_values(by=['Y','X'], ascending=False) #fill in seats from left to right, back to front  #遞減
coordinates=coordinates.iloc[:,:2]#砍掉多餘的後兩欄

seat_loc    = np.array(coordinates)

# print("seat_loc=\n",seat_loc)
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
    distance[pair] = np.sqrt(x * x + y * y)
    # print(x,y,distance[pair])  #兩個位子之間的距離


current_seat = 0 # current seat to be assigned in the for loop
seating_plan = [0]*len(seat_loc) # final seating plan; array initialized with zeros  [0,0,...,0] 共100個0
partition = 0
partition_list=[]

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
  

    k=1 #判斷需不需要重做
    while (k):
        k=0
        b = 0
        for a in g_list:
            for b in g_list:

                # if ((a < b) and (distance[a, b] > 55)):  #距離55in時，音量45分貝
                if ((a < b) and ((volume_first + 10*(math.log10((10/distance[a, b])**2))) < 45)):  #距離55in時，音量45分貝

                    print("PLAN",seating_plan)
                    k=1 #有問題所以還需要重新判斷
                    print("第",groups[group_index,0],"組有<45的情況")
                    print("有毛病",a,":",b,"D",distance[a, b])

                    seating_plan[g_list[0]]=-1 #原本的第一個變成-1
                    print("-1的是",g_list[0])
                    #將一個人填入下一個可行位置
                    for seat in range(current_seat, len(seat_loc)):  # for each unchecked seat range(start, stop)
                        if seating_plan[current_seat] == 0:  # if seat is available
                            seating_plan[current_seat] = groups[group_index, 0]  # assign a group number(ID) to the seat   將0改成groupID

                            group_seats.append(current_seat)  # add seat to the group of seats occupied by the group
                            g_list.append(current_seat)
                            group_seats.pop(0)
                            g_list.pop(0)#刪掉第一個
                            print("G--",g_list)

                            current_seat = current_seat + 1
                            b = 1
                            break

                        else:  # if seat is unavailable because of social distance constraints
                            current_seat = current_seat + 1

                    print(current_seat)
                    if b:
                        break
                    # current_seat=current_seat-groups[group_index,1]
            if b:
                break
    if len(g_list)>0:
        if max(g_list) < len(seat_loc)-1:
            seating_plan[(max(g_list)+1)] = -2
            print("partition",max(g_list)+1)


    #for each unchecked seat, define the seat as unavailable if the distance between
    #the seat and one of the seats occupied by the group is greater than the social distance threshold
    for i in range(current_seat, len(seat_loc)):

        for j in group_seats:  #已有group佔據
            if seating_plan[i] !=-2:
                if distance[j,i] < 15:
                    seating_plan[i] = -1


# print(seat_loc)
# save the output file.
coordinates["SeatingPlan"] = seating_plan

coordinates.to_excel("G:\我的雲端硬碟\ORA\seat assignment\output\hall_group_result_partition.xlsx", index=False)

#how many seats are occupied
print(str(sum(coordinates["SeatingPlan"] > -1)) + " occupied seats ")

