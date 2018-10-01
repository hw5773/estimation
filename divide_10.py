import sys

def usage():
    print ("Divide the input dataset into 10 small datasets")
    print ("python3 divide_10.py <input data>")
    exit(1)

def total_lines(f):
    count = 0
    f.seek(0)
    f.readline()

    for line in f:
        count += 1

    return count

def divide(f, of):
    tot = total_lines(f)
    f.seek(0)
    f.readline()
    threshold = tot / 10

    count = 0
    idx = 0

    for line in f:
        count += 1
        if count > threshold:
            count = 1
            idx += 1

        of[idx].write(line)

        if idx == 9:
            break

    for line in f:
        of[idx].write(line)

def main():
    if len(sys.argv) != 2:
        usage()

    fname = sys.argv[1]
    f = open(fname, "r")

    if "production" in fname:
        s = "production"
    else:
        s = "attraction"

    of = {}
    for i in range(10):
        ofname = "output_%s_%d.txt" % (s, i)
        of[i] = open(ofname, "w")

    divide(f, of)

    f.close()

    for i in range(10):
        of[i].close()

if __name__ == "__main__":
    main()
