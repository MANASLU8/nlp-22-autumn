from sklearn import svm, metrics
import time
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
from svm_exp import load_vectors, train_test_model
from sklearn.decomposition import PCA


def conduct_experiment():
    train_x, train_y = load_vectors('projects/mansurov-project/assets/vector_corpus/train.tsv')
    test_x, test_y = load_vectors('projects/mansurov-project/assets/vector_corpus/test.tsv')
    
    kernel = 'rbf'
    epoch = 5000
    
    dimensions = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    
    stats = []
    
    for dimension in dimensions:        
        pca = PCA(n_components=dimension)
        new_train_x = pca.fit_transform(train_x) 
        new_test_x = pca.transform(test_x) 
        clf = svm.SVC(kernel=kernel, max_iter=epoch, tol=1e-6)
        tm, sc = train_test_model(clf, new_train_x, train_y, new_test_x, test_y)
        stats.append((dimension, tm, sc.to_csv(index=False, header=True, sep=',')))
    
    with open('projects/mansurov-project/assets/classification/stats_optimal.tsv', 'w') as output:
        output.write(f"dimension\ttime\tstats\n")
        for stat in stats:
            output.write(f"{stat}\n")
    
def plot_results():
    with open('projects/mansurov-project/assets/classification/stats_optimal.tsv', 'r') as input:
        lines = input.readlines()
        lines = [line[1:-1].split(', ') for line in lines[1:]]
        stats = [(int(line[0]), float(line[1]), pd.read_csv(StringIO(line[2].replace('\\r\\n', '\r\n')), sep=",")) for line in lines]
    
    dimensions = [10, 20, 30, 40, 50, 60, 70, 80, 90]
    default_x_ticks = range(len(dimensions))
    
    fig, ax = plt.subplots()
    ax.plot(default_x_ticks, [stat[1] for stat in stats])
    plt.xticks(default_x_ticks, dimensions)
    fig.savefig('projects/mansurov-project/assets/classification/opt_time.png', dpi=100)
    
    fig, ax = plt.subplots(2, 2)
    fig.set_size_inches(18.5, 10.5)
    ax[0, 0].plot(default_x_ticks, [e[2]['precision'][4] for e in stats])
    ax[0, 0].set_title("precision")
    
    ax[0, 1].plot(default_x_ticks, [e[2]['recall'][4] for e in stats])
    ax[0, 1].set_title("recall")
    ax[0, 1].sharex(ax[0, 0])
    
    ax[1, 0].plot(default_x_ticks, [e[2]['f1_score'][4] for e in stats])
    ax[1, 0].set_title("f1_score")
    ax[1, 0].sharex(ax[0, 0])
    
    ax[1, 1].plot(default_x_ticks, [e[2]['accuracy'][4] for e in stats])
    ax[1, 1].set_title("accuracy")  
    ax[1, 1].sharex(ax[0, 0]) 
    
    plt.xticks(default_x_ticks, dimensions) 
    fig.savefig('projects/mansurov-project/assets/classification/opt_scores.png', dpi=100)
 

if __name__=="__main__":
    print("")
    
    # conduct_experiment()
    
    plot_results()
    
    print("")