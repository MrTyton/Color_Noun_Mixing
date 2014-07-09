from sklearn.ensemble import RandomForestRegressor
from dataManip import *
import pickle

with open("training_data.pkl", "r") as fp:
    training_data = pickle.load(fp)

print "Creating Forest"

forest_regressor = RandomForestRegressor()
forest_regressor.fit([x[0] for x in training_data], [x[1][1] for x in training_data])

#print forest_regressor.feature_importances_ #have to use this to see which features it finds important, could be trying to predict too many things at once

with open("testing_data.pkl", "r") as fp:
    testing_data = pickle.load(fp)

results = forest_regressor.predict([x[0] for x in testing_data])

r2_tests = []

total = len(results)

fp = open("raw_output.txt", "w")

for i, (x, y) in enumerate(zip(results, [x[1][0] for x in testing_data])):
    print "Testing %d out of %d"  % (i+1, total)
    predicted = createDistribution(y, x)
    test_result = r2test(y, LUX.getColor(y), predicted)
    r2_tests.append(test_result)
    
    fp.write("%s\n%f\n%s\n%s\n\n----\n" % (y, test_result, LUX.getColor(y).printStats(), predicted.printStats()))

fp.close()    
     
with open("results.pkl", "w") as fp:
    pickle.dump(r2_tests, fp)
    
    