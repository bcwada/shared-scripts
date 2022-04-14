from argparse import ArgumentParser
from tools.basis import Basis

def read_single_arguments():
    description_string = "What is doing."
    parser = ArgumentParser(description=description_string)
    parser.add_argument("-r", "--reactions", type=str, default="", help="Required string")
    return parser.parse_args()


def main():
    args = read_single_arguments()
    
    stringa = args.reactions
    Basis.aa()
    print(stringa)

if __name__ == "__main__":
    main()