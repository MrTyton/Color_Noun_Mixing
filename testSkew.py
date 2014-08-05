print "Importing Lux"
import lux
LUX = lux.LUX("lux.xml")
import pickle
print "Testing Skew"
results = {}
with open("skew_test.txt", "w") as fp:
    total = len(LUX.all)
    for i, x in enumerate(LUX.all):
        print "Testing %d out of %d" % (i+1, total)
        current = LUX.getColor(x)
        current([0, 0, 0])
        a, b, c = current.skew()
        fp.write("%s:\n\t%f\n, %f, %f" % (x, a, b, c))
        results[x] = (a, b, c)
with open("skew_test.pkl", "w") as fp:
    pickle.dump(results, fp)
print "Done"