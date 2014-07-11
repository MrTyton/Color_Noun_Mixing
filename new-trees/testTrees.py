from sklearn.ensemble import RandomForestRegressor
from dataManip import *
import pickle

directory = "./Fake Data"

branch = 2

with open("%s/forest_regressor.pkl" % (directory), "r") as fp:
    if branch == 0:
        forest_regressor = pickle.load(fp)
    else:
        forest_regressor_hue, forest_regressor_saturation, forest_regressor_value = pickle.load(fp)

with open("%s/testing_data.pkl" % (directory), "r") as fp:
    testing_data = pickle.load(fp)

if branch == 0:
    results = forest_regressor.predict([x[0] for x in testing_data])
else:
    hues = forest_regressor_hue.predict([x[0][2:14] + x[0][40:52] for x in testing_data])
    saturation = forest_regressor_saturation.predict([x[0][14:26] + x[0][52:64] for x in testing_data])
    value = forest_regressor_value.predict([x[0][26:38] + x[0][64:76] for x in testing_data])
    def appending(x, y, z):
        ans = []
        ans.extend(x)
        ans.extend(y)
        ans.extend(z)
        return ans
    results = [appending(x, y, z) for x, y, z in zip(hues, saturation, value)]

r2_tests = []

total = len(results)

fp = open("%s/raw_output.txt" % (directory), "w")

for i, (x, y) in enumerate(zip(results, [x[1][0] for x in testing_data])):
    print "Testing %d out of %d"  % (i+1, total)
    predicted = createDistribution(y, x)
    if branch != 2:
        actual = LUX.getColor(y)
    else:
        with open("Fake Data/new_wordlist.pkl", "r") as fp2:
            words = pickle.load(fp2)
        actual = createDistribution(y, words[y])
    test_result = r2test(y, actual, predicted)
    r2_tests.append(test_result)
    
    fp.write("%s\n%f\n%s\n%s\n\n----\n" % (y, test_result, actual.printStats(), predicted.printStats()))

    #if i == 0 or i == 1 or i == 5 or i == 27:
    #    print test_result
    #    plotData(y, LUX.getColor(y), predicted, axis="H")
    #    plotData(y, LUX.getColor(y), predicted, axis="S")
    #    plotData(y, LUX.getColor(y), predicted, axis="V")

fp.close()    
     
with open("%s/results.pkl" % (directory), "w") as fp:
    pickle.dump(r2_tests, fp)