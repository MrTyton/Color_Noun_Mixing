
from dataManip import *
import pickle
destination = "./Split + Skew + Broadness - Availability - Adjust"

with open("composed_wordlist.pkl", "r") as fp:
    composed_wordlist = pickle.load(fp)
    
composed_wordlist = [(x, composed_wordlist[x][0], composed_wordlist[x][1]) for x in composed_wordlist]

manipulated_wordlist = []

for i, (composed, first, second) in enumerate(composed_wordlist):
    print "Working on %d out of %d, %s and %s." % (i+1, len(composed_wordlist), first, second)
    with open("../skew_test.pkl", "r") as fp:
        broadness = pickle.load(fp)
    
    current = []
    start = 2
    first_vector = convertToVector(first)
    second_vector = convertToVector(second)
    for x, y in zip(broadness[first], broadness[second]):
        first_comparison = x#log(x)
        first_vector[1] = first_comparison
        second_comparison = y#log(y)
        second_vector[1] = second_comparison
        if first_comparison > second_comparison:
            current.append((first_vector[1:2] + first_vector[start:start+12] + second_vector[1:2] + second_vector[start:start+12]))
        else:
            current.append((second_vector[1:2] + second_vector[start:start+12] + first_vector[1:2] + first_vector[start:start+12]))
        start += 12
    composed_vector = convertToVector(composed)
    manipulated_wordlist.append(((current[0], current[1], current[2]), composed, (composed_vector[2:14], composed_vector[14:26], composed_vector[26:38])))       
                                
composed_wordlist = manipulated_wordlist #now composed_wordlist is x, y, z, with x being the less broad, y being the more broad, and z being the composed

diff = len(composed_wordlist) - (len(composed_wordlist) / 3)

training_data = composed_wordlist[:diff]
testing_data = composed_wordlist[diff:]

with open("%s/training_data.pkl" % (destination), "w") as fp:
    pickle.dump(training_data,fp)
with open("%s/testing_data.pkl" % (destination), "w") as fp:
    pickle.dump(testing_data, fp)