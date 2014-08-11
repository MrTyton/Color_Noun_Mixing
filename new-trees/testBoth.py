from sklearn.ensemble import RandomForestRegressor
from dataManip import *
import pickle
import numpy as np

directory = "./Both Classifier"

with open("%s/forest_regressor_skew.pkl" % (directory), "r") as fp:
    forests_skew = pickle.load(fp)

with open("%s/testing_data_skew.pkl" % (directory), "r") as fp:
    testing_data_skew = pickle.load(fp)
    
with open("%s/forest_regressor_broad.pkl" % (directory), "r") as fp:
    forests_broad = pickle.load(fp)

with open("%s/testing_data_broad.pkl" % (directory), "r") as fp:
    testing_data_broad = pickle.load(fp)
    
with open("%s/classifier_decider.pkl" % (directory), "r") as fp:
    classifier = pickle.load(fp) 

initial_results = [[],[],[]]

for i, (current_skew, current_broad, current_result) in enumerate(zip(forests_skew, forests_broad, initial_results)):
    for x, y in zip(testing_data_skew, testing_data_broad):
        full = x[0][0] + x[0][1] + x[0][2]
        use = classifier.predict(full)
        if use == 1:
            print "Used Skew"
            current_result.append(current_skew.predict(x[0][i]))
        else:
            print "Used Broad"
            current_result.append(current_broad.predict(y[0][i]))

results = []

for x, y, z in zip(initial_results[0], initial_results[1], initial_results[2]):
    
    temp = np.append(x, y)
    temp = np.append(temp, z)
    results.append(temp)

dkl_tests = []

total = len(results)

fp = open("%s/raw_output_final.txt" % (directory), "w")

for i, (x, y) in enumerate(zip(results, [x[1] for x in testing_data_skew])):
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
     
with open("%s/results_final.pkl" % (directory), "w") as fp:
    pickle.dump(dkl_tests, fp)