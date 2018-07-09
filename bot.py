import praw
import markovify
import sys
import re
import os
import json
import time
import ast

wftWeaponTitleModelFile = ''
wftWeaponDescModelFile = ''

if(len(sys.argv) < 2):
    wftWeaponTitleModelFile = input(
        "Please enter a filename (with a .json extension)to read the text model for weapon titles from: ")
else:
    wftWeaponTitleModelFile = sys.argv[1]

if(len(sys.argv) < 3):
    wftWeaponDescModelFile = input(
        "Please enter a filename (with a .json extension)to read the text model for weapon flavors from: ")
else:
    wftWeaponDescModelFile = sys.argv[2]

wftWeaponTitleJsonModel = open(wftWeaponTitleModelFile, 'r').read()
wftWeaponTitleModel = markovify.Text.from_json(wftWeaponTitleJsonModel)
wftWeaponDescJsonModel = open(wftWeaponDescModelFile, 'r').read()
wftWeaponDescModel = markovify.Text.from_json(wftWeaponDescJsonModel)

reddit = praw.Reddit('DestinyFlavorTextSim')
subredditNames = ['HellerBotTest']

postsAlreadyRepliedTo = []

if(os.path.isfile('posts_already_replied_to.txt')):
    postsText = open('posts_already_replied_to.txt', 'r').read()
    postJsonTextList = postsText.split(';')
    for postJsonText in postJsonTextList:
        postsAlreadyRepliedTo.append(ast.literal_eval(postJsonText))
    print(postsAlreadyRepliedTo)

def replyToPost(post):
    print('Replying to post: ' + str(post.id))
    #weaponTitle = None
    weaponDesc = None
    while((weaponDesc == None)):
        #weaponTitle = wftWeaponTitleModel.make_short_sentence(25, tries = 100)
        weaponDesc = wftWeaponDescModel.make_short_sentence(
            100, tries=100)

    botReplyFooter = '\r\n\r\n ------- Beep Bop, I am a bot ------- \r\n\r\nCreator: /u/HellerChigs \r\n\r\nSource: [DestinyFlavorTextSim](https://github.com/phulsechinmay)\r\n\r\nDownvote to remove.'
    botReply = '#### Here is a custom weapon description for you: \r\n\r\n>' + \
        weaponDesc + botReplyFooter
    comment = post.reply(botReply)

    postJson = {
        "id": post.id,
        "commentID": comment.id
    }
    postsAlreadyRepliedTo.append(postJson)
    writeToFile()

def writeToFile():
    with open('posts_already_replied_to.txt', 'w+') as f:
        for (i,postJson) in enumerate(postsAlreadyRepliedTo):
                f.write(str(postJson))
                if(i != (len(postsAlreadyRepliedTo) - 1)):
                    f.write(';')
        
def runBot():
    while(True):
        for subredditName in subredditNames:
            subreddit = reddit.subreddit(subredditName)
            for post in subreddit.hot(limit=5):
                if(len(postsAlreadyRepliedTo) < 1):
                    searchText = post.selftext + ' ' + post.title
                    if('+wfts' in searchText):
                        replyToPost(post)
                else:
                    if(not (post.id in [postJSON['id'] for postJSON in postsAlreadyRepliedTo])):
                        searchText = post.selftext + ' ' + post.title
                        if('+wfts' in searchText):
                            replyToPost(post)

while(True):
    try:
        runBot()
    except praw.exceptions.APIException as e:
        print("An exception occured " + str(e))
        minutesToSleep = 10
        if('you are doing that too much' in str(e)):
            minutesToSleep = int(str(e)[54])
        print('Sleeping for ' + str(minutesToSleep) + ' minutes')
        time.sleep(minutesToSleep * 60)
    

