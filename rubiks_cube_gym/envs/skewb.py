import pickle
import random
import gym
from gym import spaces
import os
import cv2
import numpy as np
import gc
import wget


class SkewbEnv(gym.Env):
    metadata = {'render.modes': ['human', 'rgb_array', 'ansi']}

    def __init__(self):
        self.cube = None
        self.cube_reduced = None
        self.cube_state = None
        # spaces
        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Discrete(3149280)

        state_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "skewb_states.pickle")
        if not os.path.exists(state_file):
            print("State file not found")
            print("Downloading...")
            wget.download("https://storage.googleapis.com/rubiks_cube_gym/skewb_states.pickle", state_file)
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

        if move == "L":
            layer_cubies_old = np.array([10, 12, 14, 8, 7, 6, 26, 27, 28])
            vertex_cubies_old = np.array([13, 9, 25])
            side_cubies_old = np.array([3, 24, 18])

        elif move == "R":
            layer_cubies_old = np.array([16, 17, 18, 26, 27, 28, 24, 22, 20])
            vertex_cubies_old = np.array([19, 29, 23])
            side_cubies_old = np.array([1, 14, 8])

        elif move == "U":
            layer_cubies_old = np.array([3, 2, 1, 20, 22, 24, 8, 7, 6])
            vertex_cubies_old = np.array([0, 21, 5])
            side_cubies_old = np.array([16, 28, 10])

        elif move == "B":
            layer_cubies_old = np.array([21, 22, 23, 29, 27, 25, 9, 7, 5])
            vertex_cubies_old = np.array([24, 28, 8])
            side_cubies_old = np.array([0, 19, 13])

        layer_cubies_new = np.roll(layer_cubies_old, -3 * repetitions)
        vertex_cubies_new = np.roll(vertex_cubies_old, -1 * repetitions)
        side_cubies_new = np.roll(side_cubies_old, -1 * repetitions)

        np.put(self.cube, layer_cubies_old, self.cube[layer_cubies_new])
        np.put(self.cube, vertex_cubies_old, self.cube[vertex_cubies_new])
        np.put(self.cube, side_cubies_old, self.cube[side_cubies_new])

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
        if self.cube_reduced == "WWWWWOOOOOGGGGGRRRRRBBBBBYYYYY":
            return 100, True
        else:
            return -1, False

    def reset(self, scramble=None):
        self.cube = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
                              25, 26, 27, 28, 29], dtype=np.uint8)
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
            img = np.zeros((225, 300, 3), np.uint8) * 255

            face_anchor_map = {0: (75, 0), 1: (0, 75), 2: (75, 75), 3: (150, 75), 4: (225, 75), 5: (75, 150)}
            triangle_map = {0: [(0, 0), (37, 0), (0, 37)], 1: [(38, 0), (75, 0), (75, 37)],
                            3: [(0, 38), (0, 75), (37, 75)], 4: [(38, 75), (75, 38), (75, 75)]}
            for face in range(6):
                w, h = face_anchor_map[face]
                cv2.rectangle(img, (w, h), (w + 75, h + 75), COLOR_MAP[TILE_MAP[self.cube[5 * face + 2]]], -1)

                for tile in range(5):
                    if tile == 2:
                        continue

                    triangle_cnt = np.array([(w, h)] * 3) + triangle_map[tile]
                    cv2.drawContours(img, [triangle_cnt], 0, COLOR_MAP[TILE_MAP[self.cube[5 * face + tile]]], -1)


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
    0: 'W', 1: 'W', 2: 'W', 3: 'W', 4: 'W',
    5: 'O', 6: 'O', 7: 'O', 8: 'O', 9: 'O',
    10: 'G', 11: 'G', 12: 'G', 13: 'G', 14: 'G',
    15: 'R', 16: 'R', 17: 'R', 18: 'R', 19: 'R',
    20: 'B', 21: 'B', 22: 'B', 23: 'B', 24: 'B',
    25: 'Y', 26: 'Y', 27: 'Y', 28: 'Y', 29: 'Y'
}

COLOR_MAP = {
    'W': (255, 255, 255),
    'O': (255, 165, 0),
    'G': (0, 128, 0),
    'R': (255, 0, 0),
    'B': (0, 0, 255),
    'Y': (255, 255, 0)
}

ACTION_MAP = {0: ("L", None), 1: ("R", None), 2: ("U", None), 3: ("B", None)}

