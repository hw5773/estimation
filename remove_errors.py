import sys

SERIAL = 0
HOME_MEMNO = 2
CAR_YESNO = 4
HOME_INCOME = 15

def usage():
    print ("Remove error data")
    print ("python3 remove_errors.py <input data>")
    exit(1)

def main():
    if len(sys.argv) != 2:
        usage()

    fname = sys.argv[1]
    f = open(fname, "r")
    ofname = "%s_revised.txt" % fname.split(".")[0]
    of = open(ofname, "w")
    efname = "%s_errors.txt" % fname.split(".")[0]
    ef = open(efname, "w")

    ememno = 0
    ecar = 0
    eincome = 0

    for line in f:
        tmp = line.strip().split("\t")
        memno = tmp[HOME_MEMNO]
        car = tmp[CAR_YESNO]
        income = tmp[HOME_INCOME]

        if memno == ' ' or car == ' ' or income == ' ':
            if memno == ' ':
                ememno += 1
            if car == ' ':
                ecar += 1
            if income == ' ':
                eincome += 1
            s = "%s\n" % tmp[SERIAL]
            ef.write(s)
            continue
        of.write(line)

    print ("ememno: %d, ecar: %d, eincome: %d" % (ememno, ecar, eincome))
    f.close()
    of.close()
    ef.close()

if __name__ == "__main__":
    main()
