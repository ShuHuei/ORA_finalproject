# ORA_finalproject
###### `January 14, 2022 / by Shu-Huei Yang and Meng-Xiu Lu`
<!-- <br /> -->

#### This study use **Markov Decision Process (MDP)** models to provide prevemtion strategy suggestions of the COVID-19.

#### Contents:
1. [Motivation and Background](#Motivation-and-Background)
2. [Methodology](#Methodology)
3. [Analysis Result in Group1](#Part-I:-Analysis-Result-in-Group1)
4. [Analysis Result in Group2](#Part-II:-Analysis-Result-in-Group2)
5. [Conclusion](#Conclusion)
6. [Reference](#Reference)
<br />

## Motivation and Background
Because of the COVID-19 outbreak in China, all the world are greatly affected. Epidemic prevention strategies of each country are highly valued. Especially when the epidemic is not getting better, variant virus appears. Now we can collect data for two years, it may exist some information to let us investigate the strategy we have done before. If we can use historical data to give suitable strategy, we can make a small contribution to specific country.

## Methodology
We choose **Markov Decision Process** to analysis our problem. The main dependent variable is the number of confiremed cases in our target country and we will collect other variables like number of travelers of our target country, number of confirmed cases in neighbors countries, the distance of interested countries, the number of people entering and leaving the country and  the number of vaccination to help us make a better decision.

In this methodology, we need to decide the state, action, transition matrix and reward. For simplified, we choose three variables to define the state space in the beginning(the number of confiremed cases in our target country / the number of vaccination / the number of people entering and leaving the country). And we seperate the three variables to two groups. Group1 are # of confirmed and vaccination. Group2 are # of confirmed and # of entering and leaving.

The action space represents the behaviors of prevention strategy, we refer th prevention timeline of Taiwan. Here are some action we will focus on : mask, airport control and  vaccination. 

As for the reward space, we need to discretize the variables we focus on first. We use quantile for discretization and the picture below is the boxplot of # of confirmed of Taiwan. We can see that most confirmed number are low. Then we use this kind of method to define our state. 
<table style="width:80%" class="table for Q25" >
  <thead>
    <tr >
        <th scope="col" width="40%"><img src="https://github.com/ShuHuei/ORA_finalproject/blob/main/boxplot.png" width="100%" height="100%"></th>
        <th scope="col" align="center">
            <table>
                <thead>
                    <tr>
                        <th>min</th>
                        <th>Q25</th>
                        <th>Q50</th>
                        <th>Q75</th>
                        <th>Max</th>
                    </tr>
                    <tr>
                        <th>-2</th>
                        <th>0</th>
                        <th>3</th>
                        <th>8</th>
                        <th>723</th>
                    </tr>
                    <tr>
                        <img src="https://github.com/ShuHuei/ORA_finalproject/blob/main/fordemo.png" width="100%" height="100%">
                    </tr>
                </thead>
            </table>    
        </th>
    </tr>
  </thead>
</table>

In Group1 state, # of confirmed case is less than 0 then the first location of our state is 0. Others and so on. The second location is about the number of vaccination. Because the time range of data is 2020/01 to 2021/12, most of the number of vaccination are zero. The second location of state we only use the variable that whether the # of vaccination is more than zero.

Then we can define our state in Group1 as below:
<table align="center">
    <thead>
        <tr>
            <td>state</td>
            <th align="center">(3 0)</th>
            <th align="center">(2 0)</th>
            <th align="center">(1 0)</th>
            <th align="center">(0 0)</th>
        </tr>
        <tr>
            <td>meaning</td>
            <th># confirmed > 8<br>
                no vaccination</th>
            <th>3 < # confirmed < 8<br>
                no vaccination</th>
            <th>0 < # confirmed < 3<br>
                no vaccination</th>
            <th># confirmed < 0<br>
                no vaccination</th>
        </tr>
        <tr>
            <td>state</td>
            <th align="center">(3 1)</th>
            <th align="center">(2 1)</th>
            <th align="center">(1 1)</th>
            <th align="center">(0 1)</th>
        </tr>
        <tr>
            <td>meaning</td>
            <th># confirmed > 8<br>
                vaccination</th>
            <th>3 < # confirmed < 8<br>
                vaccination</th>
            <th>0 < # confirmed < 3<br>
                vaccination</th>
            <th># confirmed < 0<br>
                vaccination</th>
        </tr>
    </thead>
</table>    

So does in Group2.

Then we can use this self-defined state and historical data to calculate the transition matrix. Some of the results are as follows.
<img src="https://github.com/ShuHuei/ORA_finalproject/blob/main/transition%20matrix.PNG" width="100%" height="100%">

Now we can define the reward. All the state we have explained above. So we know that the state (3 0) Group1 is the worst case and the state (0 1) is the best case. The rewards are defined in the following table.
<table align="center">
    <thead>
        <tr>
            <td>state</td>
            <th align="center">(3 0)</th>
            <th align="center">(2 0)</th>
            <th align="center">(1 0)</th>
            <th align="center">(0 0)</th>
            <th align="center">(3 1)</th>
            <th align="center">(2 1)</th>
            <th align="center">(1 1)</th>
            <th align="center">(0 1)</th>
        </tr>
        <tr>
            <td>reward</td>
            <th align="center">-10</th>
            <th align="center">-7</th>
            <th align="center">-5</th>
            <th align="center">-2</th>
            <th align="center">1</th>
            <th align="center">4</th>
            <th align="center">7</th>
            <th align="center">10</th>
        </tr>
    </thead>
</table> 

<br>
So does in Group2

<table align="center" class="AAA">
    <thead>
        <tr>
            <td>state</td>
            <th align="center">(0 0)</th>
            <th align="center">(0 1)</th>
            <th align="center">(0 2)</th>
            <th align="center">(0 3)</th>
            <th align="center">(1 0)</th>
            <th align="center">(1 1)</th>
            <th align="center">(1 2)</th>
            <th align="center">(1 3)</th>
        </tr>
        <tr>
            <td>reward</td>
            <th align="center">10</th>
            <th align="center">6</th>
            <th align="center">2</th>
            <th align="center">0</th>
            <th align="center">6</th>
            <th align="center">2</th>
            <th align="center">-2</th>
            <th align="center">-4</th>
        </tr>
        <tr>
            <td>state</td>
            <th align="center">(2 0)</th>
            <th align="center">(2 1)</th>
            <th align="center">(2 2)</th>
            <th align="center">(2 3)</th>
            <th align="center">(3 0)</th>
            <th align="center">(3 1)</th>
            <th align="center">(3 2)</th>
            <th align="center">(3 3)</th>
        </tr>
        <tr>
            <td>reward</td>
            <th align="center">2</th>
            <th align="center">-2</th>
            <th align="center">-6</th>
            <th align="center">-8</th>
            <th align="center">0</th>
            <th align="center">-4</th>
            <th align="center">-8</th>
            <th align="center">-10</th>
        </tr>
    </thead>
</table>    

The algorithm will learn from historical data and help us to make decision. The following analysis results can be discussed in two sections, which are Group1 and Group2 respectively. 
And we arrange the current results in the following table.

<table align="center" class="table justify-content-center" >
  <thead>
    <tr >
      <th scope="col"></th> 
      <th scope="col" >Group 1</th>
      <th scope="col" >Group 2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">State</th>
      <td> # of confirmed <br> vaccination or not</td>
      <td># of confirmed  <br> # of entering and leaving</td>
    </tr>
    <tr>
      <th scope="row">Action</th>
      <td colspan="2">Mask (M)<br>
                      Mask + Airport control (MA)<br>
                      Mask + Airport control + Vaccination (MAV)<br>
                      Mask + Airport control + Vaccination rate > 20% (MAVV)<br>
      </td>
    </tr>
    <tr>
      <th scope="row">Reward</th>
      <td colspan="2">on the table above repectively</td>
    </tr>
  </tbody>
</table>



<br/>

## Part I: Analysis Result in Group1

### **Data Collection**
The dataset used for this study is # of confirmed and vaccination data [github](https://github.com/owid/covid-19-data/tree/master/public/data).  The columns *date, new_cases and new_vaccinations* are the variable we use in Group1. Then we collect the timeline of the strategies we focus on and type into a excel and then join with the table which includes date, new_cases and new_vaccinations.
<br>
<img src="https://github.com/ShuHuei/ORA_finalproject/blob/main/timeline.PNG" width=100% height=100% align="center"/>

Calculate the transition matrix.

### **Markov Decision Process via Value Iteration**
In each iteration, the algorithm calculates the expected reward for each action under the current state. Then, it selects the action which brings the highest reward, and updates the value table of the current state with the maximal reward value. The algorithm will stop until the improvement is small enough, which implies convergence.

### **Result**

As the below convergence diagram shows, the iteration process did converge within the first 100 iterations. Also, the value shows that state (0 1) which is the best case has the highest reward, and the state (3 0) with the lowest value. The value table indicates that the agent tends to move forward to the states with a higher reward, which meets our expectation.

<img src="https://github.com/ShuHuei/ORA_finalproject/blob/main/group1%20iteration.PNG" width=90% height=90% align="center"/>

<br />

From the analysis above we can easily see that the value iteration method helps determine which state is better according to the reward function. And we can conclude the action we can decide in eac state in the folloing table.
<br>

<img src="https://github.com/ShuHuei/ORA_finalproject/blob/main/group1%20result.PNG" width=90% height=90% align="center"/>

The conclusion in Group1 are
+ When we discuss the # of confirmed and vaccination or not, most of the strategies will be MAV (Mask, Airport control and vaccination).
+ One interesting thing is that when the # of confirmed is high but we haven’t started to vaccinate, it will recommend to achieve 20% vaccination rate.

<br/>


## Part-II: Analysis Result in Group2

### **Data Collection**
In this part, we also use the data from github. But we add a new variable which is about the number of arrival and departure of Taiwan. This data is from the open data of the [government](https://data.moi.gov.tw/moiod/Data/DataDetail.aspx?oid=905908DA-0EF6-4B24-87B0-35B7EDA4CFD2). We download all of these excels and sum the number of each airport and port. Then do the same thing as in the first part. We use quantile to discretize the variable.

**State and Reward Settings**
We have posted this table in the above. But we don't explain it. 
The state in Group2 still has two location. The first location is the same as Group1 which indicate that the # of confirmed. "0" means # of confirmed < 0 and "3" means # of confirmed > 8. And the second location is about the number of arrival and departure. When the epidemic is stable, the number of arrival and departure will be relatively high, and vice versa. So the second location of the state is defined as "0" means the number of arrival and departure is high and "3" means the number of arrival and departure is low. 

That's why the reward of (0 0) is the highest which means that the # of confirmed < 0 and the number of arrival and departure is high and (3 3) is the lowest reward.
<br>
<table align="center" class="AAA">
    <thead>
        <tr>
            <td>state</td>
            <th align="center">(0 0)</th>
            <th align="center">(0 1)</th>
            <th align="center">(0 2)</th>
            <th align="center">(0 3)</th>
            <th align="center">(1 0)</th>
            <th align="center">(1 1)</th>
            <th align="center">(1 2)</th>
            <th align="center">(1 3)</th>
        </tr>
        <tr>
            <td>reward</td>
            <th align="center">10</th>
            <th align="center">6</th>
            <th align="center">2</th>
            <th align="center">0</th>
            <th align="center">6</th>
            <th align="center">2</th>
            <th align="center">-2</th>
            <th align="center">-4</th>
        </tr>
        <tr>
            <td>state</td>
            <th align="center">(2 0)</th>
            <th align="center">(2 1)</th>
            <th align="center">(2 2)</th>
            <th align="center">(2 3)</th>
            <th align="center">(3 0)</th>
            <th align="center">(3 1)</th>
            <th align="center">(3 2)</th>
            <th align="center">(3 3)</th>
        </tr>
        <tr>
            <td>reward</td>
            <th align="center">2</th>
            <th align="center">-2</th>
            <th align="center">-6</th>
            <th align="center">-8</th>
            <th align="center">0</th>
            <th align="center">-4</th>
            <th align="center">-8</th>
            <th align="center">-10</th>
        </tr>
    </thead>
</table>    

### **Result**
As the below convergence diagram shows, the iteration process did converge within the first 100 iterations.

<img src="https://github.com/ShuHuei/ORA_finalproject/blob/main/group2%20iteration.PNG" width=90% height=90% align="center"/>

<br />

From the analysis above we can easily see that the value iteration method helps determine which state is better according to the reward function. And we can conclude the action we can decide in eac state in the folloing table.
<br>

<img src="https://github.com/ShuHuei/ORA_finalproject/blob/main/group2%20result.PNG" width=90% height=90% align="center"/>

The conclusion in Group2 are
+ When we discuss the # of confirmed and # of arrivals, we only find that if the # of confirmed is between Q25 and Q50,we will suggest that the strategy is MA(Mask and airport control).
+ And other interesting things. The first thing is highlight in green triangle. When the # of confirmed is high(the first location of the state is 2 or 3), then the suggest action may be MAV(Mask, airport control and vaccination). The second one is that if the # of confirmed is high and the # of arrivals starts decrease, then the suggest action may be the most serious one MAVV, which means we should let the vaccination rate achieve 20% as soon as possible.   

<br/>

## Conclusion

In our research, we implemented and compared different approaches of reinforcement learning on dynamic pricing issues, both of them are effective in providing pricing suggestions. However, as we’re facing more complicated situations and environments in real life retailing, Deep Q-learning might serve as the better method, since it is shown in our work that DQN has the ability to adopt more realistic state space settings, which enables it to take different conditions into consideration. Also, we found that having more state variables helps the DQN model gain higher profits, since the model shows more reasonable actions in the Q-table plot. Eventually, different settings on the reward function may influence the extent of convergence and lead to different optimizing results, yet we observe that there is a positive relationship between difference of conversion rate and profit, which makes it an alternative perspective on pricing suggestions.

<br />

---
### Reference
[How To Code The Value Iteration Algorithm For Reinforcement Learning, François St-Amant (2021)](https://towardsdatascience.com/how-to-code-the-value-iteration-algorithm-for-reinforcement-learning-8fb806e117d1)

[增強式學習 (DQN) - 股票操作](https://ithelp.ithome.com.tw/articles/10228127?sc=iThelpR)

[Reinforcement Learning 進階篇：Deep Q-Learning
](https://medium.com/pyladies-taiwan/reinforcement-learning-%E9%80%B2%E9%9A%8E%E7%AF%87-deep-q-learning-26b10935a745)