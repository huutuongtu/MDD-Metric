from metric import Correct_Rate, Accuracy, Align
from jiwer import wer, cer
import pandas as pd



#You need 3 file to analysis - First align ref_our_detail (Canonical vs Predict), human_our_detail (Transcript vs Predict), ref_human_detail (Canonical vs Transcript) - Change in line 35 and 36


test = pd.read_csv("notone_NCCF.csv")
del_sub_count = 0
ins_del_sub_count = 0
number_phoneme = 0
for i in range(len(test)):
    cnt, len_sentence, all_Del = Correct_Rate((test['Transcript'][i].split(" ")), (test['Predict'][i].split(" ")))
    del_sub_count+=cnt
    cnt, len_sentence = Accuracy((test['Transcript'][i].split(" ")), (test['Predict'][i].split(" ")))
    ins_del_sub_count+=cnt
    number_phoneme+=len_sentence


print("Correctness:", (number_phoneme-del_sub_count)/number_phoneme)
print("Accuracy:", (number_phoneme-ins_del_sub_count)/number_phoneme)


f = open("./ref_human_detail", 'a', encoding='utf-8') #change human_our and ref_our here
cor_cnt = 0
sub_cnt = 0
ins_cnt = 0
del_cnt = 0
for i in range(len(test)):
    path = test['Path'][i]
    path = str(path)
    # Transcript and Predict for human_our, Canonical and Predict for ref_our
    seq1 = test['Canonical'][i]
    seq2 = test['Transcript'][i]
    seq1, seq2 = Align(seq1.split(" "), seq2.split(" "))
    REF = ''
    HYP = ''
    OP = ''
    cor = 0
    sub = 0
    ins = 0
    dell = 0

    for i in range(len(seq1)):
        REF = REF  + seq1[i] + " "
        HYP = HYP  + seq2[i] + " "
        if seq1[i]!="<eps>" and seq2[i]=="<eps>":
            OP = OP + "D" + " "
            dell = dell + 1
            del_cnt +=1
        elif seq1[i] == "<eps>" and seq2[i]!="<eps>" :
            OP = OP + "I" + " "
            ins = ins + 1
            ins_cnt+=1
        elif (seq1[i]!=seq2[i]) and seq2[i]!="<eps>" and seq1[i]!="<eps>":
            OP = OP + "S" + " "
            sub = sub + 1
            sub_cnt+=1
        else:
            OP = OP + "C" + " "
            cor = cor + 1
            cor_cnt+=1
    # print(REF)
    # print(HYP)
    # print(OP)
    cor = str(cor)
    sub = str(sub)
    ins = str(ins)
    dell = str(dell)
    
    # print(cor)
    # print(sub)
    # print(ins)
    # print(dell)
    # print(REF)
    # print(HYP)
    # print(OP)
    f.write(path + " " + "ref" + " " + REF + "\n")
    f.write(path + " " + "hyp" + " " + HYP + "\n")
    f.write(path + " " + "op" + " " + OP + "\n")
    f.write(path + " " + "#csid" + " " + cor + " " + sub + " " + ins + " " + dell + "\n")

print(cor_cnt)
print(sub_cnt)
print(ins_cnt)
print(del_cnt)
