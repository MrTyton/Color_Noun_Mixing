
from dataManip import *
import pickle
destination = "./Full + Broadness - Availability - Adjust"

with open("composed_wordlist.pkl", "r") as fp:
    composed_wordlist = pickle.load(fp)
    
composed_wordlist = [(x, composed_wordlist[x][0], composed_wordlist[x][1]) for x in composed_wordlist]

manipulated_wordlist = []

for i, (composed, first, second) in enumerate(composed_wordlist):
    print "Working on %d out of %d, %s and %s." % (i+1, len(composed_wordlist), first, second)
    with open("../broadness_test.pkl", "r") as fp:
        broadness = pickle.load(fp)
        first_comparison = sum([log(x) for x in broadness[first]])
        second_comparison = sum([log(x) for x in broadness[second]])
    
    if first_comparison > second_comparison:
        manipulated_wordlist.append((convertToVector(first, broad=first_comparison) + convertToVector(second, broad=second_comparison), (composed, convertToVector(composed))))
    else:
        manipulated_wordlist.append((convertToVector(second, broad=second_comparison) + convertToVector(first, broad=first_comparison), (composed, convertToVector(composed))))

composed_wordlist = manipulated_wordlist #now composed_wordlist is x, y, z, with x being the less broad, y being the more broad, and z being the composed

diff = len(composed_wordlist) - (len(composed_wordlist) / 3)

training_data = composed_wordlist[:diff]
testing_data = composed_wordlist[diff:]

with open("%s/training_data.pkl" % (destination), "w") as fp:
    pickle.dump(training_data,fp)
with open("%s/testing_data.pkl" % (destination), "w") as fp:
    pickle.dump(testing_data, fp)