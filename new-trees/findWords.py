import pickle
import lux

LUX = lux.LUX("../lux.xml")

with open("../Singular Words/wordlist.pkl", "r") as fp:
    noun_colors = pickle.load(fp)

noun_colors = [x[1] for x in noun_colors if len(x[1]) == 1]
noun_colors = [x for y in noun_colors for x in y]

all_colors = LUX.all

composed_colors = {}

for x in all_colors:
    for y in all_colors:
        z = ""
        if "%s %s" % (x, y) in all_colors:
            z = "%s %s" % (x, y)
        if "%s-%s" % (x, y) in all_colors:
            z = "%s-%s" % (x, y)
        if z == "" or z in noun_colors or z in composed_colors or "weird" in z or "ugly" in z or  "ish" in z or "light" in z or "dark" in z or "bright" in z or "pale" in z:
            continue
        else:
            composed_colors[z] = (x, y)

with open("composed_wordlist.pkl", "w") as fp:
    pickle.dump(composed_colors, fp)

print len(composed_colors)

#for x in composed_colors:
#    print x, composed_colors[x] 