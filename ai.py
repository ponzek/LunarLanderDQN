import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from collections import deque
import random

class LunarLanderAI:
    def __init__(self):
        self.model = Sequential([
            Dense(64, activation='relu', input_shape=(8,)),  # State shape is (8,)
            Dense(64, activation='relu'),
            Dense(4, activation='linear')  # Action space is 4-dimensional
        ])
        self.model.compile(optimizer='adam', loss='mse')
        self.memory = deque(maxlen=2000)  # Experience replay buffer

    def remember(self, state, action, reward, next_state, done):
        # Store experience in the replay buffer
        self.memory.append((state, action, reward, next_state, done))

    def train(self, batch_size=32):
        if len(self.memory) < batch_size:
            return  # Not enough samples to train

        batch = random.sample(self.memory, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)

        actions = np.array(actions)
        states = np.array(states).squeeze()
        next_states = np.array(next_states).squeeze()
        rewards = np.array(rewards)
        dones = np.array(dones)

        next_q_values = self.model.predict(next_states)
        targets = rewards + 0.99 * np.max(next_q_values, axis=1) * (1 - dones)

        target_vec = self.model.predict(states)
        print("target_vec shape:", target_vec.shape)
        print("actions shape:", actions.shape)
        for i in range(batch_size):
            target_vec[i, actions[i]] = targets[i].reshape(-1, 1)

        self.model.fit(states, target_vec, epochs=1, verbose=0)

    def predict(self, state):
        return self.model.predict(state)

    def save(self, name):
        self.model.save_weights(name)

    def load(self, name):
        self.model.load_weights(name)
