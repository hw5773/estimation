import sys
import math
import matplotlib.pyplot as plt
import numpy as np

SERIAL = 0
HOME_MEMNO = 2
CAR_YESNO = 4
HOME_INCOME = 15

def usage():
    print ("Validation the result")
    print ("python3 validation.py <home file> <output file>")
    exit(1)

def frequency(result, f, hf, p):
    f.seek(0)
    f.readline()
    hf.seek(0)
    hf.readline()

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

        if p == 0:
            result[memno][int(htmp[CAR_YESNO])][int(htmp[HOME_INCOME])]["ahousehold"].add(serial)
            result[memno][int(htmp[CAR_YESNO])][int(htmp[HOME_INCOME])]["attraction"] += 1
        else: # p == 1
            result[memno][int(htmp[CAR_YESNO])][int(htmp[HOME_INCOME])]["phousehold"].add(serial)
            result[memno][int(htmp[CAR_YESNO])][int(htmp[HOME_INCOME])]["production"] += 1

def validation(result, model, of):
    s = "home_menno, car_yesno, home_income, num_of_household (p), rate for production, estimation (p), productions, num_of_household (a), rate for attraction, estimation (a), attraction\n"
    of.write(s)
    psum_error_squared = 0.0
    asum_error_squared = 0.0

    for i in range(1, 7):
        for j in range(1, 3):
            for k in range(1, 7):
                plen = len(result[i][j][k]["phousehold"])
                rp = model[i][j][k]["production"]
                ep = plen * rp
                np = result[i][j][k]["production"]

                alen = len(result[i][j][k]["ahousehold"])
                ra = model[i][j][k]["attraction"]
                ea = alen * ra
                na = result[i][j][k]["attraction"]

                s = "%d, %d, %d, %d, %.02f, %.02f, %d, %d, %.02f, %.02f, %d\n" % (i, j, k, plen, rp, ep, np, alen, ra, ea, na)
                of.write(s)
                psum_error_squared += (ep - np) ** 2
                asum_error_squared += (ea - na) ** 2

    pmse = math.sqrt(psum_error_squared / 72.0)
    amse = math.sqrt(asum_error_squared / 72.0)

    return pmse, amse

def analysis(pf, af, rf, hf, of):
    result = {}
    model = {}
    for i in range(1, 7): # Number of household (1, 2, 3, 4, 5, >=6)
        result[i] = {}
        model[i] = {}
        for j in range(1, 3): # Car (1: no, 2: yes)
            result[i][j] = {}
            model[i][j] = {}
            for k in range(1, 7): # Income
                result[i][j][k] = {}
                result[i][j][k]["phousehold"] = set([])
                result[i][j][k]["ahousehold"] = set([])
                result[i][j][k]["production"] = 0
                result[i][j][k]["attraction"] = 0
                model[i][j][k] = {}

    rf.readline()
    for line in rf:
        tmp = line.strip().split(",")
        i = int(tmp[0])
        j = int(tmp[1])
        k = int(tmp[2])
        model[i][j][k]["production"] = float(tmp[-2])
        model[i][j][k]["attraction"] = float(tmp[-1])

    frequency(result, pf, hf, 1)
    frequency(result, af, hf, 0)
    pmse, amse = validation(result, model, of)
    return pmse, amse

def draw_graph(fname):
    f = open(fname, "r")
    f.readline()

    x = []
    p = []
    a = []

    for line in f:
        tmp = line.strip().split(",")
        label = "%d" % int(tmp[0])
        x.append(label)
        p.append(float(tmp[1]))
        a.append(float(tmp[2]))

    vals = [p, a]
    n = len(vals)
    xn = np.arange(len(x))
    width = 0.8

    for i in range(n):
        plt.bar(xn - width/2. + i/float(n) * width, vals[i], width=width/float(n), align="edge")
    plt.xticks(xn, x)
    plt.xlabel("Estimation set to validation set")
    plt.ylabel("Root-Mean-Squared-Error (RMSE)")
    plt.legend(["Production", "Attraction"])
    figname = "rmse.png"
    plt.savefig(figname)
    plt.show()
    f.close()

def main():
    if len(sys.argv) != 3:
        usage()

    hfname = sys.argv[1]
    hf = open(hfname, "r")

    out_name = sys.argv[2]
    out = open(out_name, "w")

    s = "estimation rate, validation rate, pmse, amse\n"
    out.write(s)
    print (s)

    for i in range(10):
        pfname = "production_validation_%d.txt" % i
        afname = "attraction_validation_%d.txt" % i
        rfname = "%d_result.csv" % i
        ofname = "%d_validation.csv" % i

        pf = open(pfname, "r")
        af = open(afname, "r")
        rf = open(rfname, "r")
        of = open(ofname, "w")

        pmse, amse = analysis(pf, af, rf, hf, of)

        s = "%d, %.02f, %.02f\n" % (i, pmse, amse)
        out.write(s)
        print (s)
        pf.close()
        af.close()
        rf.close()
        of.close()

    hf.close()
    out.close()
    draw_graph(out_name)

if __name__ == "__main__":
    main()
