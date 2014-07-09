import lux
import pickle
import scipy.stats
import numpy as np
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
        primary_data = dataManip.getData("../Data", primary, False) #have to split them up.........
        noun_data = dataManip.getData("../Data", noun, False)
        primary_mu, primary_std = scipy.stats.norm.fit([x[0] for x in primary_data])
        noun_mu, noun_std = scipy.stats.norm.fit([x[0] for x in noun_data])
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
    plt.hist(means, 30)
    plt.show()
        
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
    
    #plt.hist(r2_results, 30)
    #plt.show()
    print sum(r2_results) / len(r2_results) #.37~ about

def compareGauss():
    legend_val = []
    name = "avocado"
    axis = 0
    data = dataManip.getData("../Data", name)
    data = [x[axis] for x in data]
    linspace = np.linspace(max([0, min(data)-20]), 100 if max(data) <= 100 else min([max(data) + 20, 360]), num=500)
    avocado = LUX.getColor(name)
    avocado([0, 0, 0])
    phi_values = [avocado.dim_models[axis].phi(x) for x in linspace]
    plt.hist(data, bins=30, normed=True, color='w')
    first_dist, = plt.plot(linspace, phi_values, color='r')
    legend_val.append(first_dist)
    legend_label = ["Original " + name]
    data = [x[0] for x in dataManip.getData("../Data", name, False)]
    mu, std = scipy.stats.norm.fit(data)
    created_norm = scipy.stats.norm(loc=mu, scale=std)
    phi_values = [created_norm.pdf(x) for x in linspace]
    second_dist, = plt.plot(linspace, phi_values, color='b', label='second_distribution')
    legend_val.append(second_dist)
    legend_label.append("Created " + name)
    
    name = "avocado green"
    data = dataManip.getData("../Data", name)
    data = [x[axis] for x in data]
    linspace = np.linspace(max([0, min(data)-20]), 100 if max(data) <= 100 else min([max(data) + 20, 360]), num=500)
    avocado = LUX.getColor(name)
    avocado([0, 0, 0])
    phi_values = [avocado.dim_models[axis].phi(x) for x in linspace]
    plt.hist(data, bins=30, normed=True, color='w')
    first_dist, = plt.plot(linspace, phi_values, color='g', label='third_distribution')
    legend_val.append(first_dist)
    legend_label.append("Original " + name)
    data = [x[0] for x in dataManip.getData("../Data", name, False)]
    mu, std = scipy.stats.norm.fit(data)
    created_norm = scipy.stats.norm(loc=mu, scale=std)
    phi_values = [created_norm.pdf(x) for x in linspace]
    second_dist, = plt.plot(linspace, phi_values, color='c', label='fourth_distribution')
    legend_val.append(second_dist)
    legend_label.append("Created " + name)
    
    
    plt.legend(legend_val, legend_label)
    plt.xlabel("Value")
    plt.ylabel("Probability/Count (Histogram is Normalized")
    #plt.suptitle("%s versus %s on %s's data" % (first_distribution, second_distribution, first_distribution))
    plt.xlim(max([0, min(data)-20]), 100 if max(data) <= 100 else min([max(data) + 20, 360]))
    plt.show()
    plt.clf()
    return

#norm_comps()
#are_same()
compareGauss()
        
        