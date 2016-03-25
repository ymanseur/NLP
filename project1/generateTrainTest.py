# Yacine Manseur
# Split input list into training and test set

import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input")
args = vars(ap.parse_args())

inputfile = open(args['input'], 'rb')

train = "generatedTrain.labels"
test = "generatedTest.list"
correct = "generatedTest.labels"

trainF = open(train, 'wb')
testF = open(test, 'wb')
correctF = open(correct, 'wb')

count = 2

for temp in inputfile:
	line = temp.split()
	if count % 2 == 0: #create training file
		trainF.write(line[0] + " " + line[1] + "\n")
	else:
		testF.write(line[0] + "\n")
		correctF.write(line[0] + " " + line[1] + "\n")
	count += 1

inputfile.close()
trainF.close()
testF.close()
correctF.close()