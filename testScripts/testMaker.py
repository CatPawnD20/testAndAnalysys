from testScripts import testDataPrepatory, tradeMaker


def generateTradeList(testDataList):
    #do one trade for each testData from testDataList
    tradeList = []
    for testData in testDataList:
        trade = tradeMaker.makeTrade(testData)
        tradeList.append(trade)
        if tradeMaker.before_cash == 0 and tradeMaker.before_bitcoin == 0:
            #stop the test if the cash and bitcoin are 0
            break
    return tradeList


def doTest():
    testData = testDataPrepatory.getTestTupleList()
    tradeList = generateTradeList(testData)
    readableTradeList = tradeMaker.makeReadableTradeList(tradeList)
    controlledTradeList = tradeMaker.controlTradeList(readableTradeList)
    print("TradeList")
    tradeMaker.printTradeList(controlledTradeList)