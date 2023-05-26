#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 16:18:42 2023

@author: elliot
"""
globals().clear()

import matplotlib.pyplot as plt
import re



def plotGSR(fileID):
    with open('/Users/elliot/Documents/GitHub/Music_eng/physical test/experiment/data/'+fileID+'_GSR.txt', 'r') as file:
        # Read the contents of the file
        contents = file.read()
        
        num_tem = re.findall(r'\d+', contents)
        
        # Convert the extracted numbers to integers
        num_list = [int(num) for num in num_tem]
        
        end_index= num_list[12:].index(2023)+12 #the last dataindex 
        
        X= [num for num in range(0, len(num_list[12:end_index]))]
        
        plt.plot(X,num_list[12:end_index],color="black", linewidth=2.0)
        
        
        ddot=len(X)/981
        ticks=[]
        label = list(range(1, 13))
        for i in range(10,900,80):#12 songs begin time
            ticks.append(i*ddot)
            
        plt.xticks(ticks,label)
        plt.grid(True)
        
        plt.savefig(fileID+'_GSR.svg',dpi=300,format="svg");
        
        plt.show();




name=['ca12','CH12','AG23',"xo66","kp34"];

for i in range(0,5):
    plotGSR(name[i])


