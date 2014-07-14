from sklearn.ensemble import RandomForestRegressor
import pickle

directory = "./Fake Data"

with open("%s/training_data.pkl" % (directory), "r") as fp:
    training_data = pickle.load(fp)

print "Creating Forest"

target_data = [x[1][1][2:] for x in training_data]
forests = []
for i in range(len(target_data[0])):
    forest_regressor = RandomForestRegressor()
    forest_regressor.fit([x[0][2:38] + x[0][40:] for x in training_data], [x[i] for x in target_data])
    forests.append(forest_regressor)

with open("%s/forest_regressor.pkl" % (directory), "w") as fp:
    pickle.dump(forests, fp) 
    