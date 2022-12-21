import matplotlib.pyplot as plt
from math import log
import numpy as np
from sklearn.metrics import r2_score

components = [2, 4, 5, 10, 20, 40, 60]
iterations = [10, 20, 40, 80]
# iterations = [40]

def get_values():
    values = []
    
    for iteration in iterations:
        values.append([])
        for component in components:
            with open(f"projects/mansurov-project/assets/clasterization/experiment_model/model_{component}_i{iteration}/perplexity.txt", "r") as input:
                _ = float(input.readline())
                # _ = log(_)
                values[-1].append(_)
    return values

def plot_results(values1, models):
    fig, axs = plt.subplots(1, 2)
    fig.set_figwidth(12)
    fig.set_figheight(6)
    ax = axs[0]
    ax.plot(components, values1[0], label='10')
    ax.plot(components, values1[1], label='20')
    ax.plot(components, values1[2], label='40')
    ax.plot(components, values1[3], label='80')
    ax.set_title("perplexity")
    ax.legend()
    ax = axs[1]
    
    x = list(range(1,61))
    values2=[model(x) for model in models]
    
    ax.plot(x, values2[0], label='10')
    ax.plot(x, values2[1], label='20')
    ax.plot(x, values2[2], label='40')
    ax.plot(x, values2[3], label='80')
    ax.set_title("perplexity")
    ax.legend()
    fig.savefig('projects/mansurov-project/assets/clasterization/perplexity.png', dpi=100)
    plt.show()
    
def approximate(x_, values):
    degrees = list(range(1,6))
    x = np.array(x_)
    max_degrees = []
    max_deg_model = []
    for y_ in values:
        y = np.array(y_)
        max_r2 = 0
        max_degree = 0
        for degree in degrees:
            model = np.poly1d(np.polyfit(x, y, degree))
            
            ypr = model(x)            
            r2 = r2_score(y, ypr)
            if r2>max_r2:
                max_r2 = r2
                max_degree = degree
                max_model = model
        max_degrees.append(max_degree)
        max_deg_model.append(max_model)
    return max_degrees, max_deg_model
    
if __name__=="__main__":
    print("")
    values = get_values()
    mds, max_deg_models = approximate(components, values)
    print(mds)
    plot_results(values, max_deg_models)
    