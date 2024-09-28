import datetime

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
    start_time = datetime.datetime.now()

    testData = testDataPrepatory.getTestTupleList()
    test_data_preparation_time = datetime.datetime.now() - start_time
    print("Test data preparation time: ", test_data_preparation_time)

    tradeList = generateTradeList(testData)
    tradeList_time = datetime.datetime.now() - test_data_preparation_time
    print("TradeList preparation time: ", tradeList_time)

    readableTradeList = tradeMaker.makeReadableTradeList(tradeList)
    readableTradeList_time = datetime.datetime.now() - tradeList_time
    print("ReadableTradeList preparation time: ", readableTradeList_time)

    controlledTradeList = tradeMaker.controlTradeList(readableTradeList)
    controlledTradeList_time = datetime.datetime.now() - readableTradeList_time
    print("ControlledTradeList preparation time: ", controlledTradeList_time)


    print("winningTradeCount: ", tradeMaker.winningTradeCount(controlledTradeList) , "  winningTradeRate: %",
          100*tradeMaker.winningTradeCount(controlledTradeList) / len(controlledTradeList)  )
    print("losingTradeCount: ", tradeMaker.losingTradeCount(controlledTradeList) , "  losingTradeRate: %",  100*tradeMaker.losingTradeCount(controlledTradeList) / len(controlledTradeList) )

    tradeMaker.printTradeList(controlledTradeList)
    printTradeList_time = datetime.datetime.now() - controlledTradeList_time
    print("PrintTradeList preparation time: ", printTradeList_time)

    print("TradeList ready total time: ", datetime.datetime.now() - start_time)