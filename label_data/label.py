import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

data = pd.read_csv('data_label_2019.csv')

#visualize AH1N1
f, ax = plt.subplots(6, 2, sharey=True, figsize=(15,15))
f.tight_layout(pad=3.0)
year = 2009
data_2009 = data[data['year'] == year]['Ah1n1']
choose = {'2009':[range(35,40)], '2010':[], '2011':[range(111,118), range(120, 128), range(130, 148)], '2012':[], '2013':[range(222,237)], 
          '2014':[range(268, 275)], '2015':[range(323, 333)], '2016':[range(384,390)], '2017':[range(434, 450)], 
          '2018':[range(490, 502)], '2019':[range(555, 567)], '2020':[]}

choose_list = {}
for key in choose.keys():
    tmp = []
    for rage in choose[key]:
        tmp.append([x for x in rage])
    choose_list[key] = tmp

years = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
for i in range(2):
    for j in range(6):
        year = years[i*6+j]
        data1 = data[data['year'] == year]['Ah1n1']
        ax[j][i].plot(data1)
        for idx in choose_list[str(year)]:
            ax[j][i].plot(data1[idx], color='r')
        ax[j][i].set_title(str(year) + '_AH1N1')
    
f.savefig('Ah1n1.png')

#visualize AH3
f, ax = plt.subplots(6, 2, sharey=True, figsize=(15,15))
f.tight_layout(pad=3.0)
choose = {'2009':[range(11,29)], '2010':[range(79,91)], '2011':[], '2012':[range(175, 184)], '2013':[range(222,242), range(250, 257)], 
          '2014':[range(277, 286)], '2015':[range(332, 362)], '2016':[range(392,400)], '2017':[range(447, 462)], 
          '2018':[range(507, 518)], '2019':[], '2020':[]}
choose_list = {}
for key in choose.keys():
    tmp = []
    for rage in choose[key]:
        tmp.append([x for x in rage])
    choose_list[key] = tmp

years = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
for i in range(2):
    for j in range(6):
        year = years[i*6+j]
        data1 = data[data['year'] == year]['Ah3']
        ax[j][i].plot(data1)
        for idx in choose_list[str(year)]:
            ax[j][i].plot(data1[idx], color='r')
        ax[j][i].set_title(str(year) + '_AH3')
    
f.savefig('Ah3.png')

#visualize B
f, ax = plt.subplots(6, 2, sharey=True, figsize=(15,15))
f.tight_layout(pad=3.0)
choose = {'2009':[range(9,33)], '2010':[range(61,65), range(75,84), range(87,102)], 
          '2011':[range(105,109)], '2012':[range(161, 174), range(192, 207)], '2013':[range(247,260)], 
          '2014':[range(267, 276), range(278,283), range(297,312)], '2015':[], '2016':[range(384,391)], 
          '2017':[range(435, 449), range(456,464)], '2018':[range(514, 520)], '2019':[range(544,548), range(552,559),range(560,566)], '2020':[]}
choose_list = {}
for key in choose.keys():
    tmp = []
    for rage in choose[key]:
        tmp.append([x for x in rage])
    choose_list[key] = tmp

years = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
for i in range(2):
    for j in range(6):
        year = years[i*6+j]
        data1 = data[data['year'] == year]['B']
        ax[j][i].plot(data1)
        for idx in choose_list[str(year)]:
            ax[j][i].plot(data1[idx], color='r')
        ax[j][i].set_title(str(year) + '_B')
f.savefig('B.png')