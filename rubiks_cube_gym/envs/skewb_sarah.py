from rubiks_cube_gym.envs.skewb import SkewbEnv
import numpy as np
from operator import itemgetter


class SkewbEnvSarah(SkewbEnv):
    def __init__(self):
        super(SkewbEnvSarah, self).__init__()
        self.FL = None

    def check_FL(self):
        for pos in FL_POS:
            if itemgetter(*pos)(self.cube_reduced) == itemgetter(*pos)("WWWWWOOOOOGGGGGRRRRRBBBBBYYYYY"):
                return True
        return False

    def check_solved(self):
        if self.cube_reduced == "WWWWWOOOOOGGGGGRRRRRBBBBBYYYYY":
            return True

    def reward(self):
        reward = -40 * self.FL
        done = False

        if self.check_FL():
            reward += 40
            self.FL = True
        else:
            self.FL = False

        if self.check_solved():
            reward += 60
            done = True

        if reward <= 0:
            reward -= 1

        return reward, done

    def reset(self, scramble=None):
        super(SkewbEnvSarah, self).reset(scramble=scramble)
        self.FL = self.check_FL()

        return self.cube_state


FL_POS = [[0, 1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21], [5, 6, 7, 8, 9, 0, 3, 10, 13, 25, 28, 21, 24],
          [10, 11, 12, 13, 14, 3, 4, 15, 18, 25, 26, 6, 9], [15, 16, 17, 18, 19, 1, 4, 20, 23, 26, 29, 11, 14],
          [20, 21, 22, 23, 24, 16, 19, 28, 29, 5, 8, 0, 1], [25, 26, 27, 28, 29, 8, 9, 13, 14, 18, 19, 23, 24]]
