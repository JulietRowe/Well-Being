# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 10:31:32 2020

@author: julie
"""

#Import necessary modules
import pandas as pd
import numpy as np
import PySimpleGUI as sg
import matplotlib.pyplot as plt
from IPython import get_ipython

#Clear variables and console
get_ipython().magic('clear')
get_ipython().magic('reset -f')

#Select .csv file for data analysis
sg.theme('LightBlue2')

File = sg.popup_get_file('Please select .csv file for analyzing',
                          title = 'Select File',
                          keep_on_top = True)
Data = pd.read_csv(File,
                    header = 0, 
                    keep_default_na = False)

# Data = pd.read_csv('C:/Users/julie/GitHub/Well-Being/Subjective.csv',
#                     header = 0, 
#                     keep_default_na = False
#                     )

#Fill blanks with NaN's
Data.replace(r'^\s*$', np.nan, regex = True, inplace = True)

#Sort Data based on ID
Data.sort_values('ID', inplace = True, ascending = True)

#Redine df with needed columns
Data = Data[['Sleep hours', 'Monitoring Z-Score']].copy()

#Rename column name
Data.rename(columns = {"Monitoring Z-Score": "Z-Score"}, inplace = True)

#Drop all NaNs
Data = Data.dropna()

#Define dtype for specific columns
Data['Sleep hours'] = Data['Sleep hours'].astype(float)
Data['Z-Score'] = Data['Z-Score'].astype(float)


def estimate_coef(x,y):
    #number of obersvations/points
    n = np.size(x)
    
    #Mean of x and y vector
    m_x, m_y = np.mean(x), np.mean(y)
    
    #Calculating cross-deviation and deviations about x
    SS_xy = np.sum(y*x) - n*m_y*m_x
    SS_xx = np.sum(x*x) - n*m_x*m_x
    
    #Calculating regression coefficients
    slope = SS_xy / SS_xx
    intercept = m_y - slope*m_x
    
    return(intercept, slope)
    
def plot_regression_line(x,y,b):
    #Creating a figure
    fig = plt.figure(figsize = (8,5), dpi = 300)
    
    #plotting the actual ploints as scatter plot
    plt.scatter(x,y, color = "b", marker = "o", s = 30)
    
    #Predicted response vecotr
    y_pred = b[0] + b[1]*x
    
    #Plotting the regression line
    plt.plot(x, y_pred, color = "r")
    
    #Putting labels
    plt.xlabel('Hours of sleep (hrs)')
    plt.ylabel('Z-Score')
    plt.title('Sleep hours versus Z-score')
    
    #Removing spines
    plt.gca().spines['right'].set_color('none')
    plt.gca().spines['top'].set_color('none')
    
    #Function to show plot
    plt.show()
    
def main():
    #Observations
    x = Data['Sleep hours']
    y = Data['Z-Score']
    
    #Estimating coefficients
    b = estimate_coef(x, y)
    print("Estimated coefficients:\nintercept = {} \nslope = {}".format(str(b[0]), str(b[1]))) 
          
    #Plotting the regression line
    plot_regression_line(x, y, b)
    
if __name__ == "__main__":
    main()