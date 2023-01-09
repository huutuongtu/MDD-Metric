from metric import Correct_Rate, Accuracy, Align
from jiwer import wer
import pandas as pd



test = pd.read_csv("./test.csv")
f = open("./ref_human_detail", 'a')
for i in range(len(test)):
    # f.write("000" + str(test['Path'][i]) + "\t")
    path = test['Path'][i]
    path = str(path)
    seq1 = test['Canonical'][i]
    seq2 = test['Transcript'][i]
    seq1, seq2 = Align(seq1.split(" "), seq2.split(" "))
    REF = ''
    HYP = ''
    OP = ''
    for i in range(len(seq1)):
        REF = REF  + seq1[i] + "\t"
        HYP = HYP  + seq2[i] + "\t"
        if seq1[i]!="<eps>" and seq2[i]=="<eps>":
            OP = OP + "D" + "\t"
        elif seq1[i] == "<eps>" and seq2[i]!="<eps>" :
            OP = OP + "I" + "\t"
        elif (seq1[i]!=seq2[i]) and seq2[i]!="<eps>" and seq1[i]!="<eps>":
            OP = OP + "S" + "\t"
        else:
            OP = OP + "C" + "\t"
    print(REF)
    print(HYP)
    print(OP)
    
    f.write(path + "\t" + "ref" + "\t" + REF + "\n")
    f.write(path + "\t" + "hyp" + "\t" + HYP + "\n")
    f.write(path + "\t" + "op" + "\t" + OP + "\n")


