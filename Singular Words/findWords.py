import lux
import pickle

LUX = lux.LUX('../lux.xml')

names = LUX.all.keys()

name_groups = []

for x in names:
    for y in names:
        if x is not y and x in y and "dark" not in y and "light" not in y and "bright" not in y and "pale" not in y:
            name_groups.append([x, y])

print len(name_groups)

groups_copy = name_groups[:]
for x in groups_copy:
    print("Do you wish to keep the following:\n\n%s\n\t%s\n" % (x[0], x[1]))
    ans = raw_input("Blank for yes, n for no: ")
    if ans != "":
        name_groups.remove(x)
    print ""
    

fp = open("wordlist.txt", "w")

for x in name_groups:
    fp.write("%s\n\t%s\n" % (x[0], x[1]))
        
fp.close()  

fp = open("wordlist.pkl", "w")
pickle.dump(name_groups, fp)
fp.close()