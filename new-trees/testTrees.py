from sklearn.ensemble import RandomForestRegressor
from dataManip import *
import pickle
import numpy as np

directory = "./Split + Skew + Broadness - Availability - Adjust"

with open("%s/forest_regressor.pkl" % (directory), "r") as fp:
    forests = pickle.load(fp)

with open("%s/testing_data.pkl" % (directory), "r") as fp:
    testing_data = pickle.load(fp)

initial_results = []

for i, current in enumerate(forests):
    initial_results.append(([current.predict(x[0][i]) for x in testing_data]))

results = []

for x, y, z in zip(initial_results[0], initial_results[1], initial_results[2]):
    temp = np.append(x, y)
    temp = np.append(temp, z)
    results.append(temp)

dkl_tests = []

total = len(results)

fp = open("%s/raw_output.txt" % (directory), "w")

for i, (x, y) in enumerate(zip(results, [x[1] for x in testing_data])):
    print "Testing %d out of %d: %s."  % (i+1, total, y)
    predicted = createDistribution(y, x)
    
    actual = LUX.getColor(y)
    test_result = klDivergence(y, actual, predicted)
    dkl_tests.append(test_result)
    
    fp.write("%s\n%f\n%s\n%s\n\n----\n" % (y, test_result, actual.printStats(), predicted.printStats()))

    plotData(y, LUX.getColor(y), predicted, axis="H", filename="%s/Results/Hue/%s-hue.png" % (directory, y), created=True)
    plotData(y, LUX.getColor(y), predicted, axis="S", filename="%s/Results/Saturation/%s-saturation.png" % (directory, y), created=True)
    plotData(y, LUX.getColor(y), predicted, axis="V", filename="%s/Results/Value/%s-value.png" % (directory, y), created=True)

fp.close()    
     
with open("%s/results.pkl" % (directory), "w") as fp:
    pickle.dump(dkl_tests, fp)