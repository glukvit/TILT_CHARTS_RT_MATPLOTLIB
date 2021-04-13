#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing
from screeninfo import get_monitors
#for m in get_monitors():
#    print(str(m))
print(list(get_monitors()))

a=list(get_monitors())
mn=str(a[0])
mon=mn.split(' ')
for every in mon:
    if 'width=' in every:
	    wght=every[6:]
    elif 'height=' in every:
	    hght=every[7:]

print(wght)
print(hght)
pause=20
plt.ion()
plt.style.use('ggplot')
#col=plt.cm.jet([0,1])
dfP=pd.read_csv('/home/gluk/MIR_TILT_VIZ/PETT/PETT_week.csv', usecols=['HAE','HAN'])
ln=dfP['HAE'].size
#print(ln)
ncol=ln
colors=plt.cm.jet(np.linspace(0,1,ncol))
my_dpi=88

fig1,(ax1) =plt.subplots(1,1,sharex='all', sharey='row',figsize=(0.65*1920/2.45/my_dpi, 1080/2.45/my_dpi), dpi=my_dpi)#, figsize=(10,10))
fig2,(ax2) =plt.subplots(1,1,sharex='all', sharey='row',figsize=(0.65*1920/2.45/my_dpi, 1080/2.45/my_dpi), dpi=my_dpi)
fig3,(ax3) =plt.subplots(1,1,sharex='all', sharey='row',figsize=(0.65*1920/2.45/my_dpi, 1080/2.45/my_dpi), dpi=my_dpi)
#plt.gca().set_aspect('equal', adjustable='box')

while True:

    dfP=pd.read_csv('/home/gluk/MIR_TILT_VIZ/PETT/PETT_week.csv')
    dfP['HAEP']=dfP['HAE']
    dfP['HANP']=dfP['HAN']
    dfI=pd.read_csv('/home/gluk/MIR_TILT_VIZ/IVST/IVST_week.csv')
    dfI['HAEI']=dfI['HAE']#*(-1)
    dfI['HANI']=dfI['HAN']#*(-1)
    dfPR=pd.read_csv('/home/gluk/MIR_TILT_VIZ/PETR/PETR_week.csv')
    dfPR['HAEPR']=dfPR['HAE']
    dfPR['HANPR']=dfPR['HAN']

#    df=pd.concat([dfP['HAEP'],dfP['HANP'],dfI['HAEI'],dfI['HANI'], dfPR['HAEPR'], dfPR['HANPR']],axis=1)
#    df_norm=(df - df.mean()) / (df.max() - df.min()) #Нормализация четырех каналов
#    print(df_norm)

    ax1.scatter(dfP['HAEP'],dfP['HANP'], s=1, marker='.', c=colors)
#    ax1.axis('squre')
    ax2.scatter(dfI['HAEI'],dfI['HANI'], s=1, marker='.', c=colors)
    ax3.scatter(dfPR['HAEPR'],dfPR['HANPR'], s=1, marker='.', c=colors)


    plt.pause(pause)
