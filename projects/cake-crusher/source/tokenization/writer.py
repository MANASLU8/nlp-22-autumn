
def write_to_tsv(set_type, category, filename, tokens, stems, lemms):
    with open('../../assets/annotated-corpus/' + set_type + '/' + category + '/' + filename + '.tsv', 'w') as file:
        for i in range(len(tokens)):
            if tokens[i] == '🍰':
                file.write('\n')
                continue
            else:
                file.write(tokens[i] + '\t' + stems[i] + '\t' + lemms[i] + '\n')