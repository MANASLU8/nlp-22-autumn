import csv

def distance_v_f(a, b):
    # Вычисляеем расстояние Левенштейна между a и b.
    l1, l2 = len(a), len(b)
    if l1 > l2:
        # Проверим, что l1 <= l2, чтобы использовать пространство O(min(l1, l2))
        a, b = b, a
        l1, l2 = l2, l1
    cur = range(l1 + 1) # Сохранить текущий и предыдущий столбец, а не всю матрицу
    for i in range(1, l2 + 1):
        prev = cur
        cur = [i] + [0] * l2
        for j in range(1, l1 + 1):
            zamena = prev[j - 1]
            if a[j - 1] != b[i - 1]:
                zamena += 1 # + zamena price
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, zamena)
    return cur[l1]
# Выводим результат вычисления для для строки a и строки b
a = 'cat'
b = 'dogs'
print(a)
print(b)
print(distance_v_f(a,b))


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
            distance = distance_v_f(value, word)
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
