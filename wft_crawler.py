from requests import get
from bs4 import BeautifulSoup
import sys
import re

fileName = ''

weaponFlavorTexts = []
weaponTitles = []

dismissedFlavorTexts = ['An Awoken gift from the Reef, marked with the Queen\'s crown.', 'A prestigious trophy earned in battle during the Trials of Osiris.', 'Executor-issued sidearm for loyal supporters of the New Monarchy.', 'A sharpshooter\'s weapon forged in fire by the Lords of the Iron Banner.', 'An elite trophy earned only by Trials of Osiris champions.', 'A prestigious trophy earned in battle during the Trials of Osiris.', 'A common engram. A cryptarch can decode this into a weapon.', 'An engram with remarkable but familiar markers. A Cryptarch would be pleased to decode it.', 'An encrypted matter engram of unusual properties. The Cryptarch can decrypt this into a primary weapon.', 'A matter engram of remarkable potency. The Cryptarch can decrypt this into a primary weapon.', 'The Cryptarch in the Tower may be able to decrypt this object and reveal its contents.', 'A rare engram with unusual markers. A cryptarch should be able to decode this into a weapon.', 'An engram with complex markers. A cryptarch should be able to decode this into a weapon.', 'An engram with remarkable encoding markers. A cryptarch would be thrilled to decode it into a weapon.', 'An encrypted matter engram of unusual properties. The Cryptarch can decrypt this into a special weapon.', 'A matter engram of remarkable potency. The Cryptarch can decrypt this into a special weapon.', 'An encrypted matter engram of unusual properties. The Cryptarch can decrypt this into a heavy weapon.', 'A matter engram of remarkable potency. The Cryptarch can decrypt this into a heavy weapon.', 'A personal firearm, forged in fire by the Lords of the Iron Banner.', 'Executor-issued personal firearm for loyal supporters of the New Monarchy.', 'A personal firearm, augmented, named and sanctified by the leaders of the Future War Cult.', 'A personal firearm, named and sanctified by the leaders of the Future War Cult.', 'A personal firearm modified by Dead Orbit\'s superb technicians and specialists.', 'A personal firearm, named and sanctified by the Future War Cult\'s leaders.', 'Executor-issued personal firearm, for loyal supporters of the New Monarchy.']

dismissedWords = ['New Monarchy', 'Future War Cult', 'Executor', 'Dead Orbit', 'Iron Banner', 'glory in the Crucible', 'Vanguard-issue']

def checkValidity(weaponDescription):
    if(weaponDescription in dismissedFlavorTexts):
        return False
    else:
        for dismissedWord in dismissedWords:
            if(dismissedWord in weaponDescription):
                return False
    return True

def GetD2WFT():
    mainBaseUrl = 'https://db.destinytracker.com/d2/en/items/weapon?t=6&t=5&t=4&t=3'
    baseUrl = 'https://db.destinytracker.com'
    weaponPageUrls = []
    weaponSearchUrls = []

    for x in range(1,21):
        weaponSearchUrls.append(mainBaseUrl + '&page=' + str(x))

    for weaponSearchUrl in weaponSearchUrls:
        weaponSearchResponse = get(weaponSearchUrl)
        weaponSearchText = weaponSearchResponse.text

        htmlText = BeautifulSoup(weaponSearchText, 'html.parser')

        weaponTagsOnPage = htmlText.find_all('a', class_ = 'td-link')

        for weaponATag in weaponTagsOnPage:
            weaponPageUrls.append(baseUrl + weaponATag['href'])

    for weaponPageUrl in weaponPageUrls:
        weaponPageResponse = get(weaponPageUrl)
        weaponPageText = weaponPageResponse.text

        weaponsHtmlText = BeautifulSoup(weaponPageText, 'html.parser')

        weaponDescriptionList = weaponsHtmlText.find_all('p', class_ = 'item-description')
        weaponTitleDivList = weaponsHtmlText.find_all('div', class_ = 'item-details')

        weaponDescription = weaponDescriptionList[0].string
        weaponTitle = weaponTitleDivList[0].h1.string

        weaponTitles.append(weaponTitle)

        '''
        for c in '\'\"[]()':
            weaponDescription = weaponDescription.replace(c, '')
        #weaponDescription = re.sub('[[]()\'\"]', '', weaponDescription)
        #weaponDescription = weaponDescription.translate(None, '()[]\"\'')
        '''
        if(checkValidity(weaponDescription)):
            weaponFlavorTexts.append(weaponDescription)

def GetD1WFT():
    mainBaseUrl = 'https://db.destinytracker.com/d1/items/' #primary-weapons?page=1&tier=30' 1-13 1-10 1-6
    baseUrl = 'https://db.destinytracker.com'
    weaponTypes = ['primary-weapons', 'special-weapons', 'heavy-weapons']
    tier = 'tier=30'
    pageRanges = [range(1,14), range(1,11), range(1,7)]
    weaponPageUrls = []
    weaponSearchUrls = []

    for (i, weaponType) in enumerate(weaponTypes):
        pageRange = pageRanges[i]
        for pageNum in pageRange:
            weaponSearchUrls.append(mainBaseUrl + weaponType + '?page=' + str(pageNum) + '&' + tier)

    for weaponSearchUrl in weaponSearchUrls:
        weaponSearchResponse = get(weaponSearchUrl)
        weaponSearchText = weaponSearchResponse.text

        htmlText = BeautifulSoup(weaponSearchText, 'html.parser')

        weaponTagsOnPage = htmlText.find_all('a', class_ = 'tier-color')
        
        for weaponATag in weaponTagsOnPage:
            weaponPageUrls.append(baseUrl + weaponATag['href'])

    for weaponPageUrl in weaponPageUrls:
        weaponPageResponse = get(weaponPageUrl)
        weaponPageText = weaponPageResponse.text

        weaponsHtmlText = BeautifulSoup(weaponPageText, 'html.parser')

        weaponDescriptionList = weaponsHtmlText.find_all('div', class_ = 'title-container')

        weaponDescription = weaponDescriptionList[0].p.string
        weaponTitle = weaponDescriptionList[0].h1.string

        weaponTitles.append(weaponTitle)

        if(checkValidity(weaponDescription)):
            weaponFlavorTexts.append(weaponDescription)

        

def main():
    if(len(sys.argv) < 2):
        fileName = input("Please enter a filename without an extension to write the text: ")
    else:
        fileName = sys.argv[1]

    titleFile = fileName + '-titles.txt'
    flavorFile = fileName + '-flavor.txt'

    GetD1WFT()
    GetD2WFT()
    
    print("Finished crawling")

    # Write to files
    with open(flavorFile, "w+") as f:
        for flavorText in weaponFlavorTexts:
            f.write(flavorText)
            f.write('\n')

    with open(titleFile, "w+") as f:
        for titleText in weaponTitles:
            f.write(titleText)
            f.write('\n')

    print("Finished writing the file")
    

if __name__ == "__main__":
    main()
