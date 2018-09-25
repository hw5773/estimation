import sys
import random

def usage():
    print ("Divide dataset into the estimation set and the validation set according to the input ratio")
    print ("Note that the sum of the estimation ratio and the validation ratio must be 10.")
    print ("python3 divide.py <input dataset> <estimation ratio> <validation ratio>")
    exit(1)

def divide(f, e, v, ofe, ofv):
    s = "sheet_code\tsheet_type\tseq\ttr_seq\ttr_mokjek\ttr_sudan\tstart_type\tstart_zcode\tstart_time\tend_type\tend_zcode\tend_time\tperson\thighway\n"
    ofe.write(s)
    ofv.write(s)
    est = 0
    val = 0

    f.readline()
    for line in f:
        r = random.randint(1, 10)
        if r > e:
            val += 1
            ofv.write(line)
        else:
            est += 1
            ofe.write(line)

    return est, val

def main():
    if len(sys.argv) != 4:
        usage()

    estr = int(sys.argv[2])
    valr = int(sys.argv[3])

    if estr + valr != 10:
        print ("Ratio inputs are wrong!")
        print ("The sum of the estimation and the validation ratios should be 10.")
        usage()

    fname = sys.argv[1]
    f = open(fname, "r")

    if "attraction" in fname:
        ofename = "attraction_estimation_%d.txt" % estr
        ofvname = "attraction_validation_%d.txt" % valr
    elif "production" in fname:
        ofename = "production_estimation_%d.txt" % estr
        ofvname = "production_validation_%d.txt" % valr
    else:
        print ("The input file name should include 'attraction' or 'production'")
        usage()

    ofe = open(ofename, "w")
    ofv = open(ofvname, "w")

    est, val = divide(f, estr, valr, ofe, ofv)
    print ("Total: ", est + val, ", # of Data for estimation: %d (%f)" % (est, (est * 100.0) / (est + val)), ", # of Data for validation: %d (%f)", (val, (val * 100.0) / (est + val)))
    f.close()
    ofe.close()
    ofv.close()

if __name__ == "__main__":
    main()
