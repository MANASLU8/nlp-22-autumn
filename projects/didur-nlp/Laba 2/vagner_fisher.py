from math import *
def distance(a, b):
   n, m = len(a), len(b) #длина слова a и слова b
   if n > m:
      a, b = b, a
      n, m = m, n

   current_row = range(n+1)
   for i in range(1, m+1):
      previous_row, current_row = current_row, [i]+[0]*n
      for j in range(1,n+1):
         add = previous_row[j]+1
         delete = current_row[j-1]+1
         change = previous_row[j-1]
         if a[j-1] != b[i-1]:
            change +=qwerty(a[j-1], b[i-1])
         current_row[j] = min(add, delete, change)

   return current_row[n]

def qwerty(a, b):
    try:
        a = letter_map[a]
        b = letter_map[b]
        distance = round(sqrt(pow((a[0] - b[0]), 2) + pow((a[1] - b[1]), 2)), 2)
    except: return 2
    if distance < 1.5:
        return distance
    return 2
letter_map = {}
board = [['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
         ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ' '],
         [' ', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ' ', ' ']]
for row_index, row in enumerate(board):
    for col_index, letter in enumerate(row):
        if letter != ' ':
            letter_map[letter] = (row_index, col_index)
print(letter_map)
#print(distance('argument', 'rudiment')) # 4
#print(distance('it is good argument for me', 'rudiment')) # 21