from hirschberg import lev_hirschberg, len_lev_hirschberg


dictionary = []
    
def load_dict(file):
    global dictionary, dict_meta
    with open(file, 'rb') as tsv_file:
        dictionary = [word.decode('utf8')[:-1] for word in tsv_file.readlines()]
        dictionary.sort()
        # i = 0
        # for d in range(len(dictionary)):
        #     if len(dictionary[d])==i:
        #         continue
        #     else:
        #         dict_meta[i] = d
        #         i=len(dictionary[d])

def spellcheck(word):
    # preprocess
    normal = False
    # if normal word then lowercase
    if (word.isalpha() and word[1:].islower()):
        word0 = word.lower()
        normal = True
    else:
        word0 = word
    # find
    min_val = 10000
    min_word = ''
    
    min_word = binary_search(dictionary, word0)
    if min_word == -1:
        for d in dictionary:
            # print(d)
            val = len_lev_hirschberg(lev_hirschberg(word0, d))
            if val==0:
                min_word = d
                break
            if val<min_val:
                min_val = val
                min_word = d  
    else:
        min_word = dictionary[min_word]    
            
    # print(normal)
    # print(word[0].isupper())
    # print(min_word)
    if normal and word[0].isupper():  
        min_word = min_word.capitalize()
    return min_word

def binary_search(ls, item):
    low = 0  
    high = len(ls) - 1  
    mid = 0  
  
    while low <= high:  
        # for get integer result   
        mid = (high + low) // 2  
  
        # Check if n is present at mid   
        if ls[mid] < item:  
            low = mid + 1  
  
        # If n is greater, compare to the right of mid   
        elif ls[mid] > item:  
            high = mid - 1  
  
        # If n is smaller, compared to the left of mid  
        else:  
            return mid  
  
            # element was not present in the list, return -1  
    return -1     

def __init__():
    load_dict('projects/mansurov-project/assets/dictionary/dict.tsv')
    
if __name__ == "__main__":
    __init__()
    # print(len(dictionary))
    # print(dict_meta)
    # print(spellcheck('Good'))
    # print(dictionary[:100])