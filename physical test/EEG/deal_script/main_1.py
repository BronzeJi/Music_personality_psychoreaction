#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 13:18:52 2023

@author: elliot
"""

from dealEEG import get_EEG,plot_EEG,plot_EEG_heatmap,plot_EEG_aver

name=['ca12','CH12','AG23',''];



for i in range(len(name)):
    data=get_EEG(name[i]);
    
    plot_1=plot_EEG(data,name[i]);
    
    plot_2=plot_EEG_heatmap(data,name[i]);
    
    plot_3=plot_EEG_aver(data,name[i]);