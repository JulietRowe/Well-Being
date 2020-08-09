# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 09:54:56 2020

@author: julie
"""


import pandas as pd
import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
from IPython import get_ipython

#Clear variables and console
get_ipython().magic('clear')
get_ipython().magic('reset -f')

#Grab necessary .csv file
sg.theme('LightBlue2')

File = sg.popup_get_file('Please select .csv file for analyzing',
                          title = 'Select File',
                          keep_on_top = True)
Data = pd.read_csv(File,
                    header = 0, 
                    keep_default_na = False)

# Data = pd.read_csv('C:/Users/julie/GitHub/Well-Being/RPE.csv',
#                    header = 0, 
#                    keep_default_na = False
#                    )

#Fill blanks with NaN's
Data.replace(r'^\s*$', np.nan, regex = True, inplace = True)

#Create New df, remove NaN, and sort
Data = Data[['Date', 'ID', 'A:C Ratio']].copy()
Data = Data.dropna()
Data.sort_values('ID', inplace = True, ascending = True)
Data['Date'] = pd.to_datetime(Data['Date'])
Data['A:C Ratio'] = pd.to_numeric(Data['A:C Ratio'])

#Creating a dictionary of athletes
dict_of_athletes = {k: v for k, v in Data.groupby('ID')}

#Creating plots
selectfolder = sg.popup_get_folder('Select a folder to save all plots and files', keep_on_top = True)
for key, value in dict_of_athletes.items():
    fig = plt.figure(figsize = (8,5))
    y = dict_of_athletes[key]['A:C Ratio']
    x = dict_of_athletes[key]['Date']
    colors = np.where(dict_of_athletes[key]['A:C Ratio'] >= 2.5, 'r', 'b')
    plt.scatter(x,y, c = colors)
    locator = mdate.MonthLocator()
    plt.gca().xaxis.set_major_locator(locator)
    plt.xticks(rotation = 45)
    plt.xlabel('Date')
    plt.ylabel('A:C Ratio')
    plt.title(key)
    plt.gca().spines['right'].set_color('none')
    plt.gca().spines['top'].set_color('none')
    fig.savefig(selectfolder + "/" + key + ".png")
plt.show()


    
 





