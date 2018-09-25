import matplotlib.pylab as plt
import sys
import numpy as np

HOME_MENNO = 0
CAR_YESNO = 1
HOME_INCOME = 2
P_HOUSEHOLD = 3
P_MODEL = 4
P_ESTIMATION = 5
P_ANSWER = 6
A_HOUSEHOLD = 7
A_MODEL = 8
A_ESTIMATION = 9
A_ANSWER = 10

def usage():
    print ("Draw graph")
    print ("python3 draw_graph.py <input file>")
    exit(1)

def draw_graph(f, ofname):
    x = []
    pe = []
    pa = []
    ae = []
    aa = []

    f.readline()
    car = {}
    car[1] = "No Car"
    car[2] = "Has Car"

    income = {}
    income[1] = "Under 100"
    income[2] = "Under 200"
    income[3] = "Under 300"
    income[4] = "Under 400"
    income[5] = "Under 500"
    income[6] = "More than 600"

    count = 0
    for line in f:
        count += 1
        tmp = line.strip().split(",")
        xl = "Men: %d\n%s\n%s" % (int(tmp[HOME_MENNO]), car[int(tmp[CAR_YESNO])], income[int(tmp[HOME_INCOME])])
        x.append(count)
        pe.append(float(tmp[P_ESTIMATION]))
        pa.append(int(tmp[P_ANSWER]))
        ae.append(float(tmp[A_ESTIMATION]))
        aa.append(int(tmp[A_ANSWER]))

    vals = [pe, pa, ae, aa]
    n = len(vals)
    xn = np.arange(len(x))
    width = 0.8

    for i in range(n):
        plt.bar(xn - width/2. + i/float(n)*width, vals[i], width=width/float(n), align="edge")
    plt.xticks(xn, x)
    plt.xlabel("Category")
    plt.ylabel("Frequency")
    plt.legend(["Model Outputs of Production", "Answers of Production", "Model Outputs of Attraction", "Answers of Attraction"])
    #plt.legend(["Model Outputs of Attraction", "Answers of Attraction"])

    plt.show()
    plt.savefig(ofname)

def main():
    if len(sys.argv) != 2:
        usage()

    fname = sys.argv[1]
    ofname = "%s.png" % fname.split(".")[0]

    f = open(fname, "r")

    draw_graph(f, ofname)

    f.close()

if __name__ == "__main__":
    main()
