#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 13:20:28 2023

@author: elliot
"""
import numpy as np
import matplotlib.pyplot as plt

"""
get_EEG(name) gives the eeg data.


plot_EEG(data,name) plot attention meditation and signal quality 


plot_EEG_heatmap(data,name) plot the heat map of brain waves


"""




def get_EEG(name):
    #name is the code of each participnts
    generatedChecksum = 0
    checksum = 0
    
    payloadLength = 0
    payloadData = bytearray(32)
    
    signalquality =[]
    attention = []
    meditation = []
    
    
    # Create an empty 2D list with flexible number of columns
    wavetype = 8 #7 type
    wave = [[] for _ in range(wavetype)]
    
    i=0
    
    try:
        file = open(name+"_EEG_test.txt","r") # Open the file for reading, change the path here!
        content = file.read().replace('\n', '')
        
        contentlength=len(content)-42
        for i in range(contentlength):
            currentbyte=content[i:i+2]
            i+=2
            if currentbyte=="aa":
                if content[i:i+2]=="aa":
                    i=i+2
                    payloadLength = int(content[i:i+2],16)
                    i=i+2
                    
                    #check if it is a big package with a length of 32, otherwise it is a small package contains raw data
                    if payloadLength == 32:
                        generatedChecksum = 0
                        for j in range(payloadLength):
                            try:
                                payloadData[j] = int(content[i:i+2],16)
                                i+=2;
                            except:
                                print("aaa")
                                
                            # check sum 
                            generatedChecksum += payloadData[j]
                        checksum = int(content[i:i+2],16)
                        i=i+2;
                        generatedChecksum = (~generatedChecksum) & 0xFF
                        
                        
                        # get data from this big packafe
                        if checksum == generatedChecksum:
                            signalquality.append(payloadData[1])
                            attention.append(payloadData[29])
                            meditation.append(payloadData[31])
                            
                            #wave data:
                            for j in range(0,8):
                                val0=payloadData[4+j*3]
                                val1=payloadData[5+j*3]
                                val2=payloadData[6+j*3]
                                val=val0*65536+val1*256+val2
                                try:
                                    wave[j].append(val)
                                except:
                                    pass
    
                        """ print("get the data" )   
    
                            print(f"SignalQuality: {signalquality}")
                            print(f"Attention: {attention}")
                            print(f"Meditation: {meditation}")   """
    
    except FileNotFoundError:
        print("File not found."+name)
    
    data={'signalquality':signalquality,'attention':attention,'meditation':meditation,'wave':wave,'name':name} 
    return data  
    
    
#data=get_EEG('ca12');    
#plot_EEG('CH12');    
#plot_EEG('AG23');   
#plot_EEG('kp34');   
#plot_EEG('xo66');  


    


def plot_EEG(data,name):                         
    #plot three main factor                       
    ddot=len(data['attention'])/981
    ticks=[]
    label = list(range(1, 14))
    for i in range(10,980,80):#12 songs begin time
        ticks.append(i*ddot)
        
        
    plt.figure(num=data['name'],figsize=(16, 6))
    plt.plot(data['attention'],linewidth=1.0,label="attention")
    plt.plot(data['meditation'],linewidth=1.0,label="meditation")
    plt.plot(data['signalquality'],label="noise")
    #plt.plot(data['wave'][1],linewidth=1.0,label="Theta")
    #plt.plot(data['wave'][2],linewidth=1.0,label="Low_alpha")
    #plt.plot(data['wave'][3],linewidth=1.0,label="High_alpha")
    
    
    plt.yticks(fontsize=18)
    plt.xticks(ticks,label,fontsize=18)
    plt.grid(True)
    plt.legend(fontsize=18)

    plt.savefig(name+"_signal.svg", dpi=300,format="svg");   
    
    
def plot_EEG_aver(data,name):

    ddot=len(data['attention'])/981
    ticksR=[]
    label = list(range(1, 14))
    for i in range(10,980,80):#12 songs begin time
        ticksR.append(round(i*ddot))

    matrix=data['wave']
    num_rows = len(matrix)
    fig, axes = plt.subplots(num_rows, 1, figsize=(8, 2*num_rows))

    for j in range(num_rows):
        aver_data=[]
        variance=[]
        standdiv=[]
        for i in range(0,12):
            anlysis_data=matrix[j][ticksR[i]:ticksR[i+1]]
            aver_data.append(np.mean(anlysis_data))
            variance.append(np.var(anlysis_data))
            standdiv.append(np.std(anlysis_data))
        axes[j].plot(aver_data,linewidth=1.0,label="aver")
        axes[j].plot(standdiv,linewidth=1.0,label="standard divation")
        #set
        axes[j].set_xticks(range(len(standdiv)))
        axes[j].set_xticklabels(label[:-1])
        axes[j].grid(True)
    #plt.legend(fontsize=18)

    # Adjust spacing between subplots
    plt.tight_layout()

    # Show the plot
    #plt.show()
    
    plt.savefig(name+"_average.svg", dpi=300,format="svg");
    

def plot_EEG_heatmap(data,name):
    #plot wavs by heatmap

    #set ticks
    ddot=len(data['attention'])/981
    ticks=[]
    label = list(range(1, 14))
    for i in range(10,980,80):#12 songs begin time
        ticks.append(i*ddot)
        
    # Generate sample matrix
    matrix = data['wave']  # Example matrix with 5 rows and 10 columns

    # Create subplots for each row
    num_rows = len(matrix)
    fig, axes = plt.subplots(num_rows, 1, figsize=(8, 2*num_rows))
    #colormaps = ['viridis', 'hot', 'cool', 'inferno', 'spring','viridis', 'hot', 'cool']  # Example colormaps

    #title
    title=["Delta","Theta","Low_Alpha","High_Alpha","Low_Beta","High_Beta","Low_gamma","High_gamma"]
    
    # Plot heatmap for each row
    for i in range(num_rows):
        #vmin = np.min(matrix[i][:])  # Minimum value of current row
        vmax = np.max(matrix[i][:])  # Maximum value of current row
        
        axes[i].imshow(matrix[i:i+1][:], vmin=0, vmax=vmax, cmap='hot',aspect='auto')
        axes[i].set_title(title[i])
        axes[i].axis('off')
        
        #set
        axes[i].set_xticks(ticks[:-1])
        axes[i].set_xticklabels(label[:-1])
        axes[i].grid(True)
        #cbar = plt.colorbar(im, ax=axes[i])
        #cbar.set_label('Value')

    # Adjust spacing between subplots
    plt.tight_layout()

    # Show the plot
    #plt.show()
    
    plt.savefig(name+"_heatmap.svg",dpi=300, format="svg");