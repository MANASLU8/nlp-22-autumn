from sklearn.decomposition import LatentDirichletAllocation as LDA
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from util import write_to_tsv, show_topics
import pickle
import pandas as pd
import numpy as np


td_matrix = pd.read_csv("../../assets/train_td_matrix2911.tsv", index_col=0) #, skipfooter=10000, engine='python')
test_td_matrix = pd.read_csv("../../assets/test_td_matrix2911.tsv", index_col=0) #, skipfooter=10000, engine='python')


def lda_pipe(**hparams):
    lda = LDA(**hparams)
    print(f"Model: {lda}")
    lda = lda.fit(td_matrix)
    topic_keywords = show_topics(lda_model=lda, columns=td_matrix.columns, n_words=10)
    df_topic_keywords = pd.DataFrame(topic_keywords)
    df_topic_keywords.columns = ['Word ' + str(i) for i in range(df_topic_keywords.shape[1])]
    df_topic_keywords.index = ['Topic ' + str(i) for i in range(df_topic_keywords.shape[0])]
    print(df_topic_keywords.to_string())

    pred = lda.transform(test_td_matrix)
    perplexity = lda.perplexity(test_td_matrix)
    print(perplexity)

    # Get best documents for each topic
    topic_names = ['Topic' + str(i) for i in range(lda.n_components)]
    doc_names = test_td_matrix.index
    df_document_topic = pd.DataFrame(pred, columns=topic_names, index=doc_names)
    df_topic_document = df_document_topic.T
    df_topic_document = df_topic_document.apply(lambda x: pd.Series(x.sort_values(ascending=False).iloc[:5]
                                                                    .index,
                                                                    index=['top1', 'top2', 'top3', 'top4', 'top5']),
                                                                    axis=1)
    print(df_topic_document.to_string(), end='\n\n')

    return pred, round(perplexity, 2)


def main():
    # 2, 5, 10, 20, 40
    perplexities = dict()
    pred_2, perplexities[2] = lda_pipe(n_components=2)
    pred_5, perplexities[5] = lda_pipe(n_components=5)
    pred_10, perplexities[10] = lda_pipe(n_components=10)
    pred_20, perplexities[20] = lda_pipe(n_components=20)
    pred_40, perplexities[40] = lda_pipe(n_components=40)
    with open('../../assets/perplexities.pk', 'wb') as file:
        pickle.dump(perplexities, file)
    # with open('../../assets/perplexities.pk', 'rb') as file:
    #     perplexities = pickle.load(file)
    print(perplexities)

    # график изменения perplexity
    x = list(perplexities.keys())
    y = list(perplexities.values())
    plt.figure(figsize=(12, 7))
    plt.plot(x, y, 'o-r', alpha=0.7, label="topics-perplexity", lw=5, mec='b', mew=2, ms=10)
    plt.legend()
    plt.grid(True)
    plt.show()

    # выбор степени полинома r-squared
    best_r2 = 0.0
    best_deg = 3
    for degree in range(1, 7):
        model = np.poly1d(np.polyfit(x, y, degree))
        polyline = x
        r2 = r2_score(y, model(polyline))
        print(r2)
        if r2 > best_r2:
            best_deg = degree
            best_r2 = r2


    # polynomial fit with best degree
    model = np.poly1d(np.polyfit(x, y, best_deg))
    polyline = np.linspace(1, 41)
    plt.scatter(x, y)
    plt.plot(polyline, model(polyline))
    plt.show()

    perps_10 = dict()
    pred_10_5, perps_10[5] = lda_pipe(n_components=10, max_iter=5)
    pred_10_20, perps_10[20] = lda_pipe(n_components=10, max_iter=20)

    # запись вероятностей в файл для лучшего случая
    write_to_tsv(pred_10_20, test_td_matrix.index)


if __name__ == "__main__":
    main()
