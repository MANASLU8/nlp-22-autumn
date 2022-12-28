from vectorize import VectorizationNeuro
from math import sqrt

def get_sentences():
    with open("projects/mansurov-project/assets/vectorize/filtered_sentences.tsv", 'rb') as input:
        lines = input.readlines()
        sentences = [line.decode('utf8').split("\t")[:-1] for line in lines]
    return sentences

def cosine_dist(a, b):
    S, A, B = 0, 0, 0
    for i in range(len(a)):
        S += a[i]*b[i]
        A += a[i]*a[i]
        B += b[i]*b[i]
    return 1 - S/sqrt(A)/sqrt(B)

if __name__=="__main__":
    model = VectorizationNeuro(from_file=True, sentences=get_sentences())
    
    metal_similar = ['steel', 'iron', 'ore']
    metal_area = ['rock', 'earth', 'mineral']
    metal_other = ['pilot', 'election', 'cat']
    metal = metal_similar + metal_area + metal_other
    
    games_similar = ['game', 'entertainment', 'contest']
    games_area = ['sport', 'competition', 'bet']
    games_other = ['document', 'expense', 'trade']
    games = games_similar + games_area + games_other
    
    south_similar = ['north', 'east', 'west']
    south_area = ['map', 'ocean', 'compass']
    south_other = ['master', 'enemy', 'papers']
    south = south_similar + south_area + south_other
    
    palace_similar = ['castle', 'mansion', 'bastion']
    palace_area = ['king', 'royal', 'tower']
    palace_other = ['rain', 'defect', 'south']
    palace = palace_similar + palace_area + palace_other
    
    with open("projects/mansurov-project/assets/vectorize/cosine_test.txt", "wb") as output:
        output.write("\nMETAL\n\n".encode())   
        for score in [(word, cosine_dist(model.get_vector('metal'), model.get_vector(word))) for word in metal]:
            output.write(f"{score[0]} - {score[1]}\n".encode())
        
        output.write("\nGAMES\n".encode())
        for score in [(word, cosine_dist(model.get_vector('games'), model.get_vector(word))) for word in games]:
            output.write(f"{score[0]} - {score[1]}\n".encode())
        
        output.write("\nSOUTH\n".encode())
        for score in [(word, cosine_dist(model.get_vector('south'), model.get_vector(word))) for word in south]:
            output.write(f"{score[0]} - {score[1]}\n".encode())
            
        output.write("\nPALACE\n".encode())
        for score in [(word, cosine_dist(model.get_vector('palace'), model.get_vector(word))) for word in palace]:
            output.write(f"{score[0]} - {score[1]}\n".encode())