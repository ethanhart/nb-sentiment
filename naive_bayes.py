from __future__ import division 
#Ethan Hart
#Movie Review
#NLP HW 3, NAIVE BAYES

#NOTE! For this program, all the training a did worked perfectly,
#however the test set files were formatted slightly differently
#(a \n after each sentence).  I did NOT modify my code in any way,
#but to ensure that i functioned properly, I had to write a script
#to remove all \n from the test data files

import os, glob
from sets import Set
import math
from sys import argv

#this function opens group of files and creates 
#a dictionary with words as key and count as value  

def loadStopList(list):
    #stoplist = open("/Users/ejhart/Documents/stoplist.txt", "r")
    stoplist = open("stoplist.txt", "r")
    list = [] 
    for i in stoplist:
        i = i.strip()
        list.append(i)
    return list
        
stopList = []       
stopList = loadStopList(stopList)
    
#function that iterates through a path directory, text files
#and adds each word to the dictionary, where the dictionary 
#key = word and the value = count of the word
def loadReviews(filePath):
    #list = []
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
                    #list.append(word)
    return dict
    
#function that removes all entries in the dictionary
#that match a word in the Stop List

#NOTE! This function is not employed- the stop list only
#hurt my results during original testing on training data
def remStopWords(stoplist, dictionary):
    for i in stoplist:
        if i in dictionary:
            del dictionary[i]   
            
                        
#posReview = "/Users/ejhart/Downloads/moviedata/pos/" 
posReview = "txt_sentoken/pos/" 
#negReview = "/Users/ejhart/Downloads/moviedata/neg/"
negReview = "txt_sentoken/neg/" 
    
testPos = loadReviews(posReview)
testNeg = loadReviews(negReview)


#adds one to the value of every entry in the dictionary
#for laplace smoothing
def laplacePre(dictionary):
    for i in dictionary:
        dictionary[i] += 1 

#adds one for each entry in dictionary in prep
#for 0 count entries to be added with count = 1
laplacePre(testPos)
laplacePre(testNeg)

#adds 0 count entries into other dictionary
#with a count of 1
def addZeroEnts(dict1, dict2):
    for keys in dict1:
        if keys not in dict2:
            dict2[keys] = 1

addZeroEnts(testPos, testNeg)
addZeroEnts(testNeg, testPos)

#conditional prob = (word count/total words in class)
#this conditional probability becomes the new value
#of the dictionary key
def conditProb(dictionary):
    probDict = {}
    total = sum([i for i in dictionary.values()])
    for item in dictionary:
        conProb = dictionary[item]/total
        conProb = math.log(conProb)
        probDict[item] = conProb
    return probDict
        

probDictPos = conditProb(testPos)
probDictNeg = conditProb(testNeg)

outFile = open("naiveBayesOutput.txt", "w")

#function reads in a single file, looks word by word, and keeps two scores
#one score for negative, one postitive.  The score is the addition of the 
#values of the keys (these are logs, so they are added) that match the word 
#in the new file.  Finally, the higher score is determined between postive
#or negative. If it is positive, it will return filename +. 
def probDetermine(file):
    poscount=0
    fileName = file
    #print fileName
    #lines = open(file).read().replace('\n', '') 
    file = open(file, 'r')
    lines = file.readlines()
    #print len(lines)
    countPos = 0
    countNeg = 0
    #print len(lines)
    for line in lines:
        words = line.split(' ')
        #words = line.rstrip('\n')
        for word in words:
            if word in probDictPos:
                print 'POS: ', probDictPos[word]
                countPos = countPos + probDictPos[word]
            if word in probDictNeg:
                print 'NEG: ', probDictNeg[word]
                countNeg = countNeg + probDictNeg[word]
        #print countPos
        #print countNeg
        if (countPos) > (countNeg):
            posMatch = fileName + "+"
            print posMatch
            poscount = poscount+1 #SEE NOTE BELOW
            outFile.write(posMatch)
            outFile.write('\n')
        else:
            negMatch = fileName + "-"
            print negMatch
            outFile.write(negMatch)
            outFile.write('\n')
    return poscount
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
poscount = 0
for subdir, dirs, files in os.walk(foo):
    for file in files:
        test = len(files)
        f = foo + file
        x = probDetermine(f)
        #print x
        poscount = poscount+x

#print test #make sure total # of files is correct
#print poscount #number of positive files found
#print poscount/test #gives me a percentage of pos files/total files

    


