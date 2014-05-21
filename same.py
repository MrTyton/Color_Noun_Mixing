import lux
from math import log
from sklearn import linear_model
import numpy
import matplotlib.pyplot as plt
from dataManip import *
import dataManip

LUX = lux.LUX('lux.xml')


#def output(first_model, second_model, learned, predict, num_points, test, perplexity):
#    print "%s model on %s points:\t%f\n%s model on %s points:\t%f\nTotal Points:\t%d\nLog Likelihood Ratio:\t%f\nPerplexity of %s on %s:\t%f\n" % (first_model , first_model, learned , second_model , first_model , predict , num_points, test, second_model, first_model, perplexity)
#    return

def color_swap_likelihood(first, second, fp=None):
    better_than = 0
    try:
        first_distribution = LUX.getColor(first)
    except:
        first_distribution = LUX.getColor(first.replace("-", " "))
    try:
        second_distribution = LUX.getColor(second)
    except:
        second_distribution = LUX.getColor(second.replace("-", " "))
    
    #print "Availability of %s:\t%f\nAvailability of %s:\t%f\n" % (first_distribution.name, first_distribution.availability, second_distribution.name, second_distribution.availability)
    #print "With Availability Taken Out:"
    #first's data
    first_score, second_score, num_points, perplexity = testDistributions(first_distribution, second_distribution)
    first_perplex = perplexity
    test = (-2 * first_score) + (2 * second_score)
    output(first_distribution, second_distribution, first_score, second_score, num_points, test, perplexity, fp)
    if test > 0: better_than += 1
    #second's data
    second_score, first_score, num_points, perplexity  = testDistributions(second_distribution, first_distribution)
    second_perplex = perplexity
    test = (-2 * first_score) + (2 * second_score)
    output(second_distribution, first_distribution, second_score, first_score, num_points, test, perplexity, fp)
    if test > 0: better_than += 1
    return better_than, (first_perplex, second_perplex), ((first_distribution.availability, second_distribution.availability), (second_distribution.availability, first_distribution.availability))

def get_swapped_colors():
    fp = open("Data\corpusindex.txt", "r")
    names = [x.split(",")[0] for x in fp.readlines()]
    fp.close()
    same_names_first = [(x.split("-")[0], x.split("-")[1]) for x in names if "-" in x and x.split("-")[1] + "-" + x.split("-")[0] in names]
    same_names_second = [(x.split(" ")[0], x.split(" ")[1]) for x in names if " " in x and x.split(" ")[1] + " " + x.split(" ")[0] in names]
    new_names = []
    for x,y in same_names_first + same_names_second:
        if x == "apple" or y == "apple": continue
        if (x,y) and (y, x) not in new_names: new_names.append((x, y))
    return new_names

    
def availAndPerplex():
    both_better = 0
    one_better = 0
    none_better = 0
    fp = open("twins_raw_output.txt", 'w')
    perplexities = []
    availabilities = []
    for i, (x,y) in enumerate(get_swapped_colors()):
        #print "Availability of %s:\t%f\nAvailability of %s:\t%f" % (x, LUX.getColor(x).availability, y, LUX.getColor(y).availability)
        print "Working on number %d" % (i+1)
        temp, perplexity, availability = color_swap_likelihood(x + '-' + y, y + '-' + x, fp)
        perplexities.append(perplexity[0])
        perplexities.append(perplexity[1])
        availabilities.append(availability[0])
        availabilities.append(availability[1])
        if temp == 0: none_better += 1
        elif temp == 1: one_better += 1
        else: both_better += 1
        #print "------------\n"
    
    plt.hist(perplexities, bins=20)
    plt.xlabel("Perplexity")
    plt.ylabel("Count")
    plt.suptitle("Perplexities of Twins")
    plt.savefig("./Results/4-21-2014/twin-perplexities.png")
    #plt.show()
    plt.clf()
    availability_percentage = [(y - x) * 100 / x for x,y in availabilities]
    
    plt.hist(availability_percentage, bins=30)
    plt.xlabel("Availability Percentage Change")
    plt.ylabel("Count")
    plt.suptitle("Availability Percentage Change for Twins")
    plt.savefig("./Results/twin-availabilities.png")
    plt.show()
    print "Out of %d cases, %d of them no models did better on their twin, %d of them one model did better on its twin, and %d both of them did better on their twins" % (len(get_swapped_colors()), none_better, one_better, both_better)
    #testing_things()


def r2():
    words = getWordLists(method=lambda x, y: (x, y), checkRedundancy=False)
    words = dict([((x, y), z) for x, y, z in words])
    combos = {}
    for x, y in words:
        if (y, x) in words and (x, y) not in combos and (y, x) not in combos:
            combos[(x, y)] = (words[x, y], words[y, x])
        
    r2_results = []
    log_likelihoods = [] 
    for x in combos:
        first, second = combos[x]
        first_distribution = LUX.getColor(first)
        second_distribution = LUX.getColor(second)
        r2_results.append(dataManip.r2test(first, first_distribution, second_distribution))
        r2_results.append(dataManip.r2test(second, second_distribution, first_distribution))
        first_log_learned, first_log_predicted, first_num_points, first_perp = testDistributions(first_distribution, second_distribution)
        second_log_learned, second_log_predicted, second_num_points, second_perp = testDistributions(second_distribution, first_distribution)
        log_likelihoods.append((first_log_learned, first_log_predicted, first_num_points))
        log_likelihoods.append((second_log_learned, second_log_predicted, second_num_points))
                               
    print sum([x / z for x, y, z in log_likelihoods]) / len(log_likelihoods)
    print sum([y / z for x, y, z in log_likelihoods]) / len(log_likelihoods)
    
availAndPerplex()
#insert in the labels
#get the log likelihood data organized as well

    