# Yacine Manseur
# train.py

import argparse
from nltk.tokenize import RegexpTokenizer

def processArguments():
	ap = argparse.ArgumentParser()
	ap.add_argument("-l", "--trainingSet", help="path to labelled training set")
	ap.add_argument("-o", "--testSet", help="parth to unlabelled test set")
	args = vars(ap.parse_args())




def main():
	processArguments()


if __name__ == "__main__":
	main()