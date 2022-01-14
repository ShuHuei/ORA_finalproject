import os
import pandas as pd
import numpy as np

#------------------------------------------------------------------------------
#存取所有出入境資料並合併
dir = r"C:\Users\Owner\Desktop\cindy\ORA\final project\出入境資料" #設定工作路徑

chose_index = [0,8,11,32,38,47,53,56,62,65,68,71,80,113]  #所需column的位置

filename_excel = []
frames = []

for root,dirs,files in os.walk(dir):
  for file in files:
    filename_excel.append(os.path.join(root,file))
    df = pd.read_csv(os.path.join(root,file)) #CSV轉換成DataFrame
    rr = df.iloc[:,chose_index]   
    frames.append(rr)

result = pd.concat(frames) 

#------------------------------------------------------------------------------
#將出入境資料與整理好的taiwan_action合併

df = pd.read_excel("C:\\Users\\Owner\\Desktop\\cindy\\論文方向查找\\owid-covid-data.xlsx")

t_df = df.loc[(df['continent'] == 'Asia') & (df['location'] == 'Taiwan'),['date','new_cases']]
t_df = t_df[t_df['new_cases'].notna()]
t_df = t_df.fillna(0)

t_df = t_df.reset_index().loc[:,['date', 'new_cases']]

for i in range(len(result.iloc[:,0])):
    old_date = str(result.iloc[i,0])
    new = old_date[0:4] + "-" + str(old_date[4:6]) + "-" + str(old_date[6:])
    result.iloc[i,0] = new

result = result.rename(columns = {'日期':'date'}) #column 改名
all_data = pd.merge(t_df,result, on = 'date') #以date作為key去merge

all_data = pd.merge(t_df,result, on = 'date') #以date作為key去merge

count = []  #所有機場人數加總
for i in range(len(all_data.iloc[:,0])):    
    count.append(sum(all_data.iloc[i,2:]))

all_data = all_data.iloc[:,0:2]
all_data["Entry_Exit_count"] = count  #整理完的資料

#------------------------------------------------------------------------------
#state 離散化
#level-4 最嚴重 level-1 最輕微 (e.g. 入境人數最多 = 1, 確診人數最少 = 1 )

Entry_Exit_count_q = all_data['Entry_Exit_count'].quantile([0.25,0.5,0.75]).tolist() #確診人數4分位數
new_cases_q = all_data['new_cases'].quantile([0.25,0.5,0.75]).tolist() #出入境人數4分位數

#確診人數四分位數: 0  3  8
#出入境人數四分位數: 1775.5  2626.0  3798.5

for i in range(len(all_data)):
    r = all_data.iloc[i,1]
    if r <= new_cases_q[0]:
        all_data.iloc[i,1] = 0
    elif r > new_cases_q[0] and r <= new_cases_q[1] :   
        all_data.iloc[i,1] = 1
    elif r > new_cases_q[1] and r <= new_cases_q[2] : 
        all_data.iloc[i,1] = 2
    else:
        all_data.iloc[i,1] = 3
        
        
for i in range(len(all_data)):
    r = all_data.iloc[i,2]
    if r <= Entry_Exit_count_q[0]:
        all_data.iloc[i,2] = 3
    elif r > Entry_Exit_count_q[0] and r <= Entry_Exit_count_q[1] :   
        all_data.iloc[i,2] = 2
    elif r > Entry_Exit_count_q[1] and r <= Entry_Exit_count_q[2] : 
        all_data.iloc[i,2] = 1
    else:
        all_data.iloc[i,2] = 0       

#------------------------------------------------------------------------------
all_data.new_cases = all_data.new_cases.astype(int)

state = []
for i in range(len(all_data)):
    state.append('(' + str(all_data.iloc[i,1]) + ' ' + str(all_data.iloc[i,2]) + ')')
    
all_data["state"] = state
all_data = all_data[["date","state"]]
        
action = pd.read_excel(r"C:\Users\Owner\Desktop\cindy\ORA\final project\all_data.xlsx")
action = action[["date","acttion"]]        

all_data = pd.merge(all_data,action, on='date')    
all_data = all_data.iloc[:-3,:]

all_data = all_data.iloc[::-1]   # df倒敘
    
next_state = list(all_data["state"])
next_state.pop(0)

next_state.append(00)

all_data["next_state"] = next_state

all_data = all_data.iloc[:-1,:]

#------------------------------------------------------------------------------   
#計算每個transition的機率

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
all_data = all_data.dropna()

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
            
transition_data.to_csv("transitions_Group2.csv", header=False,index=False)    #輸出transition_data        
#------------------------------------------------------------------------------ 

next_status = list(np.unique(all_data["next_state"]))        
   
#reward設置
rwd_value = {"0":5,
             "1":1,
             "2":-3,
             "3":-5}

rwd = []
state = []
for o in next_status:
    old = str(o)
    state.append(old)
    rwd.append(rwd_value[old[1]] + rwd_value[old[3]])


reward = {"state" : state,
          "reward" : rwd}  
        
reward = pd.DataFrame(reward)        
  
reward.to_csv("rewards_Group2.csv", header=False,index=False)     #輸出reward_data  
    
    

