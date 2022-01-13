# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 17:27:42 2022

@author: Owner
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

df = pd.read_excel("C:\\Users\\Owner\\Desktop\\cindy\\論文方向查找\\owid-covid-data.xlsx")

df_Taiwan = df.loc[(df['continent'] == 'Asia') & (df['location'] == 'Taiwan'),['date','new_cases','new_vaccinations']]
df_Taiwan = df_Taiwan[df_Taiwan['new_cases'].notna()]
df_Taiwan = df_Taiwan.fillna(0)

df_Taiwan = df_Taiwan.reset_index().loc[:,['date', 'new_cases', 'new_vaccinations']]

index = int(round(len(df_Taiwan)*0.8,0))
training = df_Taiwan[:index]
testing = df_Taiwan[index:]

training['new_cases_quartile'] = pd.qcut(training['new_cases'], q=4, labels=['0', '1', '2', '3'])
training['new_vaccinations_quartile'] = np.where(training['new_vaccinations'] > 0, '1', '0')

state = []
for i in range(len(training)):
    state.append('(' + str(training.iloc[i,3]) + ' ' + str(training.iloc[i,4]) + ')')
    
training["state"] = state
data = training[["date","state"]]

action = pd.read_excel(r"C:\Users\Owner\Desktop\cindy\ORA\final project\all_data.xlsx")
action = action[["date","acttion"]]        

all_data = pd.merge(data,action, on='date')    
all_data = all_data.dropna()

all_data['next_state'] = all_data['state'].shift(-1)
all_data = all_data.dropna()

def count_pro(c_status,freq):
    freq = pd.DataFrame(freq)
    freq = freq.reset_index(drop = False)
    temp = freq.groupby("acttion")      
    next_action = np.unique(freq["acttion"])
    data = pd.DataFrame()
    for i in next_action:
        tmp2 = temp.get_group(i)
        tmp2 = np.array(tmp2)
        tmp2[:,2] = tmp2[:,2]/sum(tmp2[:,2])
        full = np.full((len(tmp2[:,2]), 1), c_status)
        ttt = np.concatenate((full, tmp2), axis=1)
        ttt = pd.DataFrame(ttt)
        data = pd.concat([data,ttt],axis=0)
    return data    

all_data = all_data.iloc[:,1:]

l = np.unique(all_data.iloc[:,0])

sector = all_data.groupby("state")
transition_data = pd.DataFrame()
for i in l:  
    temp = sector.get_group(i)
    temp_action = np.unique(temp["acttion"])
    temp_next = np.unique(temp["next_state"])
    freq = temp.groupby(['acttion', 'next_state']).size()
    print(i)
    print(freq)                                                #每個state下每個action會導致下個state發生的次數統計
    print("===========================================")
    data2 = count_pro(i,freq)
    transition_data = pd.concat([transition_data,data2],axis=0)
            
transition_data.to_csv("transitions_Group1.csv", header=False,index=False)    #輸出transition_data 
# =============================================================================
# reward
# =============================================================================
next_status = list(np.unique(all_data["next_state"]))        
   
#reward設置
rwd_value = [-2, 10, -5, 7, -7, 4, -10, 1]

rwd = []
state = []
i = 0
for o in next_status:
    old = str(o)
    state.append(old)
    rwd.append(rwd_value[i])
    i += 1


reward = {"state" : state,
          "reward" : rwd}  
        
reward = pd.DataFrame(reward)        
  
reward.to_csv("rewards_Group1.csv", header=False,index=False)     #輸出reward_data        
