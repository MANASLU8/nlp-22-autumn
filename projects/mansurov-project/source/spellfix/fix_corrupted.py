from tokenizer import tokenize

from spellcheck import spellcheck, __init__

import csv

__init__()

def fix_text(text):
    # print(text)
    sentences = tokenize(text)
    # print(sentences)
    fixed = []
    for sentence in sentences:
        # print(sentence)
        _ = [spellcheck(token) for token in sentence]
        # print(_)
        fixed.append(_)
    return fixed
            
def fix_all(rows = 1064, from_ = 0):
    file_cor = 'projects/mansurov-project/assets/test-corrupted.csv'
    file_nor = 'projects/mansurov-project/assets/test.csv'
    file_out = 'projects/mansurov-project/assets/test-corrupted-fixed0.csv'
    with open(file_cor, 'r') as file_cor:
        with open(file_nor, 'r') as file_nor:
            with open(file_out, 'w') as out_file:
                if from_ == -1:
                    out_file.write("tokens, mistakes, mistakes (fixed), value, value (fixed), difference\n")
                csv_reader_cor = csv.reader(file_cor, delimiter=',')
                csv_reader_nor = csv.reader(file_nor, delimiter=',')
                line_count = 0
                for cor, nor in zip(csv_reader_cor, csv_reader_nor):
                    if line_count<from_:
                        line_count += 1
                        continue
                        
                    tokens_cor = tokenize(". ".join(cor[1:]))
                    tokens_nor = tokenize(". ".join(nor[1:]))
                    tokens_fix = fix_text(". ".join(cor[1:]))
                    
                    tokens_cor = [item for sublist in tokens_cor for item in sublist]
                    tokens_nor = [item for sublist in tokens_nor for item in sublist]
                    tokens_fix = [item for sublist in tokens_fix for item in sublist]
                    
                    # print(tokens_cor)
                    # print(tokens_nor)
                    # print(tokens_fix)
                    
                    if len(tokens_nor) == len(tokens_cor):
                        tk, mc, mf = len(tokens_nor), 0, 0
                        for i in range(len(tokens_cor)):
                            if tokens_cor[i] != tokens_nor[i]:
                                mc+=1
                            if tokens_fix[i] != tokens_nor[i]:
                                mf+=1
                        vc = mc/tk
                        vf = mf/tk
                        out_file.write(f"{tk}, {mc}, {mf}, {vc:.3f}, {vf:.3f}, {(vc-vf):.3f}\n")
                    else:
                        out_file.write("0, 0, 0, 0, 0, 0\n")
                    
                    line_count += 1
                    print(line_count)
                    if (line_count==rows):
                        break
    print(f'\nProcessed {line_count} rows')
    return

def calculate_mean():
    count_, value_, valuef_, diff_ = -1, 0, 0, 0
    file_values = 'projects/mansurov-project/assets/test-corrupted-fixed.csv'
    with open(file_values, 'r') as values_file:
        csv_reader = csv.reader(values_file, delimiter=',')
        for values in csv_reader:
            if values[0] == 0:
                continue
            count_ += 1
            # skip headers
            if count_ == 0:
                continue
            value_ += float(values[3])
            valuef_ += float(values[4])
            diff_ += float(values[5])
    file_out = 'projects/mansurov-project/assets/test-corrupted-fixed-mean.csv'
    with open(file_out, 'w') as file:
        mean_value = value_/count_
        mean_valuef = valuef_/count_
        mean_diff = diff_/count_
        file.write(f"mean value, mean value (fixed), mean difference\n")
        file.write(f"{mean_value:.3f}, {mean_valuef:.3f}, {mean_diff:.3f}")
            
if __name__ == "__main__":
    # print(fix_text("Tyeannosaurus rex achieved itw mssive size u to an dnormous growth spurt during its adolescent years."))
    
    # cor = ["Terreblanche challenges SA arrest","White supremacidt Eugene Terreblanche is detained after allegedly bteaking the terms of hs arole."]
    # nor = ["Terreblanche challenges SA arrest","White supremacist Eugene Terreblanche is detained after allegedly breaking the terms of his parole."]
    # tokens_cor = tokenize(". ".join(cor))
    # tokens_nor = tokenize(". ".join(nor))
    # tokens_fix = fix_text(". ".join(cor))
    # tokens_cor = [item for sublist in tokens_cor for item in sublist]
    # tokens_nor = [item for sublist in tokens_nor for item in sublist]
    # tokens_fix = [item for sublist in tokens_fix for item in sublist]
    # print(len(tokens_cor))
    # if len(tokens_nor) == len(tokens_cor):
    #     tk, mc, mf = len(tokens_nor), 0, 0
    #     for i in range(len(tokens_cor)):
    #         if tokens_cor[i] != tokens_nor[i]:
    #             mc+=1
    #         if tokens_fix[i] != tokens_nor[i]:
    #             mf+=1
    #     vc = mc/tk
    #     vf = mf/tk
    #     print(f"{tk}, {mc}, {mf}, {vc:.3f}, {vf:.3f}, {(vc-vf):.3f}\n")
    # else:
    #     print("0, 0, 0, 0, 0, 0\n")
        
    # print(tokens_cor)
    # print(tokens_nor)
    # print(tokens_fix)
                    
    calculate_mean()
    
    # fix_all()