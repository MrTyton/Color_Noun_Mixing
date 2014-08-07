print "Importing Lux"
import lux
LUX = lux.LUX("lux.xml")
import pickle
print "Testing Broadness"
results = {}
with open("broadness_test.txt", "w") as fp:
    total = len(LUX.all)
    for i, x in enumerate(LUX.all):
        print "Testing %d out of %d" % (i+1, total)
        current = LUX.getColor(x)
        current([0, 0, 0])
        a, b, c = current.broadness()
        fp.write("%s:\n\t%f\n, %f, %f\n\n" % (x, a, b, c))
        results[x] = (a, b, c)
with open("broadness_test.pkl", "w") as fp:
    pickle.dump(results, fp)
print "Done"