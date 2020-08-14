# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 11:28:45 2020

@author: julie
"""


#Import necessary modules
import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
import seaborn as seabornInstance 
from sklearn.linear_model import LinearRegression
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

#Plot linear regression 
fig = plt.figure(figsize = (8,5), dpi = 300)
x = Data['Sleep hours']
y = Data['Z-Score']
plt.scatter(x,y)
#Putting labels
plt.xlabel('Hours of sleep (hrs)')
plt.ylabel('Z-Score')
plt.title('Sleep hours versus Z-score')

#Removing spines
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')

model = LinearRegression(fit_intercept = True)
model.fit(x[:, np.newaxis], y)
xfit = np.linspace(0, 30, 1000)
yfit = model.predict(xfit[:, np.newaxis])
plt.scatter(x,y)
plt.plot(xfit, yfit)

print("Model slope:    ", model.coef_[0])
print("Model intercept:", model.intercept_)