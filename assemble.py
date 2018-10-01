import sys

def usage():
    print ("Make dataset")
    print ("python3 assemble.py <production/attraction>")
    exit(1)

def main():
    if len(sys.argv) != 2:
        usage()

    s = sys.argv[1]

    for i in range(10):
        f = open("output_%s_%d.txt" % (s, i), "r")
        af = {}

        for j in range(10):
            if j == i:
                continue
            af[j] = open("output_%s_%d.txt" % (s, j), "r")
    
        ofename = "%s_estimation_%d.txt" % (s, i)
        ofvname = "%s_validation_%d.txt" % (s, i)

        ofe = open(ofename, "w")
        ofv = open(ofvname, "w")

        for line in f:
            ofv.write(line)

        for k in af.keys():
            for line in af[k]:
                ofe.write(line)

        f.close()
        for k in af.keys():
            af[k].close()

if __name__ == "__main__":
    main()
