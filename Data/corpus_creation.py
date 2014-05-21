from colorsys import rgb_to_hsv
import MySQLdb as mysqldb
import pickle
from math import floor

class worker:
        #note, this is just-above-mysql-level-worker.  
        def __init__(self):
                self.db = mysqldb.connect("localhost", "color", "color", "colors")
                self.dbc = self.db.cursor() 

        def execute(self, query):
            self.dbc.execute(query)

        def insert_and_commit(self, query):
                self.dbc.execute(query) 
                self.db.commit() 

        def select(self, query):
                return self.dbc.execute(query)

        def fetchall(self):
                return self.dbc.fetchall()

        def fetchone(self):
                return self.dbc.fetchone()
            
        def __iter__(self):
            return self
        
        def next(self):
            item = self.fetchone()
            if item:
                return item
            raise StopIteration
        

class corpus_creation:
    def __init__(self):
        pass
    
    @staticmethod 
    def genesis(location,mergeset_filename="merge_sets.pkl"):
	if not os.path.exists(location+"/data/"):
    		os.makedirs(location+"/data/")
        #main corpus_creation creation function
        print "Grabbing the data from mysql and making the dictionary"
        color_data = corpus_creation.make_dictionary(english_only=True)
        print "Merging and Purging data"
        fp = open(mergeset_filename); merge_sets = pickle.load(fp); fp.close()
        color_data = corpus_creation.merge_and_purge(color_data, merge_sets)
        print "Making the sampling normalizer"
        (train,test) = corpus_creation.data_split(color_data)
        print "Splitting and saving the data"
        #corpus_creation.make_sampling_normalizer(train,location)
        corpus_creation.save(train,test,location)
    
    @staticmethod
    def make_dictionary(english_only):
        #Get the data ready to be split apart, takes as input whether or not to only use subjects who marked "English" or some variant
        #Returns a dictionary of the form: color_data = {Color_Label:[List of HSV value tuples]
        if english_only: user_query = "select id from users where language LIKE '%%English%%' and colorblind=0"
        else: user_query = "select id from users where colorblind=0"
        color_data = {}
        color_labels = set()
        w = worker()
        w.execute(user_query)
        user_ids = set([x[0] for x in w.fetchall()])
        w.execute("select r,g,b,colorname,user_id from answers")
        for r,g,b,colorname,user_id in w:
            colorname = colorname.lower()
            if len(colorname)<=2:
                continue
            if user_id in user_ids:
                if colorname not in color_labels:
                    color_labels |= set([colorname])
                    color_data[colorname]=[]
                color_data[colorname].append(corpus_creation.r2h(r,g,b))
        print "%s color names" % len(color_data.keys())
        return color_data
    

    
    @staticmethod
    def merge_and_purge(color_data,merge_sets,cutoff=100):
        #Purge first
        purge_list = []
        purge_dict = {}
        for label in color_data.keys():
            if len(color_data[label])<cutoff:
                purge_list.append(label)
        for label in purge_list:
            purge_dict[label] = color_data[label]
            del color_data[label]
        print "Purged %s crappy labels" % len(purge_list)
        
        for merge_set in merge_sets:
            max_label = ""; max_val = 0
            for label in merge_set:
                if len(color_data[label])>max_val:
                    max_label=label; max_val=len(color_data[label])
            print "For this merge set, %s is the most with %s" % (max_label, max_val)
            for label in merge_set:
                if label!=max_label:
                    color_data[max_label]+=color_data[label]
                    del color_data[label]
            print "And now it has %s" % len(color_data[max_label])
        return color_data
    
    @staticmethod
    def make_sampling_normalizer(color_data,location):
        """
        The space was not sampled evenly. To give a fairer statistical weight, the normalizer
        reweights the posterior probabilities during learning according to the bin the value falls in.
        """
        n_h_bins=11
        n_s_bins=11
        n_v_bins=11
        def gb(x,i,t):
            #t is max value, i in number of bins, x is the thing to be binned
            if x==t:
                return i-1
            elif x==0.0:
                return 0
            return int(floor(float(x)*i/t))
        
        bin_h = lambda x: gb(x, n_h_bins, 1)
        bin_s = lambda x: gb(x, n_s_bins, 1)
        bin_v = lambda x: gb(x, n_v_bins, 1)
        
        s_bins = [0.0 for x in range(n_s_bins)]
        v_bins = [0.0 for x in range(n_v_bins)]
        h_bins = [0.0 for x in range(n_h_bins)]
        
        for data in color_data.values():
            for datum in data:
                h_bins[bin_h(datum[0])]+=1.0
                s_bins[bin_s(datum[1])]+=1.0
                v_bins[bin_v(datum[2])]+=1.0
        
        normalizer = [[x/sum(h_bins) for x in h_bins], [x/sum(s_bins) for x in s_bins], [x/sum(v_bins) for x in v_bins]]
        fp = open("%s/sampling_normalizer.pkl" % location,"w"); pickle.dump(normalizer, fp); fp.close()
    
    @staticmethod
    def data_split(color_data):
        from random import shuffle
        train={}; test={}
        for label in color_data.keys():
            shuffle(color_data[label]); split_index = int(len(color_data[label])*0.7)
            train[label]=color_data[label][:split_index]; test[label]=color_data[label][split_index:]
        return (train,test)
    
    @staticmethod
    def save(train,test,location):
        handmadebad = ['penis', 'idontknow', 'fuck', 'ericisfaggot', 'idk', 'sdf', 'yourmom', 'aids', 'nigger', 'dunno', 'megan', 'boring', 'rickastley', 'ugh', 'asdf', 'dun', 'gay', 'dicks', 'cock', 'blah', 'noidea','dontknow']

        import re; pattern = re.compile('[\W_]+')
        exts = ["h_train", "s_train", "v_train", "test"]
        make_fn = lambda c,x: "%s/data/%s.%s" % (location, c, exts[x])
        directory = [] 
        existing_fn = set()
        for color in train.keys():
            #print "saving %s" % color
            color_h = [x[0] for x in train[color]]; color_s = [x[1] for x in train[color]]; color_v = [x[2] for x in train[color]];
            test_values = ["%s,%s,%s" % (x[0], x[1], x[2]) for x in test[color]]
            filtered = pattern.sub('',color)
            if len(filtered)<1: continue
            elif filtered in handmadebad: continue
            if filtered not in existing_fn: existing_fn |= set([filtered])
            else:filtered+="2"
            corpus_creation._save(make_fn(filtered,0),color_h); corpus_creation._save(make_fn(filtered,1),color_s); corpus_creation._save(make_fn(filtered,2),color_v); 
            corpus_creation._save(make_fn(filtered,3), test_values)
            directory.append([color,filtered])
        corpus_creation._save("%s/corpusindex.txt" % location, directory)
        
    @staticmethod
    def r2h(r,g,b):
        if type(r)==type(1): return rgb_to_hsv(r/255.0,g/255.0,b/255.0)    
        else: return rgb_to_hsv(r,g,b)
    
    @staticmethod
    def _save(filename, contents):
        handler = open(filename, "w")
        for line in contents:
                if type(line)==type("") or type(line)==type(0) or type(line)==type(0.0):
                    handler.write("%s\n" % line)
                elif type(line)==type([]):
                    t = ""
                    for val in line:
                        t+="%s," % val
                    t=t[:-1]
                    handler.write("%s\n" % t)
                else: print "I DON'T KNOW WHAT TO DO --- Save method. Contents are not list of string, int, float, or list"
        handler.close()


if __name__ == '__main__':
    corpus_creation.genesis(".","merge_sets.pkl")

