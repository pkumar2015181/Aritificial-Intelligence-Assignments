import numpy as np 
import pandas as pd 
import itertools 
import sys
import matplotlib 
import matplotlib.style 
import plotting
import time
from tabulate import tabulate
from matplotlib import pyplot as plt
import copy

matplotlib.style.use('ggplot') 
from tkinter import *

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Environment
states = [
    ['R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R'],
    ['R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R'],
    ['R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R', 'R'],
    ['S', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'G']
]

# Rewards map
rewards = {
    'R': -1,    # R : Road penalty is agent stays in road (-1 will force agent to move),
    'S': -20,   # S : Start penalty if agent again back to start,
    'C': -100,  # C : Cliff penalty if agent move toward cliff,
    'G': +100   # G : Goal reward if agent achieves its goal.
}

# Possible actions
actions = {
    'UP': (-1, 0),
    'DOWN': (+1, 0),
    'RIGHT': (0, +1),
    'LEFT': (0, -1)
}

# Parameters
episodes = 100  # No. of episodes
alpha = 0.5     # Learning rate
gamma = 0.9       # Discount Factor
epsilon = 0.1   # Value of epsilon
eps_flag = 0    # For third case where epsilon converges to 0 with time when value is 1
greedy = 1      # Greedy policy for action i.e. always choose best action based on Q-value when value is 1

print("Learning rate: ", alpha, " Discount Factor: ", gamma, " Epsilon: ", epsilon, " Episodes: ", episodes)
sarsa_epsilon = copy.copy(epsilon)

# Tkinter params :
width = 500
height = 500
title = "Maze Game"
colors = {"C": "#1ae5ef", "S": "#c96134", "R": "#7e9296", "G": "#2ccc44"}
agent_color = "red"
step_wait_time = 750  # in millis

# Initial position
start_i = 3
start_j = 0
print("Start state : (", start_i, start_j, ")")

# Goal state
goal_i = 3
goal_j = 11
print("Goal state : (", goal_i, goal_j, ")")

curr_state_i, curr_state_j = start_i, start_j

flag = 0
total_reward = 0
sarsa_total_reward = 0

####################################################################################

# Possible action from given position (i, j)
def possible_actions(i, j):
    act_list = []
    for action in actions.items():
        next_i, next_j = i + action[1][0], j + action[1][1]
        if 0 <= next_i < len(states) and 0 <= next_j < len(states[i]):
            act_list.append(action[0])
    return act_list

# Reward function
def compute_reward(next_i, next_j):
    return rewards[states[next_i][next_j]]

# Initialize Q function with zeros
def initialize_q(q):
    for i in range(0, len(states)):
        for j in range(0, len(states[i])):
            for action in possible_actions(i, j):
                q[(i, j, action)] = 0
    return q

# action choose policy (here best action is the one with immediately best reward or least penalty)
def best_action_policy(q, next_i, next_j):
    max_act = max(possible_actions(next_i, next_j), key=lambda possible_action: q[(next_i, next_j, possible_action)])
    return max_act

# take the given action and returns new status
def take_action(i, j, action):
    return i + actions[action][0], j + actions[action][1]


#####################################  Q-Learning start  ###############################

# Q-update function
def q_update(i, j, action, next_i, next_j):
    reward = compute_reward(next_i, next_j)
    return (1 - alpha) * q[(i, j, action)] + alpha * (reward + gamma * q[(next_i, next_j, best_action_policy(q, next_i, next_j))])

# the q-learning algorithm
def q_learning(i, j):
    pos_act = possible_actions(i, j)
    num_actions = len(pos_act)
#    for act in pos_act:
#        next_i, next_j = take_action(i, j, act)
#        q[(i, j, act)] = q_update(i, j, act, next_i, next_j)
    best_act = best_action_policy(q, i, j)
    
#    print("BA = ", best_act, " type = ", type(best_act))
    
    if greedy == 0:
    
        # Epsilon-Greedy Policy (Start)
        
        # get probabilities of all actions from current state
        act_prob = np.ones(num_actions, dtype = float) * epsilon / num_actions 
    #    print(act_prob)
        act_prob[pos_act.index(best_act)] = act_prob[pos_act.index(best_act)] + (1.0 - epsilon) 
    #    print(act_prob)
        
        # choose action according to the probability distribution 
        best_act_index = np.random.choice(np.arange(len(act_prob)), p = act_prob) 
        best_act = pos_act[best_act_index]
    #    print("BA = ", best_act, " type = ", type(best_act))
        # Epsilon-Greedy Policy (End)
    
    next_i, next_j = take_action(i, j, best_act)
    q[(i, j, best_act)] = q_update(i, j, best_act, next_i, next_j)
    if flag == 1:
        reward = compute_reward(next_i, next_j)
        global total_reward
        total_reward += reward
        print('Old state : (', i, j, ') -', best_act, '- new state : (', next_i, next_j, ') - reward: ', reward)
    return next_i, next_j



def q_learning_episodes():
    
    global epsilon
    
    # Keeps track of useful statistics
    episode_lengths = np.zeros(episodes)
    episode_rewards = np.zeros(episodes)
    
    # For every episode
    for episode in range(episodes):
        
        if eps_flag == 1:
            epsilon = epsilon - (epsilon/episodes)
        
        # Reset the environment and pick the first action
        curr_state_i, curr_state_j = start_i, start_j
        for t in itertools.count():
            curr_state_i, curr_state_j = q_learning(curr_state_i, curr_state_j)
            reward = compute_reward(curr_state_i, curr_state_j)
            
            # Update statistics
            episode_rewards[episode] += reward
            episode_lengths[episode] = t
            
            # episode terminated if current state is equal to goal state
            if curr_state_i == goal_i and curr_state_j == goal_j:
                break
            
            # agent enters in cliff area
            if states[curr_state_i][curr_state_j] == 'C':
                break
    return (episode_lengths, episode_rewards)


# game function is recursively call for next state using canvas.after
def game():
    # next iteration of Q-Learning algorithm
    global curr_state_i, curr_state_j, q
    curr_state_i, curr_state_j = q_learning(curr_state_i, curr_state_j)
    # update game visual with new status from q_learning
    canvas.delete(ALL)
    nb_cells_ver = len(states)
    for i in range(0, nb_cells_ver):
        nb_cells_hor = len(states[i])
        cell_width = width / nb_cells_hor
        cell_height = height / nb_cells_ver
        for j in range(0, nb_cells_hor):
            canvas.create_rectangle(cell_width * j, cell_height * i, cell_width * (j + 1), cell_height * (i + 1), fill=colors[(states[i][j])])
            if i == curr_state_i and j == curr_state_j:
                canvas.create_oval(cell_width * j, cell_height * i, cell_width * (j + 1), cell_height * (i + 1), fill=agent_color)
    if curr_state_i  == 3 and curr_state_j == 11:
        return -1
    canvas.after(step_wait_time, game)
    

# initialize Q function
q = {}
q = initialize_q(q)

# Learning phase
print("\n\nQ-Learning")
print("Learning phase has started .....")
stats = q_learning_episodes()
print("Learning phase has finished")
flag = 1
episode_lengths = stats[0]
episode_rewards = stats[1]

# Plot the episode length over time
fig1 = plt.figure(figsize=(10,5))
plt.plot(episode_lengths)
plt.xlabel("Episode")
plt.ylabel("Episode Length")
plt.title("Episode length vs No. of episodes in Q-learning")
plt.show(fig1)

# Plot the episode reward over time
fig2 = plt.figure(figsize=(10,5))
plt.plot(episode_rewards)
plt.xlabel("Episode")
plt.ylabel("Episode Rewards")
plt.title("Sum of rewards in episode vs No. of episodes in Q-learning")
plt.show(fig2)


#print(q)
policy = []
policy_qval = []
for i in range(0, len(states)):
    for j in range(0, len(states[i])):
        max_act = max(possible_actions(i, j), key=lambda possible_action: q[(i, j, possible_action)])
        policy_qval.append(q[(i, j, max_act)])
        policy.append(max_act)

np_arr = np.array(policy).reshape([4,12])
#print(np_arr)
df = pd.DataFrame(np_arr, columns=[0,1,2,3,4,5,6,7,8,9,10,11])
print(tabulate(df))
#print(df)

#np_arr = np.array(policy_qval).reshape([4,12])
##print(np_arr)
#df = pd.DataFrame(np_arr, columns=[0,1,2,3,4,5,6,7,8,9,10,11])
#print(tabulate(df))


print("Learning has finished")



time.sleep(2)

# Launch the app
#window = Tk()
#window.title(title)
#window.geometry(str(width) + "x" + str(height))
#canvas = Canvas(window, width=width, height=height, borderwidth=0, highlightthickness=0)
#canvas.pack()
#curr_state_i, curr_state_j = start_i, start_j
#canvas.after(0, game)
#window.mainloop()

#print("Total Reward: ", total_reward)

#####################################  Q-Learning end  ###############################



#State–action–reward–state–action (SARSA)
#####################################  SARSA start  ##################################

# Q-update function
def sarsa_update(i, j, action, next_i, next_j):
    reward = compute_reward(next_i, next_j)
    pos_act = possible_actions(next_i, next_j)
    num_actions = len(pos_act)
    best_act = best_action_policy(sarsa_q, next_i, next_j)
    
    if greedy == 0:
    
        # Epsilon-Greedy Policy (Start)
        
        # get probabilities of all actions from current state
        act_prob = np.ones(num_actions, dtype = float) * epsilon / num_actions 
    #    print(act_prob)
        act_prob[pos_act.index(best_act)] = act_prob[pos_act.index(best_act)] + (1.0 - epsilon) 
    #    print(act_prob)
        
        # choose action according to the probability distribution 
        best_act_index = np.random.choice(np.arange(len(act_prob)), p = act_prob) 
        best_act = pos_act[best_act_index]
    #    print("BA = ", best_act, " type = ", type(best_act))
        # Epsilon-Greedy Policy (End)
    
    return (1 - alpha) * sarsa_q[(i, j, action)] + alpha * (reward + gamma * sarsa_q[(next_i, next_j, best_act)])


# the q-learning algorithm
def sarsa_learning(i, j):
    pos_act = possible_actions(i, j)
    num_actions = len(pos_act)
#    for act in pos_act:
#        next_i, next_j = take_action(i, j, act)
#        q[(i, j, act)] = sarsa_update(i, j, act, next_i, next_j)
    best_act = best_action_policy(sarsa_q, i, j)
    
#    print("state = ", i, j , "BA = ", best_act)
    
    if greedy == 0:
    
        # Epsilon-Greedy Policy (Start)
        
        # get probabilities of all actions from current state
        act_prob = np.ones(num_actions, dtype = float) * epsilon / num_actions 
    #    print(act_prob)
        act_prob[pos_act.index(best_act)] = act_prob[pos_act.index(best_act)] + (1.0 - epsilon) 
    #    print(act_prob)
        
        # choose action according to the probability distribution 
        best_act_index = np.random.choice(np.arange(len(act_prob)), p = act_prob) 
        best_act = pos_act[best_act_index]
    #    print("BA = ", best_act, " type = ", type(best_act))
        # Epsilon-Greedy Policy (End)
    
    next_i, next_j = take_action(i, j, best_act)
    sarsa_q[(i, j, best_act)] = sarsa_update(i, j, best_act, next_i, next_j)
    if flag == 1:
        reward = compute_reward(next_i, next_j)
        global sarsa_total_reward
        sarsa_total_reward += reward
        print('Old state : (', i, j, ') -', best_act, '- new state : (', next_i, next_j, ') - reward: ', reward)
    return next_i, next_j



def sarsa_learning_episodes():
    
    global epsilon
    
    if eps_flag == 1:
        epsilon = sarsa_epsilon
    
    # Keeps track of useful statistics
    episode_lengths = np.zeros(episodes)
    episode_rewards = np.zeros(episodes)
    
    # For every episode
    for episode in range(episodes):
#        print("E = ", episode)
        
        if eps_flag == 1:
            epsilon = epsilon - (epsilon/episodes)
        
        # Reset the environment and pick the first action
        curr_state_i, curr_state_j = start_i, start_j
        for t in itertools.count():
            curr_state_i, curr_state_j = sarsa_learning(curr_state_i, curr_state_j)
            reward = compute_reward(curr_state_i, curr_state_j)
            
            # Update statistics
            episode_rewards[episode] += reward
            episode_lengths[episode] = t
            
            # episode terminated if current state is equal to goal state
            if curr_state_i == goal_i and curr_state_j == goal_j:
                break
            
            # agent enters in cliff area
            if states[curr_state_i][curr_state_j] == 'C':
                break
    return (episode_lengths, episode_rewards)


# game function is recursively call for next state using canvas.after
def sarsa_game():
    # next iteration of Q-Learning algorithm
    global curr_state_i, curr_state_j, sarsa_q
    curr_state_i, curr_state_j = sarsa_learning(curr_state_i, curr_state_j)
    # update game visual with new status from q_learning
    sarsa_canvas.delete(ALL)
    nb_cells_ver = len(states)
    for i in range(0, nb_cells_ver):
        nb_cells_hor = len(states[i])
        cell_width = width / nb_cells_hor
        cell_height = height / nb_cells_ver
        for j in range(0, nb_cells_hor):
            sarsa_canvas.create_rectangle(cell_width * j, cell_height * i, cell_width * (j + 1), cell_height * (i + 1), fill=colors[(states[i][j])])
            if i == curr_state_i and j == curr_state_j:
                sarsa_canvas.create_oval(cell_width * j, cell_height * i, cell_width * (j + 1), cell_height * (i + 1), fill=agent_color)
    if curr_state_i  == 3 and curr_state_j == 11:
        return -1
    sarsa_canvas.after(step_wait_time, sarsa_game)
    

# initialize Q function
sarsa_q = {}
sarsa_q = initialize_q(sarsa_q)

flag = 0

# Learning phase
print("\n\nSARSA Algorithm")
print("Learning phase has started .....")
sarsa_stats = sarsa_learning_episodes()
print("Learning phase has finished")
flag = 1
sarsa_episode_lengths = sarsa_stats[0]
sarsa_episode_rewards = sarsa_stats[1]

# Plot the episode length over time
fig1 = plt.figure(figsize=(10,5))
plt.plot(sarsa_episode_lengths)
plt.xlabel("Episode")
plt.ylabel("Episode Length")
plt.title("Episode length vs No. of episodes in SARSA")
plt.show(fig1)

# Plot the episode reward over time
fig2 = plt.figure(figsize=(10,5))
plt.plot(sarsa_episode_rewards)
plt.xlabel("Episode")
plt.ylabel("Episode Rewards")
plt.title("Sum of rewards in episode vs No. of episodes in SARSA")
plt.show(fig2)


#print(q)
sarsa_policy = []
sarsa_policy_qval = []
for i in range(0, len(states)):
    for j in range(0, len(states[i])):
        max_act = max(possible_actions(i, j), key=lambda possible_action: sarsa_q[(i, j, possible_action)])
        sarsa_policy_qval.append(sarsa_q[(i, j, max_act)])
        sarsa_policy.append(max_act)

sarsa_np_arr = np.array(sarsa_policy).reshape([4,12])
#print(np_arr)
sarsa_df = pd.DataFrame(sarsa_np_arr, columns=[0,1,2,3,4,5,6,7,8,9,10,11])
print(tabulate(sarsa_df))
#print(df)

#sarsa_np_arr = np.array(sarsa_policy_qval).reshape([4,12])
##print(np_arr)
#sarsa_df = pd.DataFrame(sarsa_np_arr, columns=[0,1,2,3,4,5,6,7,8,9,10,11])
#print(tabulate(sarsa_df))
##print(df)


    
print("Learning has finished")
time.sleep(2)

# Launch the app
#sarsa_window = Tk()
#sarsa_window.title(title)
#sarsa_window.geometry(str(width) + "x" + str(height))
#sarsa_canvas = Canvas(sarsa_window, width=width, height=height, borderwidth=0, highlightthickness=0)
#sarsa_canvas.pack()
#curr_state_i, curr_state_j = start_i, start_j
#sarsa_canvas.after(0, sarsa_game)
#sarsa_window.mainloop()

#print("Total Reward: ", sarsa_total_reward)


print("Comparison between both algorithm learnings")
print("Red color for SARSA and Green color for Q-learning")
# Plot the episode length over time
fig1 = plt.figure(figsize=(10,5))
plt.plot(sarsa_episode_lengths, 'r', episode_lengths, 'g')
plt.xlabel("Episode")
plt.ylabel("Episode Length")
plt.title("Episode length vs No. of episodes (red for SARSA and green for QL)")
plt.show(fig1)

# Plot the episode reward over time
fig1 = plt.figure(figsize=(10,5))
plt.plot(sarsa_episode_rewards, 'r', episode_rewards, 'g')
plt.xlabel("Episode")
plt.ylabel("Episode Rewards")
plt.title("Sum of rewards in episode vs No. of episodes (red for SARSA and green for QL)")
plt.show(fig1)

print("\nQ-Leaning")
print("Average Episode Length = ", sum(episode_lengths)/len(episode_lengths))
print("Average Episode Reward = ", sum(episode_rewards)/len(episode_rewards))
print("\nSARSA")
print("Average Episode Length = ", sum(sarsa_episode_lengths)/len(sarsa_episode_lengths))
print("Average Episode Reward = ", sum(sarsa_episode_rewards)/len(sarsa_episode_rewards))


#####################################  SARSA end  ##################################




















