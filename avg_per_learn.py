import sys
import os
import random
import json

from collections import defaultdict


def read_recursive(src):

    file_dict=defaultdict(dict)
    weight_of_word={}
    avg_weight_of_words={}
    file_counter=1

    jenc = json.JSONEncoder();

    for root, directories, filenames in os.walk(src):

        for directory in directories:
            # if the directory is HAM

            if (directory == "ham"):

                # look for files in directory HAM
                for root_1, directories_1, filenames_1 in os.walk(os.path.join(root, directory)):
                    # open files in HAM folder

                    for filename_1 in filenames_1:
                        input = open(os.path.join(root_1, filename_1), "r", encoding="latin1").read()
                        tokens = input.split()

                        file_dict[file_counter]["ham"] = tokens

                        for each_token in tokens:
                            if each_token not in weight_of_word:
                                weight_of_word[each_token]=0
                                avg_weight_of_words[each_token]=0


                        file_counter=file_counter+1;

            elif (directory == "spam"):
                # look for files in directory SPAM
                for root_1, directories_1, filenames_1 in os.walk(os.path.join(root, directory)):
                    # open files in SPAM folder

                    for filename_1 in filenames_1:

                        input = open(os.path.join(root_1, filename_1), "r", encoding="latin1").read()
                        tokens = input.split()

                        file_dict[file_counter]["spam"] = tokens
                        for each_token in tokens:
                            if each_token not in weight_of_word:
                                weight_of_word[each_token] = 0
                                avg_weight_of_words[each_token] = 0

                        file_counter = file_counter + 1;

    list_of_files=[]
    for file_number in file_dict.keys():
        list_of_files.append(file_number)

    distinct_words=defaultdict()



    bias=0
    beta=0
    counter=1

    for iteration in range (0,30):

        random.shuffle(list_of_files)

        for each_file in list_of_files:

            check_if_spam_or_ham = file_dict[each_file]
            # print (check_if_spam_or_ham)

            for item in check_if_spam_or_ham:
                if item=="ham":
                    all_tokens = file_dict[each_file][item]
                    sum_of_weights=0

                    for each_token in all_tokens:
                        sum_of_weights=sum_of_weights + weight_of_word[each_token]

                    alpha=sum_of_weights+bias

                    product=alpha * (-1)
                    if(product <= 0):
                        for each_token in all_tokens:
                            weight_of_word[each_token]= weight_of_word[each_token] - 1
                            avg_weight_of_words[each_token]=avg_weight_of_words[each_token] + (-1 * counter)

                        beta=beta - counter
                        bias=bias - 1

                    counter=counter+1

                if item=="spam":
                    all_tokens = file_dict[each_file][item]
                    sum_of_weights=0


                    for each_token in all_tokens:
                        sum_of_weights=sum_of_weights + weight_of_word[each_token]

                    alpha=sum_of_weights+bias

                    product=alpha
                    if(product <= 0):
                        for each_token in all_tokens:
                            weight_of_word[each_token]= weight_of_word[each_token] + 1
                            avg_weight_of_words[each_token] = avg_weight_of_words[each_token] + counter

                        beta = beta + counter

                        bias=bias + 1

                    counter = counter + 1

    for each_word in weight_of_word:
        avg_value=avg_weight_of_words[each_word]
        avg_weight_of_words[each_word]= float(weight_of_word[each_word]) - float(avg_value/counter)

    beta= float(bias - (beta/counter))
    try:
        os.remove('per_model.txt')
    except OSError:
        pass
    f=open('per_model.txt', "w", encoding="latin1")
    f.write(jenc.encode(beta) + "\n")
    f.write(jenc.encode(avg_weight_of_words))

read_recursive(sys.argv[1])