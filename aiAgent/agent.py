from typing import final
import torch
import random
import numpy as np
import sys
from collections import deque
from trafficSim import TraciSim
from model import Linear_QNet, QTrainer
from helper import plot

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # randomness
        self.gamma = 0.9  # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(28, 64, 8)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        traffic_state = game.traffic_state
        mean_speeds = game.mean_speeds
        jam_length = game.jam_length
        state = [*traffic_state, *mean_speeds, *jam_length]

        return np.array(state, dtype=float)

    def remember(self, state, action, reward, next_state, done):
        # popleft if MAX_MEMORY is reached
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(
                self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        # for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        if random.randint(0, 200) < self.epsilon:
            final_move = [random.choice([0.0, 0.5, 1.0]),
                          random.choice([0.0, 0.5, 1.0]),
                          random.choice([0.0, 0.5, 1.0]),
                          random.choice([0.0, 0.5, 1.0]),
                          random.choice([0.0, 0.5, 1.0]),
                          random.choice([0.0, 0.5, 1.0]),
                          random.choice([0.0, 0.5, 1.0]),
                          random.choice([0.0, 0.5, 1.0])]
        else:
            state0 = torch.tensor(state, dtype=torch.float, device=device)
            prediction = self.model(state0)
            # normalize range from -1 to 1 -> 0 to 1
            move_normalized = np.divide(np.add(torch.tensor(prediction.cpu()), 1), 2)
            # round prediction to 0.0, 0.5, or 1.0
            move_rounded = np.divide(
                np.round(np.multiply(move_normalized, 2)), 2)
            final_move = move_rounded.tolist()

            print(f'prediction: {prediction}')
            print(f'normalized: {move_normalized}')
        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = TraciSim()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(
            state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        # output debug info
        debug_print = [f'Frame Iteration: {game.frame_iteration}',
                       f'Traffic State: {game.traffic_state}',
                       f'Jam Length: {game.jam_length}',
                       f'Mean Speeds: {game.mean_speeds}',
                       f'Reward: {game.reward}',
                       f'Score (No. of cars exited): {game.score}']

        print(debug_print)

        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            # TODO: do some shit

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()
