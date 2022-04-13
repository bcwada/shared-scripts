import numpy as np
from dataclasses import dataclass


@dataclass
class casguess:
    c: np.array

    @classmethod
    def load(cls, c0, numaos, nummos):
        c = np.fromfile(c0)
        c = c.reshape((numaos, nummos))
        return cls(c)

    def swap(self, indexi, indexj, matchMolden=True):
        if matchMolden:
            i = indexi-1
            j = indexj-1
        temp = self.c[:, i] + 0
        self.c[:, i] = self.c[:, j] + 0
        self.c[:, j] = temp

    def swaprows(self, indexi, indexj, matchMolden=True):
        if matchMolden:
            i = indexi-1
            j = indexj-1
        temp = self.c[i, :] + 0
        self.c[i, :] = self.c[j, :] + 0
        self.c[j, :] = temp

    def move(self, i, j):
        # moves column i to j
        pass

    def save(self, name):
        self.c.tofile(name)

    def moldenstein(self, transform, moldenfile, writename):
        l = []
        with open(moldenfile) as f:
            for line in f.readlines():
                l.append(line)
                if "[MO]" in line:
                    break
        
        with open(writename,'w') as f:
            f.writelines(l)
            for row in self.c:
                perm_row = transform@row
                f.write(" Ene= 0.0\n")
                f.write(" Spin= alpha\n")
                f.write(" Occup= 2.0000\n")
                for i,coeff in enumerate(perm_row):
                    f.write(f"{i:04d}   {coeff}\n")