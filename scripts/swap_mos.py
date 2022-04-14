from argparse import ArgumentParser
from pathlib import Path
from sharedtools.casguess import CasGuess

def parse():
    parser = ArgumentParser(description="generates a molden file from a c0.casscf file")
    parser.add_argument("c0", type=Path, help="the c0.casscf file to use")
    parser.add_argument("nbf", type=int, help="the number of atomic basis functions")
    parser.add_argument("nmo", type=int, help="the number of molecular orbitals")
    parser.add_argument("mo1", type=int, help="the first column to swap")
    parser.add_argument("mo2", type=int, help="the second column in the swap")
    parser.add_argument("--out", type=str, default="c0_edited.casscf", help="the name of the outputfile")
    return parser.parse_args()

def main():
    args = parse()
    c0 = CasGuess.load(args.c0,args.nbf,args.nmo)
    c0.swap(args.mo1,args.mo2)
    c0.save(args.out)

if __name__ == "__main__":
    main()