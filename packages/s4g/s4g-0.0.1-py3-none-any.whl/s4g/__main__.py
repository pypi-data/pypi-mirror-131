from sys import argv, exit
from s4g import render

def main():
    if len(argv) != 4:
        print("Usage: s4g path/to/src path/to/dst path/to/template")
        exit(-1)

    render.generate(argv[1], argv[2], argv[3])

if __name__ == "__main__":
    main()