import os
import sys

if __name__ == '__main__':
    open("codegen_replaced.sq", 'w').close()
    
    with open (sys.argv[1], "rt") as fin:
        with open (sys.argv[2], "wt") as fout:
            for line in fin:
                fout.write(line.replace('$INPUTFILE', sys.argv[3]))
