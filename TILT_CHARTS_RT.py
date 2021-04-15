#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing
from screeninfo import get_monitors
import paramiko #импорт модуля для ssh соедиения
import os
import sys

dest_ip = "10.10.4.167"
usernm = "gluhov"
paswd = "iwt"

pause = 5
plt.ion()
plt.style.use('ggplot')

path = '/home/gluhov/TEMP_DATA/STREAM'
coef_path = '/home/gluk/my_bin/TILT_VIEW/conf_koef.txt'

with open (coef_path, 'r' ) as file: #Получаем из файла аппаратурные коэффициенты
    for every in file:
        if 'KLYT' in every:
            strng=every.split(' ')
            KLYT_coef_HAE=float(strng[1])
            KLYT_coef_HAN=float(strng[2])
        elif 'IVST' in every:
            strng=every.split(' ')
            IVST_coef_HAE=float(strng[1])
            IVST_coef_HAN=float(strng[2])
        elif 'PETT' in every:
            strng=every.split(' ')
            PETT_coef_HAE=float(strng[1])
            PETT_coef_HAN=float(strng[2])

#sys.exit()
ssh=paramiko.SSHClient() #создание класса SSHClient.
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #добавление ключа безопасносности не задавая лишних вопросов
ssh.connect(dest_ip,username=usernm,password=paswd)  #соединение по ssh

command = "ls"+" "+path
stdin, stdout, stderr = ssh.exec_command(command) #выполнение команд терминала. Получаем список директорий по указанному адресу.
result=stdout.read().split() #Считываем список со стандартного вывода, получаем строку байтов.

file_list = [] #Здесь будет список файлов  директории сервера /home/gluhov/TEMP_DATA/STREAM
for every in list(result):
    every = every.decode('utf-8') #Переводим байт в стринг
    every = os.path.join(path, every) # Создаем полный путь до каждого файла в удаленной директории.
    file_list.append(every) #Складываем имена файлов в список
print(file_list) # лист из файлов которые будем получать
ssh = ssh.open_sftp()
remote_file = ssh.open(file_list[1])

try:
    dfP = pd.read_csv(remote_file, usecols=['HAE','HAN'])
    print('Файл для длины скачивается')
finally:
    remote_file.close()

a = list(get_monitors()) #Получаем список параметров мониторов
mn = str(a[0]) #Превращаем в стриг параметры первого монитора
mon = mn.split(' ') #Разбиваем стринг на слова
for every in mon: #Перебираем список
    if 'width=' in every:  #Если находим ширину монитора то, 
	    wght=every[6:] #Получаем ширину 
    elif 'height=' in every: # И длину
	    hght=every[7:]

ln=dfP['HAE'].size # Длина столбца по файла из списка file_list Длина нужна для определения количества градаций цветов
print(ln)
ncol=ln #Переменная для задания шага градаций цветов
colors = plt.cm.jet(np.linspace(0,1,ncol)) #С помощью матрицы задается количество градаций цветов
my_dpi = 88 #Разрешение монитора
# Создаем субплоты размеры исходя из размеров монитора и разрешения коэффициенты 0.65, 2.45 подбирались опытным путем,
# чтобы получить окно приближенное к квадрату
fig1,(ax1) = plt.subplots(1,1,sharex='all', sharey='row',figsize=(0.65*1920/2.45/my_dpi, 1080/2.45/my_dpi), dpi=my_dpi) 
fig2,(ax2) = plt.subplots(1,1,sharex='all', sharey='row',figsize=(0.65*1920/2.45/my_dpi, 1080/2.45/my_dpi), dpi=my_dpi)
fig3,(ax3) = plt.subplots(1,1,sharex='all', sharey='row',figsize=(0.65*1920/2.45/my_dpi, 1080/2.45/my_dpi), dpi=my_dpi)
#plt.gca().set_aspect('equal', adjustable='box')
#
def get_remote_files(file_list): # Процедура удаленного считывания данных. На вход список считываемых файлов
    for every in file_list: # Перебираем список считываемых файлов
  #      ssh = ssh.open_sftp()
        remote_file = ssh.open(every) #Считываем каждый файл из списка
        print(every)
        try:
             if 'IVST' in every : #Если станция IVST, то        
                dfI = pd.read_csv(remote_file) # Присваиваем данные датафрейму для IVST
 
             elif 'KLYT' in every:
  
                dfK = pd.read_csv(remote_file) #Для KLYT
   
             elif 'IVS1' in every:
   
                dfI1 = pd.read_csv(remote_file) # Для тестовой станции IVS1 

        finally:
            remote_file.close() #Закрываем открытый файл
    return(dfI,dfK,dfI1) #Возвращаем из процедуры три датафрейма

while True: # Основной цикл обновления 
     dfI,dfK,dfI1 = get_remote_files(file_list) #Процедура считывания файлов с удаленного сервера через ssh. На вход список файлов
     #на выходе три датафрейма с данными по станциям
     # Прикручиваем аппаратурные коэффициенты
     dfI['HAE'] = dfI['HAE'] * IVST_coef_HAE
     dfI['HAN'] = dfI['HAN'] * IVST_coef_HAN
     
     dfK['HAE'] = dfK['HAE'] * KLYT_coef_HAE
     dfK['HAN'] = dfK['HAN'] * KLYT_coef_HAN

     
     ax1.scatter(dfI['HAE'],dfI['HAN'], s = 1, marker = '.', c = colors)
     ax2.scatter(dfK['HAE'],dfK['HAN'], s = 1, marker = '.', c = colors)
     #ax3.scatter(dfI1['HAE'],dfI1['HAN'], s=1, marker='.', c=colors)

 
     plt.pause(pause)
        
# # Нормализация по всем каналам пока не используем
# #    df=pd.concat([dfP['HAEP'],dfP['HANP'],dfI['HAEI'],dfI['HANI'], dfPR['HAEPR'], dfPR['HANPR']],axis=1)
# #    df_norm=(df - df.mean()) / (df.max() - df.min()) #Нормализация четырех каналов
# #    print(df_norm)

#     ax1.scatter(dfP['HAEP'],dfP['HANP'], s=1, marker='.', c=colors)
#     ax2.scatter(dfI['HAEI'],dfI['HANI'], s=1, marker='.', c=colors)
#     ax3.scatter(dfPR['HAEPR'],dfPR['HANPR'], s=1, marker='.', c=colors)
    
