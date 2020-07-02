from rubiks_cube_gym.envs.rubiks_cube_222 import RubiksCube222Env
import numpy as np
from operator import itemgetter


class RubiksCube222EnvOrtega(RubiksCube222Env):
    def __init__(self):
        super(RubiksCube222EnvOrtega, self).__init__()
        self.FF = None
        self.OLL = None

    def check_FF(self):
        for pos in FF_POS:
            if itemgetter(*pos)(self.cube_reduced) == itemgetter(*pos)("WWWWOOGGRRBBOOGGRRBBYYYY"):
                return True
        return False

    def check_OLL(self):
        for pos in OLL_POS:
            if itemgetter(*pos)(self.cube_reduced) == itemgetter(*pos)("WWWWOOGGRRBBOOGGRRBBYYYY"):
                return True
        return False

    def check_solved(self):
        if self.cube_reduced == "WWWWOOGGRRBBOOGGRRBBYYYY":
            return True

    def reward(self):
        reward = -15 * self.FF - 25 * self.OLL
        done = False

        if self.check_FF():
            reward += 15
            self.FF = True
        else:
            self.FF = False

        if self.check_OLL():
            reward += 25
            self.OLL = True
        else:
            self.OLL = False

        if self.check_solved():
            reward += 60
            done = True

        if reward <= 0:
            reward -= 1

        return reward, done

    def reset(self, scramble=None):
        super(RubiksCube222EnvOrtega, self).reset(scramble=scramble)
        self.FF = self.check_FF()
        self.OLL = self.check_OLL()

        return self.cube_state


FF_POS = [[0, 1, 2, 3], [4, 5, 12, 13], [6, 7, 14, 15], [8, 9, 16, 17], [10, 11, 18, 19], [20, 21, 22, 23]]
OLL_POS = [[0, 1, 2, 3, 20, 21, 22, 23], [4, 5, 8, 9, 12, 13, 16, 17], [6, 7, 10, 11, 14, 15, 18, 19], ]
