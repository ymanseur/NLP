# Yacine Manseur
# classifier.py

import argparse, math, sys
from nltk.tokenize import RegexpTokenizer


# Process Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-a", "--trainingSet", default="corpus1_train.labels", help="path to labelled training set")
ap.add_argument("-b", "--testSet", default="corpus1_test.list", help="path to unlabelled test set")
ap.add_argument("-c", "--outputFileName", default="corpus1_predictions.labels", help="name for output predictions set")
args = vars(ap.parse_args())

# access training set
inputTraining = open(args['trainingSet'], 'rb')

# initialize tokenizer and other variables used
alpha = 0.11
tokenizer = RegexpTokenizer(r'\w+')
categories = {} # list of categories and their frequency
categorySize = {} # number of words in each category
totalDocuments = 0 # number of total documents
dictionary = {} # frequency of every word overall
dictionarySize = 0 # size of entire dictionary
wordFrequency = {} # frequency of every word per category
probabilities = {} # probability for making prediction

# loop through training set
for document in inputTraining:

	# split up current line
	line = document.split()

	# add new categories
	category = line[1]
	if category not in categories:
		categories[category] = 0.0
		wordFrequency[category] = {}
		probabilities[category] = 0.0
		categorySize[category] = 0.0

	# open file and tokenize
	fileT = open(line[0], 'rb')
	text = tokenizer.tokenize(fileT.read())

	# loop through every token in the file
	for word in text:

		categorySize[category] += 1

		# clean word
		word = word.lower()

		# add word to global dictionary
		if word not in dictionary:
			dictionary[word] = 1
			dictionarySize += 1
		else:
			dictionary[word] += 1

		# update word frequency in wordFrequency{}
		if word not in wordFrequency[category]:
			wordFrequency[category][word] = alpha + 1
		else:
			wordFrequency[category][word] += 1

	# keep track of number of documents for each category and total documents
	categories[category] += 1
	totalDocuments += 1

	# close current document and move to the next one
	fileT.close()

# Done processing training documents
inputTraining.close()

# Access test set and open a prediction file
inputTest = open(args['testSet'], 'rb')
open(args['outputFileName'],'w').close() # delete contents of prediction file first
predictions = open(args['outputFileName'], 'wb')

# Loop through each document in the test set
for testDoc in inputTest:

	# Access the document
	testDoc = testDoc.split()[0]
	fileT = open(testDoc, 'rb')

	# Reset probabilities to zero
	for category in probabilities:
		probabilities[category] = 0.0

	# Tokenize the document
	text = tokenizer.tokenize(fileT.read())

	# Loop through every token in the file
	for word in text:

		# clean word
		word = word.lower()

		# Update probabilities
		for category in probabilities:
			if word in wordFrequency[category]:
				probabilities[category] += math.log( wordFrequency[category][word] / (categorySize[category] + alpha*dictionarySize) )
			else:
				probabilities[category] += math.log( alpha / (categorySize[category] + alpha*dictionarySize) )

	# Also consider probability based off of number of each type of category
	for category in probabilities:
		probabilities[category] += math.log( categories[category] / totalDocuments )

	# Done reading through document
	fileT.close()

	# Now to make a prediction
	highestProb = -sys.maxint - 1
	prediction = ""
	for category in probabilities:
		if probabilities[category] > highestProb:
			prediction = category
			highestProb = probabilities[category]

	predictions.write(testDoc + " " + prediction + "\n")

inputTest.close()
predictions.close()

exit()
