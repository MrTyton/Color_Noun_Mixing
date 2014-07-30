print "Importing Lux"
import lux
LUX = lux.LUX("lux.xml")
import pickle
#purple = LUX.getColor("purple")
#purple([0, 0, 0])
#hue = purple.dim_models[0]
print "Testing Broadness"
#print hue.broadness(360)
#print purple.dim_models[1].broadness(100)
#print purple.dim_models[2].broadness(100)
results = {}
with open("broadness_test.txt", "w") as fp:
    total = len(LUX.all)
    for i, x in enumerate(LUX.all):
        print "Testing %d out of %d" % (i+1, total)
        current = LUX.getColor(x)
        current([0, 0, 0])
        a, b, c = current.broadness()
        fp.write("%s:\n\t%f\n, %f, %f" % (x, a, b, c))
        results[x] = (a, b, c)
with open("broadness_test.pkl", "w") as fp:
    pickle.dump(results, fp)
print "Done"