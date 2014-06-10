import lux
import pickle
import scipy.stats
import dataManip #have to go and adjust dataManip to load from ../lux.xml...

LUX = lux.LUX("../lux.xml")


def norm_comps():
    with open("wordlist.pkl", "r") as fp:
        words = pickle.load(fp)
    
    
    words = [x for x in words if len(x[1]) == 1]
    
    for x in words:
        primary = x[0]
        noun = x[1][0]
        if primary == "robin's egg": continue
        primary_data = dataManip.getData("../Data", primary, False)
        noun_data = dataManip.getData("../Data", noun, False)
        primary_mu, primary_std = scipy.stats.norm.fit(primary_data)
        noun_mu, noun_std = scipy.stats.norm.fit(noun_data)
        print "For %s and %s" % (primary, noun)
        print primary_mu, primary_std
        print noun_mu, noun_std
        
        #still have to do the stat analysis on this...
        
def are_same():
    with open("wordlist.pkl", "r") as fp:
        words = pickle.load(fp)
    words = [x for x in words if len(x[1]) == 1]
    r2_results = []
    for x in words:
        primary = x[0]
        noun = x[1][0]
        if primary == "robin's egg": continue
        primary = LUX.getColor(primary)
        noun = LUX.getColor(noun)
        primary([0, 0, 0]) #normalizing
        noun([0, 0, 0]) #normalizing
        r2_results.append(dataManip.r2test(primary.name, primary, noun))
        r2_results.append(dataManip.r2test(noun.name, noun, primary))
    
    plt.hist(r2_results, 30)
    plt.show()
    print sum(r2_results) / len(r2_results)
    
are_same()
        
        