import sys

SERIAL = 0
HOME_MEMNO = 2
CAR_YESNO = 4
HOME_INCOME = 15

def usage():
    print ("Categorize the dataset")
    print ("python3 categorize.py <production input file> <attraction input file> <independent variables file>")
    exit(1)

def analysis(result, f, hf, p):
    f.seek(0)
    f.readline()
    hf.seek(0)
    hf.readline()
    error = 0
    edict = {}

    htmp = hf.readline().strip().split("\t")
    hserial = htmp[SERIAL]
    for line in f:
        tmp = line.strip().split("\t")
        serial = tmp[SERIAL]

        while serial != hserial:
            htmp = hf.readline().strip().split("\t")
            hserial = htmp[SERIAL]

        memno = int(htmp[HOME_MEMNO])
        if memno > 6:
            memno = 6

        try:
            if p == 0:
                result[memno][int(htmp[CAR_YESNO])][int(htmp[HOME_INCOME])]["ahousehold"].add(serial)
                result[memno][int(htmp[CAR_YESNO])][int(htmp[HOME_INCOME])]["attraction"] += 1
            else: # p == 1
                result[memno][int(htmp[CAR_YESNO])][int(htmp[HOME_INCOME])]["phousehold"].add(serial)
                result[memno][int(htmp[CAR_YESNO])][int(htmp[HOME_INCOME])]["production"] += 1
        except ValueError:
            error += 1
            if serial not in edict:
                edict[serial] = 1
            else:
                edict[serial] += 1
    
    return error, edict

def categorize(pf, af, hf, of):
    result = {}
    for i in range(1, 7): # Number of household (1, 2, 3, 4, 5, >=6)
        result[i] = {}
        for j in range(1, 3): # Car (1: no, 2: yes)
            result[i][j] = {}
            for k in range(1, 7): # Income
                result[i][j][k] = {}
                result[i][j][k]["phousehold"] = set([])
                result[i][j][k]["ahousehold"] = set([])
                result[i][j][k]["production"] = 0
                result[i][j][k]["attraction"] = 0

    ep, pd = analysis(result, pf, hf, 1)
    ea, pa = analysis(result, af, hf, 0)
    output_result(result, of)
    print ("Production errors: %d" % ep)
    output_errors(pd, 1)
    print ("Attraction errors: %d" % ea)
    output_errors(pa, 0)

def output_result(result, of):
    s = "home_menno, car_yesno, home_income, num_of_household (p), productions, num_of_household (a), attractions, rate_of_productions, rate_of_attractions\n"
    print (s)
    of.write(s)
    for i in range(1, 7):
        for j in range(1, 3):
            for k in range(1, 7):
                plen = len(result[i][j][k]["phousehold"])
                np = result[i][j][k]["production"]
                if plen > 0:
                    rp = np / plen
                else:
                    rp = 0

                alen = len(result[i][j][k]["ahousehold"])
                na = result[i][j][k]["attraction"]
                if alen > 0:
                    ra = na / alen
                else:
                    ra = 0

                s = "%d, %d, %d, %d, %d, %d, %d, %.02f, %.02f\n" % (i, j, k, plen, np, alen, na, rp, ra)
                print (s)
                of.write(s)

def output_errors(d, p):
    count = 0
    if p == 0:
        print ("Attraction Errors =====")
    else:
        print ("Production Errors =====")

    for k in d.keys():
        print ("  %s: %d" % (k, d[k]))
        count += d[k]

    print ("# of household: %d, errors: %d\n" % (len(d.keys()), count))

def main():
    if len(sys.argv) != 4:
        usage()

    pfname = sys.argv[1]
    afname = sys.argv[2]
    hfname = sys.argv[3]

    pf = open(pfname, "r")
    af = open(afname, "r")
    hf = open(hfname, "r")

    est = int(pfname.split(".")[0].split("_")[-1])
    val = 10 - est
    ofname = "%d_%d_result.csv" % (est, val)
    of = open(ofname, "w")

    categorize(pf, af, hf, of)
    pf.close()
    af.close()
    hf.close()
    of.close()

if __name__ == "__main__":
    main()
