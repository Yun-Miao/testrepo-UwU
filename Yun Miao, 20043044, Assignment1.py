"""
Many of the required functions have been provided for you. Your task is to complete the
calculateSD() function at the end of this file. The calculateSD() function will make use
of all of the provided functions.

You will also need to write the countAdjectives(), countAdverbs(), getUniqueWords(), and 
countWords() functions in this Python file.

"""

import nltk

"""
Importing the necessary NLTK libraries and modules.
"""
from nltk.tag import StanfordPOSTagger
from nltk.corpus import wordnet
from nltk import pos_tag, word_tokenize
from nltk.corpus import words
from nltk.tokenize import word_tokenize



"""
To identify the part-of-speech of the words retrieved from
Word2vec, we used the conditional frequency feature of the NLTK module
which returns a frequency-ordered list of the possible parts of speech associated
with all of the English words that are found in the Brown Corpus. Our sys-
tem uses the Brown Corpus to generate the frequency-ordered list because
of the fact that the words contained in the Brown Corpus are annotated with
part-of-speech tags.
"""

wordtags = nltk.ConditionalFreqDist((w.lower(), t) 
        for w, t in nltk.corpus.brown.tagged_words(tagset="universal"))


def findPOS(word):
    """
    This is a function that accepts a word as its parameter and returns the part-of-speech of the word.
    The function considers adjectives, adverbs and nouns.
    """
	
    lisPOS = list(wordtags[word])
    if "ADJ" in lisPOS:
        return "ADJECTIVE"
    if "ADV" in lisPOS:
        return "ADVERB"
    if "NN" in lisPOS:
        return "NOUN"
    

def readFile(filename):
    """
    This is a function that accepts a path to a file as its parameter, reads in and returns the file
    """
    speechFile = open(filename, "r")
    speech = speechFile.read()
    speechFile.close()
    return speech


def getWords(text):
    """
    This is a function that segments the words in a document
    """
    text = text.replace("\n", " ")
    text = text.replace("-", " ")
    while text.count("  ") > 0 :
        text = text.replace("  ", " ")
    text = text.lower()
    cleanedUp = ""
    for char in text:
        if char.isalpha() or char == " ":
            cleanedUp = cleanedUp + char
    return  sorted(cleanedUp.split())


def prepareSemanticDifferential():
    """
    This is a function that reads in the EPA values from the Osgood wordlist and stores the values in 
    a Python dictionary.
    """
	
    filename = ("OsgoodOriginal.csv") 
    fileIn = open(filename, 'r')
    allData = {}
    line = fileIn.readline()
    while line != "":
        line = fileIn.readline().strip()
        if line != "":
            values = line.split(',')
            wordData = {}
            wordData['evaluation'] = float(values[1])
            wordData['activity'] = float(values[2])
            wordData['potency'] = float(values[3])
            allData[str(values[0])] = wordData
    fileIn.close()
    return allData


#This is the function that calculate the EPA valuess
def calculateSD(filename):
    """
    This is the function that you need to write. This function will calculate the evaluation, activity and 
    potency levels of the text. You will need to use all of provided functions findPOS(), readFile(), 
    getWords() and prepareSemanticDifferential() in your solution. 
    """
    #evaluationSum: store the running sum of evaluation scores.
    #activitySum: store the running sum of activity scores.
    #potencySum: store the running sum of potency scores.
    speech = readFile(filename)
    words = getWords(speech)
    evaluationSum = 0
    activitySum = 0
    potencySum = 0
    allData = prepareSemanticDifferential()
    for word in words:
        if findPOS(word) and findPOS(word) != "NOUN":
            if word in allData:
                evaluationSum += allData[word]['evaluation']
                activitySum += allData[word]['activity']
                potencySum += allData[word]['potency']

    print("Evaluation Score: ",evaluationSum)
    print("Activity Score: ",activitySum)
    print("Potency Score: ",potencySum)


#This is the function that returns the number of adjectives in the text file.
def countAdjectives(filename):
    words = getWords(readFile(filename))
    countAdj = 0
    for word in words: 
        if findPOS(word) == "ADJECTIVE":
            countAdj += 1
    print("The total number of adjective is: ",countAdj)


#This is the function that returns the number of adverbs in the text file. 
def countAdverbs(filename):
    words = getWords(readFile(filename))
    countAdv = 0
    for word in words:
        if findPOS(word) == "ADVERB":
            countAdv += 1
    print("The total number of adverbs is: ",countAdv)


#This is the function that returns the subset of unique words from the text file.
def getUniqueWords(filename):
    words = getWords(readFile(filename))
    uniqueWords = []
    for word in words:
        if not word in uniqueWords:
            uniqueWords.append(word)
    return uniqueWords
    

#This is the function that returns the count of each of the unique words
def countWords(filename):
    words = getWords(readFile(filename))
    uniqueWords = getUniqueWords(filename)
    result = {}
    for word in uniqueWords:
        result[word] = words.count(word)
    return result


def main():
    filename = "a.txt"
    calculateSD(filename)
    countAdjectives(filename)
    countAdverbs(filename)
    print(getUniqueWords(filename))
    print(countWords(filename))

main()