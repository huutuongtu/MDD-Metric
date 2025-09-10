from metric import Correct_Rate, Accuracy, Align
from jiwer import wer, cer
import pandas as pd

# Load CSV
test = pd.read_csv("xyz.csv")

# === PER and Correctness ===
del_sub_count = 0
ins_del_sub_count = 0
number_phoneme = 0
del_All = []

for i in range(len(test)):
    cnt, len_sentence, all_Del = Correct_Rate(test['Transcript'][i].split(), test['Predict'][i].split())
    del_All.extend(all_Del)
    del_sub_count += cnt

    cnt, len_sentence = Accuracy(test['Transcript'][i].split(), test['Predict'][i].split())
    ins_del_sub_count += cnt
    number_phoneme += len_sentence


print(number_phoneme)
print(del_sub_count)
print(ins_del_sub_count)
print("PER", (1 - (number_phoneme - ins_del_sub_count) / number_phoneme) * 100)
print("Correctness", ((number_phoneme - del_sub_count) / number_phoneme) * 100)


# === Utility ===
def cjustify(s, width):
    if s is None:
        s = ""
    if width <= len(s):
        return s
    left = (width - len(s)) // 2
    right = width - len(s) - left
    return " " * left + s + " " * right


def write_alignment(file, path, seq1, seq2):
    """Align seq1 and seq2 and write alignment details into file."""
    seq1, seq2 = Align(seq1.split(), seq2.split())

    REF, HYP, OP = [], [], []
    cor = sub = ins = dele = 0

    for r, h in zip(seq1, seq2):
        if r != "<eps>" and h == "<eps>":
            op = "D"; dele += 1
        elif r == "<eps>" and h != "<eps>":
            op = "I"; ins += 1
        elif r != h:
            op = "S"; sub += 1
        else:
            op = "C"; cor += 1
        REF.append(r); HYP.append(h); OP.append(op)

    col_widths = [max(len(r), len(h), len(o)) for r, h, o in zip(REF, HYP, OP)]
    ref_str = "  ".join(cjustify(r, w) for r, w in zip(REF, col_widths))
    hyp_str = "  ".join(cjustify(h, w) for h, w in zip(HYP, col_widths))
    op_str  = "  ".join(cjustify(o, w) for o, w in zip(OP, col_widths))

    file.write(f"{path} ref  {ref_str}\n")
    file.write(f"{path} hyp  {hyp_str}\n")
    file.write(f"{path} op   {op_str}\n")
    file.write(f"{path} #csid {cor} {sub} {ins} {dele}\n\n")


# === Run all three alignments in one pass ===
with open("./ref_human_detail", 'w', encoding='utf-8') as f_ref_human, \
     open("./ref_our_detail", 'w', encoding='utf-8') as f_ref_our, \
     open("./human_our_detail", 'w', encoding='utf-8') as f_human_our:

    for i in range(len(test)):
        path = str(test['Path'][i])
        ref = test['Canonical'][i].replace("*", "")
        human = test['Transcript'][i].replace("*", "")
        our = test['Predict'][i].replace("*", "")

        # Align 3 pairs
        write_alignment(f_ref_human, path, ref, human)
        write_alignment(f_ref_our, path, ref, our)
        write_alignment(f_human_our, path, human, our)
