import matplotlib.pyplot as plt
import pickle

directory = "Split + Broadness - Availability - Adjust"

with open("%s/results.pkl" % (directory), "r") as fp:
    data = pickle.load(fp)


averaged = sum([x[1] for x in data]) / float(len(data))
model_averaged = sum([x[0] for x in data]) / float(len(data))

#data = [x for x in data if x[0] < 10]


plt.scatter(range(len(data)), [x[0] for x in data], c='b', label="Learned Model")
plt.scatter(range(len(data)), [x[1] for x in data], c='m', label="Averaged Model")
plt.plot(range(len(data)), [.1947] * len(data), 'g--', label="Twin's Average")
plt.plot(range(len(data)), [averaged] * len(data), 'r--', label="Average's Average")
plt.plot(range(len(data)), [model_averaged] * len(data), 'k--', label="Learned Average")
plt.legend(loc=2)
plt.xlabel("Color")
plt.ylabel("Kullback-Liebler Divergence")
plt.savefig("%s/summary_plot-all.png" % (directory))
plt.show()