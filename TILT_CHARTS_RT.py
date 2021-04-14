#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing
from screeninfo import get_monitors
import paramiko #импорт модуля для ssh соедиения
import os

dest_ip="10.10.4.167"
usernm="gluhov"
paswd="iwt"

pause=5
plt.ion()
plt.style.use('ggplot')

ssh=paramiko.SSHClient() #создание класса SSHClient.
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #добавление ключа безопасносности не задавая лишних вопросов

path='/home/gluhov/TEMP_DATA/STREAM'

ssh.connect(dest_ip,username=usernm,password=paswd)  #соединение по ssh

command = "ls"+" "+path
stdin, stdout, stderr = ssh.exec_command(command) #выполнение команд терминала. Получаем список директорий по указанному адресу.
result=stdout.read().split() #Считываем список со стандартного вывода, получаем строку байтов.

#print(list(result))
file_list = [] #Здесь будет список файлов  директории сервера /home/gluhov/TEMP_DATA/STREAM
for every in list(result):
    every = every.decode('utf-8') #Переводим байт в стринг
    every = os.path.join(path, every) # Создаем полный путь до каждого файла в удаленной директории.
    file_list.append(every) #Складываем имена файлов в список
print(file_list) # лист из файлов которые будем получать
ssh = ssh.open_sftp()
remote_file = ssh.open(file_list[1])
#print(remote_file)
try:
    dfP=pd.read_csv(remote_file, usecols=['HAE','HAN'])
    print('Файл для длины скачивается')
finally:
    remote_file.close()

#for m in get_monitors():
#    print(str(m))
#print(list(get_monitors()))

a=list(get_monitors())
mn=str(a[0])
mon=mn.split(' ')
for every in mon:
    if 'width=' in every:
	    wght=every[6:]
    elif 'height=' in every:
	    hght=every[7:]

#print(wght)
#print(hght)
#col=plt.cm.jet([0,1])

ln=dfP['HAE'].size
print(ln)
ncol=ln
colors=plt.cm.jet(np.linspace(0,1,ncol))
my_dpi=88

fig1,(ax1) =plt.subplots(1,1,sharex='all', sharey='row',figsize=(0.65*1920/2.45/my_dpi, 1080/2.45/my_dpi), dpi=my_dpi)#, figsize=(10,10))
fig2,(ax2) =plt.subplots(1,1,sharex='all', sharey='row',figsize=(0.65*1920/2.45/my_dpi, 1080/2.45/my_dpi), dpi=my_dpi)
fig3,(ax3) =plt.subplots(1,1,sharex='all', sharey='row',figsize=(0.65*1920/2.45/my_dpi, 1080/2.45/my_dpi), dpi=my_dpi)
#plt.gca().set_aspect('equal', adjustable='box')
#
def get_remote_files(file_list):
    for every in file_list:
  #      ssh = ssh.open_sftp()
        remote_file = ssh.open(every)
        print(every)
        try:
             if 'IVST' in every :
                dfI = pd.read_csv(remote_file)
 #               print(every)
 #               print(dfI)
             elif 'KLYT' in every:
  #              print(every)
                dfK = pd.read_csv(remote_file)
   #             print(dfK)
             elif 'IVS1' in every:
   #             print(every)
                dfI1 = pd.read_csv(remote_file)
    #            print(dfI1)
#            print(dfP)
        finally:
            remote_file.close()
    return(dfI,dfK,dfI1)

while True:
     dfI,dfK,dfI1 = get_remote_files(file_list)

     ax1.scatter(dfI['HAE'],dfI['HAN'], s=1, marker='.', c=colors)
     ax2.scatter(dfK['HAE'],dfK['HAN'], s=1, marker='.', c=colors)
     #ax3.scatter(dfI1['HAE'],dfI1['HAN'], s=1, marker='.', c=colors)

 
     plt.pause(pause)
        
# # Нормализация по всем каналам пока не используем
# #    df=pd.concat([dfP['HAEP'],dfP['HANP'],dfI['HAEI'],dfI['HANI'], dfPR['HAEPR'], dfPR['HANPR']],axis=1)
# #    df_norm=(df - df.mean()) / (df.max() - df.min()) #Нормализация четырех каналов
# #    print(df_norm)

#     ax1.scatter(dfP['HAEP'],dfP['HANP'], s=1, marker='.', c=colors)
#     ax2.scatter(dfI['HAEI'],dfI['HANI'], s=1, marker='.', c=colors)
#     ax3.scatter(dfPR['HAEPR'],dfPR['HANPR'], s=1, marker='.', c=colors)
    
