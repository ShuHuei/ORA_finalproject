# ORA_finalproject
###### `January 14, 2022 / by Shu-Huei Yang and Meng-Xiu Lu`
<!-- <br /> -->

#### This study proposes **value iteration** and **Markov Decision Process (MDP)** models to provide prevemtion strategy suggestions of the COVID-19.

#### Contents:
1. [Motivation and Background](#Motivation-and-Background)
2. [Methodology](#Methodology)
3. [Value Iteration Model](#Part-I-Value-Iteration)
4. [Deep Q-learning Models](#Part-II-Deep-Q-learning)
5. [Conclusion](#Conclusion)
6. [Reference](#Reference)
<br />

## Motivation and Background
Because of the COVID-19 outbreak in China, all the world are greatly affected. Epidemic prevention strategies of each country are highly valued. Especially when the epidemic is not getting better, variant virus appears. Now we can collect data for two years, it may exist some information to let us investigate the strategy we have done before. If we can use historical data to give suitable strategy, we can make a small contribution to specific country.

## Methodology
We choose **Markov Decision Process** to analysis our problem. The main dependent variable is the number of confiremed cases in our target country and we will collect other variables like number of travelers of our target country, number of confirmed cases in neighbors countries, the distance of interested countries, the number of people entering and leaving the country and  the number of vaccination to help us make a better decision.

In this methodology, we need to decide the state, action, transition matrix and reward. For simplified, we choose three variables to define the state space in the beginning(the number of confiremed cases in our target country / the number of vaccination / the number of people entering and leaving the country). And we seperate the three variables to two groups. Group1 are # of confirmed and vaccination. Group2 are # of confirmed and # of entering and leaving.

The action space represents the behaviors of prevention strategy, we refer th prevention timeline of Taiwan. Here are some action we will focus on : mask, airport control and  vaccination. 

As for the reward space, we need to discretize the variables we focus on first. We use quantile for discretization and the picture below is the boxplot of # of confirmed of Taiwan. We can see that most confirmed number are low.
<img src="https://github.com/ShuHuei/ORA_finalproject/blob/main/boxplot.png" width="75%" height="75%">

The algorithm will learn from historical data and help us to make the price adjustment decision, which makes it an ideal approach for implementing this concept. The following analysis can be broken down into two sections. First we apply **value iteration**, which requires the transition probability between each state to be given. The agent updates the value table of the states according to **Bellman’s Equation** in each iteration until convergence. Secondly, we expand the problem to using **Deep Q-learning**, the agent now no longer needs to know either the transition probability or the reward function, instead, we construct a neural network to generate the optimal action under the given state. Also, DQN allows us to attempt more complicated state settings such as continuous state space. 
<!-- (修正For each of the two methods, we consider both single state variable and multiple state variables versions to observe the differences. ) -->

<table class="table justify-content-center" >
  <thead>
    <tr >
      <th scope="col"></th> 
      <th scope="col" >Group 1 (# of confirmed and vaccination or not)</th>
      <th scope="col" >Group 2 (# of confirmed and # of entering and leaving)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">State</th>
      <td> single variable <br/> (discrete) </td>
      <td>single / multiple variables <br/> (continuous)</td>
    </tr>
    <tr>
      <th scope="row">Action</th>
      <td>five price values</td>
      <td>remain / increase / reduce price</td>
    </tr>
    <tr>
      <th scope="row">Reward</th>
      <td>best profit state: 1, <br/> worst profit state: -1, <br />else: 0</td>
      <td> profit / difference of conversion rate </td>
    </tr>
    <tr>
      <th scope="row">Comparison</th>
      <td> - Require transition probability matrix <br />- Agent knows the reward fnction </td>
      <td> - Transition probability is not required <br />
 - Agent does not know reward funciton
</td>
    </tr>
  </tbody>
</table>



<br/>

## Part I: Value Iteration
#### Contents:
1. [Data Collection](#Data-Collection)
2. [Markov Decision Process Setup](#Markov-Decision-Process-Setup)
3. [Value Iteration Algorithm](#Value-Iteration-Algorithm)
4. [Result](#Result)


### **Data Collection**
The dataset used for this study is a specific product demand data over 145 weeks, which is collected from an [online food demand dataset on Kaggle](https://www.kaggle.com/firebee/food-demand-forcasting).  The columns *checkout_price, num_orders* serve as the price and demand values . <!-- For the multiple variables state, we add *homepage_featured* column, which stands for whether the particular food is featured on the homepage of the platform, into our model.  -->

<!-- ### Demand Prediction
First, in order to calculate the profit reward, we developed a mapping between the price and demand variables with regard to the historical data,  -->

### **Markov Decision Process Setup**

<img src="https://i.imgur.com/IqdPhU4.png" width=35% height=35%/>


To obtain the state space, the price variable is discretized into five points. The agent can choose to move to any of the states as its action. 

As for the reward function, a mapping between the price and demand variables is developed with regard to the historical data, thus, the predicted profit for each state is able to calculated respectively as the below figure shows. The reward of the state is set to be one for the highest profit case, and negative one for the lowest case, others zero.

<img src="https://i.imgur.com/I6rdZHP.png" width=45% height=45% align="center"/>

<br />

### **Value Iteration Algorithm**
The algorithm uses the Bellman’s Equation:
<!-- $$V(s_t) = \max_{a_t}\{ R(s_t) + \gamma \sum_{s_{t+1}}P(s_{t+1}|s_t, a_t) V(s_{t+1})\}, \forall s$$ -->
<img src="https://i.imgur.com/pVlXibT.png" width=50% height=50%/>

In each iteration, the algorithm calculates the expected reward for each action under the current price state. Then, it selects the action which brings the highest reward, and updates the value table of the current state with the maximal reward value. The algorithm will stop until the improvement is small enough, which implies convergence.

<!-- (pseudo) -->

### **Result**

As the below convergence diagram shows, the iteration process did converge within the first 100 iterations. Also, the value table shows that state zero, which has the highest profit, also has the highest value, and the state with lowest profit (state four) has the lowest value. The value table indicates that the agent tends to move forward to the states with a higher predicted profit, which meets our expectation.

<img src="https://i.imgur.com/Gs4rn7O.png" width=90% height=90%/>

<br />

From the analysis above we can easily see that the value iteration method helps determine pricing decisions and tells which state is better according to the reward function, however, due to the simple setting of the state space, the result is relatively trivial. Thus we adopted DQN as our second method to see if it can deal with a more complicated case.



<br/>


## Part II: Deep Q-learning

**Content:**
1. [Data Collection](#Data-Collection1)
2. [Study Overview](#Study-Overview)
3. [Result](#Result1)
    * [Single-variable with Profit-reward Model](#Single-variable-with-Profit-reward-Model)
    * [Multiple-variable with Profit-reward Model](#Multiple-variable-with-Profit-reward-Model)
    * [Single-variable with DCR-reward Model](#Single-variable-with-DCR-reward-Model)
    * [Multiple-variable with DCR-reward Model](#Multiple-variable-with-DCR-reward-Model)

### **Data Collection**
The dataset is collected from an online shoes shop. It consists of two tables: order data and customer behavior data. The order data contains the *purchased item amount* and *price* of each order, and the behavior data contains the everyday *page-view times* and *add-to-cart times*. The customer behavior data thus serves as a great source for trying multiple state process.  


### **Study Overview**
According to [Liu et al. (2019)](https://arxiv.org/abs/1912.02572), experiment results suggest that difference of revenue conversion rates is a more appropriate reward function than revenue. Therefore, we define the daily *conversion rate* as the daily *item amount sold* divided by the *page-view times*.

<img src="https://i.imgur.com/SV21Wj2.png" width=35% height=35%/>
<!-- $$ \mathsf{conversion\ rate = \frac{item\ amount\ sold}{page\ view\ times}}$$ -->

The following study implements four models with two different state settings and two different reward functions.

**State Settings**
1. **Single-variable state:** The state is constructed by a vector of *price* variables looking back at a *window_size* of time. The *window_size* is set to be ten in our study. That is to say, the state is composed of the *price* of the past ten time periods.
<!-- $$\mathsf{[price_1,\ price_2,\ ...,\ price_{10} ]}$$ -->

   <img src="https://i.imgur.com/JkXZASa.png" width=30% height=30%/>

2. **Multiple-variables state:** This state is constructed by vectors of *price*, *add-to-cart times*, *page-view times* variables. Same as above, each vector is composed of the past ten times data.
<!-- $$\begin{align}
\mathsf{[}\ & \mathsf{[price_1,\ price_2,\ ...,\ price_{10} ]}\\
& \mathsf{[addToCart_1,\ ...,\ addToCart_{10} ]} \\
& \mathsf{[pageView_1,\ ...,\ pageView_{10} ]\ ]}
\end{align}$$ -->

   <img src="https://i.imgur.com/TDGmLZ4.png" width=33% height=33%/>


**Reward Functions**

<img src="https://i.imgur.com/P0yibio.png" width=57% height=57%/>
<!-- 1. **Profit:** $\mathsf{price \times predicted\ product\ amount\ sold.}$
2. **Difference of conversion rate (DCR):** 
$$\mathsf{\frac{predicted\ product\ amount\ sold_t}{page\ view\ times_t} - \frac{predicted\ product\ amount\ sold_{t-1}}{page\ view\ times_{t-1}}}$$ -->

The four models share the same action space, which is defined as below:

<img src="https://i.imgur.com/uYiaeRt.png" width=32% height=32%/>
<!-- **Action Space**$\mathsf{ = \{remain,\ increase,\ reduce\}}$
1. **Remain:** $\mathsf{price_t = price_{t-1}.}$
2. **Increase:** $\mathsf{price_t = 1.03 \times price_{t-1}.}$
3. **Reduce:** $\mathsf{price_t = 0.97 \times price_{t-1}.}$ -->

To predict the product amount sold, we simply construct a Random Forest model as a mapping between price and demand. The figures below show the expected relationship between price and the rewards.

<img src="https://i.imgur.com/5ZVI7OH.png" width=90% height=90%/>

<br />

### **Result**
### <ins>Single-variable with Profit-reward Model</ins>
<img src="https://i.imgur.com/BcmaVow.png" width=30% height=30%/>
<!-- **State:** single-variable state.
**Action:** $\mathsf{\{remain,\ increase,\ reduce\}}$.
**Reward:** Profit.
**Episode:** 750. -->

<img src="https://i.imgur.com/Q2Cl6Jq.png" width=90% height=90% />
<br />


The model shows no sign of convergence after 750 episodes, and the agent tends to choose the increasing price action in every condition. This can be concluded that, in this model, the state variable price alone is not enough to represent the current state, thus we moved on to the next model with multiple state variables.
<br />

### <ins>Multiple-variable with Profit-reward Model</ins>
<img src="https://i.imgur.com/G1UB5xP.png" width=30% height=30%/>
<!-- **State:** multiple-variable state.
**Action:** $\mathsf{\{remain,\ increase,\ reduce\}}$.
**Reward:** Profit.
**Episode:** 750. -->

<img src="https://i.imgur.com/WY7N0E6.png" width=90% height=90%/>

<!-- <img src="https://i.imgur.com/T6wq0bZ.png"  width=45% height=45% />
<br/>
<img src="https://i.imgur.com/bxBerWp.png"  width=45% height=45% />
<img src="https://i.imgur.com/szzHsKr.png"  width=45% height=45% /> -->
<br /> 

We can observe that the total profit has a higher converging tendency compared to the single state variable one. Moreover, the profits it gains generally surpass the profits obtained from the single state model. 

The previous figure shows that  the peak of predicted profit is located at nearly 410 dollars. In the Q-table plot, we can see that most states with prices higher than 410 are suggested to reduce prices, and the increasing price suggestion takes place as prices being lower than 410, which meets our expectation.

### <ins>Single-variable with DCR-reward Model</ins>
<img src="https://i.imgur.com/iHwPnDM.png" width=30% height=30%/>
<!-- **State:** single-variable state.
**Action:** $\mathsf{\{remain,\ increase,\ reduce\}}$.
**Reward:** Difference of Conversion Rate.
**Episode:** 730. -->

<img src="https://i.imgur.com/VPiJuW6.png" width=90% height=90%/>

<!-- <img src="https://i.imgur.com/1EjJ15F.png"  width=45% height=45%/>
<img src="https://i.imgur.com/BnPwshF.png"  width=45% height=45% />
<br /> 
<img src="https://i.imgur.com/SBDf0BO.png"  width=45% height=45% /> -->
<br/>

After adjusted the reward function to the difference of conversion rate, in this single state model, we can see the model converged really fast. While the total profits fluctuated between 405,000 and 400,000. 

### <ins>Multiple-variable with DCR-reward Model</ins>
<img src="https://i.imgur.com/Hd4oObZ.png" width=30% height=30%/>
<!-- **State:** multiple-variable state.
**Action:** $\mathsf{\{remain,\ increase,\ reduce\}}$.
**Reward:** Difference of Conversion Rate.
**Episode:** 750. -->

<img src="https://i.imgur.com/Gc4tz3w.png" width=90% height=90%/>

<!-- <img src="https://i.imgur.com/lRhDa1t.png"  width=45% height=45%/>
<img src="https://i.imgur.com/UMhuTK5.png"  width=45% height=45% />
<br /> 

<img src="https://i.imgur.com/nbwdrYS.png"   width=45% height=45% />
<img src="https://i.imgur.com/OWWgOD1.png"  width=45% height=45% /> -->
<br/>

This model gains better performance on the reward value, yet did not obtain higher profit. This may result from the model doing better on maximizing the difference of conversion rate, but did not fully transform into profit performance.
<br />

## Conclusion

In our research, we implemented and compared different approaches of reinforcement learning on dynamic pricing issues, both of them are effective in providing pricing suggestions. However, as we’re facing more complicated situations and environments in real life retailing, Deep Q-learning might serve as the better method, since it is shown in our work that DQN has the ability to adopt more realistic state space settings, which enables it to take different conditions into consideration. Also, we found that having more state variables helps the DQN model gain higher profits, since the model shows more reasonable actions in the Q-table plot. Eventually, different settings on the reward function may influence the extent of convergence and lead to different optimizing results, yet we observe that there is a positive relationship between difference of conversion rate and profit, which makes it an alternative perspective on pricing suggestions.

<br />

---
### Reference
[How To Code The Value Iteration Algorithm For Reinforcement Learning, François St-Amant (2021)](https://towardsdatascience.com/how-to-code-the-value-iteration-algorithm-for-reinforcement-learning-8fb806e117d1)

[增強式學習 (DQN) - 股票操作](https://ithelp.ithome.com.tw/articles/10228127?sc=iThelpR)

[Reinforcement Learning 進階篇：Deep Q-Learning
](https://medium.com/pyladies-taiwan/reinforcement-learning-%E9%80%B2%E9%9A%8E%E7%AF%87-deep-q-learning-26b10935a745)