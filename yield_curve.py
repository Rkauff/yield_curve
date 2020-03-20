 # -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 16:40:10 2020

@author: Ryan Kauffman
"""

from matplotlib import pyplot as plt
import requests
import bs4

us_treasury_url = 'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield'

us_treasury_yields = requests.get(us_treasury_url)
us_treasury_yields_string = bs4.BeautifulSoup(us_treasury_yields.text, 'html.parser')
yield_curve_date = us_treasury_yields_string.select('div.updated')[0]
yield_curve_labels = us_treasury_yields_string.select('th')[1:11] #Treasury Security Labels
yield_curve_values = us_treasury_yields_string.select('td.text_view_data')[118:128] #Treasury Security Values

x_axis = [] 
y_axis = []

yield_curve_date = yield_curve_date.getText()

for x in range(len(yield_curve_values)):
    x_axis.append(yield_curve_labels[x].getText()) 
    y_axis.append(float(yield_curve_values[x].getText()))

font = {'family': 'serif', 'color':  'blue', 'weight': 'normal', 'size': 12}

def inversion():
    """To determine whether the yield curve is normal, flat, or inverted."""
    if y_axis[0] > y_axis[9]:
        return 'The Yield curve is inverted by ' + str(int(abs(y_axis[9] - y_axis[0]) * 100)) + ' bps.*'
    elif y_axis[0] == y_axis[9]:
        return 'The Yield curve is flat.*'
    else:
        return 'The Yield curve is normal by ' + str(int(abs(y_axis[9] - y_axis[0]) * 100)) + ' bps.*'

plt.figure(figsize=(10, 5))
plt.title("Yield Curve as of " + yield_curve_date)
plt.scatter(x_axis, y_axis, c='r', label='Treasury Securities')
plt.plot(x_axis, y_axis, label="Yield Curve")
plt.legend()
plt.ylim(bottom=0, top=3)  #To set the y-axis at 0, Top at 3.
plt.xlabel('Treasury Security', fontdict=font)
plt.ylabel('Rate (%)', fontdict=font)
graph_description = plt.text(0, 2.7, inversion(), bbox=dict(facecolor='yellow', alpha=0.5))
graph_description2 = plt.text(0, 2.5, str(x_axis[0]) + " T-bill against the " + str(x_axis[9]) + " T-note", bbox=dict(facecolor='yellow', alpha=0.5))
