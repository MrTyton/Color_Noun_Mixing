import lux
import pickle

LUX = lux.LUX('../lux.xml')

names = LUX.all.keys()

name_groups = []

for x in names:
    for y in names:
        if x is not y and x in y and "dark" not in y and "light" not in y and "bright" not in y and "pale" not in y:
            try:
                name_groups[x].append(y)
            except KeyError:
                name_groups[x] = [y]

name_groups = [(x, name_groups[x]) for x in name_groups]

name_groups.sort(key=lambda x: len(x[1]))

print len(name_groups)

groups_copy = name_groups[:]
for x in groups_copy:
    print("Do you wish to keep the following:\n\n%s\n" % (x[0]))
    for y in x[1]:
        print("\t%s\n" % y)
    ans = raw_input("Blank for yes, n for no: ")
    if ans != "":
        name_groups.remove(x)
    print ""
    

fp = open("wordlist.txt", "w")

for x in name_groups:
    fp.write("%s\n" % (x[0]))
    for y in x[1]:
        fp.write("\t%s\n" % y)
        
fp.close()

fp = open("wordlist.pkl", "w")
pickle.dump(name_groups, fp)
fp.close()