import pickle
import random
import gym
from gym import spaces
import os
import cv2
import numpy as np
import gc
import wget


class PyraminxWoTipsEnv(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array', 'ansi']}

    def __init__(self):
        self.cube = None
        self.cube_reduced = None
        self.cube_state = None
        # spaces
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Discrete(993120)

        state_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "pyraminx_wo_tips_states.pickle")
        if not os.path.exists(state_file):
            print("State file not found")
            print("Downloading...")
            wget.download("https://storage.googleapis.com/rubiks_cube_gym/pyraminx_wo_tips_states.pickle", state_file)
            print("Download complete")

        with open(state_file, "rb") as f:
            self.cube_states = pickle.load(f)

    def update_cube_reduced(self):
        self.cube_reduced = ''.join(TILE_MAP[tile] for tile in self.cube)

    def update_cube_state(self):
        self.cube_state = self.cube_states[self.cube_reduced]

    def generate_scramble(self):
        scramble_len = 0
        prev_move = None
        scramble = ""
        layer_moves = ['L', 'R', 'U', 'B']
        layer_move_types = ['', "'"]

        while scramble_len < 11:
            move = random.choice(layer_moves)
            while move == prev_move:
                move = random.choice(layer_moves)
            scramble += move + random.choice(layer_move_types) + " "
            prev_move = move
            scramble_len += 1

        return scramble[:-1]

    def move(self, move, move_type=None):
        repetitions = dict({None: 1, "'": 2})[move_type]

        if move.isupper():
            if move == "L":
                layer_cubies_old = np.array([14, 22, 23, 11, 12, 13, 29, 28, 32])
            elif move == "R":
                layer_cubies_old = np.array([16, 24, 23, 29, 30, 34, 19, 18, 17])
            elif move == "U":
                layer_cubies_old = np.array([2, 3, 13, 14, 15, 16, 17, 7, 8])
            elif move == "B":
                layer_cubies_old = np.array([11, 1, 2, 8, 9, 19, 34, 33, 32])

            layer_cubies_new = np.roll(layer_cubies_old, -3 * repetitions)
            np.put(self.cube, layer_cubies_old, self.cube[layer_cubies_new])

            move = move.lower()

        if move == "l":
            vertex_cubies_old = np.array([20, 27, 21])
        elif move == "r":
            vertex_cubies_old = np.array([25, 31, 26])
        elif move == "u":
            vertex_cubies_old = np.array([4, 5, 6])
        elif move == "b":
            vertex_cubies_old = np.array([0, 10, 35])

        vertex_cubies_new = np.roll(vertex_cubies_old, -1 * repetitions)
        np.put(self.cube, vertex_cubies_old, self.cube[vertex_cubies_new])

    def algorithm(self, moves):
        for move in moves.split(" "):
            if len(move) == 2:
                self.move(move[0], move[1])
            else:
                self.move(move[0])

    def step(self, action):
        move = ACTION_MAP[action]
        self.move(move[0], move[1])

        self.update_cube_reduced()
        self.update_cube_state()

        reward, done = self.reward()
        observation = self.cube_state
        info = {"cube": self.cube, "cube_reduced": self.cube_reduced}

        return observation, reward, done, info

    def reward(self):
        if self.cube_reduced == "RRRRRGBBBBBRRRGGGBBBRGGGGGBYYYYYYYYY":
            return 100, True
        else:
            return -1, False

    def reset(self, scramble=None):
        self.cube = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
                              25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35], dtype=np.uint8)
        if scramble:
            self.algorithm(scramble)
        elif scramble == False:
            pass
        else:
            self.algorithm(self.generate_scramble())

        self.update_cube_reduced()
        self.update_cube_state()

        return self.cube_state

    def render(self, mode='human', render_time=100):
        if mode == 'ansi':
            return self.cube_reduced
        else:
            img = np.zeros((312, 360, 3), np.uint8) * 255

            s = 60
            s_2 = 30
            h = 52
            ctr = 0

            for row in range(6):
                pt1 = row * s_2, row * h
                inverse = 1
                for tile in range(11 - 2 * row):
                    pt2 = pt1[0] + s, pt1[1]
                    pt3 = pt1[0] + s_2, pt1[1] + inverse * h

                    triangle_cnt = np.array([pt1, pt2, pt3])
                    cv2.drawContours(img, [triangle_cnt], 0, COLOR_MAP[TILE_MAP[self.cube[ctr]]], -1)

                    pt1 = pt1[0] + s_2, pt1[1] + inverse * h
                    inverse *= -1

                    ctr += 1

            if mode == 'rgb_array':
                return img
            elif mode == "human":
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                cv2.imshow("Cube", img)
                cv2.waitKey(render_time)

    def close(self):
        del self.cube_states
        gc.collect()
        cv2.destroyAllWindows()


TILE_MAP = {
    0: 'R', 1: 'R', 2: 'R', 3: 'R', 4: 'R',
    5: 'G',
    6: 'B', 7: 'B', 8: 'B', 9: 'B', 10: 'B',
    11: 'R', 12: 'R', 13: 'R',
    14: 'G', 15: 'G', 16: 'G',
    17: 'B', 18: 'B', 19: 'B',
    20: 'R',
    21: 'G', 22: 'G', 23: 'G', 24: 'G', 25: 'G',
    26: 'B',
    27: 'Y', 28: 'Y', 29: 'Y', 30: 'Y', 31: 'Y',
    32: 'Y', 33: 'Y', 34: 'Y',
    35: 'Y'
}

COLOR_MAP = {
    'G': (0, 128, 0),
    'R': (255, 0, 0),
    'B': (0, 0, 255),
    'Y': (255, 255, 0)
}

ACTION_MAP = {0: ("L", None), 1: ("R", None), 2: ("U", None), 3: ("B", None)}

