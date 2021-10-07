import numpy as np
import csv
#train
data = []
with open('train.csv', 'r') as f:
     reader = csv.reader(f)
     print(type(reader))
     
     for row1 in reader:
         data.append(row1)
data = np.array(data)
labels = data[1:,1]
length = len(labels)
live = 0
for i in range(length):
    if labels[i] == '1':
        live = live+1
live_per = live/length
dead = length-live
dead_per = 1-live_per
age = data[1:,5]
sex = data[1:,4]
n,m = 0,0  #n为男性有年龄数量，m为女性有年龄数量
male_age,female_age = 0,0
for i in range(length):
    if sex[i] == 'male':
        if age[i] != '':
            male_age += float(age[i])
            n = n+1
    elif sex[i] == 'female':
        if age[i] != '':
            female_age += float(age[i])
            m = m+1
male_mean = male_age/n
female_mean = female_age/m
for i in range(length):
    if sex[i] == 'male':
        if age[i] == '':
            age[i] = male_mean
    elif sex[i] == 'female':
        if age[i] == '':
            age[i] = female_mean
people = []
for i in range(length):
    people.append(int(data[i+1,6])+int(data[i+1,7]))

for i in range(length):
    if float(age[i])<18:
        age[i] = 0
    elif float(age[i])>17 and float(age[i])<30:
        age[i] = 1
    elif float(age[i])>29 and float(age[i])<50:
        age[i] = 2
    elif float(age[i])>49:
        age[i] = 3
#男女先验概率
male_live = 0
male_num = 0
female_live = 0
female_num = 0
for i in range(length):
    if sex[i] == 'male':
        male_num = male_num+1
        if labels[i] == '1':
            male_live = male_live+1
    if sex[i] == 'female':
        female_num = female_num+1
        if labels[i] == '1':
            female_live = female_live+1
p_m_live = male_live/live  #已知生存，为男性的条件概率
p_fem_live = female_live/live  #已知生存，为女性的条件概率
#已知死亡的条件概率
p_m_dead = (male_num-male_live)/dead
p_fem_dead = (female_num-female_live)/dead
#年龄先验概率
zero_live = 0
zero_num = 0
one_live = 0
one_num = 0
two_live = 0
two_num = 0
three_live = 0
three_num = 0
for i in range(length):
    if age[i] == '0':
        zero_num = zero_num+1
        if labels[i] == '1':
            zero_live = zero_live+1
    if age[i] == '1':
        one_num = one_num+1
        if labels[i] == '1':
            one_live = one_live+1
    if age[i] == '2':
        two_num = two_num+1
        if labels[i] == '1':
            two_live = two_live+1
    if age[i] == '3':
        three_num = three_num+1
        if labels[i] == '1':
            three_live = three_live+1
#已知生存条件下，各年龄段的条件概率
p_0_live = zero_live/live  
p_1_live = one_live/live
p_2_live = two_live/live  
p_3_live = three_live/live
#已知死亡的条件概率
p_0_dead = (zero_num-zero_live)/dead  
p_1_dead = (one_num-one_live)/dead
p_2_dead = (two_num-two_live)/dead  
p_3_dead = (three_num-three_live)/dead
#朋友亲人数量先验概率
for i in range(length):
    if people[i] == 0:
        pass
    else:
        people[i] = 1
people_live = 0
people_num = 0
no_live = 0
no_num = 0
for i in range(length):
    if people[i] == 1:
        people_num = people_num+1
        if labels[i] == '1':
            people_live = people_live+1
    if people[i] == 0:
        no_num = no_num+1
        if labels[i] == '1':
            no_live = no_live+1
p_people_live = people_live/live  #已知生存，有亲人的条件概率
p_nopeople_live = no_live/live  #已知生存，无亲人的条件概率
#已知死亡的条件概率
p_people_dead = (people_num-people_live)/dead
p_nopeople_dead = (no_num-no_live)/dead

#test
result = []
with open('test.csv', 'r') as L:
     reader1 = csv.reader(L)
     for row in reader1:
         try:
             q = float(row[0])  #判断第二行开始
             if row[4] == '':
                 if row[3] == 'male':
                     row[4] = male_mean
                 elif row[3] == 'female':
                     row[4] = female_mean
             if row[3] == 'male':
                 x1 = p_m_live
                 y1 = p_m_dead
             elif row[3] == 'female':
                 x1 = p_fem_live
                 y1 = p_fem_dead
             
             if float(row[4])<18:
                 x2 = p_0_live
                 y2 = p_0_dead
             elif float(row[4])>17 and float(row[4])<30:
                 x2 = p_1_live
                 y2 = p_1_dead
             elif float(row[4])>29 and float(row[4])<50:
                 x2 = p_2_live
                 y2 = p_2_dead
             elif float(row[4])>49:
                 x2 = p_3_live
                 y2 = p_3_dead
             
             if int(row[5])+int(row[6]) > 0:
                 x3 = p_people_live
                 y3 = p_people_dead
             else:
                 x3 = p_nopeople_live
                 y3 = p_nopeople_dead
             
             alive = live_per*x1*x2*x3
             death = dead_per*y1*y2*y3
             if alive>death:
                 result.append(1)
             else:
                 result.append(0)
         except Exception as e:
             print(str(e))
             print(row)

with open('submission.csv','w',newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["PassengerId","Survived"])
    for i in range(len(result)):
        writer.writerow([i+1,result[i]])




