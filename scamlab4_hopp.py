#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 15:10:47 2020

@author: luisacarettahopp

Structure:
    
- Reading .eml files, one by another
- Extraction of the words with tokenizing & lemmatizing
- Comparison with the general scamwordsample: 
  An email is marked as scam if it includes more than 5 scamwords
- if scam further categorizing into business or charity

"""

from __future__ import print_function, division
import os
import codecs
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords
import fileinput

## Ignoring Errors with UTF-8
codecs.register_error("strict", codecs.ignore_errors)
## Source: https://stackoverflow.com/questions/9537356/can-i-make-decodeerrors-ignore-the-default-for-all-strings-in-a-python-2-7-p

## Reducing the words to the important ones, since it is compared with non stopwords,
## it is not needed now, but for ML
stoplist = stopwords.words('english')

# Introducing the Scamword Categorizer
f = list( fileinput.input( 'categories/scamwords_business.txt' ))  

## Reading the emails
def init_file(a_file):
    a_list = []
    f = open('hamorscam/'+ a_file, 'r', encoding='utf-8')
    a_list.append(f.read())
    f.close()
    return a_list


## Extraction of the words in the emails
def extract_words(mail):     
    lemmatizer = WordNetLemmatizer()
    if not mail:
        print('The text to be tokenized is a None type. Defaulting to blank string.')
        mail = ''
    else:
        return [lemmatizer.lemmatize(word.lower()) for word in word_tokenize(str(mail))]

    ## Source: https://github.com/samdash/naive


## Extraction of the body, wasn't working because too slow
def extract_body(mail):
    bodylist = []  
    print(bodylist)
    for i in mail:
        if i == 'head':
            bodylist.append(i)
            while i != 'body':
                bodylist.append(i)
            break
    return bodylist
                     

## Direct comparison with the scam words
def compare_scam(body):
    f = list( fileinput.input( 'categories/scamwords_general.txt' ))           
    ##print(f)
    lemmatizer = WordNetLemmatizer()
    b = [lemmatizer.lemmatize(word.lower()) for word in word_tokenize(str(f))]
    for i in b:
        if i == ',':
            b.remove(i)
        if i == '[':
            b.remove(i)
        if i == "'":
            b.remove(i)
    ##print(b)
    resultlist = []
    result = 0
    counter = 0
    counter_correct = 0
    for word in body:
        for classifier in b:
            if word == classifier and word !=']':
                resultlist.append(word)
                counter +=1
    cleaned_list = list(set(resultlist))
    counter_correct = len(cleaned_list)
    if counter_correct > 5:
        result = 1
    return result, cleaned_list, counter_correct

def test_categoryBusiness(body):         
    ##print(f)
    lemmatizer = WordNetLemmatizer()
    b = [lemmatizer.lemmatize(word.lower()) for word in word_tokenize(str(f))]
    for i in b:
        if i == ',':
            b.remove(i)
        if i == '[':
            b.remove(i)
        if i == "'":
            b.remove(i)
    ##print(b)
    resultlist = []
    result = 0
    counter = 0
    counter_correct = 0
    for word in body:
        for classifier in b:
            if word == classifier and word !=']':
                resultlist.append(word)
                counter +=1
    cleaned_list = list(set(resultlist))
    counter_correct = len(cleaned_list)
    if counter_correct > 5:
        result = 1
    return result

def test_categoryCharity(body):
    f = list( fileinput.input( 'categories/scamwords_charity.txt' ))           
    ##print(f)
    lemmatizer = WordNetLemmatizer()
    b = [lemmatizer.lemmatize(word.lower()) for word in word_tokenize(str(f))]
    for i in b:
        if i == ',':
            b.remove(i)
        if i == '[':
            b.remove(i)
        if i == "'":
            b.remove(i)
    ##print(b)
    resultlist = []
    result = 0
    counter = 0
    counter_correct = 0
    for word in body:
        for classifier in b:
            if word == classifier and word !=']':
                resultlist.append(word)
                counter +=1
    cleaned_list = list(set(resultlist))
    counter_correct = len(cleaned_list)
    if counter_correct > 5:
        result = 1
    return result


## Main function
if __name__ == '__main__' :
    
    frequencyscam = 0
    frequencyham = 0
    scamlist =[]
    hamlist = []
    
    ## Showing all emails which are used: 
    file_list = os.listdir('hamorscam/')
    print(file_list)
    
    # Showing the scam words:
    print(f)
    
    for file in file_list:
        mail = init_file(file)
        ##print(mail)
        words = extract_words(mail)
        ##print(words)
        """body = extract_body(words)
        print(body)"""    
        (result, resultlist, counter)= compare_scam(words)
        ##print(result, resultlist)
        if result == 1:
            categoryB = test_categoryBusiness(words)
            categoryC = test_categoryCharity(words)
            scamlist.append(resultlist)
            frequencyscam += 1
            print('The Mail ' + os.path.basename('hamorscam/' + file) + ' is a Scam because of the following amount of scam words: ' + str(counter))
            ##print(resultlist)
            """if categoryB == 1 & categoryC == 1: 
                print('The Mail could not be categorized in one of the fraud categories.')
            if categoryC == 1 & categoryB == 0:
                print('Also the Mail is categorized as business fraud.')
            if categoryB == 1 & categoryC == 0:
                print('Also the Mail is categorized as charity fraud.')"""
        else: 
            hamlist.append(resultlist)
            frequencyham += 1 
            print('The Mail ' + os.path.basename('hamorscam/' + file) + ' is a Ham because only the following amount of words matches with the spam categorizer: ' + str(counter))
            ##print(resultlist)
    print('In Total we have an amount of ' + str(frequencyscam) + ' Scam Mails and ' + str(frequencyham) + ' Ham Mails.')
    print('The ratio of correct categorizing to incorrect is 17 to 9, so lies the accuracy of the model at 65,38%.')
    ##return hamlist, scamlist, frequencyham, frequencyscam
    