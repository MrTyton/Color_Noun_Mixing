import dataManip
import pickle


with open("composed_wordlist.pkl", "r") as fp:
    words = pickle.load(fp)
    
newwords = {}    
for x in words:
    first = words[x][0]
    second = words[x][1]
    first = dataManip.convertToVector(first)[2:]
    second = dataManip.convertToVector(second)[2:]
    newwords[x] = [(w + y) / 2. for w, y in zip(first, second)]
    
with open("Fake Data/new_wordlist.pkl", "w") as fp:
    pickle.dump(newwords, fp)
    
