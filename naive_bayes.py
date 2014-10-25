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


def loadStopList():
    """
    Open stoplist file and return list of stoplist words
    """

    stoplist = open("stoplist.txt", "r")
    for i in stoplist:
        i = i.strip()
        list.append(i)
    return list


#stopList = loadStopList()


def loadReviews(filePath):
    """
    Given a directory, read all files and add each word to the dictionary
    where the dictionary key = word and value = count of the word
    """

    dict = {}
    path = filePath
    listing = os.listdir(path)
    for subdir, dirs, files in os.walk(path):
        for file in files:
            file = path + file
            f = open(file, 'r')
            lines = f.readlines()
            for line in lines:
                words = line.split(' ')
                for word in words:
                    dict[word] = dict.get(word,0) + 1
    return dict


def remStopWords(stoplist, dictionary):
    """
    Remove stopword entries from dictionary

    NOTE! This function is not employed- the stop list only hurt my results
    during original testing on training data
    """

    for i in stoplist:
        if i in dictionary:
            del dictionary[i]


posReview = "txt_sentoken/pos/"
negReview = "txt_sentoken/neg/"

testPos = loadReviews(posReview)
testNeg = loadReviews(negReview)


def laplacePre(dictionary):
    """
    Adds one to the value of every entry in the
    dictionary for laplace smoothing
    """

    for i in dictionary:
        dictionary[i] += 1


#adds one for each entry in dictionary in prep
#for 0 count entries to be added with count = 1
laplacePre(testPos)
laplacePre(testNeg)


def addZeroEnts(dict1, dict2):
    """
    Adds 0 count entries into other dictionary with a count of 1
    """

    for keys in dict1:
        if keys not in dict2:
            dict2[keys] = 1

addZeroEnts(testPos, testNeg)
addZeroEnts(testNeg, testPos)

def conditProb(dictionary):
    """
    conditional prob = (word count/total words in class)
    This conditional probability becomes the new value of the dictionary key
    """

    probDict = {}
    total = sum([i for i in dictionary.values()])
    for item in dictionary:
        conProb = dictionary[item] / float(total)
        conProb = math.log(conProb)
        probDict[item] = conProb
    return probDict


probDictPos = conditProb(testPos)
probDictNeg = conditProb(testNeg)

outFile = open("naiveBayesOutput.txt", "w")


def probDetermine(file):
    """
    Given a single file, look word by word and keeps two scores: onenegative,
    one postitive. The score is the addition of the values of the keys (these
    are logs, so they are added) that match the word in the new file. Finally,
    the higher score is determined between postive or negative. If it is
    positive, it will return filename +.
    """

    poscount=0
    fileName = file
    #print fileName
    #lines = open(file).read().replace('\n', '')
    file = open(file, 'r')
    #lines = file.readlines()
    lines = file.read()
    words = lines.split()
    #print len(lines)
    countPos = 0
    countNeg = 0
    #for line in lines:
        #words = line.split(' ')
        #words = line.rstrip('\n')
    for word in words:
        if word in probDictPos:
            #print 'POS: ', probDictPos[word]
            countPos = countPos + probDictPos[word]
        if word in probDictNeg:
            #print 'NEG: ', probDictNeg[word]
            countNeg = countNeg + probDictNeg[word]
        #print countPos
        #print countNeg
    if (countPos) > (countNeg):
        result = fileName + "+"
        #print posMatch
        poscount = poscount+1 #SEE NOTE BELOW
        #outFile.write(posMatch)
        #outFile.write('\n')
    else:
        result = fileName + "-"
        #print negMatch
        #outFile.write(negMatch)
        #outFile.write('\n')
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
print probDetermine(test_file)
#poscount = 0
#for subdir, dirs, files in os.walk(foo):
    #for file in files:
        #test = len(files)
        #f = foo + file
        #x = probDetermine(f)
        #poscount = poscount+x

#print test #make sure total # of files is correct
#print poscount #number of positive files found
#print poscount/test #gives me a percentage of pos files/total files


#def main():
    #test_file = argv[1]


#if __name__ == "__main__":
    #main()
