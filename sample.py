import sys

START = 7
END = 10
SEOUL = "01"
SERIAL = 0

def usage():
    print ("Sample manageable data")
    print ("python3 sample.py <input data> <home error data>")
    exit(1)

def sample(f, ofp, ofa, errors):
    title = f.readline()
    ofp.write(title)
    ofa.write(title)

    lines = 0
    out = 0
    err = 0
    within = 0
    productions = 0
    attractions = 0

    for line in f:
        lines = lines + 1
        tmp = line.strip().split("\t")
        start_city = tmp[START].split("-")[0]
        end_city = tmp[END].split("-")[0]
        serial = tmp[SERIAL]

        # Exclude the error data.
        if serial in errors:
            err += 1
            continue

        # Exclude the trips outside of Seoul.
        if start_city != SEOUL and end_city != SEOUL:
            out += 1
            continue
        
        # Exclude the trips within Seoul
        if start_city == SEOUL and end_city == SEOUL:
            within += 1
            continue

        # Extract the trips from Seoul to outside (production)
        if start_city == SEOUL and end_city != SEOUL:
            productions += 1
            ofp.write(line)

        # Extract the trips from outside to Seoul (attraction)
        if start_city != SEOUL and end_city == SEOUL:
            attractions += 1
            ofa.write(line)

    print ("Total: ", lines, ", Outside of Seoul: ", out, ", Within Seoul: ", within, ", From Seoul to outside: ", productions, " From outside to Seoul: ", attractions, ", Errors: ", err)

def main():
    if len(sys.argv) != 3:
        usage()

    # output files: seoul_production.txt, seoul_attraction.txt
    ofpname = "seoul_production.txt"
    ofaname = "seoul_attraction.txt"
    ofp = open(ofpname, "w")
    ofa = open(ofaname, "w")

    # open the input file
    fname = sys.argv[1]
    f = open(fname, "r")

    efname = sys.argv[2]
    ef = open(efname, "r")
    errors = []

    for line in ef:
        serial = line.strip()
        errors.append(serial)

    ef.close()

    sample(f, ofp, ofa, errors)

    # close the input/output files
    f.close()
    ofp.close()
    ofa.close()

if __name__ == "__main__":
    main()
