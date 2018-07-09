import markovify
import sys

fileName = ''
corpusFileName = ''

if(len(sys.argv) < 2):
    corpusFileName = input("Please enter a filename with an extension to read the text from: ")
else:
    corpusFileName = sys.argv[1]

if(len(sys.argv) < 3):
    fileName = input("Please enter a filename (with a .json extension) to write the text model to: ")
else:
    fileName = sys.argv[2]

with open(corpusFileName, 'r') as corpusFile:
    corpus = corpusFile.read()

wftModel = markovify.Text(corpus)

wftModelJson = wftModel.to_json()

with open(fileName, 'w+') as f:
    f.write(wftModelJson)
