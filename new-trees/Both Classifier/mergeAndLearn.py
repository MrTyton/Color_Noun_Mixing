from sklearn.ensemble import RandomForestClassifier
import pickle

with open("results_broad.pkl", "r") as fp:
    broad_results = pickle.load(fp)
    
with open("results_skew.pkl", "r") as fp:
    skew_results = pickle.load(fp)
    
with open("training_data_skew_2.pkl", "r") as fp:
    data = pickle.load(fp)
    
learning = []
results = []  

for datum, broad, skew in zip(data, broad_results, skew_results):
    datum = datum[0][0] + datum[0][1] + datum[0][2]
    learning.append(datum)
    results.append(1 if broad > skew else 0)

print results

classifier = RandomForestClassifier()
classifier.fit(learning, results)

with open("classifier_decider.pkl", "w") as fp:
    pickle.dump(classifier, fp)