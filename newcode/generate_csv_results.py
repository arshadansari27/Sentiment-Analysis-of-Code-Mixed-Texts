from pymongo import MongoClient
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import os

if not os.path.exists("../reports"):
    os.mkdir("../reports")

conn = MongoClient()
db = conn.sentiment_analysis_db

fields = [
        ('lang', "%s"),
        ('train_percent', "%d"),
        ('total', "%d"),
        ('max_accuracy', "%.2f"),
        ('linear_svm', "%.2f"),
        ('rbf_svm', "%.2f"),
        ('nb', "%.2f")
]

HNB = []
HRBFSVM = []
HLSVM = []
MNB = []
MRBFSVM = []
MLSVM = []


hindi_overall = db.results_overall.find_one({'lang': 'H'})
marathi_overall = db.results_overall.find_one({'lang': 'M'})

with open('../reports/output.csv', 'w') as outfile:
    outfile.write("Lang, Overall Accuracy, Overall F1 Score, Train Percent, Total, Max Accuracy, Max F1 Score, SVM (linear) Accuracy, SVM (linear) F1 Score, SVM (RBF) Accuracy, SVM (RBF) F1 Score, Naive Bayes Accuracy, Naive Bayes F1 Score\n")
    for data in db.results_percentwise.find({}):

        overall = hindi_overall if 'H' in str(data['lang']) else marathi_overall
        print data['lang'], overall['accuracy'], 'H' in str(data['lang'])
        d = [
            data['lang'],
            "%.2f" % overall['accuracy'],
            "%.2f" % overall['f1_score'],
            "%d" % data['train_percent'],
            "%d" % data['total'],
            "%.2f" % data['max_accuracy'][0],
            "%.2f" % data['max_accuracy'][1],
            "%.2f" % data['linear_svm'][0],
            "%.2f" % data['linear_svm'][1],
            "%.2f" % data['rbf_svm'][0],
            "%.2f" % data['rbf_svm'][1],
            "%.2f" % data['nb'][0],
            "%.2f" % data['nb'][1]
        ]
        outfile.write(','.join(d) + '\n')
        if data['lang'] == 'H':
            HNB.append((data['train_percent'], (data['max_accuracy'][0] * 100, data['nb'][0] * 100)))
            HRBFSVM.append((data['train_percent'], (data['max_accuracy'][0] * 100, data['rbf_svm'][0] * 100)))
            HLSVM.append((data['train_percent'], (data['max_accuracy'][0] * 100, data['linear_svm'][0] * 100)))
        else:
            MNB.append((data['train_percent'], (data['max_accuracy'][0] * 100, data['nb'][0] * 100)))
            MRBFSVM.append((data['train_percent'], (data['max_accuracy'][0] * 100, data['rbf_svm'][0] * 100)))
            MLSVM.append((data['train_percent'], (data['max_accuracy'][0] * 100, data['linear_svm'][0] * 100)))

HNB = sorted(HNB)
HRBFSVM = sorted(HRBFSVM)
HLSVM = sorted(HLSVM)
MNB = sorted(MNB)
MRBFSVM = sorted(MRBFSVM)
MLSVM = sorted(MLSVM)

exit()

charts = [
    ("hindi-nb", "Naive Bayes", HNB),
    ("hindi-lsvm", "Linear SVM", HLSVM),
    ("hindi-svm", "RBF SVM", HRBFSVM),
    ("marathi-nb", "Naive Bayes", MNB),
    ("marathi-lsvm", "Linear SVM", MLSVM),
    ("marathi-svm", "RBF SVM", MRBFSVM)
]

# No Display
matplotlib.use('Agg')


for filename, algorithm, data in charts:
    xaxis = np.array([u[0] for u in data])
    yaxis_max_accuracy = np.array([u[1][0] for u in data])
    yaxis_specific = np.array([u[1][1] for u in data])

    fig = plt.figure()
    ax = fig.add_subplot(111)
    lns1 = ax.plot(xaxis, yaxis_max_accuracy, '-', label='Max Accuracy')
    lns2 = ax.plot(xaxis, yaxis_specific, '-', label=algorithm)
    ax.legend(loc=0)
    ax.grid()
    ax.set_xlabel("Training Data (%)")
    ax.set_ylabel("Accuracy (%)")
    ax.set_ylim(0, 100)
    plt.savefig("../reports/" + filename + ".png", format='png')
    plt.clf()



