from sklearn import svm, metrics
import time
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt

def load_vectors(file):
    with open(file, "r") as input:
        vecs = input.readlines()
        vecs = [line.split(' ')[1:] for line in vecs]
        vecs_y = [int(val[0]) for val in vecs]
        vecs = [[float(val) for val in vec[1:]] for vec in vecs]
    return vecs, vecs_y

def scores(y, pred):
    classes_num = 4
    
    matrix = [[0]*classes_num for _ in range(classes_num)]
    full = len(y)
    for i in range(full):
        _y = y[i]
        _p = pred[i]
        matrix[_y-1][_p-1] += 1
    
    classes = []
    precision = []
    recall = []
    f1_score = []
    accuracy = []
    
    tp_full = 0
    for cl_ in range(classes_num):
        tp = matrix[cl_][cl_]
        tpfp = sum([line[cl_] for line in matrix])
        tpfn = sum(matrix[cl_])
        tn = full+tp-tpfp-tpfn
        
        classes.append(cl_+1)
        precision.append(tp/tpfp)
        recall.append(tp/tpfn)
        f1_score.append(2*tp/(tpfp+tpfn))
        accuracy.append((tp+tn)/full)
        
        tp_full += tp
    
    classes.append("macro_avg")
    precision.append(sum(precision)/classes_num)
    recall.append(sum(recall)/classes_num)
    f1_score.append(sum(f1_score)/classes_num)
    accuracy.append(sum(accuracy)/classes_num)
    
    classes.append("micro_avg")
    precision.append(tp_full/full)
    recall.append(tp_full/full)
    f1_score.append(tp_full/full)
    accuracy.append(tp_full/full)
    
    sc = pd.DataFrame({
        'class' : classes,
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score,
        'accuracy': accuracy
    })
    
    return sc
        

def train_test_model(model, x, y, test_x, test_y):
    _st = time.time()
    model.fit(x, y)
    _et = time.time()
    _time = _et-_st
    
    pred_y = model.predict(test_x)

    sc = scores(test_y, pred_y)
    return _time, sc
    
def conduct_experiment():
    train_x, train_y = load_vectors('projects/mansurov-project/assets/vector_corpus/train.tsv')
    test_x, test_y = load_vectors('projects/mansurov-project/assets/vector_corpus/test.tsv')
    
    kernels = ['linear', 'poly', 'rbf']
    epochs = [1, 2, 5, 10, 20, 50, 100, 500, 1000, 5000, 10000]
    
    stats = {
        'epochs': [],
        'linear': [],
        'poly': [],
        'rbf': [],
    }
    
    for epoch in epochs:        
        stats['epochs'].append(epoch)
        for kernel in kernels:    
            clf = svm.SVC(kernel=kernel, max_iter=epoch, tol=1e-6)
            tm, sc = train_test_model(clf, train_x, train_y, test_x, test_y)
            stats[kernel].append((tm, sc.to_csv(index=False, header=True, sep=',')))
    
    stats = pd.DataFrame(stats)
    stats.to_csv('projects/mansurov-project/assets/classification/stats.tsv')
    
def plot_results():
    stats = pd.read_csv('projects/mansurov-project/assets/classification/stats.tsv', sep=',')
    tms = {
        'epochs': [],
        'linear': [],
        'poly': [],
        'rbf': [],
    }
    data = {
        'epochs': [],
        'linear': [],
        'poly': [],
        'rbf': [],
    }
    for index, row in stats.iterrows():
        tms['epochs'].append(row['epochs'])
        tms['linear'].append(float(row['linear'][1:-1].split(', ')[0]))
        tms['poly'].append(float(row['poly'][1:-1].split(', ')[0]))
        tms['rbf'].append(float(row['rbf'][1:-1].split(', ')[0]))
        data['epochs'].append(row['epochs'])
        data['linear'].append(pd.read_csv(StringIO(row['linear'][1:-1].split(', ')[1][1:-1].replace('\\r\\n', '\r\n')), sep=","))
        data['poly'].append(pd.read_csv(StringIO(row['poly'][1:-1].split(', ')[1][1:-1].replace('\\r\\n', '\r\n')), sep=","))
        data['rbf'].append(pd.read_csv(StringIO(row['rbf'][1:-1].split(', ')[1][1:-1].replace('\\r\\n', '\r\n')), sep=","))
        
    tms = pd.DataFrame(tms)
    data = pd.DataFrame(data)
    # print(tms)
    # print(data['linear'][0]['precision'][4])
    
    epochs = [1, 2, 5, 10, 20, 50, 100, 500, 1000, 5000, 10000]
    default_x_ticks = range(len(epochs))
    
    fig, ax = plt.subplots()
    ax.plot(default_x_ticks, tms['linear'].to_list(), label='linear')
    ax.plot(default_x_ticks, tms['poly'].to_list(), label='poly')
    ax.plot(default_x_ticks, tms['rbf'].to_list(), label='rbf')
    plt.xticks(default_x_ticks, epochs)
    ax.legend()
    fig.savefig('projects/mansurov-project/assets/classification/time.png', dpi=100)
    
    fig, ax = plt.subplots(2, 2)
    fig.set_size_inches(18.5, 10.5)
    ax[0, 0].plot(default_x_ticks, [e['precision'][4] for e in data['linear'].to_list()], label='linear')
    ax[0, 0].plot(default_x_ticks, [e['precision'][4] for e in data['poly'].to_list()], label='poly')
    ax[0, 0].plot(default_x_ticks, [e['precision'][4] for e in data['rbf'].to_list()], label='rbf')
    ax[0, 0].set_title("precision")
    
    ax[0, 1].plot(default_x_ticks, [e['recall'][4] for e in data['linear'].to_list()], label='linear')
    ax[0, 1].plot(default_x_ticks, [e['recall'][4] for e in data['poly'].to_list()], label='poly')
    ax[0, 1].plot(default_x_ticks, [e['recall'][4] for e in data['rbf'].to_list()], label='rbf')
    ax[0, 1].set_title("recall")
    ax[0, 1].sharex(ax[0, 0])
    
    ax[1, 0].plot(default_x_ticks, [e['f1_score'][4] for e in data['linear'].to_list()], label='linear')
    ax[1, 0].plot(default_x_ticks, [e['f1_score'][4] for e in data['poly'].to_list()], label='poly')
    ax[1, 0].plot(default_x_ticks, [e['f1_score'][4] for e in data['rbf'].to_list()], label='rbf')
    ax[1, 0].set_title("f1_score")
    ax[1, 0].sharex(ax[0, 0])
    
    ax[1, 1].plot(default_x_ticks, [e['accuracy'][4] for e in data['linear'].to_list()], label='linear')
    ax[1, 1].plot(default_x_ticks, [e['accuracy'][4] for e in data['poly'].to_list()], label='poly')
    ax[1, 1].plot(default_x_ticks, [e['accuracy'][4] for e in data['rbf'].to_list()], label='rbf')
    ax[1, 1].set_title("accuracy")  
    ax[1, 1].sharex(ax[0, 0]) 
    
    handles, labels = ax[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels)
    plt.xticks(default_x_ticks, epochs) 
    fig.savefig('projects/mansurov-project/assets/classification/scores.png', dpi=100)
 
if __name__=="__main__":
    print("")
    
    conduct_experiment()
    
    plot_results()
    
    print("")