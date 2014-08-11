from sklearn.ensemble import RandomForestRegressor
import pickle

directory = "./Split + Broadness - Availability - Adjust"

with open("%s/training_data.pkl" % (directory), "r") as fp:
    training_data = pickle.load(fp)

print "Creating Forest"

forests = []

for i in range(0, 3):
    current_forest = RandomForestRegressor()
    current_forest.fit([x[0][i] for x in training_data], [x[2][i] for x in training_data])
    forests.append(current_forest)

with open("%s/forest_regressor.pkl" % (directory), "w") as fp:
    pickle.dump(forests, fp) 
    