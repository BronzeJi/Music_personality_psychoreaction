#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 19:43:19 2023

@author: elliot
"""


#correaltion between brain wave and emotions

import scipy.io
import matplotlib.pyplot as plt
from dealEEG import get_EEG
import numpy as np

import seaborn as sns

def plot_corre_emotion_brainwave(name):
    data=scipy.io.loadmat('/deal_withsurvey/data/person.mat')#change the data from surve path here
    
    
    tableNo={'AG23':18,'Ca12':1,'CH12':2}
    
    song=data['person'][0][0][0][0][0]
    
    AG=[[] for _ in range(0,12)]
    
    for i in range(0,12):
        AG[i]=song[i][tableNo[name]].tolist()
        
    
    # Transpose the 2D list
    
    AG_transposed_list = [list(row) for row in zip(*AG)]
    
        
    data=get_EEG(name);# get the data from brain wave
        
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
    
    variable1= np.array(aver_data_all)
    variable3= np.array(standdiv_all)
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
    plt.figure(num=name,figsize=(8, 6));
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


xlabel=["Happy","Sad","Energetic","Agressive","Calm","Annoyed","Pleased","Like","emotion"]
ylabel=["Delta","Theta","Low_Alpha","High_Alpha","Low_Beta","High_Beta","Low_gamma","High_gamma"]
plt.figure(num="aver");
sns.heatmap(aver, annot=True,  xticklabels=xlabel, yticklabels=ylabel, cmap="coolwarm")


