from rubiks_cube_gym.envs.pyraminx_wo_tips import PyraminxWoTipsEnv
import numpy as np
from operator import itemgetter


class PyraminxWoTipsEnvLBL(PyraminxWoTipsEnv):
    def __init__(self):
        super(PyraminxWoTipsEnvLBL, self).__init__()
        self.FL = None
        self.OLL = None

    def check_FL(self):
        for pos in FL_POS:
            if itemgetter(*pos)(self.cube_reduced) == itemgetter(*pos)("RRRRRGBBBBBRRRGGGBBBRGGGGGBYYYYYYYYY"):
                return True
        return False

    def check_solved(self):
        if self.cube_reduced == "RRRRRGBBBBBRRRGGGBBBRGGGGGBYYYYYYYYY":
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
        super(PyraminxWoTipsEnvLBL, self).reset(scramble=scramble)
        self.FL = self.check_FL()

        return self.cube_state


FL_POS = [[0, 1, 2, 3, 4, 11, 12, 13, 20, 5, 14, 15, 20, 21, 6, 7, 8, 9, 10, 27, 28, 32, 33, 35],
          [5, 14, 15, 16, 21, 22, 23, 24, 25, 3, 4, 12, 13, 20, 6, 7, 17, 18, 26, 27, 28, 29, 30, 31],
          [6, 7, 8, 9, 10, 17, 18, 19, 26, 5, 15, 16, 24, 25, 30, 31, 33, 34, 35, 0, 1, 2, 3, 4],
          [27, 28, 29, 30, 31, 32, 33, 34, 35, 21, 22, 23, 24, 25, 0, 1, 11, 12, 20, 9, 10, 18, 19, 26]]
