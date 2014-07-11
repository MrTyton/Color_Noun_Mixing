from sklearn.ensemble import RandomForestRegressor
import pickle

directory = "./Fake Data"

with open("%s/training_data.pkl" % (directory), "r") as fp:
    training_data = pickle.load(fp)

print "Creating Forest"


branch = 1

if branch == 0:
    forest_regressor = RandomForestRegressor()
    forest_regressor.fit([x[0] for x in training_data], [x[1][1] for x in training_data])
    with open("%s/forest_regressor.pkl" % (directory), "w") as fp:
        pickle.dump(forest_regressor, fp)
else:
    forest_regressor_hue = RandomForestRegressor()
    forest_regressor_saturation = RandomForestRegressor()
    forest_regressor_value = RandomForestRegressor()
    forest_regressor_hue.fit([x[0][2:14] + x[0][40:52] for x in training_data], [x[1][1][2:14] for x in training_data])
    forest_regressor_saturation.fit([x[0][14:26] + x[0][52:64] for x in training_data], [x[1][1][14:26] for x in training_data])
    forest_regressor_value.fit([x[0][26:38] + x[0][64:76] for x in training_data], [x[1][1][26:38] for x in training_data])
    with open("%s/forest_regressor.pkl" % (directory), "w") as fp:
        pickle.dump((forest_regressor_hue, forest_regressor_saturation, forest_regressor_value), fp)
#print forest_regressor.feature_importances_ #have to use this to see which features it finds important, could be trying to predict too many things at once


    
    