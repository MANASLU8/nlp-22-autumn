from math import sqrt, pow

def qwerty_evaluator(a, b) -> float:
    # print(a + ' ' + b)
    try:
        a = letter_map[a]
        b = letter_map[b]
        distance = round(sqrt(pow((a[0] - b[0]), 2) + pow((a[1] - b[1]), 2)), 2)
        # print(dist)
        if distance < 2:
            # -0.01 - приоритет для операции замены, т. е. peave -> peace, а не peave -> pave
            # 2 вариант - использовать частоту встречаемости токена при одинаковой цене
            return distance # - 0.01
        else:
            return 2
    # символа нет в раскладке
    except:
        return 2

def fix_word(dictionary, word: str, type):
    min_cost = {'cost': 1000, 'id': []}
    for key in dictionary:
        cost = levenshtein(word, dictionary[key], min_cost['cost'])
        if min_cost['cost'] > cost:
            min_cost['cost'] = cost
            min_cost['id'] = []
            min_cost['id'].append(key)
        elif min_cost['cost'] == cost:
            min_cost['id'].append(key)
        if cost == 0:
            break

    if len(min_cost['id']) > 1:
        max_number = 0
        most_likely = ''
        for id in min_cost['id']:
            if dictionary.dfs[id] > max_number:
                max_number = dictionary.dfs[id]
                most_likely = dictionary[id]
    else:
        most_likely = dictionary[min_cost['id'][0]]
    if type == 1:
        return most_likely
    elif type == 2:
        return [dictionary[key] for key in min_cost['id']]

def levenshtein(S1: str, S2: str, threshold):

        delete_cost = 1
        insert_cost = 1
        cost = 0

        # print(S1)
        n = len(S1)
        m = len(S2)

        # # уменьшение длины строки
        # if n > m:
        #     S1, S2 = S2, S1
        #     n, m = m, n

        current = range(n + 1)
        for i in range(1, m + 1):
            previous = current
            current = [i] + [0] * n
            #print(previous_row)
            for j in range(1, n + 1):
                #print(S1[j - 1] + ' ' + S2[i - 1])
                delete = previous[j] + delete_cost
                insert  = current[j - 1] + insert_cost
                if S1[j - 1] != S2[i - 1] and previous[j - 1] < min(delete, insert):
                    #subst = previous[j - 1] + qwerty_evaluator(S1[j - 1], S2[i - 1])
                    # subst = previous[j - 1] + 2 #qwerty_evaluator(S1[j - 1], S2[i - 1])
                    try:
                        if S1[i - 1] != S2[i - 1]:
                            subst = previous[j - 1] + qwerty_evaluator(S1[i - 1], S2[i - 1])
                    except:
                        subst = previous[j - 1] + 1
                else:
                    subst = previous[j - 1]
                current[j] = min(delete, insert, subst)
                # if (current[j] == subst) and (S1[j - 1] != S2[i - 1]):
                #     try:
                #         #print(S2[i - 1] + ' ' + S1[i - 1])
                #         current[j] += qwerty_evaluator(S2[i - 1], S1[i - 1]) - subst_cost
                #     except:
                #         pass
            # print(previous)

            # saving ~30% of time
            if min(current) > threshold:
                #print(current)
                #print(S1 + ' ' + S2 + ' ' + str(i))
                return min(current) + 1
        cost = current[-1]
        # print(current)
        return float(cost)

letter_map = {}
board = [['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
         ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ' ',],
         [' ', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ' ', ' ']]

for row_index, row in enumerate(board):
    for col_index, letter in enumerate(row):
        if letter != ' ':
            letter_map[letter] = (row_index, col_index)