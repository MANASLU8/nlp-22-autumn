from os.path import exists

def cdis(a, b):
    return sum(map(lambda i, j: abs(i-j), a, b))

class key_distance():
    keys = {
            'q' : (0,  0   , 0), 'Q' : (0,  0   , 0.5),
            'w' : (0,  1   , 0), 'W' : (0,  1   , 0.5),
            'e' : (0,  2   , 0), 'E' : (0,  2   , 0.5),
            'r' : (0,  3   , 0), 'R' : (0,  3   , 0.5),
            't' : (0,  4   , 0), 'T' : (0,  4   , 0.5),
            'y' : (0,  5   , 0), 'Y' : (0,  5   , 0.5),
            'u' : (0,  6   , 0), 'U' : (0,  6   , 0.5),
            'i' : (0,  7   , 0), 'I' : (0,  7   , 0.5),
            'o' : (0,  8   , 0), 'O' : (0,  8   , 0.5),
            'p' : (0,  9   , 0), 'P' : (0,  9   , 0.5),
            '[' : (0, 10   , 0), '{' : (0, 10   , 0.5),
            ']' : (0, 11   , 0), '}' : (0, 11   , 0.5),
            'a' : (1,  0.25, 0), 'A' : (1,  0.25, 0.5),
            's' : (1,  1.25, 0), 'S' : (1,  1.25, 0.5),
            'd' : (1,  2.25, 0), 'D' : (1,  2.25, 0.5),
            'f' : (1,  3.25, 0), 'F' : (1,  3.25, 0.5),
            'g' : (1,  4.25, 0), 'G' : (1,  4.25, 0.5),
            'h' : (1,  5.25, 0), 'H' : (1,  5.25, 0.5),
            'j' : (1,  6.25, 0), 'J' : (1,  6.25, 0.5),
            'k' : (1,  7.25, 0), 'K' : (1,  7.25, 0.5),
            'l' : (1,  8.25, 0), 'L' : (1,  8.25, 0.5),
            ';' : (1,  9.25, 0), ':' : (1,  9.25, 0.5),
            '\'': (1, 10.25, 0), '"' : (1, 10.25, 0.5),
            '\\': (1, 11.25, 0), '|' : (1, 11.25, 0.5),
            'x' : (2,  1.75, 0), 'X' : (2,  1.75, 0.5),
            'z' : (2,  0.75, 0), 'Z' : (2,  0.75, 0.5),
            'c' : (2,  2.75, 0), 'C' : (2,  2.75, 0.5),
            'v' : (2,  3.75, 0), 'V' : (2,  3.75, 0.5),
            'b' : (2,  4.75, 0), 'B' : (2,  4.75, 0.5),
            'n' : (2,  5.75, 0), 'N' : (2,  5.75, 0.5),
            'm' : (2,  6.75, 0), 'M' : (2,  6.75, 0.5),
            ',' : (2,  7.75, 0), '<' : (2,  7.75, 0.5),
            '.' : (2,  8.75, 0), '>' : (2,  8.75, 0.5),
            '/' : (2,  9.75, 0), '?' : (2,  9.75, 0.5),   
        }
    
    dist = {}
    
    max_dist = 3
    default_dist = 2
    
    def __init__(self, dist_file='projects/mansurov-project/assets/dictionary/key_dist.tsv'):
        if exists(dist_file):
            with open(dist_file, 'r') as f:
                _ = [line.split('\t') for line in f.readlines()]
                for line in _:
                    self.dist.setdefault(line[0], {})[line[1]] = float(line[2])
        else:
            with open(dist_file, 'w') as f:
                for k1, v1 in self.keys.items():
                    self.dist[k1] = {}
                    for k2, v2 in self.keys.items():
                        self.dist[k1][k2] = round(cdis(v1, v2), 2)
                        f.write(f"{k1}\t{k2}\t{self.dist[k1][k2]}\n")
            
    def __getitem__(self, arg):
        x, y = arg
        if x=='' or y=='':
            return self.default_dist
        if self.dist.get(x) is None:
            return self.max_dist
        else:
            return self.dist[x].get(y, self.max_dist)

def lev_length(s1, s2):
    s1, s2 = '\t'+s1, '\t'+s2
    cur = list(range(len(s2)))
    # print(cur)
    for x in s1[1:]:
        prev = cur[:]
        cur[0] = prev[0]+1
        for i, y in enumerate(s2[1:]):
            i+=1
            if x == y:
                cur[i] = prev[i-1]
            else:
                cur[i] = min(cur[i-1], prev[i-1], prev[i])+1
        # print(cur)
    return cur

def lev_hirschberg(s1, s2):
    s1_len = len(s1)
    if s1_len == 0:
        return [('', w) for w in s2]
    elif s1_len == 1:
        if s1[0] in s2:
            return [(('', w),(s1, w))[s1==w] for w in s2]
            # return [(s1, s2)]
        else:
            if len(s2)==0:
                return [(s1, '')]
            else:
                _ = [('', w) for w in s2[:-1]]
                _.append((s1, s2[-1]))
                return _
    else:
        if len(s2)==0:
            return [(w, '') for w in s1]
        i = s1_len // 2 # 1//2=0  2//2=1
        b, e = s1[:i], s1[i:]
        lb = lev_length(b, s2)
        le = lev_length(e[::-1], s2[::-1])[::-1]
        # print(lb)
        # print(le)
        l = [ lb[k] + le[k] for k in range(len(s2)) ]
        _, j = min((sum_val, sum_i) for sum_i, sum_val in enumerate(l))
        h1 = lev_hirschberg(b, s2[:j])
        h2 = lev_hirschberg(e, s2[j:])
        return h1 + h2
    
key_dist = key_distance()    

def len_lev_hirschberg(values:str, dist = key_dist):
    length = 0
    for x in values:
        if x[0]=='' or x[1]=='':
            length += 1
        else:
            length += dist[x[0], x[1]]
    return length
    
if __name__ == "__main__":
    print("")
    # print(lev_hirschberg('good cat', 'god cats'))
    # print(lev_length('ACGTACGTACGT', 'AGTACCTACCGT'))
    # print(lev_hirschberg('ACGTACGTACGT', 'AGTACCTACCGT'))
    # print(len_lev_hirschberg(lev_hirschberg('ACGTACGTACGT', 'AGTACCTACCGT')))
    # print(lev_hirschberg('good', '£'))
    # print(len_lev_hirschberg(lev_hirschberg('good', '£')))
    # print(len_lev_hirschberg(lev_hirschberg('£', 'good')))
    # print(lev_hirschberg('good', 'good'))
    # print(len_lev_hirschberg(lev_hirschberg('good', 'good')))
    # print(lev_hirschberg('good', 'googly'))
    # print(len_lev_hirschberg(lev_hirschberg('good', 'googly')))
    # print(lev_length('ACGTACGTACGT'[:6], 'AGTACCTACCGT'))
    # print(lev_length('ACGTACGTACGT'[6:], 'AGTACCTACCGT'))
    # print([lev_length('ACGTACGTACGT'[:6], 'AGTACCTACCGT')[i]+lev_length('ACGTACGTACGT'[:6:-1], 'AGTACCTACCGT'[::-1])[::-1][i] for i in range(len('AGTACCTACCGT')+1)])
    # print([lev_length('ACGTACGTACGT'[:6], 'AGTACCTACCGT')[i]+lev_length('ACGTACGTACGT'[:5:-1], 'AGTACCTACCGT'[::-1])[::-1][i] for i in range(len('AGTACCTACCGT')+1)])
    
    
    # print(lcs_hirschberg('ACGTACGTACGT', 'AGTACCTACCGT'))
    # print(lcs_hirschberg('ACGTACGTACGT', 'AGTACCTACCGT'))
    # print(hirschberg('A', 'A'))
    # print(hirschberg('A', 'AA'))
    # print(hirschberg('AA', 'A'))
    # print(hirschberg('AA', 'AA'))
    # print(hirschberg('AAA', 'A'))
    # print(hirschberg('AAA', 'AA'))
    # print(hirschberg('AAA', 'AAA'))
    
    # print('a'[:-1])
    
    # _ = {
    #     'a' : 1,
    #     'b' : 2,
    #     'c' : 3
    # }
    
    # _['d'] = 2
    # _['a'] = 4
    
    # for i, v in _.items():
    #     print(i+ str(v))
        
    # a = (1, 2.3, 0)
    # b = (1, 2, 0.5)
    # print(round(cdis(a, b), 2))
    # print(float('0.8'))
    
    # print(key_distance().dist)
    
    # print('abcd'.center())