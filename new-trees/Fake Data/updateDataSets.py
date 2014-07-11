import pickle

with open("training_data.pkl", "r") as fp:
    training_data = pickle.load(fp)

with open("testing_data.pkl", "r") as fp:
    testing_data = pickle.load(fp)
    
with open("new_wordlist.pkl", "r") as fp:
    words = pickle.load(fp)

temp = []

for x in training_data:
    name = x[1][0]
    temp.append((x[0], (name, [0, 0] + words[name])))
    
training_data = temp
    
with open("training_data.pkl", "w") as fp:
    pickle.dump(training_data, fp)

temp = []
for x in testing_data:
    name = x[1][0]
    temp.append((x[0], (name, [0, 0] + words[name])))
    
testing_data = temp
    
with open("testing_data.pkl","w") as fp:
    pickle.dump(testing_data, fp)