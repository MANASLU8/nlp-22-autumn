import pickle as pk
from vectorize import VectorizationNeuro, VectorizationTFIDF
from math import sqrt, acos, pi

def cosine_dist(a, b):
    S, A, B = 0, 0, 0
    for i in range(len(a)):
        S += a[i]*b[i]
        A += a[i]*a[i]
        B += b[i]*b[i]
    return 1 - S/sqrt(A)/sqrt(B)

if __name__=="__main__":
    modelNeuro = VectorizationNeuro(from_file=True, sentences=None)
    modelTfidf = VectorizationTFIDF()
    
    pca = pk.load(open("projects/mansurov-project/assets/vectorize/pca.pkl",'rb'))
    
    
    with open("projects/mansurov-project/assets/vectorize/compare_test.txt", "wb") as output:
        # test 1
        output.write("\n\nTest 1\n\n".encode())
        words_word = 'year'
        words_similar = ['day', 'week', 'minute']
        words_area = ['weekend', 'time', 'calendar']
        words_other = ['agency', 'shooter', 'service']
        words = words_similar+ words_area + words_other
        
        tfidf_words = pca.transform([modelTfidf.get_text_vector(words_word)])[0]
        tfidf = [pca.transform([modelTfidf.get_text_vector(word)])[0] for word in words]
        tfidf = [cosine_dist(tfidf_words, word) for word in tfidf]
        neuro_words = modelNeuro.get_vector(words_word)
        neuro = [modelNeuro.get_vector(word) for word in words]
        neuro = [cosine_dist(neuro_words, word) for word in neuro]
        
        output.write("word: {words_word}\n".encode())
        output.write(f"{'word':10}\t{'tfidf_dist':10}\t{'neuro_dist':10}\n".encode())
        for i in range(len(words)):
            output.write(f"{words[i]:10}\t{tfidf[i]:10f}\t{neuro[i]:10f}\n".encode())
        
        # test 2
        output.write("\n\nTest 2\n\n".encode())
        words_word = 'metal'
        words_similar = ['steel', 'iron', 'ore']
        words_area = ['rock', 'earth', 'mineral']
        words_other = ['pilot', 'election', 'cat']
        words = words_similar+ words_area + words_other
        
        tfidf_words = pca.transform([modelTfidf.get_text_vector(words_word)])[0]
        tfidf = [pca.transform([modelTfidf.get_text_vector(word)])[0] for word in words]
        tfidf = [cosine_dist(tfidf_words, word) for word in tfidf]
        neuro_words = modelNeuro.get_vector(words_word)
        neuro = [modelNeuro.get_vector(word) for word in words]
        neuro = [cosine_dist(neuro_words, word) for word in neuro]
        
        output.write("word: {words_word}\n".encode())
        output.write(f"{'word':10}\t{'tfidf_dist':10}\t{'neuro_dist':10}\n".encode())
        for i in range(len(words)):
            output.write(f"{words[i]:10}\t{tfidf[i]:10f}\t{neuro[i]:10f}\n".encode())
        
        
        # test 3
        output.write("\n\nTest 3\n\n".encode())
        sent1 = "One of the oldest textile operators on the Indian Ocean island of Mauritius last week shut seven factories and cut 900 jobs"
        sent2 = "Seven factories were shuted last week by the oldest textile company on the Indian Ocean island of Mauritius, it also fired 900 employees"
        sent3 = "One of the oldest 900 islands in Indian Ocean cut last textile and shut seven week operators"
        sent4 = "Economic growth in Japan slows down as the country experiences a drop in domestic and corporate spending"
        
        tfidf1 = pca.transform([modelTfidf.get_text_vector(sent1)])[0]
        neuro1 = modelNeuro.get_text_vector(sent1)
        tfidf2 = pca.transform([modelTfidf.get_text_vector(sent2)])[0]
        neuro2 = modelNeuro.get_text_vector(sent2)
        tfidf3 = pca.transform([modelTfidf.get_text_vector(sent3)])[0]
        neuro3 = modelNeuro.get_text_vector(sent3)
        tfidf4 = pca.transform([modelTfidf.get_text_vector(sent4)])[0]
        neuro4 = modelNeuro.get_text_vector(sent4)
        
        
        output.write("Sentences\n".encode())
        output.write(f"{sent1}\n".encode())
        output.write(f"{sent2}\n".encode())
        output.write(f"{sent3}\n".encode())
        output.write(f"{sent4}\n".encode())
        output.write(f"\n{'sentences':10}\t{'tfidf_dist':10}\t{'neuro_dist':10}\n".encode())
        score1 = cosine_dist(tfidf1, tfidf2)
        score2 = cosine_dist(neuro1, neuro2)
        output.write(f"{'1-2':10}\t{score1:10f}\t{score2:10f}\n".encode())
        score1 = cosine_dist(tfidf1, tfidf3)
        score2 = cosine_dist(neuro1, neuro3)
        output.write(f"{'1-3':10}\t{score1:10f}\t{score2:10f}\n".encode())
        score1 = cosine_dist(tfidf1, tfidf4)
        score2 = cosine_dist(neuro1, neuro4)
        output.write(f"{'1-4':10}\t{score1:10f}\t{score2:10f}\n".encode())
        score1 = cosine_dist(tfidf2, tfidf3)
        score2 = cosine_dist(neuro2, neuro3)
        output.write(f"{'2-3':10}\t{score1:10f}\t{score2:10f}\n".encode())
        score1 = cosine_dist(tfidf2, tfidf4)
        score2 = cosine_dist(neuro2, neuro4)
        output.write(f"{'2-4':10}\t{score1:10f}\t{score2:10f}\n".encode())
        score1 = cosine_dist(tfidf3, tfidf4)
        score2 = cosine_dist(neuro3, neuro4)
        output.write(f"{'3-4':10}\t{score1:10f}\t{score2:10f}\n".encode())
        
        
        # test 4
        output.write("\n\nTest 4\n\n".encode())
        sent1 = "A red-footed falcon spotted for the first time in North America is enticing birdwatchers to Martha's Vineyard"
        sent2 = "A bird with red legs seen for the first time in North America is attracting ornithologists to Martha's Vineyard"
        sent3 = "A spotted red-footed birdwatchers in North America enticing falcon to Martha's Vineyard for the first time"
        sent4 = "Celebrity fashion is booming. These webpreneurs are bringing it to main street"
        
        tfidf1 = pca.transform([modelTfidf.get_text_vector(sent1)])[0]
        neuro1 = modelNeuro.get_text_vector(sent1)
        tfidf2 = pca.transform([modelTfidf.get_text_vector(sent2)])[0]
        neuro2 = modelNeuro.get_text_vector(sent2)
        tfidf3 = pca.transform([modelTfidf.get_text_vector(sent3)])[0]
        neuro3 = modelNeuro.get_text_vector(sent3)
        tfidf4 = pca.transform([modelTfidf.get_text_vector(sent4)])[0]
        neuro4 = modelNeuro.get_text_vector(sent4)
        
        
        output.write("Sentences\n".encode())
        output.write(f"{sent1}\n".encode())
        output.write(f"{sent2}\n".encode())
        output.write(f"{sent3}\n".encode())
        output.write(f"{sent4}\n".encode())
        output.write(f"\n{'sentences':10}\t{'tfidf_dist':10}\t{'neuro_dist':10}\n".encode())
        score1 = cosine_dist(tfidf1, tfidf2)
        score2 = cosine_dist(neuro1, neuro2)
        output.write(f"{'1-2':10}\t{score1:10f}\t{score2:10f}\n".encode())
        score1 = cosine_dist(tfidf1, tfidf3)
        score2 = cosine_dist(neuro1, neuro3)
        output.write(f"{'1-3':10}\t{score1:10f}\t{score2:10f}\n".encode())
        score1 = cosine_dist(tfidf1, tfidf4)
        score2 = cosine_dist(neuro1, neuro4)
        output.write(f"{'1-4':10}\t{score1:10f}\t{score2:10f}\n".encode())
        score1 = cosine_dist(tfidf2, tfidf3)
        score2 = cosine_dist(neuro2, neuro3)
        output.write(f"{'2-3':10}\t{score1:10f}\t{score2:10f}\n".encode())
        score1 = cosine_dist(tfidf2, tfidf4)
        score2 = cosine_dist(neuro2, neuro4)
        output.write(f"{'2-4':10}\t{score1:10f}\t{score2:10f}\n".encode())
        score1 = cosine_dist(tfidf3, tfidf4)
        score2 = cosine_dist(neuro3, neuro4)
        output.write(f"{'3-4':10}\t{score1:10f}\t{score2:10f}\n".encode())