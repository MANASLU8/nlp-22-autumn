from sklearn.decomposition import LatentDirichletAllocation as LDA
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import numpy as np
import pandas as pd
import operator


def main():
    term_document_train = pd.read_csv("../assets/termin_document_train1.tsv", index_col=0)
    term_document_test = pd.read_csv("../assets/termin_document_test1.tsv", index_col=0)

    perplexities = dict()
    for n in [2, 5, 10, 20, 40]:
        lda_model = LDA(n_components=n)
        lda_model = lda_model.fit(term_document_train)
        pred = lda_model.transform(term_document_test)
        perplexity = lda_model.perplexity(term_document_test)
        print(f"Topic number: {lda_model.n_components}, perplexity: {perplexity}")
        perplexities[n] = round(perplexity, 2)

        # top 10 words for each topic
        words = np.array(term_document_train.columns)
        for i, topic in enumerate(lda_model.components_):
            print(f"Top 10 words for Topic {i}:")
            print([words[index] for index in topic.argsort()[-10:]])
        print("")

        # top documents for each topic
        index_names = ['Topic' + str(i) for i in range(lda_model.n_components)]
        column_names = term_document_test.index
        df_topic_document = pd.DataFrame(np.transpose(pred), columns=column_names, index=index_names)
        df_topic_document = pd.DataFrame(
            df_topic_document.apply(lambda x: list(df_topic_document.columns[np.array(x).argsort()[::-1][:5]]),
                                    axis=1).to_list(), columns=['Top1', 'Top2', 'Top3', 'Top4', 'Top5'])
        print(df_topic_document.to_string(), end='\n\n')

    print(perplexities)

    # график изменения perplexity
    n_topics = list(perplexities.keys())
    perplexity = list(perplexities.values())
    plt.figure(figsize=(16, 10))
    plt.plot(n_topics, perplexity)
    plt.grid(True)
    plt.show()

    # выбор степени полинома r-squared
    start = 1
    end = 6
    result = []
    for degree in range(start, end):
        model = np.poly1d(np.polyfit(n_topics, perplexity, degree))
        r2 = r2_score(perplexity, model(n_topics))
        result.append(r2)
    max = 0.0
    best_degree = 3
    for degree, r2 in enumerate(result):
        if r2 > max:
            max = r2
            best_degree = degree + 1
            if r2 == 1.0:
                break
    print(best_degree)

    # аппроксимация полиномом
    model = np.poly1d(np.polyfit(n_topics, perplexity, best_degree))
    line = np.linspace(1, 42)
    plt.scatter(n_topics, perplexity)
    plt.plot(line, model(line))
    plt.show()

    # поиск лучшего кол-ва итераций при 5 темах
    result = {}
    for iter in [5, 10, 20]:
        lda_model = LDA(n_components=5, max_iter=iter)
        lda_model = lda_model.fit(term_document_train)
        perplexity = lda_model.perplexity(term_document_test)
        print(f"N_components: {lda_model.n_components}, max_iter: {iter}, perplexity: {perplexity}")
        pred = lda_model.transform(term_document_test)
        result[iter] = (round(perplexity, 2), pred, iter)
    result = sorted(result.values(), key=operator.itemgetter(0))
    print(f"Best perplexity = {result[0][0]} ({result[0][2]} iter)")
    best_pred = result[0][1]

    # запись предиктов в файл
    with open(f"../assets/annotated-corpus/test_topics.tsv", 'w') as file:
        rows = ""
        for predict, filename in zip(best_pred, term_document_test.index):
            string = ""
            for pred in predict:
                string += '\t' + str(round(pred, 3))
            rows += filename + '\t' + string[1:] + '\n'
        file.write(rows)


if __name__ == "__main__":
    main()
