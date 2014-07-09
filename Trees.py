import lux
LUX = lux.LUX('lux.xml')
from random import shuffle
from sklearn.ensemble import RandomForestRegressor
from math import log
import matplotlib.pyplot as plt
import numpy as np
import pickle
from dataManip import *
import os
import dataManip

generateImages = False

curPath = "7-8-test"


    



def sortAverage(first, second):
    first = LUX.getColor(first)
    second = LUX.getColor(second)
    first_avg = (first.dim_models[0].params[0] + first.dim_models[0].params[3]) / 2
    second_avg = (second.dim_models[0].params[0] + second.dim_models[0].params[3]) / 2
    return (first.name, second.name) if first_avg >= second_avg else (second.name, first.name)

def doNothing(first, second):
    return first, second

def trainTwoWords(trainHSV=False):
    print "Gathering labels..."
    labels = getWordLists(method=sortAvail, checkRedundancy = False)
    shuffle(labels)
    training = []
    targets = []
    print "Converting to vectors..."
    for x, y, z in labels:
        training.append(convertToVector(x) + convertToVector(y))
        targets.append(convertToVector(z, True))
    training_data = training[:len(training) * 7 / 10]
    training_targets = targets[:len(targets) * 7 / 10]
    training_labels = labels[:len(labels) * 7 / 10]
    print len(training_data)
    print len(training_data[0])
    test_data = [x for x in training if x not in training_data]
    test_targets = [x for x in targets if x not in training_targets]
    test_labels = [x[2] for x in labels if x not in training_labels]
    print len(test_data)
    print "Fitting data..."
    if not trainHSV:
        clf = RandomForestRegressor(n_jobs = -1)
        clf.fit(training_data, training_targets)
        print "Predicting distributions..."
        test_data_results = clf.predict(test_data)
    else: #go through everything and make a separate tree for each 'zone' in the model
        clf = []
        print "Fitting Initial...."
        initial_clf = RandomForestRegressor(n_jobs = -1)
        initial_clf.fit(training_data, [x[0:3] for x in training_targets]) #replace this with something else later
        hue_clf = RandomForestRegressor(n_jobs = -1)
        print "Fitting Hue..."
        hue_clf.fit([x[2:14] + x[40:52] for x in training_data], [x[3:15] for x in training_targets])
        saturation_clf = RandomForestRegressor(n_jobs = -1)
        print "Fitting Saturation..."
        saturation_clf.fit([x[14:26] + x[52:64] for x in training_data], [x[15:27] for x in training_targets])
        value_clf = RandomForestRegressor(n_jobs = -1)
        print "Fitting Value..."
        value_clf.fit([x[26:38] + x[64:76] for x in training_data], [x[27:39] for x in training_targets])
        clf.append(initial_clf)
        clf.append(hue_clf)
        clf.append(saturation_clf)
        clf.append(value_clf)
        print "Predicting distributions..."
        initial_results = initial_clf.predict(test_data)
        hue_results = hue_clf.predict([x[2:14] + x[40:52] for x in test_data])
        saturation_results = saturation_clf.predict([x[14:26] + x[52:64] for x in test_data])
        value_results = value_clf.predict([x[26:38] + x[64:76] for x in test_data])
        #print initial_results
        #print hue_results
        #print saturation_results
        #print value_results
        #print len(initial_results)
        test_data_results = [np.hstack((w, x, y, z)) for w, x, y, z in zip(initial_results, hue_results, saturation_results, value_results)]
        #print len(test_data_results)
        #print test_data_results
    return test_data, test_data_results, test_labels, test_targets, clf
    
def analysis(test_data, test_data_results, test_labels, test_targets, clf): #test targets is not used
    if not os.path.exists("./Results/%s" % (curPath)):
        os.makedirs("./Results/%s" % (curPath))
    fp = open("./Results/%s/raw_comparison_output.txt" % (curPath), "w")
    availability_list = []
    perplexity_list = []
    log_likelihoods = []
    print "Testing points..."
    for i, (data, label) in enumerate(zip(test_data_results, test_labels)):
        print "Working on %d out of %d..." % (i+1, len(test_data_results))
        
        #ans = clf.predict([data])[0]
        ans = createDistribution(label, data)
        real = LUX.getColor(label)
        availability_list.append((ans.availability, real.availability))
        real_score, generated_score, num_points, perplexity = testDistributions(real, ans)
        log_likelihoods.append((real_score, generated_score, num_points))
        perplexity_list.append(perplexity)
        test = (-2 * real_score) + (2 * generated_score)
        output(real, ans, real_score, generated_score, num_points, test, perplexity, fp)
        if generateImages:
            path = "./Results/%s/%s/" % (curPath, label)
            if not os.path.exists(path):
                os.makedirs(path)
            plotData(label, real, ans, axis="H", filename=path + "Hue.png", created=True)
            plotData(label, real, ans, axis="S", filename=path + "Saturation.png", created=True)
            plotData(label, real, ans, axis="V", filename=path + "Value.png", created=True)
            tempfp = open(path + "raw_output.txt", 'w')
            output(real, ans, real_score, generated_score, num_points, test, perplexity, tempfp)
            tempfp.close()
    fp.close()
    availability_percentage = [(y - x) * 100. / x for x, y in availability_list]
    plt.hist(availability_percentage, bins=30)
    plt.xlabel("Availability Percentage Change")
    plt.ylabel("Count")
    plt.suptitle("Availability Percentage Change from Real to Generated Models")
    plt.savefig("./Results/%s/generated-availabilities.png" % (curPath))
    plt.clf()
    
    plt.hist(perplexity_list, bins=20)
    plt.xlabel("Perplexity")
    plt.ylabel("Count")
    plt.suptitle("Perplexities of Generated Models")
    plt.savefig("./Results/%s/generated-perplexities.png" % (curPath))
    
    print sum([x / z for x, y, z in log_likelihoods]) / len(log_likelihoods)
    print sum([y / z for x, y, z in log_likelihoods]) / len(log_likelihoods)
    
def r2Analysis(test_data_results, test_labels, mode=None):
    
    print "Testing points..."
    r2_results = []
    for i, (data, label) in enumerate(zip(test_data_results, test_labels)):
        print "Working on %d out of %d..." % (i+1, len(test_data_results))
        generated = createDistribution(label, data)
        real = LUX.getColor(label)
        r2_results.append(dataManip.r2test(label, real, generated, mode))
    print sum(r2_results) / len(r2_results)
    plt.hist(r2_results, bins=20)
    plt.show()
    
def createPickles():
    test_data, test_data_results, test_labels, test_targets, clf = trainTwoWords()
    path = "./trees/%s/" % (curPath)
    if not os.path.exists(path):
        os.makedirs(path)
    with open("%s/test_data.pkl" % (path), "w") as fp: pickle.dump(test_data, fp)
    with open("%s/test_data_results.pkl" % (path), "w") as fp: pickle.dump(test_data_results, fp)
    with open("%s/test_labels.pkl" % (path), "w") as fp: pickle.dump(test_labels, fp)
    with open("%s/test_targets.pkl" % (path), "w") as fp: pickle.dump(test_targets, fp)
    with open("%s/clf.pkl" % (path), "w") as fp: pickle.dump(clf, fp)
    print "Done"

def continuePickles():
    path = "./trees/%s/" % (curPath)
    with open("%s/test_data.pkl" % (path), "r") as fp: test_data = pickle.load(fp)
    with open("%s/test_data_results.pkl" % (path), "r") as fp: test_data_results =  pickle.load(fp)
    with open("%s/test_labels.pkl" % (path), "r") as fp: test_labels = pickle.load(fp)
    with open("%s/test_targets.pkl" % (path), "r") as fp: test_targets = pickle.load(fp)
    with open("%s/clf.pkl" % (path), "r") as fp: clf = pickle.load(fp)
    analysis(test_data, test_data_results, test_labels, test_targets, clf)
    r2Analysis(test_data_results, test_labels)
    


if __name__ == "__main__":
    create = 10
    if create == 10:
        createPickles()
    else:
        continuePickles()
    #main()
