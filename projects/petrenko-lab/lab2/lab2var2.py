import csv

def lev_distance(i, j, s1, s2, matrix):
    if i == 0 and j == 0:
        return 0
    elif j == 0 and i > 0:
        return i
    elif i == 0 and j > 0:
        return j
    else:
        m = 0 if s1[i-1] == s2[j-1] else 1
        return min(matrix[i][j-1]+1, matrix[i-1][j]+1, matrix[i-1][j-1]+m)

def calculate_levenshtein_distance(s1, s2):
    n = len(s1)
    m = len(s2)
    matrix = [[0 for i in range(m+1)] for j in range(n+1)]
    for i in range(n+1):
        n = len(s1)
        m = len(s2)
        matrix = [[0 for i in range(m+1)] for j in range(n+1)]
        for i in range(n+1):
            for j in range(m+1):
                matrix[i][j] = lev_distance(i, j, s1, s2, matrix)
        return matrix[n][m]

s1 = "cat"
s2 = "dots"

print(calculate_levenshtein_distance(s1, s2))


theme = 'comp.os.ms-windows.misc'
dict_file = f'dicts/{theme}.tsv'
test_file = f'test_data/{theme}/10004'

dictionary = [x.replace("\n", '').split('\t')[0] for x in open(dict_file).readlines() if len(x.replace("\n", '').split('\t')[0]) > 2]
dictionary.sort(key = lambda x:len(x))

items = []

print(len(dictionary))
test_data = open(f"test_data/{theme}/10004", "r").read().split()
test_data.sort(key = lambda x:len(x))
with open(f"out/{theme}.tsv", "w") as fout:
    for word in test_data:
        min_d = 999
        min_word = '999'
        for value in dictionary:
            distance = calculate_levenshtein_distance(value, word)
            if distance < min_d:
                min_d = distance
                min_word = value
            if distance == 0:            
                break
        if min_d == 999:
            print("WTF")
            break
        print(f'{word}\t{min_word}\t{min_d}')
        items.append((word, min_word, min_d))
        fout.write(f"{word}\t{min_word}\t{min_d}\n")


vsego = len(items)
not_modified = 0
for item in items:
    if item[2] == 0:
        not_modified = not_modified + 1
print(not_modified/vsego)


#я выполнил 2 лабораторную работу
#я выполнил 2 лабараторную работя
#0,6 корректные слова
#я выполнил 2 лабораторную работа
#0,8
