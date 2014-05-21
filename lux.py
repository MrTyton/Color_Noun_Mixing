"""
Lexicon of Uncertain Color Standards
Written by XXXXXXXXXXXXXXXXXXXXXXX

This is a demo script for the LUX release.  
There is an accompanying CSV file.  This script opens it and offers basic functionality
"""

from scipy.stats import gamma as gam_dist
from math import sin, cos, atan2, pi
import xml.etree.ElementTree as ET
class LUX:
    def __init__(self, filename):
        """
        Input: full path filename to lux.csv
        Function: Parse lux.csv and make available several probability functions:
            1) predict(datum): predicts most likely label; return [label,probability]
            2) posterior_likelihood(datum,label): Returns P(datum|label)
            3) full_posterior(datum): returns all labels ordered by decreasing posterior likelihood
        """
        tree = ET.parse(filename)
        root = tree.getroot()

        self.all = {child.get("name"):color_label(child) for child in root}
        
        
    def full_posterior(self, datum):
        probabilities = [[dist.name,dist(datum)] for dist in self.all.values()]
        total = sum([x[1] for x in probabilities])
        return sorted([[name,prob/total] for name,prob in probabilities], key=lambda x:x[1], reverse=True)
        
           
    def predict(self, datum):
        #NOTE: This returns the unnormalized posterior likelihood 
        probabilities = [[dist.name,dist(datum)] for dist in self.all.values()]
        sorted_probabilities = sorted(probabilities, key=lambda x: x[1], reverse=True)
        return sorted_probabilities[0]
    
    def posterior_likelihood(self, datum, label):
        probabilities = [dist(datum) for dist in self.all.values()]
        if label not in self.all.keys(): raise OutOfVocabularyException("Label '%s' was not in the lexicon" % label)
        return self.all[label](datum)/sum(probabilities)
    
    def getColor(self, name):
        try:
            return self.all[name]
        except KeyError:
            raise OutOfVocabularyException("Color not found")
    
class color_label:
    def __init__(self,label_node):
        """
        The all-dimension model for each color label
        """
        name = label_node.get("name"); availability = float(label_node.get("availability")); hue_adjust = eval(label_node.get("hue_adjust"))
        
        self.name = name; self.availability = availability
        self.hue_adjust = hue_adjust
        self.dim_models = [single_dim(child) for child in label_node]
        self.dim_models[0].adjust = hue_adjust

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    def __call__(self, *args):
        return self.phi(args[0])#*self.availability
    
    def getFrequency(self):
        name = self.name.replace('-', '')
        name = name.replace(" ", "")
        #fp = open("%s/data/%s.test" % ('Data', name))
        #count = len(fp.readlines())
        #fp.close()
        fp = open("%s/data/%s.h_train" % ('Data', name))
        count = len(fp.readlines())
        fp.close()
        return count
    
    def phi(self,x):
        if self.dim_models[0].auc_val is None:
            self.dim_models[0].auc(360)
        if self.dim_models[1].auc_val is None:
            self.dim_models[1].auc(100)
        if self.dim_models[2].auc_val is None:
            self.dim_models[2].auc(100)
                    
        return self.dim_models[0].phi(x[0])*self.dim_models[1].phi(x[1])*self.dim_models[2].phi(x[2])
    
    #) / ((self.getFrequency() * 360 * 100 * 100) / self.availability)
                    
    def isSingleWord(self):
        return " " not in self.name.replace("-", " ")
    
    def printStats(self):
        ans = "Name:\t\t%s\nAvailability:\t%f\nHue Adjust:\t%r\n" % (self.name, self.availability, self.hue_adjust)
        for x in self.dim_models:
            ans += x.printStats() + " "
        return ans
    
class single_dim:
    """
    The single dimension for each color label
    """
    def __init__(self, dim_node):
        def get_node(name):
            for child in dim_node:
                if child.tag==name:
                    return child
        paramdict = {child.tag:child for child in dim_node}
        paramnames =["mulower","shapelower","scalelower","muupper","shapeupper","scaleupper"]
        self.params = [float(paramdict[paramname].get("value")) for paramname in paramnames]
        self.stdevs = [float(paramdict[paramname].get("stdev")) for paramname in paramnames]
        mu1,sh1,sc1,mu2,sh2,sc2 = self.params
        left_gamma=gam_dist(sh1,scale=sc1); lbounds=left_gamma.interval(0.99)
        right_gamma=gam_dist(sh2,scale=sc2); rbounds=right_gamma.interval(0.99)
        self.region = lambda x: (2 if x>mu2 else 1) if x>=mu1 else 0
        self.f= [lambda x: left_gamma.sf(abs(x-mu1)),
                 lambda x: 1,
                 lambda x: right_gamma.sf(abs(x-mu2))]
        self.adjust=False
        self.auc_val = None
    
    def phi(self, x):
        if self.adjust: x = atan2(sin(x*pi/180),cos(x*pi/180))*180/pi
        if self.auc_val is None:
            return self.f[self.region(x)](x)
        else:
            return self.f[self.region(x)](x) / self.auc_val
    
    def reload(self):
        mu1,sh1,sc1,mu2,sh2,sc2 = self.params
        left_gamma=gam_dist(sh1,scale=sc1); lbounds=left_gamma.interval(0.99)
        right_gamma=gam_dist(sh2,scale=sc2); rbounds=right_gamma.interval(0.99)
        self.region = lambda x: (2 if x>mu2 else 1) if x>=mu1 else 0
        self.f= [lambda x: left_gamma.sf(abs(x-mu1)),
                 lambda x: 1,
                 lambda x: right_gamma.sf(abs(x-mu2))]
        self.auc_val = None
        
    def frange(self, start, stop, jump):
        while start <= stop:
            yield start
            start += jump  
                
    def auc(self, maximum):
        maximum = float(maximum)
        if self.auc_val is None:
            h = maximum/(2 * 999.)
            summation = 0
            for i in self.frange(0, maximum, maximum / 1000.):
                if i != 0 and i != maximum:
                    summation += 2 * self.phi(i)
                else:
                    summation += self.phi(i)
            ans = h * summation
            self.auc_val = ans #/ maximum
        return self.auc_val

    def printStats(self):
        mu1,sh1,sc1,mu2,sh2,sc2 = self.params
        return "mu1: %f, sh1: %f, sc1: %f, mu2: %f, sh2: %f, sc2: %f" % (mu1, sh1, sc1, mu2, sh2, sc2)
     
        

class OutOfVocabularyException(Exception):
    pass
