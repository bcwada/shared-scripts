import numpy as np
from dataclasses import dataclass


@dataclass
class CasGuess:
    c: np.array

    @classmethod
    def load(cls, c0, numaos, nummos):
        c = np.fromfile(c0)
        c = c.reshape((numaos, nummos))
        return cls(c.T)

    def swap(self, indexi, indexj, matchMolden=True):
        if matchMolden:
            i = indexi - 1
            j = indexj - 1
        else:
            i = indexi
            j = indexj
        temp = self.c[:, i] + 0
        self.c[:, i] = self.c[:, j] + 0
        self.c[:, j] = temp

    def swaprows(self, indexi, indexj, matchMolden=True):
        raise Exception("This would swap your ao labels which you probably don't want to do")
        if matchMolden:
            i = indexi - 1
            j = indexj - 1
        else:
            i = indexi
            j = indexj
        temp = self.c[i, :] + 0
        self.c[i, :] = self.c[j, :] + 0
        self.c[j, :] = temp

    def move(self, i, j):
        # uhh needs tests
        # uhh, always is in molden order
        # moves column i to j
        diff = i - j
        if diff == 0:
            return
        elif diff > 0:
            self.swap(i, i - 1)
            self.swap(i - 1, j)
        elif diff < 0:
            self.swap(i, i + 1)
            self.swap(i + 1, j)

    def save(self, name):
        self.c.T.tofile(name)
