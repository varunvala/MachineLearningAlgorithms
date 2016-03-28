'''
Created on Dec 7, 2015

@author: Varun
'''
import math
from collections import Counter
class DecisionTree(object):
    def __init__(self,feature=None,childNodes=None):
        self.feature = feature
        self.childNodes = {}
        

def answerValuesSplitRatio(data):
    answers = []
    for dataElement in data:
        answers.append(dataElement[1])
    
    tempdict = Counter(answers)
    sum = 0
    for k,v in tempdict.items():
        sum += v
    answerValuesSplit = []
    for k,v in tempdict.items():
        answerValuesSplit.append(float(v)/sum)
    
    #print answerValuesSplit
    return answerValuesSplit

def integer_informationGain(data,index):
    dataSize = len(data)
    listOfIntegers = [dataElement[0][index] for dataElement in data]
    minValue = min(listOfIntegers)
    maxValue = max(listOfIntegers)
    midValue = float(float(minValue) + float(maxValue))/2
    #print ("listOfIntegers and index are::  ",index," ", listOfIntegers)
    
    #print ("dataSize is: ",dataSize, " and data is: ",data)
    
    subSets = splitDataSubSets_IntegerOrFloat(data, index, str(midValue))
    initialEntropy = entropy(data)
    subSetEntropies = 0
    for subSet in subSets:
        subSetSize = len(subSet)
        subSetEntropies += (float(subSetSize*entropy(subSet))/dataSize)
        #print ("subSetEntropies is::: ",subSetEntropies)
    finalEntropy = initialEntropy - subSetEntropies
    return finalEntropy
    
def float_informationGain(data,index):
    dataSize = len(data)
    listOfFloats = [dataElement[0][index] for dataElement in data]
    minValue = min(listOfFloats)
    maxValue = max(listOfFloats)
    print("min and max are: ",minValue," ",maxValue)
    midValue = float(float(minValue) + float(maxValue))/2
    #print ("listOfFloats and index are::  ",index," ", listOfFloats)
    
    #print ("dataSize is: ",dataSize, " and data is: ",data)
    
    subSets = splitDataSubSets_IntegerOrFloat(data, index, str(midValue))
    initialEntropy = entropy(data)
    subSetEntropies = 0
    for subSet in subSets:
        subSetSize = len(subSet)
        subSetEntropies += (float(subSetSize*entropy(subSet))/dataSize)
        #print ("subSetEntropies is::: ",subSetEntropies)
    finalEntropy = initialEntropy - subSetEntropies
    return finalEntropy
    
    
def informationGain(data,index):
    index = 1
    dataSize = len(data)
    #print ("dataSize is: ",dataSize, " and data is: ",data)
    subSets = splitDataSubSets(data, index)
    initialEntropy = entropy(data)
    subSetEntropies = 0
    for subSet in subSets:
        subSetSize = len(subSet)
        subSetEntropies += (float(subSetSize*entropy(subSet))/dataSize)
        #print ("subSetEntropies is::: ",subSetEntropies)
    finalEntropy = initialEntropy - subSetEntropies
    return finalEntropy

def entropy(data):
    listOfDistribution = answerValuesSplitRatio(data)
    entropyValue = 0
    for listValue in listOfDistribution:
        entropyValue -= (listValue)*(math.log(listValue,2))
    #print entropyValue
    return entropyValue

"""def splitDataSubSets_IntegerOrFloat_backup(data,index,max):
    listOfIntegers = [dataElement[0][index] for dataElement in data]
    maxValueList = max(listOfIntegers)
    minValueList = min(listOfIntegers)
    intervalValue = float(maxValueList - minValueList)/5
    
    possibleFeatureValues = []
    for dataElement in data:
        possibleFeatureValues.append(dataElement[0][index])
    possibleFeatureValues = list(set(possibleFeatureValues))
    
    subSets = []
        
    for i in len(range(1,6)):
        subSet_Integer = []
        min_value = minValueList
        max_value = (min_value + (i*intervalValue))
        for dataElement in data:
            if ((dataElement[0][index] >= min_value):
                subSet_Integer1.append(dataElement)
        subSets.append(subSet_Integer1)
        
    print("afsdf")"""

def splitDataSubSets_IntegerOrFloat(data,index,mid):

    subSets = []
        
    #for featureValue in possibleFeatureValues:
    subSet_Integer1 = []
    for dataElement in data:
        #dataElement[0][index] = '00519'
        #mid = '490.0'
        print ("mid and dataElemet are::: ", mid," ",dataElement[0][index])
        print float(dataElement[0][index]) <= float(mid)
        if (float(dataElement[0][index]) <= float(mid)):
            print("111111111111")
            subSet_Integer1.append(dataElement)
    subSets.append(subSet_Integer1)
        
    #for featureValue in possibleFeatureValues:
    subSet_Integer2 = []
    for dataElement in data:
        if (float(dataElement[0][index]) > float(mid)):
            print("22222222222")
            subSet_Integer2.append(dataElement)
    subSets.append(subSet_Integer2)
    
    print subSets
    return subSets

def splitDataSubSets(data,index):
    possibleFeatureValues = []
    for dataElement in data:
        possibleFeatureValues.append(dataElement[0][index])
    possibleFeatureValues = list(set(possibleFeatureValues))
    
    #print possibleFeatureValues
    
    subSets = []
        
    for featureValue in possibleFeatureValues:
        SmallsubSetForMainSubSet = []
        for dataElement in data:
            if dataElement[0][index] == featureValue :
                SmallsubSetForMainSubSet.append(dataElement)
        subSets.append(SmallsubSetForMainSubSet)
    
    return subSets

def dataTypeDecider_IG_Dispatcher(data,index):
    dataTpyeOnCheck = None
    typeCheckValue = data[0][0][index]
    #print ("typeCheckValue and index are:: ",index," ",typeCheckValue)
    
    try:
        dataTpyeOnCheck = float(typeCheckValue)
    except ValueError:
        try:
            dataTpyeOnCheck = int(typeCheckValue)
        except ValueError:
            return informationGain(data, index)
        else:
            return integer_informationGain(data,index)
    else:
        return float_informationGain(data,index)

        
def sameLabelForAllData(features,data):
    answers = []
    uniqueAnswers = []
    for dataElement in data:
        answers.append(dataElement[1])
    uniqueAnswers = list(set(answers))
    if((len(uniqueAnswers)==1) and len(answers) > 1):
        return True   
    
    
def DecisionTreeBuild(features,data):
    bestSplitLocation = None
    bestGain = float('-Inf')
    listofGains = []
    count = {}
    
    if ((len(features)==0) or (len(data)==0)):
        answers = []
        uniqueAnswers = []
        for dataElement in data:
            answers.append(dataElement[1])
        uniqueAnswers = list(set(answers))
        for eachAnswer in uniqueAnswers:
            count[eachAnswer] = 0
        
        for eachAnswer in uniqueAnswers:
            for dataElement in data:
                if dataElement[1] == eachAnswer:
                    count[eachAnswer] += 1
        #sorted(count.items(), key = lambda t : t[1])
        maxLabel = max(count, key=count.get)
        #print ("count is::: ",count," and maxLabel is:: ",maxLabel)
        """count[0][0]
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print set(count)"""
        return DecisionTree(maxLabel,None)
    elif (sameLabelForAllData(features,data)):
        #return data[0][1]
        return DecisionTree(data[0][1],None)
    else:
        for eachFeature in features:
            gainAtFeature = dataTypeDecider_IG_Dispatcher(data, eachFeature)  
            listofGains.append(gainAtFeature)
            if gainAtFeature > bestGain:
                bestSplitLocation = eachFeature
                bestGain = gainAtFeature
                
        """print ("listofGains is: ",listofGains)
        print ("bestFeature is: ",bestFeature)"""
        
        #print gainAtFeature
        #print listofGains
        
        rootNode = DecisionTree(None,None)
        rootNode.feature = bestSplitLocation
        #print("featureValues before::: ",features)
        features.remove(bestSplitLocation)
        #print("featureValues after::: ",features)
        for subSetGenerated in splitDataSubSets(data, bestSplitLocation):
            featureValueGoingToChild = subSetGenerated[0][0][bestSplitLocation]
            #print("featureValues after::: ",features)
            childNode = DecisionTreeBuild(features, subSetGenerated)
            rootNode.childNodes[featureValueGoingToChild] = childNode
        
        return rootNode   
    
def classifyData(RootNode,eachElement):
    #print("RootNode is::: ",RootNode)
    answer = None
    if(len(RootNode.childNodes)==0):
        #print("Hereeeee")
        #print RootNode.childNodes
        #print RootNode.feature
        return RootNode.feature
    else:
        rootFeature = RootNode.feature
        children = RootNode.childNodes
        #print("children are::: ",children)
        for child in children.keys():
            if(child == eachElement[0][rootFeature]):
                answer = classifyData(children[child], eachElement)
    return answer        


def testAccuracyDecisionTree(RootNode):
    inputFile = open('crx.data_backup_Test.txt')
    allLines = inputFile.readlines()
    
    testingData = []
    for eachLine in allLines:
        eachLine = eachLine.rstrip().split(',')
        testingData.append([eachLine[0:14],eachLine[15]])
    
    fullData = []
    missingData = []
    for data in testingData:
        if '?' not in data[0]:
            fullData.append(data)
            #print fullData
        else:
            missingData.append(data)
            
    possibleFeatureValues = []
    for dataElement in fullData:
        possibleFeatureValues.append(dataElement[0][index])
    possibleFeatureValues = list(set(possibleFeatureValues))        
    
    actualValue = fullData[0][1]
    features = fullData[0][0]
    print("*************************************")
    count = 0
    records = 0
    for eachElement in fullData:
        records += 1
        answerReturned = classifyData(RootNode,eachElement)
        actualAnswer = eachElement[1]
        print("answerReturned and actualAnswer are::: ",answerReturned," ",actualAnswer)
        if(answerReturned == actualAnswer):
            count += 1
    accuracyLevelDecisionTree = float(count)/records
    print("accuracyLevelDecisionTree::: ",accuracyLevelDecisionTree)
        
    
   
if __name__ == '__main__':
    """stringHere = 'b'
    print type(stringHere)
    stringNotHere = 23.42
    print type(stringNotHere)
    stringIntegerHere = 24
    print type(stringIntegerHere)
    
    IntType
    StrType
    FloatType"""
    
    #inputFile = open('crx.data.txt')
    inputFile = open('crx.data_backup_Training.txt')
    allLines = inputFile.readlines()
    
    trainingData = []
    for eachLine in allLines:
        eachLine = eachLine.rstrip().split(',')
        trainingData.append([eachLine[0:14],eachLine[15]])
    
    missingValueHandling = []  
    for eachLine in allLines:
        eachLine = eachLine.rstrip().split(',')
        missingValueHandling.append([eachLine[15],eachLine[0:14]])
        
    fullData = []
    missingData = []
    for data in trainingData:
        if '?' not in data[0]:
            fullData.append(data)
            #print fullData
        else:
            missingData.append(data)
            #print missingData
    #print missingData
    
    
    """#print fullData
       #print fullData[0]
       #print fullData[0][0]
    """
    """print fullData
    print fullData[0]
    print type(fullData[0][0][0])"""
    
    answerValuesSplitRatio(fullData)
    entropy(fullData)
    informationGains = []
    for index in range(len(fullData[0][0])):
        informationGains.append(informationGain(fullData, index))
    #print informationGains
    #informationGain(fullData,0)
    
    returnedRootNode = DecisionTreeBuild(list(set(range(len(fullData[0][0])))),fullData)
    #print returnedRootNode.childNodes
    
    testAccuracyDecisionTree(returnedRootNode)