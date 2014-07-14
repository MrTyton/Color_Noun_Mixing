from sklearn.ensemble import RandomForestRegressor
from dataManip import *
import pickle

directory = "."

with open("%s/forest_regressor.pkl" % (directory), "r") as fp:
    forests = pickle.load(fp)

with open("%s/testing_data.pkl" % (directory), "r") as fp:
    testing_data = pickle.load(fp)

initial_results = []

for current in forests:
    initial_results.append(current.predict([x[0][2:38] + x[0][40:] for x in testing_data]))

results = []
for i in range(len(initial_results[0])):
    results.append([x[i] for x in initial_results])

r2_tests = []

total = len(results)

fp = open("%s/raw_output.txt" % (directory), "w")

for i, (x, y) in enumerate(zip(results, [x[1][0] for x in testing_data])):
    print "Testing %d out of %d"  % (i+1, total)
    predicted = createDistribution(y, x)
    
    actual = LUX.getColor(y)
    test_result = r2test(y, actual, predicted)
    r2_tests.append(test_result)
    
    fp.write("%s\n%f\n%s\n%s\n\n----\n" % (y, test_result, actual.printStats(), predicted.printStats()))

    if i == 0 or i == 5 or i == 27:
        print test_result
        plotData(y, LUX.getColor(y), predicted, axis="H")
        plotData(y, LUX.getColor(y), predicted, axis="S")
        plotData(y, LUX.getColor(y), predicted, axis="V")

fp.close()    
     
with open("%s/results.pkl" % (directory), "w") as fp:
    pickle.dump(r2_tests, fp)