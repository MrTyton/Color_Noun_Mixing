import lux
import pickle
import scipy.stats
import dataManip #have to go and adjust dataManip to load from ../lux.xml...
import matplotlib.pyplot as plt

LUX = lux.LUX("../lux.xml")


def norm_comps():
    with open("wordlist.pkl", "r") as fp:
        words = pickle.load(fp)
    
    
    words = [x for x in words if len(x[1]) == 1]
    results = []
    for x in words:
        primary = x[0]
        noun = x[1][0]
        if primary == "robin's egg": continue
        primary_data = dataManip.getData("../Data", primary, False)
        noun_data = dataManip.getData("../Data", noun, False)
        primary_mu, primary_std = scipy.stats.norm.fit(primary_data)
        noun_mu, noun_std = scipy.stats.norm.fit(noun_data)
        results.append(((primary, noun), (primary_mu, primary_std), (noun_mu, noun_std)))
        
        #still have to do the stat analysis on this...
    smaller_std = []
    larger_std = []
    hist_plot = []
    for x in results: #figures out if the color + noun is wider/smaller than the color itself, and appends it to the proper list
        first = x[1][1]
        second = x[2][1]
        if first < second:
            smaller_std.append((first - second) / second)
        else:
            larger_std.append((first - second) / second)
        
        hist_plot.append((second - first) / first) #gives how much of a difference the color + noun is from the color, as a percentage difference
    print len(smaller_std) #more of them are wider, which would suggest that when they say the color + noun, they are being less specific about the color, rather than just the noun itself.
    print len(larger_std)
    print len(results)
    
    print (sum(smaller_std) + sum(larger_std)) / len(results)
    
    plt.hist(hist_plot, 30)
    plt.show()
    
    print sum(smaller_std) / len(smaller_std)
    print sum(larger_std) / len(larger_std)
    
    means = []
    for x in results: #figures out how different the means are
        first = x[1][0]
        second = x[2][0]
        means.append((first - second) / second)
        
    print sum(means) / len(means)
        
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
    print sum(r2_results) / len(r2_results) #.37~ about
    
norm_comps()
        
        