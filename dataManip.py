from math import log
import lux
LUX = lux.LUX('lux.xml')
import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy

def getData(location, name, test=True):
    name = name.replace('-', '')
    name = name.replace(" ", "")
    if test:
        fp = open("%s/data/%s.test" % (location, name));  #important lines are this one and the next 3
        data = [[float(y) for y in x.replace("\n","").split(",")] for x in fp.readlines()];
        data = [[x[0]*360, x[1]*100, x[2]*100] for x in data]
        fp.close()
    else:
        fp_hue = open("%s/data/%s.h_train" % (location, name))
        fp_sat = open("%s/data/%s.s_train" % (location, name))
        fp_val = open("%s/data/%s.v_train" % (location, name))
        data = [[float(x.replace("\n", "")), float(y.replace("\n", "")), float(z.replace("\n", ""))] for x, y, z in zip(fp_hue.readlines(), fp_sat.readlines(), fp_val.readlines())]
        data = [[x[0]*360, x[1]*100, x[2]*100] for x in data]
        fp_hue.close()
        fp_sat.close()
        fp_val.close()
    return data

def testDistributions(real_distribution, created_distribution):
    test_data = getData("Data", real_distribution.name)
    log_learned = 0.0
    log_predicted = 0.0
    cross_entropy = 0.0
    offset = 0#.0000001 #mess with this
    for value in test_data:
        lp = real_distribution(value)
        log_learned += log(lp + offset)
        pp = created_distribution(value)
        log_predicted += log(pp + offset)
        cross_entropy += lp * log(pp + offset)
        #+perp = 2 ^ average log likelihood
    return log_learned, log_predicted, len(test_data), 2 ** -cross_entropy

def sortAvail(x, y):
    if LUX.getColor(x).availability > LUX.getColor(y).availability:
        larger = x
        smaller = y
    else:
        larger = y
        smaller = x
    return smaller, larger

def getWordLists(method=sortAvail, checkRedundancy = True):
    single_words = []
    for x in LUX.all:
        if LUX.getColor(x).isSingleWord() : single_words.append(x)
    single_words.remove("apple")
    single_words.remove("skin")
    single_words.remove("pale")
    single_words = [x for x in single_words if x[-3:] != "ish"]
    combinations = []
    combos = []
    for x in single_words:
        for y in single_words:
            if x + " " + y in LUX.all:
                smaller, larger = method(x, y)
                if (smaller, larger) not in combos and checkRedundancy:
                    combos.append((smaller, larger))
                combinations.append((smaller, larger, x + " " + y))
            elif x + "-" + y in LUX.all:
                smaller, larger = method(x, y)
                if (smaller, larger) not in combos and checkRedundancy:
                    combos.append((smaller, larger))
                combinations.append((smaller, larger, x + "-" + y))
            elif y + " " + x in LUX.all:
                smaller, larger = method(y, x)
                if (smaller, larger) not in combos and checkRedundancy:
                    combos.append((smaller, larger))
                combinations.append((smaller, larger, y + " " + x))
            elif y + "-" + x in LUX.all:
                smaller, larger = method(y, x)
                if (smaller, larger) not in combos and checkRedundancy:
                    combos.append((smaller, larger))
                combinations.append((smaller, larger, y + "-" + x))
    return combinations

def convertToVector(color_name, twoWord=False):
    color = LUX.getColor(color_name)
    vector = []
    vector.append(color.availability)
    vector.append(1) if color.hue_adjust else vector.append(0)
    for single_dim in color.dim_models:
        vector += single_dim.params
        vector += single_dim.stdevs
    return vector

def createDistribution(color_name, replacement_vector):
    ans = deepcopy(LUX.getColor(color_name))
    ans.availability = replacement_vector[0]
    if replacement_vector[1] == 1:
        ans.hue_adjust = True
    else:
        ans.hue_adjust = False
    ans.dim_models[0].hue_adjust = ans.hue_adjust
    ans.dim_models[0].params = replacement_vector[2:8]
    ans.dim_models[0].stdevs = replacement_vector[8:14]
    ans.dim_models[1].params = replacement_vector[14:20]
    ans.dim_models[1].stdevs = replacement_vector[20:26]
    ans.dim_models[2].params = replacement_vector[26:32]
    ans.dim_models[2].stdevs = replacement_vector[32:38]
    for x in ans.dim_models:
        x.reload()
    return ans

def output(first_model, second_model, learned, predict, num_points, test, perplexity, fp=None):
    if (fp is None):
        print "%s model on %s points:\t%f\n%s model on %s points:\t%f\nTotal Points:\t%d\nLog Likelihood Ratio:\t%f\nPerplexity of %s on %s:\t%f\n" % (first_model , first_model, learned , second_model , first_model , predict , num_points, test, second_model, first_model, perplexity)
    else:
        fp.write("Availability of Real %s model:\t%f\nAvailability of Created %s model:\t%f\nPercentage Change of Availabilities:\t%f\n\nReal %s model on %s points:\t%f\nCreated %s model on %s points:\t%f\nTotal Points:\t%d\nLog Likelihood Ratio:\t%f\nPerplexity of %s on %s:\t%f\n\nRaw Models:\n%s\n\n--------------\n\n" % (first_model, first_model.availability, second_model, second_model.availability, (second_model.availability - first_model.availability) /  first_model.availability, first_model , first_model, learned , second_model , first_model , predict , num_points, test, second_model, first_model, perplexity, first_model.printStats() + "\n\n" + second_model.printStats()))
    return

def plotData(name, first_distribution, second_distribution=None, axis="H", filename=None, created=False):
    axisDict = {"H":0, "S":1, "V":2}
    if axis not in  axisDict: return
    axis = axisDict[axis]
    data = getData("Data", name)
    data = [x[axis] for x in data]
    linspace = np.linspace(max([0, min(data)-20]), 100 if max(data) <= 100 else min([max(data) + 20, 360]), num=500)
    phi_values = [first_distribution.dim_models[axis].phi(x) for x in linspace]
    plt.hist(data, bins=30, normed=True, color='w')
    first_dist, = plt.plot(linspace, phi_values, color='r')
    legend_val = [first_dist]
    if created:
        legend_label = ["Original " + first_distribution.name]
    else:
        legend_label = [first_distribution.name]
    if second_distribution is not None:
        phi_values = [second_distribution.dim_models[axis].phi(x) for x in linspace]
        second_dist, = plt.plot(linspace, phi_values, color='b', label='second_distribution')
        legend_val.append(second_dist)
        if created:
            legend_label.append("Created " + second_distribution.name)
        else:
            legend_label.append(second_distribution.name)
    
    
    plt.legend(legend_val, legend_label)
    
    plt.xlabel("Value")
    plt.ylabel("Probability/Count (Histogram is Normalized")
    plt.suptitle("%s versus %s on %s's data" % (first_distribution, second_distribution, first_distribution))
    plt.xlim(max([0, min(data)-20]), 100 if max(data) <= 100 else min([max(data) + 20, 360]))
    if filename is not None:
        plt.savefig(filename)
    else:
        plt.show()
    plt.clf()
    return

def r2test(name, real_distribution, generated_distribution, HSV=None):
    data = getData("Data", name)
    if HSV is None:
        real_phi = [real_distribution(x) for x in data]
        generated_phi = [generated_distribution(x) for x in data]
    else:
        axis = {"H": 0, "S": 1, "V": 2}
        axis = axis[HSV]
        real_phi = [real_distribution.dim_models[axis].phi(x) for x in [y[axis] for y in data]]
        generated_phi = [generated_distribution.dim_models[axis].phi(x) for x in [y[axis] for y in data]]
    yPrime = sum(real_phi) / len(real_phi)
    SS_tot = sum([(x - yPrime) ** 2 for x in real_phi])
    SS_res = sum([(x - y) ** 2 for x, y in zip(real_phi, generated_phi)])
    r2 = 1 - (SS_res / SS_tot)
    return r2
    
    
    
    