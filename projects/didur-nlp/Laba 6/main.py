from sklearn.decomposition import LatentDirichletAllocation as LDA
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import pandas as pd
import numpy as np
import heapq


train_term_doc = pd.read_csv("../assets/train_term_doc.tsv", index_col=0)
test_term_doc = pd.read_csv("../assets/test_term_doc.tsv", index_col=0)
print('Done')


def print_top_words(model):
    words = np.array(train_term_doc.columns)
    for i, topic in enumerate(model.components_):
        print(f"Topic_{i}: {[words[i] for i in topic.argsort()[-10:]]}")
    print('')

def print_top_docs(model, pred):
    columns = [f"Topic_{i}" for i in range(model.n_components)]
    indexes = test_term_doc.index
    df = pd.DataFrame(pred, columns=columns, index=indexes)
    for column, data in df.items():
        data = data.tolist()
        maximums = heapq.nlargest(10, data)
        pos_maximums = [data.index(maximum) for maximum in maximums]
        doc_names = [indexes[pos] for pos in pos_maximums]
        print(f"{column} top docs: {doc_names}")
    print('\n')

def do_experiment(n_components, max_iter=10):
    model = LDA(n_components=n_components, max_iter=max_iter)

    model = model.fit(train_term_doc)
    perplexity = round(model.perplexity(test_term_doc), 2)

    pred = model.transform(test_term_doc)

    print(f"Model: {model}, Perplexity = {perplexity}")
    print_top_words(model)
    print_top_docs(model, pred)

    return pred, perplexity


def main():
    experiments = [(2, do_experiment(n_components=2)), (5, do_experiment(n_components=5)),
                   (10, do_experiment(n_components=10)), (20, do_experiment(n_components=20)),
                   (40, do_experiment(n_components=40))]

    # график perplexity
    x_topics = [exp[0] for exp in experiments]
    y_perplexities = [exp[1][1] for exp in experiments]
    print(x_topics)
    print(y_perplexities)
    plt.figure(figsize=(10, 12))
    plt.scatter(x_topics, y_perplexities)
    plt.plot(x_topics, y_perplexities)
    plt.legend()
    plt.grid(True)
    plt.show()

    # выбор степени полинома r-squared
    best_r2 = 0.0
    best_deg = 3
    for degree in range(1, 7):
        theta = np.polyfit(x_topics, y_perplexities, deg=degree)
        model = np.poly1d(theta)
        r2 = r2_score(y_perplexities, model(x_topics))
        print(r2)
        if r2 > best_r2:
            best_deg = degree
            best_r2 = r2


    # аппроксимация полиномом
    theta = np.polyfit(x_topics, y_perplexities, deg=best_deg)
    model = np.poly1d(theta)
    line = np.linspace(1, 41)
    plt.scatter(x_topics, y_perplexities)
    plt.plot(line, model(line))
    plt.show()


    pred_10_5, perps_10_5 = do_experiment(n_components=10, max_iter=5)
    pred_10_20, perps_10_20 = do_experiment(n_components=10, max_iter=20)

    # запись в файл
    with open(f"../assets/topic_pred.tsv", 'w') as file:
        text = ""
        for predicts, filename in zip(pred_10_20, test_term_doc.index):
            predicts_line = ""
            for pred in predicts:
                predicts_line += '\t' + str(round(pred, 2))
            line = filename + '\t' + predicts_line[1:] + '\n'
            text += line
        file.write(text)


if __name__ == "__main__":
    main()
