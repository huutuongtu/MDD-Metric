gap_penalty = -1
match_award = 1
mismatch_penalty = -1

def zeros(rows, cols):
    # Define an empty list
    retval = []
    # Set up the rows of the matrix
    for x in range(rows):
        # For each row, add an empty list
        retval.append([])
        # Set up the columns in each row
        for y in range(cols):
            # Add a zero to each column in each row
            retval[-1].append(0)
    # Return the matrix of zeros
    return retval

def match_score(alpha, beta):
    if alpha == beta:
        return match_award
    elif alpha == '-' or beta == '-':
        return gap_penalty
    else:
        return mismatch_penalty

def Align(seq1, seq2):
    
    # Store length of two sequences
    n = len(seq1)  
    m = len(seq2)
    
    # Generate matrix of zeros to store scores
    score = zeros(m+1, n+1)
   
    # Calculate score table
    
    # Fill out first column
    for i in range(0, m + 1):
        score[i][0] = gap_penalty * i
    
    # Fill out first row
    for j in range(0, n + 1):
        score[0][j] = gap_penalty * j
    
    # Fill out all other values in the score matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Calculate the score by checking the top, left, and diagonal cells
            match = score[i - 1][j - 1] + match_score(seq1[j-1], seq2[i-1])
            delete = score[i - 1][j] + gap_penalty
            insert = score[i][j - 1] + gap_penalty
            # Record the maximum score from the three possible scores calculated above
            score[i][j] = max(match, delete, insert)
    
    # Traceback and compute the alignment 
    
    # Create variables to store alignment
    align1 = ""
    align2 = ""
    
    # Start from the bottom right cell in matrix
    i = m
    j = n
    
    # We'll use i and j to keep track of where we are in the matrix, just like above
    while i > 0 and j > 0: # end touching the top or the left edge
        score_current = score[i][j]
        score_diagonal = score[i-1][j-1]
        score_up = score[i][j-1]
        score_left = score[i-1][j]
        
        # Check to figure out which cell the current score was calculated from,
        # then update i and j to correspond to that cell.
        if score_current == score_diagonal + match_score(seq1[j-1], seq2[i-1]):
            align1 += seq1[j-1]
            align2 += seq2[i-1]
            i -= 1
            j -= 1
        elif score_current == score_up + gap_penalty:
            align1 += seq1[j-1]
            align2 += '-'
            j -= 1
        elif score_current == score_left + gap_penalty:
            align1 += '-'
            align2 += seq2[i-1]
            i -= 1

    # Finish tracing up to the top left cell
    while j > 0:
        align1 += seq1[j-1]
        align2 += '-'
        j -= 1
    while i > 0:
        align1 += '-'
        align2 += seq2[i-1]
        i -= 1
    
    # Since we traversed the score matrix from the bottom right, our two sequences will be reversed.
    # These two lines reverse the order of the characters in each sequence.
    align1 = align1[::-1]
    align2 = align2[::-1]
    
    return(align1, align2)



def insertions(Seq1, Seq2):
        res = 0
        for i in range(len(Seq1)):
            if Seq1[i] == "-" and Seq2[i]!="-" :
                res = res + 1
        return res
def deletions(Seq1, Seq2):
    res = 0
    for i in range(len(Seq1)):
        if (Seq1[i].isalpha() or Seq1[i]==" ") and Seq2[i]=="-":
            res = res + 1
    return res
def substitutions(Seq1, Seq2):
    res = 0
    for i in range(len(Seq1)):
        if (Seq1[i]!=Seq2[i]) and Seq2[i]!="-" and Seq1[i]!="-":
            res = res + 1
    return res

def Correct_Rate(SEQ1, SEQ2):
    SEQ1 = SEQ1.strip()
    SEQ2 = SEQ2.strip()
    Seq1, Seq2 = Align(SEQ1, SEQ2)
    Seq1 = Seq1.strip()
    Seq2 = Seq2.strip()
    cnt = deletions(Seq1, Seq2) + substitutions(Seq1, Seq2)
    return 1 - (cnt/len(SEQ1))


def Accuracy(SEQ1, SEQ2):
    SEQ1 = SEQ1.strip()
    SEQ2 = SEQ2.strip()
    Seq1, Seq2 = Align(SEQ1, SEQ2)
    Seq1 = Seq1.strip()
    Seq2 = Seq2.strip()
    cnt = insertions(Seq1, Seq2) + deletions(Seq1, Seq2) + substitutions(Seq1, Seq2)

    return 1 - (cnt/len(SEQ1))


#Correct: *



def CheckPronunciations(Canonical, Transcript, Predict):
    CanTrans, TransCan = Align(Canonical, Transcript)
    CanPre, PreCan = Align(Canonical, Predict)

    indexCheckCanTransCorrect = 0
    indexCheckCanPreCorrect = 0
    
    ListCanTransCorrect = []
    ListCanTranInCorrect = []
    ListCanPreCorrect = []
    ListCanPreInCorrect = []

    for i in range(len(CanTrans)):
        
        if CanTrans[i]==TransCan[i] and CanTrans[i]!="-":   #Transcript is True
            ListCanTransCorrect.append(indexCheckCanTransCorrect)  #Save true index can-trans to Canonical
        elif CanTrans[i]!=TransCan[i]: #Transcript is False
            ListCanTranInCorrect.append(indexCheckCanTransCorrect) #Save false index can-trans to Canonical
        

        if (CanTrans!="-" and TransCan!="-"): #if both blank index + 1
            indexCheckCanTransCorrect = indexCheckCanTransCorrect+1

    for i in range(len(CanPre)):
        
        if CanPre[i]==PreCan[i] and CanPre[i]!="-": #Predict is true
            ListCanPreCorrect.append(indexCheckCanPreCorrect) #Save true index can-pre to Canonical
        elif CanPre[i]!=PreCan[i]: #Transcript is False
            ListCanPreInCorrect.append(indexCheckCanPreCorrect) #Save false index can-trans to Canonical

        if (CanPre!="-" and PreCan!="-"): #If both blank index + 1
            indexCheckCanPreCorrect = indexCheckCanPreCorrect+1

    print(ListCanPreCorrect)
    print(ListCanTransCorrect)
    print(ListCanPreInCorrect)
    print(ListCanTranInCorrect)

    TA = len(set(ListCanTransCorrect) & set(ListCanPreCorrect)) #True Accept
    TR = len(set(ListCanTranInCorrect) & set(ListCanPreInCorrect)) #True Reject
    FR = len(set(ListCanTransCorrect) & set(ListCanPreInCorrect)) #False Reject
    FA = len(set(ListCanTranInCorrect) & set(ListCanPreCorrect)) #False Accept

    # FRR = FR/(TA+FR)
    # FAR = FA/(FA+TR)
    # Detection_Accuracy = (TA+TR)/(TR+TA+FR+FA)
    # Precision = TR/(TR+FR)
    # Recall = TR/(TR+FA)
    # FMeasure = 2*(Precision * Recall)/(Precision + Recall)

    return TA, TR, FR, FA



        



Seq1 = 'xin chao toi la Tu dep trai a'
Seq2 = 'xin chao tôi la Tu dep trao '
Seq3 = 'xin chao tpi la Tu dep traya'
TA, TR, FR, FA = CheckPronunciations(Seq1, Seq2, Seq3)

print(TA)
print(TR)
print(FR)
print(FA)
# print(FA)
# print(Accuracy(Seq1, Seq2))
# print(cer(Seq1, Seq2))
# print(Correct_Rate(Seq1, Seq2))

"""
Res
25
2
1
1
"""