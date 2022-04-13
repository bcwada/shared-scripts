from dataclasses import dataclass
import numpy as np
from pathlib import Path

# basis should probably fuse with molden at some point
import tools.molden
import tools.ntoTools as nto


@dataclass
class basis:
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


def main():
    c0 = np.fromfile("/home/bcwada/restructuring/researchCode/testing/testing_files/IT_FC_161302_c0")
    c0 = c0.reshape((122, 122))
    molden_file = Path("/home/bcwada/restructuring/researchCode/testing/testing_files/2IT_FC_161302_nto_S0-S1.molden")
    molden_obj = tools.molden.molden.load(molden_file)
    nto_obj = nto.Nto.from_vector_file("/home/bcwada/restructuring/researchCode/testing/testing_files/2IT_FC_161302_nto_S0-S1_vector")
    basis_obj = basis.from_molden(molden_file)
    SMat = np.genfromtxt("/home/bcwada/restructuring/researchCode/testing/testing_files/IT_FC_TC_order.txt", skip_header=2)
    """
    print(c0.T@SMat@c0)
    simMat = np.isclose(c0.T@SMat@c0, np.eye(122))
    for i in range(122):
        for j in range(122):
            if not simMat[i,j]:
                pass
                print((c0.T@SMat@c0)[i,j])
                #print(i,j)
                #print(simMat[i,j])
    """
    assert np.isclose(c0.T @ SMat @ c0, np.eye(122), atol=1e-6).all()
    U = basis_obj.to_tc_order()
    alt_SMat = U.T @ SMat @ U
    # print(molden_obj.mo_coeff[:,0])
    # print(nto_obj.holes[0])
    # print(type(nto_obj.holes[0]))
    assert np.isclose(U @ molden_obj.mo_coeff[:, 0], nto_obj.holes[0], atol=1e-4).all()
    print(molden_obj.mo_coeff[:, 1])
    print(nto_obj.parts[0])
    print(np.isclose(U @ molden_obj.mo_coeff[:, 1], nto_obj.parts[0], atol=1e-4))
    assert np.isclose(U @ molden_obj.mo_coeff[:, 1], nto_obj.parts[0], atol=1e-4).all()
    ovlp1_ml = molden_obj.mo_coeff[:, 1] @ alt_SMat @ molden_obj.mo_coeff[:, 1]
    ovlp1_tc = nto_obj.holes[1] @ SMat @ nto_obj.holes[1]
    print(ovlp1_ml, ovlp1_tc)


if __name__ == "__main__":
    main()
