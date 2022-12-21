import numpy as np


def write_to_tsv(predict, index):
    with open(f"../../assets/annotated-corpus/test_topic_predicts.tsv", 'w') as file:
        lines = ""
        for predict_array, filename in zip(predict, index):
            predict_str = ""
            for pred in predict_array:
                predict_str += '\t' + str(round(pred, 3))
            lines += filename + '\t' + predict_str[1:] + '\n'
        file.write(lines)


# Show top n keywords for each topic
def show_topics(lda_model, columns, n_words=10):
    keywords = np.array(columns)
    topic_keywords = []
    for topic_weights in lda_model.components_:
        top_keyword_locs = (-topic_weights).argsort()[:n_words]
        topic_keywords.append(keywords.take(top_keyword_locs))
    return topic_keywords
