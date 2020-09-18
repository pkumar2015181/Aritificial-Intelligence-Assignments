# https://github.com/AZstudy/gym-sliding-puzzle

import gym
import random

import time

import gym_sliding_puzzle
import pygame

#from cair_maze.maze_game import MazeGame
from gym_sliding_puzzle.envs.sliding_puzzle_env import SlidingPuzzleEnv
from gym_sliding_puzzle.pathfinding import path_finding

if __name__ == "__main__":

    env = gym.make("SlidingPuzzle-v0")

    #print("Observation space:", env.observation_space)
    #print("Action space:", env.action_space)
    start = env.reset()
    start = tuple(start.reshape(1, -1)[0])
    #print(type(start))
#    print("Start state = ", start)
    goal = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    goal = tuple(goal)
    #print(path_finding.distance_func(start, goal))
    
    #print(type(goal))
#    print("Goal state = ", goal)
    
    final_actions = path_finding.search(start, goal)
#    print(final_actions)
    
    for action in final_actions:
        time.sleep(0.6)
        new_state, reward, done, info = env.step(action)
#        print("state = ", new_state)
#        print("reward = ", reward)
#        print("done = ", done)
#        print("info = ", info)
        env.render()
    
    time.sleep(5)
    env.close()
    
