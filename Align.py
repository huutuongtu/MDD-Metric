from metric import Correct_Rate, Accuracy, Align
from jiwer import wer, cer
import pandas as pd



#Align ref_our, human_our, ref_human
# def clean_corpus(string):
#     res = ''
#     for character in string:
#         if character.isalpha() or character == " ":
#             res = res + character
#     return res


test = pd.read_csv("APL_Baseline.csv")
"""del_sub_count = 0
ins_del_sub_count = 0
number_phoneme = 0
del_All = []
for i in range(len(test)):
    cnt, len_sentence, all_Del = Correct_Rate((test['Transcript'][i].split(" ")), (test['Predict'][i].split(" ")))
    # print(all_Del)
    del_All.extend(all_Del)
    del_sub_count+=cnt
    # number_phoneme+=len_sentence
    cnt, len_sentence = Accuracy((test['Transcript'][i].split(" ")), (test['Predict'][i].split(" ")))
    ins_del_sub_count+=cnt
    number_phoneme+=len_sentence

dec = ['n', 'h', 'ng', '7', 'q', 'l', 'sh', '7X', 't', '1', 'j', 'er', '2', 'a', '4', 'p', 'i', 'g', 'v', 's', 'r', 'z', 'zh', 'c', '3', 'b', 'u', 'ch', 'e', 'm', 'o', 'd', 'x', '5', 'f', 'k']

# print(number_phoneme)
# print(del_sub_count)
# print(ins_del_sub_count)
print((number_phoneme-del_sub_count)/number_phoneme)
print((number_phoneme-ins_del_sub_count)/number_phoneme)
"""


f = open("./ref_human_detail", 'a', encoding='utf-8')
cor_cnt = 0
sub_cnt = 0
ins_cnt = 0
del_cnt = 0
for i in range(len(test)):
    # f.write("000" + str(test['Path'][i]) + " ")
    path = test['Path'][i]
    path = str(path)
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
    # print(path)
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
