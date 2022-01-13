import csv
import sys
import matplotlib.pyplot as plt

Transitions = {}
Reward = {}

if len(sys.argv)>3:
    NUM_COL = int(sys.argv[3])
    NUM_ROW = int(sys.argv[4])
else:
    NUM_COL = 4
    NUM_ROW = 4
    
#gamma is the discount factor
if len(sys.argv)>5:
    gamma = float(sys.argv[5])
else:
    gamma = 0.9

#the maximum error allowed in the utility of any state
if len(sys.argv)>6:
    epsilon = float(sys.argv[6])
else:
    epsilon = 0.001

def read_file():
    #read transitions from file and store it to a variable
    with open(sys.argv[1], 'r') as csvfile:
    # with open('transitions_xiu.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[0] in Transitions:
                if row[1] in Transitions[row[0]]:
                    Transitions[row[0]][row[1]].append((float(row[3]), row[2]))
                else:
                    Transitions[row[0]][row[1]] = [(float(row[3]), row[2])]
            else:
                Transitions[row[0]] = {row[1]:[(float(row[3]),row[2])]}

    #read rewards file and save it to a variable
    with open(sys.argv[2], 'r') as csvfile:
    # with open('rewards_xiu.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            Reward[row[0]] = float(row[1]) if row[1] != 'None' else None

read_file()

class MarkovDecisionProcess:

    """A Markov Decision Process, defined by an states, actions, transition model and reward function."""

    def __init__(self, transition={}, reward={}, gamma=.9):
        #collect all nodes from the transition models
        self.states = transition.keys()
        #initialize transition
        self.transition = transition
        #initialize reward
        self.reward = reward
        #initialize gamma
        self.gamma = gamma

    def R(self, state):
        """return reward for this state."""
        return self.reward[state]

    def actions(self, state):
        """return set of actions that can be performed in this state"""
        return self.transition[state].keys()

    def T(self, state, action):
        """for a state and an action, return a list of (probability, result-state) pairs."""
        return self.transition[state][action]

#Initialize the MarkovDecisionProcess object
mdp = MarkovDecisionProcess(transition=Transitions, reward=Reward)

def printEnvironment(arr, policy=False):
    res = ""
    for r in range(NUM_ROW):
        res += "|" + str(r) + "|"
        for c in range(NUM_COL):
            # if r == 0 and c == 0:
            #     val = "+10"
            # elif r == 0 and c == (NUM_COL-1):
            #     val = "-10"
            # else:
                # if policy:
                #     val = ["Down", "Left", "Up", "Right"][arr[r][c]]
                # else:
            key = '(' + str(c) + ' ' + str(r) + ')'
            val = str(arr[key])
            res += " " + val[:5].ljust(5) + " |" # format 向左對齊
        res += "\n"
    res += "| |   0   |   1   |   2   |   3   | "
    res += "\n"
    print(res)

def value_iteration():
    """
    Solving the MDP by value iteration.
    returns utility values for states after convergence
    """
    states = mdp.states
    actions = mdp.actions
    T = mdp.T
    R = mdp.R

    #initialize value of all the states to 0 (this is k=0 case)
    V1 = {s: 0 for s in states}
    max_val = []
    print("The initial state is:\n")
    printEnvironment(V1)
    
    print("During the value iteration:\n")
    while True:
        V = V1.copy()
        delta = 0
        for s in states:
            #Bellman update, update the utility values
            V1[s] = R(s) + gamma * max([ sum([p * V[s1] for (p, s1) in T(s, a)]) for a in actions(s)])
            #calculate maximum difference in value
            delta = max(delta, abs(V1[s] - V[s]))
            
        printEnvironment(V1)
        all_values = V1.values()
        max_val.append(max(all_values))
        #check for convergence, if values converged then return V
        if delta < epsilon * (1 - gamma) / gamma:
            return V,max_val


def best_policy(V):
    """
    Given an MDP and a utility values V, determine the best policy as a mapping from state to action.
    returns policies which is dictionary of the form {state1: action1, state2: action2}
    """
    states = mdp.states
    actions = mdp.actions
    pi = {}
    Q = {}
    for s in states:
        pi[s] = max(actions(s), key=lambda a: expected_utility(a, s, V))
        for a in actions(s):
            if s in Q:
                Q[s][a] = [expected_utility(a, s, V)]
            else:
                Q[s] = {a:[expected_utility(a, s, V)]}
    return pi, Q


def expected_utility(a, s, V):
    # print(a,s)
    """returns the expected utility of doing a in state s, according to the MDP and V."""
    T = mdp.T
    R = mdp.R
    return R(s) + gamma * sum([p * V[s1] for (p, s1) in mdp.T(s, a)])


#call value iteration
V, max_value = value_iteration()
print('State - Value')
for s in V:
    print(s, ' - ' , V[s])

plt.plot(max_value)
plt.title('Max reward for each iteration')
plt.xlabel('Iteration')
plt.ylabel('Max reward')
plt.savefig('Max reward for each iteration.png', c='c')

pi, Q = best_policy(V)
print('\nOptimal policy is \nState - Action')
for s in pi:
    print(s, ' - ' , pi[s])

print('\npolicy in each state \nState - Action')
for s in Q:
    print(s, ' - ' , Q[s])
