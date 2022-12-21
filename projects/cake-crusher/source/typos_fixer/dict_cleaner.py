from gensim import corpora

dictionary = corpora.Dictionary().load_from_text('../../assets/dictionary.txt')
print("The dictionary has: " + str(len(dictionary)) + " tokens")

dictionary.filter_extremes(no_below=4)
print("The dictionary has: " + str(len(dictionary)) + " tokens")
dictionary.save_as_text('../../assets/clean_dictionary.txt')