import gymnasium as gym
import numpy as np
from PIL import Image, ImageDraw

class Game:
    def __init__(self):
        self.state = np.random.rand(10, 10)  # example: 10x10 numpy array

    def get_state(self):
        return self.state

    def generate_image(self):
        img = Image.new('RGB', (500, 500), color='white')  # 500x500 white image
        draw = ImageDraw.Draw(img)

        for i in range(self.state.shape[0]):
            for j in range(self.state.shape[1]):
                color = (int(self.state[i, j] * 255), int(self.state[i, j] * 255), int(self.state[i, j] * 255))
                draw.rectangle((j * 50, i * 50, (j + 1) * 50, (i + 1) * 50), fill=color)

        return img

class LunarLander:
    def __init__(self):
        self.env = gym.make(
            "LunarLander-v2",
            continuous=False,
            gravity=-10.0,
            enable_wind=False,
            wind_power=15.0,
            turbulence_power=1.5,
            render_mode="rgb_array"  # Specify the render mode
        )
        self.reset()

    def reset(self):
        self.state, _ = self.env.reset()

    def step(self, action):
        self.state, reward, done, truncated, _ = self.env.step(action)
        return self.state, reward, done

    def get_state(self):
        return np.array(self.state)

    def get_reward(self):
        _, reward, done, truncated, _ = self.env.step(0)
        return reward

    def is_done(self):
        _, _, done, truncated, _ = self.env.step(0)
        return done

    def generate_image(self):
        img_array = self.env.render()
        img = Image.fromarray(img_array)
        return img
