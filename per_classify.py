import sys
import os
import json


record=[]
def classify(src,dest):
    intermediate_output= open("per_model.txt", "r", encoding="latin1")
    for line in intermediate_output:
        print(type(line))
        record.append(json.loads(line))


    bias=record[0]
    weight_of_words=record[1]




    # FETCHING ACTUAL FILE COUNT
    file_counter_ham=0
    file_counter_spam=0

    identified_spam_counter=0
    identified_ham_counter=0

    correct_spam=0
    correct_ham=0



    try:
        os.remove(dest)
    except OSError:
        pass

    f = open(dest, "w", encoding="latin1")



    for root, dirs, files in os.walk(src):
        for fname in files:
            if "ham" in fname:
                file_counter_ham=file_counter_ham +1
            elif "spam" in fname:
                file_counter_spam=file_counter_spam +1


    for root, dirs, files in os.walk(src):
        for file in files:
            if file.endswith(".txt"):
                file_open=open(root + "/" + file, "r", encoding="latin1").read()
                tokens=file_open.split()

                sum_of_weights=0
                for each_token in tokens:

                    if each_token in weight_of_words:
                        sum_of_weights = sum_of_weights + weight_of_words[each_token]
                    else:
                        sum_of_weights=sum_of_weights

                alpha = sum_of_weights + bias


                if (alpha >0):
                    f.write("spam" + " " + root + '/' + file + "\n")
                    identified_spam_counter=identified_spam_counter+1

                else:
                    f.write("ham" + " " + root + '/' + file + "\n")
                    identified_ham_counter=identified_ham_counter+1

    f.close()
    output = open(dest, "r", encoding="latin1").readlines()

    for line in output:
        line=line.split()

        if line[0].lower() in line[1]:
            if line[0].lower() == "spam":
                correct_spam=correct_spam + 1
            else:
                correct_ham = correct_ham + 1

    # Precision, Recall, F score calculation


    precision_spam = correct_spam / identified_spam_counter
    precision_ham = correct_ham / identified_ham_counter

    # REcall = (correctly classified as ck) / (belongs to ck)

    recall_spam = correct_spam / file_counter_spam
    recall_ham = correct_ham / file_counter_ham

    # F-score calculation

    f_score_spam = (2 * precision_spam * recall_spam) / (precision_spam + recall_spam)
    f_score_ham = (2 * precision_ham * recall_ham) / (precision_ham + recall_ham)

    print("precison spam is ", "%.2f" %precision_spam)
    print("precison ham is ", "%.2f" %precision_ham)
    print("recall spam is ", "%.2f" %recall_spam)
    print("recall ham is ","%.2f" %recall_ham)

    print("F score spam is","%.2f" %f_score_spam)
    print("F score ham is","%.2f" %f_score_ham)

    avg_weight = round(((f_score_ham + f_score_spam) / 2),2)

    print("weighted Avg : ","%.2f" %avg_weight)




classify(sys.argv[1],sys.argv[2])