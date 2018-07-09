import sys
import markovify

modelFile = ''

limit = None

if(len(sys.argv) < 2):
    modelFile = input("Please enter a filename (with a .json extension)to read the text model from: ")
else:
    modelFile = sys.argv[1]

if(len(sys.argv) > 2):
    limit = sys.argv[2]

wftJsonModel = open(modelFile, 'r').read()

wftModel = markovify.Text.from_json(wftJsonModel)

userIn = ''

while(userIn != 'exit'):
    sentence = None
    while(sentence == None):
        if(limit):
            sentence = wftModel.make_short_sentence(limit)
        else:
            sentence = wftModel.make_sentence()
    print(sentence)
    userIn = input('Enter \'exit\' to exit or anything else to make another sentence: ')