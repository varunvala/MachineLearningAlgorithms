'''
Created on Dec 10, 2015

@author: Varun
'''
import math
digitDictionary = {}
digitDictionary_testingData = {}
labelDictionary = {}
labelDictionary_testing = {}
priorDistributionsDict = {}
LocationClassCountDictListWhiteFeature = []
LocationClassCountDictListGrayFeature = []
LocationClassCountDictListBlackFeature = []
ConditionalProbabilityWhiteFeature = []
ConditionalProbabilityGrayFeature = []
ConditionalProbabilityBlackFeature = []
classifyResultsDict = {} 


def makePriorDistributions():
    global labelDictionary, priorDistributionsDict
    priorDistributionsDict = dict.fromkeys(priorDistributionsDict,0)
    
    for i in range(1,5001):
        priorDistributionsDict[str(labelDictionary.get(i))] = 0
    
    for i in range(1,5001):
        priorDistributionsDict[str(labelDictionary.get(i))] += 1

    """for k,v in priorDistributionsDict.items():
        print k,v"""
    
    for i in range(10):
        priorDistributionsDict[str(i)] = float(priorDistributionsDict[str(i)])/5000
    
    """for k,v in priorDistributionsDict.items():
        print k,v"""
        
def makeLocationLabelCountList():
    global labelDictionary, priorDistributionsDict, digitDictionary
    
    for location in range(783):
        tempDict = {}
        for i in range(1,5001):
            tempDict[str(labelDictionary.get(i))] = 0
        for i in range(1,5001):
            if digitDictionary[i][location] == '':
                tempDict[str(labelDictionary.get(i))] += 1
        LocationClassCountDictListWhiteFeature.append(tempDict)
    
    for location in range(783):
        tempDict = {}
        for i in range(1,5001):
            tempDict[str(labelDictionary.get(i))] = 0
        for i in range(1,5001):
            if digitDictionary[i][location] == '+':
                tempDict[str(labelDictionary.get(i))] += 1
        LocationClassCountDictListGrayFeature.append(tempDict)
        
    for location in range(783):
        tempDict = {}
        for i in range(1,5001):
            tempDict[str(labelDictionary.get(i))] = 0
        for i in range(1,5001):
            if digitDictionary[i][location] == '#':
                tempDict[str(labelDictionary.get(i))] += 1
        LocationClassCountDictListBlackFeature.append(tempDict)
            
    """print ("LocationClassCountDictListWhiteFeature:: ",LocationClassCountDictListWhiteFeature)
    print ("LocationClassCountDictListGrayFeature:: ",LocationClassCountDictListGrayFeature)
    print ("LocationClassCountDictListBlackFeature:: ",LocationClassCountDictListBlackFeature)"""


        
def readTestingData():
    inputFile = open('testimages.txt')
    allLines = inputFile.readlines()
    testingData = []
   
    i = 1
    totalDigits_testingData = 1000
    digitNumber_testingData = 1
    arrayForDigit_testingData = []
    
    
    for eachLine in allLines:
        if(i<28):
            j = 1
            while (j<28):
                for eachCharacter in eachLine:
                    arrayForDigit_testingData.append(eachCharacter)
                    j += 1
            i += 1
        else:
            arrayForDigit_testingData = map(str.strip,arrayForDigit_testingData)
            digitDictionary_testingData[digitNumber_testingData] = arrayForDigit_testingData
            arrayForDigit_testingData = []
            i = 1
            digitNumber_testingData += 1
            
    
    inputFile_testingLables = open('testlabels.txt')
    allLabelLines_testing = inputFile_testingLables.readlines()
    
    labelnumber_testing = 1
    for eachlabelLine in allLabelLines_testing:
        eachlabelLine = eachlabelLine.rstrip()
        labelDictionary_testing[labelnumber_testing] = eachlabelLine
        labelnumber_testing += 1

def logCalculateForFeaturesGivenLabel(label,list):
    global ConditionalProbabilityWhiteFeature,ConditionalProbabilityGrayFeature,ConditionalProbabilityBlackFeature
    i = 0
    value  = 0
    value1 = 0
    value2 = 0
    value3 = 0
    sameLabelCountForLocation = 0

    for eachFeature in list:
        
        featureCountForLocationforLabel = 0
        sameLabelCountForLocation = (priorDistributionsDict[str(label)]*5000)+2
        
        if eachFeature == '':
            featureCountForLocationforLabel = LocationClassCountDictListWhiteFeature[i].get(str(label))+2
            value1 += math.log10(float(featureCountForLocationforLabel/sameLabelCountForLocation))
        elif eachFeature == '+':
            featureCountForLocationforLabel = LocationClassCountDictListGrayFeature[i].get(str(label))+2
            value2 += math.log10(float(featureCountForLocationforLabel/sameLabelCountForLocation))
        elif eachFeature == '#' :
            featureCountForLocationforLabel = LocationClassCountDictListBlackFeature[i].get(str(label))+2
            value3 += math.log10(float(featureCountForLocationforLabel/sameLabelCountForLocation))
            
        i += 1
        
    return (value1 + value2 + value3)
        
        
def classifyTestingData():
    global digitDictionary_testingData,priorDistributionsDict
    sampleNumber = 1
    classifiedLable = 0
    
    for i in range(1,1001):
        eachList = digitDictionary_testingData.get(i)
        tempDict = {}
        sortedList = []
        for eachLabel in range(10):
            priorProbabilityForLabel = math.log10(priorDistributionsDict[str(eachLabel)])
            value = logCalculateForFeaturesGivenLabel(eachLabel,eachList)
            tempDict[str(eachLabel)] = value + priorProbabilityForLabel 
        classifiedLable = max(tempDict, key=tempDict.get)
        
        classifyResultsDict[str(sampleNumber)] = int(classifiedLable)
        sampleNumber += 1
            
def readTrainingData():
    inputFile = open('trainingimages.txt')
    allLines = inputFile.readlines()
    trainingData = []
   
    i = 1
    totalDigits = 5000
    digitNumber = 1
    arrayForDigit = []
    
    for eachLine in allLines:
        if(i<28):
            j = 1
            while (j<28):
                for eachCharacter in eachLine:
                    arrayForDigit.append(eachCharacter)
                    j += 1
            i += 1
        else:
            arrayForDigit = map(str.strip,arrayForDigit)
            digitDictionary[digitNumber] = arrayForDigit
            arrayForDigit = []
            i = 1
            digitNumber += 1
    
    """for i in range(1,5001):
        print len(digitDictionary.get(i))"""
    
    inputFile_trainingLables = open('traininglabels.txt')
    allLabelLines = inputFile_trainingLables.readlines()
    
    labelnumber = 1
    for eachlabelLine in allLabelLines:
        eachlabelLine = eachlabelLine.rstrip()
        labelDictionary[labelnumber] = eachlabelLine
        labelnumber += 1
    
 
def calculateAccuracy():
    matchingCount = 0
    for i in range(1,1001):
        print ("^^^^^^") 
        print (labelDictionary_testing.get(i))
        print (classifyResultsDict[str(i)])                               
        if (int(labelDictionary_testing.get(i)) == int(classifyResultsDict[str(i)])):
            matchingCount += 1
    print("matchingCount is::: ",matchingCount)
    print (float(matchingCount)/1000)*100

if __name__ == '__main__':
    
    readTrainingData()
    
    makePriorDistributions()
    makeLocationLabelCountList()
    
    readTestingData()
    
    classifyTestingData()
    
    print classifyResultsDict
    
    print ("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    
    calculateAccuracy()
    
    print ("_______________________________________________________________________________")