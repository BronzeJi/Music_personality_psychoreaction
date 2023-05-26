#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 10:41:20 2023

@author: elliot
"""



#correaltion between brain wave and emotions with factor

import scipy.io
import matplotlib.pyplot as plt
from dealEEG import get_EEG
import numpy as np

import seaborn as sns

def plot_corre_emotion_brainwave(name):
    data=scipy.io.loadmat('/Users/elliot/Documents/GitHub/Music_eng/deal_withsurvey/data/person.mat')
    
    data_coef=scipy.io.loadmat("/Users/elliot/Documents/GitHub/Music_eng/deal_withsurvey/Coefficient_MBTI.mat")

    # MBTI
    dip=2
    exp=3
    tableNo={'AG23':[18,dip],'Ca12':[1,exp],'CH12':[2,dip]}
    
    song=data['person'][0][0][0][0][0]
    
    AG_raw=[[] for _ in range(0,12)]
    AG=[[] for _ in range(0,12)]
    
    #person type

    for i in range(0,12):
 
        coef=data_coef['Coef'][0][0]
        coef_for_oneperson=[]

        for j in range(0,9):
            # len=9 emotion coefficient for one MBTI per song
            coef_for_oneperson.append(coef[i].tolist()[j][tableNo[name][1]])
        
        AG_raw[i]=song[i][tableNo[name][0]].tolist()
        AG[i] = [x * y for x, y in zip(AG_raw[i], coef_for_oneperson)]
        
    """if i==3 or i==11:
            # with coeffient
            AG[i] = [x * y for x, y in zip(AG_raw[i], coef_for_oneperson)]
        else:
            AG[i]=AG_raw[i]"""
               
    # Transpose the 2D list
    
    AG_transposed_list = [list(row) for row in zip(*AG)]
    
        
    data=get_EEG(name);
        
    matrix=data['wave']
    num_rows = len(matrix)
    
    ddot=len(data['attention'])/981
    ticksR=[]
    label = list(range(1, 14))
    for i in range(10,980,80):#12 songs begin time
        ticksR.append(round(i*ddot))
    
    
    aver_data_all=[[] for _ in range(0,8)]
    standdiv_all=[[] for _ in range(0,8)]
    
    
    #wave
    for j in range(num_rows):
        aver_data=[]
        variance=[]
        standdiv=[]
        for i in range(0,12):
            anlysis_data=matrix[j][ticksR[i]:ticksR[i+1]]
            aver_data.append(np.mean(anlysis_data))
            variance.append(np.var(anlysis_data))
            standdiv.append(np.std(anlysis_data))
    
        aver_data_all[j]=aver_data;
        standdiv_all[j]=standdiv;
        
        
    # correlation
    
    variable1= np.array(aver_data_all)# average
    variable3= np.array(standdiv_all) # standard deviation
    variable2= np.array(AG_transposed_list).tolist()
    
    
    correlation_coefficient=[[] for _ in range(0,num_rows)]
    # Calculate the correlation coefficient
    for j in range(0,num_rows):
        #wave
        for i in range(0,9):
            #emotion
            #fro average/standard  divation change here 
            correlation_matrix = np.corrcoef(variable1[j], variable2[i])
            correlation_coefficient[j].append(correlation_matrix[0, 1])
        
    
    xlabel=["Happy","Sad","Energetic","Aggressive","Calm","Annoyed","Pleased","Like","emotion"]
    ylabel=["Delta","Theta","Low_Alpha","High_Alpha","Low_Beta","High_Beta","Low_gamma","High_gamma"]
    plt.figure(num=name);
    sns.heatmap(correlation_coefficient, annot=True, xticklabels=xlabel, yticklabels=ylabel,cmap="coolwarm")
    plt.savefig(name+"corr_wave_emo_standD.svg", dpi=300)
    
    plt.title(name)
    return correlation_coefficient
#plt.imshow(correlation_coefficient)




name=['Ca12','CH12','AG23'];
aver=[[] for _ in range(0,8)]

temp1=plot_corre_emotion_brainwave(name[0]);
temp2=plot_corre_emotion_brainwave(name[1]);
temp3=plot_corre_emotion_brainwave(name[2]);

aver=(np.array(temp1)+np.array(temp2)+np.array(temp3))/3


xlabel=["Happy","Sad","Energetic","Aggressive","Calm","Annoyed","Pleased","Like","emotion"]
ylabel=["Delta","Theta","Low_Alpha","High_Alpha","Low_Beta","High_Beta","Low_gamma","High_gamma"]
plt.figure(num="ave",figsize=(8, 6));
plt.title("average over three person");


sns.heatmap(aver, annot=True,  xticklabels=xlabel, yticklabels=ylabel, cmap="coolwarm")

plt.savefig("aver_corr_wave_emo_standD.svg", dpi=300);










