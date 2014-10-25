#!/usr/bin/env python
# encoding: utf-8

"""
A simple Naive Bayes text classifier

Author: Ethan Hart
v0.1 - 2011
curr - 2014
"""

from sets import Set
from sys import argv
import os
import math
import glob
import argparse


__author__ = "Ethan Hart"


def load_stop_words():
    """
    Open stoplist file and return list of stoplist words
    """

    stop_words = []
    stoplist = open("stoplist.txt", "r")
    for i in stoplist:
        i = i.strip()
        stop_words.append(i)
    return stop_words


stop_words = load_stop_words()

def get_word_counts(filePath, stop_words=[]):
    """
    Given a directory, read all files and add each word to the dictionary
    where the dictionary key = word and value = count of the word
    """

    word_dict = {}
    path = filePath
    for subdir, dirs, files in os.walk(path):
        for fname in files:
            fp = path + fname
            with open(fp, 'r') as inf:
                words = inf.read().strip()
                for word in words.split():
                    if word not in stop_words:  # replaces "remStopWords" function
                        word_dict[word] = word_dict.get(word, 0) + 1

    # Laplace smoothing preparation
    # 0 count entries will eventually get count of 1
    for w in word_dict:
        word_dict[w] += 1

    return word_dict


pos_review = "txt_sentoken/pos/"
neg_review = "txt_sentoken/neg/"
test_pos = get_word_counts(pos_review, stop_words)
test_neg = get_word_counts(neg_review, stop_words)


def add_zero_ents(dict1, dict2):
    """
    Adds 0 count entries into other dictionary with a count of 1
    """

    for keys in dict1:
        if keys not in dict2:
            dict2[keys] = 1

add_zero_ents(test_pos, test_neg)
add_zero_ents(test_neg, test_pos)


def condit_prob(dictionary):
    """
    conditional prob = (word count/total words in class)
    This conditional probability becomes the new value of the dictionary key
    """

    prob_dict = {}
    total = sum([i for i in dictionary.values()])
    for item in dictionary:
        con_prob = dictionary[item] / float(total)
        log_con_prob = math.log(con_prob)
        prob_dict[item] = log_con_prob
    return prob_dict


prob_dict_pos = condit_prob(test_pos)
prob_dict_neg = condit_prob(test_neg)


def prob_determine(test_file):
    """
    Given a single file, look word by word and keeps two scores: one negative,
    one postitive. The score is the addition of the values (probabilties) of
    the keys (these are logs, so they are added) that match the word in the new
    file. Finally, the higher score is determined between postive or negative.
    If it is positive, it will return filename +, else -.
    """

    poscount=0
    fileName = test_file
    tf = open(test_file, 'r')
    lines = tf.read()
    words = lines.split()
    countPos = 0
    countNeg = 0
    for word in words:
        if word in prob_dict_pos:
            countPos = countPos + prob_dict_pos[word]
        if word in prob_dict_neg:
            countNeg = countNeg + prob_dict_neg[word]
    if (countPos) > (countNeg):
        result = fileName + "+"
        poscount = poscount+1 #SEE NOTE BELOW
    else:
        result = fileName + "-"
    return result
    #return poscount is a simple metric that I can total
    #for all files analyzed so I can determine what percentage
    #of files I looked at were positive


#posTest = "/Users/ejhart/Downloads/moviedata/testpos/"
#negTest = "/Users/ejhart/Downloads/moviedata/testneg/"
#negTest = "/Users/ejhart/Downloads/moviedata/csci5832_hw3_test_set/"

#Path of the final test set.  Note is is different from csci5832_hw3_test_set
#because i had to reformat the files, and they are written into this new dir.
foo = "moviedata/finalTest/"


#loops through all the files in the test set, and feeds them to the
#function that determines pos or neg
#Again, the poscount is a simple tool for me to keep score
#when training and testing

test_file = argv[1]
print prob_determine(test_file)
#poscount = 0
#for subdir, dirs, files in os.walk(foo):
    #for file in files:
        #test = len(files)
        #f = foo + file
        #x = prob_determine(f)
        #poscount = poscount+x

#print test #make sure total # of files is correct
#print poscount #number of positive files found
#print poscount/test #gives me a percentage of pos files/total files


#def main():
    #test_file = argv[1]


#if __name__ == "__main__":
    #main()
