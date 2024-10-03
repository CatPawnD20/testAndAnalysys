import datetime

import config
from testScripts import testDataPrepatory, tradeMaker



def calculate_reset_money(testData):
    reset_money_trade_dict = {}
    for trade in testData:
        date = trade[1]
        month = date.month
        if month in reset_money_trade_dict:
            # Mevcut tarihle karşılaştırıp daha erken olanı seçiyoruz
            if date < reset_money_trade_dict[month]:
                reset_money_trade_dict[month] = date
        else:
            reset_money_trade_dict[month] = date
    return reset_money_trade_dict



def generateTradeList(testDataList):
    global reset_for_month
    if config.monthly_test:
        tradeList = []
        reset_money_trade_dict = calculate_reset_money(testDataList)
        for testData in testDataList:
            if testData[1] in reset_money_trade_dict.values():
                reset_for_month = True
            trade = tradeMaker.makeTrade(testData)
            reset_for_month = False
            tradeList.append(trade)
            if tradeMaker.before_cash_global == 0 and tradeMaker.before_bitcoin_global == 0:
                # stop the test if the cash and bitcoin are 0
                break
        tradeMaker.before_cash_global = 0
        tradeMaker.before_bitcoin_global = 0
        return tradeList
    else:
        tradeList = []
        for testData in testDataList:
            trade = tradeMaker.makeTrade(testData)
            tradeList.append(trade)
            if tradeMaker.before_cash_global == 0 and tradeMaker.before_bitcoin_global == 0:
                # stop the test if the cash and bitcoin are 0
                break
        tradeMaker.before_cash_global = 0
        tradeMaker.before_bitcoin_global = 0
        return tradeList

def get_reset_for_month():
    return reset_for_month


def doTest():

    testData = testDataPrepatory.getTestTupleList()

    tradeList = generateTradeList(testData)

    readableTradeList = tradeMaker.makeReadableTradeList(tradeList)

    controlledTradeList = tradeMaker.controlTradeList(readableTradeList)

    tradeMaker.printTradeList(controlledTradeList)

    return controlledTradeList

