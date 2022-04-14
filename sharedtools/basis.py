from dataclasses import dataclass
import numpy as np
from pathlib import Path

@dataclass
class Basis:
    # quick version of basis
    aos: dict

    @classmethod
    def from_molden(cls, molden_file):
        with open(molden_file) as f:
            block = None
            skip_lines = 0
            for line in f.readlines():
                if not skip_lines == 0:
                    skip_lines -= 1
                    continue
                if line.isspace():
                    continue
                if "[GTO]" in line:
                    block = "gto"
                    aos = {}
                    continue
                if "[MO]" in line:
                    block = "mo"
                    continue
                if block == "gto":
                    s = line.split()
                    if s[-1] == "0":
                        # atom line
                        atom = s[0]
                        orb_counts = {"s": 0, "p": 0, "d": 0, "f": 0}
                    if s[-1] == "1.00":
                        # basis line
                        orb = s[0]
                        orb_counts[orb] += 1
                        ind = orb_counts[orb]
                        aos[atom + "_" + orb + str(ind)] = [int(s[1])]
                    else:
                        # otherwise
                        pass

                if block == "mo":
                    break
        return cls(aos)

    @staticmethod
    def _orb_ind(s):
        if s == "s":
            return 0
        if s == "p":
            return 1
        if s == "d":
            return 2
        if s == "f":
            return 3

    def to_tc_order(self):
        # generates a matrix U such that U*C yeilds C with aos in tc order
        L = []
        for key in self.aos.keys():
            s = key.split("_")
            orb_ind = self._orb_ind(s[1][0])
            if orb_ind == 0:
                L.append((orb_ind, 0, int(s[0])))
            elif orb_ind == 1:
                for l in range(3):
                    L.append((orb_ind, int(s[0]), int(s[1][1:]), l))
            elif orb_ind == 2:
                L.append((orb_ind, int(s[0]), int(s[1][1:]), 3))
                L.append((orb_ind, int(s[0]), int(s[1][1:]), 4))
                L.append((orb_ind, int(s[0]), int(s[1][1:]), 5))
                L.append((orb_ind, int(s[0]), int(s[1][1:]), 0))
                L.append((orb_ind, int(s[0]), int(s[1][1:]), 1))
                L.append((orb_ind, int(s[0]), int(s[1][1:]), 2))
            else:
                raise Exception("f orbs not implemented in TC as of early 2022")
        decorated = [(L[i], i) for i in range(len(L))]
        # print(decorated)
        decorated.sort()
        # print(decorated)
        U = [np.eye(len(L))[i[1]] for i in decorated]
        return np.array(U)
