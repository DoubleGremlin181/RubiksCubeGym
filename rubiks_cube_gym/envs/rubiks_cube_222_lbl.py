from rubiks_cube_gym.envs.rubiks_cube_222 import RubiksCube222Env
import numpy as np
from operator import itemgetter


class RubiksCube222EnvLBL(RubiksCube222Env):
    def __init__(self):
        super(RubiksCube222EnvLBL, self).__init__()
        self.FL = None
        self.OLL = None
    
    def check_FL(self):
        for pos in FL_POS:
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
        reward = -15 * self.FL - 25 * self.OLL
        done = False
        
        if self.check_FL():
            reward += 15
            self.FL = True
        else:
            self.FL = False
        
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
        super(RubiksCube222EnvLBL, self).reset(scramble=scramble)
        self.FL = self.check_FL()
        self.OLL = self.check_OLL()
        
        return self.cube_state
    
    
FL_POS = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12], [0, 2, 4, 5, 6, 11, 12, 13, 14, 19, 20, 22],
          [2, 3, 5, 6, 7, 8, 13, 14, 15, 16, 20, 21], [1, 3, 7, 8, 9, 10, 15, 16, 17, 18, 21, 23],
          [0, 1, 4, 9, 10, 11, 12, 17, 18, 19, 22, 23], [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]]

OLL_POS = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 20, 21, 22, 23],
           [0, 2, 4, 5, 6, 8, 9, 11, 12, 13, 14, 16, 17, 19, 20, 22],
           [2, 3, 5, 6, 7, 8, 10, 11, 13, 14, 15, 16, 18, 19, 20, 21],
           [1, 3, 4, 5, 7, 8, 9, 10, 12, 13, 15, 16, 17, 18, 21, 23],
           [0, 1, 4, 6, 7, 9, 10, 11, 12, 14, 15, 17, 18, 19, 22, 23],
           [0, 1, 2, 3, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]]
