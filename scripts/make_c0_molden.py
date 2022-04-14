from argparse import ArgumentParser
from pathlib import Path
from sharedtools.basis import Basis
from sharedtools.casguess import CasGuess


def c0_to_molden(c_matrix, transform, moldenfile, writename):
    outputlines = []
    with open(moldenfile) as f:
        for line in f.readlines():
            outputlines.append(line)
            if "[MO]" in line:
                break
    with open(writename, "w") as f:
        f.writelines(outputlines)
        for col in c_matrix.T:
            perm_col = transform @ col
            f.write(" Ene= 0.0\n")
            f.write(" Spin= alpha\n")
            f.write(" Occup= 2.0000\n")
            for i, coeff in enumerate(perm_col):
                f.write(f"{i:04d}   {coeff}\n")


def parse():
    parser = ArgumentParser(description="generates a molden file from a c0.casscf file")
    parser.add_argument("c0", type=Path, help="the c0.casscf file to use")
    parser.add_argument("nbf", type=int, help="the number of atomic basis functions")
    parser.add_argument("nmo", type=int, help="the number of molecular orbitals")
    parser.add_argument("molden", type=Path, help="a reference molden file to copy the basis information from")
    parser.add_argument("--out", type=str, default="c0.casscf", help="the name of the file to save to")
    return parser.parse_args()


def main():
    args = parse()
    molden_basis = Basis.from_molden(args.molden)
    # U is the molden to tc permutation matrix
    U = molden_basis.to_tc_order()
    cas = CasGuess.load(args.c0,args.nbf,args.nmo)
    c0_to_molden(cas.c, U.T, args.molden, args.out+".molden")

if __name__ == "__main__":
    main()
