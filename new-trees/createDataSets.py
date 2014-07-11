
from dataManip import *
import pickle
destination = "."

with open("composed_wordlist.pkl", "r") as fp:
    composed_wordlist = pickle.load(fp)
    
composed_wordlist = [(x, composed_wordlist[x][0], composed_wordlist[x][1]) for x in composed_wordlist]

manipulated_wordlist = []

for composed, first, second in composed_wordlist:
    first_color = LUX.getColor(first)
    second_color = LUX.getColor(second)
    first_mu = (first_color.dim_models[0].params[0] + first_color.dim_models[0].params[3]) / 2
    second_mu = (second_color.dim_models[0].params[0] + second_color.dim_models[0].params[3]) / 2
    
    if first_mu < second_mu:
        manipulated_wordlist.append((convertToVector(first) + convertToVector(second), (composed, convertToVector(composed))))
    else:
        manipulated_wordlist.append((convertToVector(second) + convertToVector(first), (composed, convertToVector(composed))))

composed_wordlist = manipulated_wordlist #now composed_wordlist is x, y, z, with x being the lower mu,y being the higher mu, and z being the composed

diff = len(composed_wordlist) - (len(composed_wordlist) / 3)

training_data = composed_wordlist[:diff]
testing_data = composed_wordlist[diff:]

with open("%s/training_data.pkl" % (destination), "w") as fp:
    pickle.dump(training_data,fp)
with open("%s/testing_data.pkl" % (destination), "w") as fp:
    pickle.dump(testing_data, fp)