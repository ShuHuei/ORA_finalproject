# ORA_finalproject
###### `January 14, 2022 / by Shu-Huei Yang and Meng-Xiu Lu`
<!-- <br /> -->

#### This study use **Markov Decision Process (MDP)** models to provide prevemtion strategy suggestions of the COVID-19.

#### Contents:
1. [Motivation and Background](#Motivation-and-Background)
2. [Methodology](#Methodology)
3. [Analysis Result in Group1](#part-i-analysis-result-in-group1)
4. [Analysis Result in Group2](#part-ii-analysis-result-in-group2)
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
            <th># of confirmed > 8<br>
                no vaccination</th>
            <th>3 < # of confirmed < 8<br>
                no vaccination</th>
            <th>0 < # of confirmed < 3<br>
                no vaccination</th>
            <th># of confirmed < 0<br>
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
            <th># of confirmed > 8<br>
                vaccination</th>
            <th>3 < # of confirmed < 8<br>
                vaccination</th>
            <th>0 < # of confirmed < 3<br>
                vaccination</th>
            <th># of confirmed < 0<br>
                vaccination</th>
        </tr>
    </thead>
</table>    

So does in Group2.

Then we can use this self-defined state and historical data to calculate the transition matrix. Some of the results are as follows.
<img src="https://github.com/ShuHuei/ORA_finalproject/blob/main/transition%20matrix.PNG" width="100%" height="100%">

Now we can define the reward. All the state we have explained above. So we know that the state (3 0) in Group1 is the worst case and the state (0 1) is the best case. The rewards are defined in the following table.
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
      <td># of confirmed  <br> # of arrival and departure</td>
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
The dataset used for this study is # of confirmed and vaccination data which can be found on [github](https://github.com/owid/covid-19-data/tree/master/public/data).  The columns *date, new_cases and new_vaccinations* are the variable we use in Group1. Then we collect the timeline of the strategies we focus on and type into a excel and then join with the table which includes date, new_cases and new_vaccinations.
<br>
<img src="https://github.com/ShuHuei/ORA_finalproject/blob/main/timeline.PNG" width=80% height=80% align="center"/>

Then we can use the final table to calculate the transition matrix.

### **Markov Decision Process via Value Iteration**
In each iteration, the algorithm calculates the expected reward for each action under the current state. Then, it selects the action which brings the highest reward, and updates the value table of the current state with the maximal reward value. The algorithm will stop until the improvement is small enough, which implies convergence.

### **Result**

As the below convergence diagram shows, the iteration process did converge within the first 100 iterations. Also, the value shows that state (0 1) which is the best case has the highest reward, and the state (3 0) with the lowest value. The value table indicates that the agent tends to move forward to the states with a higher reward, which meets our expectation.

<img src="https://github.com/ShuHuei/ORA_finalproject/blob/main/group1%20iteration.PNG" width=90% height=90% align="center"/>

<br />

From the analysis above we can easily see that the value iteration method helps determine which state is better according to the reward function. And we can conclude the action we decide in each state in the following table.
<br>

<img src="https://github.com/ShuHuei/ORA_finalproject/blob/main/group1%20result.PNG" width=90% height=90% align="center"/>

The conclusions in Group1 are
+ When we discuss the # of confirmed and vaccination or not, most of the strategies will be MAV (Mask, Airport control and vaccination).
+ One interesting thing is that when the # of confirmed is high but we haven’t started to vaccinate, it will recommend to achieve 20% vaccination rate.

<br/>


## Part-II: Analysis Result in Group2

### **Data Collection**
In this part, we also use the data from github. But we add a new variable which is about the number of arrival and departure of Taiwan. This data is from the open data website of the [government](https://data.moi.gov.tw/moiod/Data/DataDetail.aspx?oid=905908DA-0EF6-4B24-87B0-35B7EDA4CFD2). We download all of these excels and sum the number of each airport and port. Then do the same thing as in the first part : use quantile to discretize the variable.

**State and Reward Settings** <br>
We have posted this table in the above but we don't explain it. 
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

From the analysis above we can easily see that the value iteration method helps determine which state is better according to the reward function. And we can conclude the action we decide in each state in the folloing table.
<br>

<img src="https://github.com/ShuHuei/ORA_finalproject/blob/main/group2%20result.PNG" width=90% height=90% align="center"/>

The conclusions in Group2 are
+ When we discuss the # of confirmed and # of arrivals, we only find that if the # of confirmed is between Q25 and Q50,we will suggest that the strategy is MA(Mask and airport control).
+ And other interesting things. The first thing is highlight in green triangle. When the # of confirmed is high(the first location of the state is 2 or 3), then the suggest action may be MAV(Mask, airport control and vaccination). The second one is that if the # of confirmed is high and the # of arrivals starts decrease, then the suggest action may be the most serious one MAVV, which means we should let the vaccination rate achieve 20% as soon as possible.   

<br/>

## Conclusion

In addition to the above conclusions, because the epidemic is getting worse, we collect recent data to do this process again. And this time we re-define the action because if we only extend the time we investigate, all the action are the same which is MAV(mask, airport control and vaccination). It may be difficult to find some rule in historical data.

<table align="center" class="table justify-content-center" >
  <thead>
    <tr >
      <th scope="col"></th> 
      <th scope="col" align="center">Group 2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">State</th>
      <td># of confirmed  <br> # of arrival and departure</td>
    </tr>
    <tr>
      <th scope="row">Action</th>
      <td colspan="2">Mask (M)<br>
                      Mask + Airport control (MA)<br>
                      Mask + Airport control + Vaccination (MAV)<br>
                      Mask + Airport control + Vaccination rate(i) > 20% (MAVV)<br>
                      Mask + Airport control + Vaccination rate(i) > 50% (MAVVV)<br>
                      Mask + Airport control + Vaccination rate(ii) > 20% (MAVVVV)<br>
                      Mask + Airport control + Vaccination rate(ii) > 50% (MAVVVVV)<br>
      </td>
    </tr>
    <tr>
      <th scope="row">Reward</th>
      <td colspan="2">same as the table above</td>
    </tr>
  </tbody>
</table>

<br>
The result can be showed in the following picture. And we transfer the recent data to the state we define are showned in the following table.
<img src="https://github.com/ShuHuei/ORA_finalproject/blob/main/recent%20data%20result.PNG" width=60% height=60% align="center"/>

|date|2022-01-01|2022-01-02|2022-01-03|2022-01-04|2022-01-05|2022-01-06|2022-01-07|
|----|----------|----------|----------|----------|----------|----------|----------|
|state|(3 1)|(3 1)|(3 2)|(3 1)|(3 0)|(3 0)|(3 0)|
|suggest action|MAVVVVV|MAVVVVV|MAVVVV|MAVVVVV|M|M|M|

The conclusions in this part is
+ Now the condition is serious, we should let the vaccination rate(ii) get high enough as soon as possible. But we can also see that the suggest action may be different from cognition because the # of confirmed is high and the # of arrival and departure is getting decrease. But it only suggest to wear mask. It may be caused by the historical data. So in the last part, we will mention some directions that we think we can do better in the future.

## Future work
After presentation, teacher has recommended some direction that we can try in the future.
+ nested action and the reward: <br>Because all actions are nested, maybe we should give some penalty on reward to avoid the algorithm tend to choose the most serious action.
+ We use quantile to discretize the variable. But in different time, there may exist different quantile. So we thought it might be more precise if the quantiles could be determined by different time intervals.
+ After discussion in the Group1 and Group2, we hope that we can extend our method to multiple state or other country to make sure the result is okay.
+ The last recommendation is partial MDP which can deal with some condition we can not see in advance or DQN which can deal with more complicated case.

<br />

---
### Reference
[疫情相關資料](https://github.com/owid/covid-19-data/tree/master/public/data)

[出入境資料](https://data.moi.gov.tw/moiod/Data/DataDetail.aspx?oid=905908DA-0EF6-4B24-87B0-35B7EDA4CFD2)

[Vaccination data](https://github.com/owid/covid-19-data/tree/master/public/data)

[MDP reference](https://github.com/sachinbiradar9/Markov-Decision-Processes/blob/master/mdp.py)
