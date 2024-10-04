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


def calculate_gradual_take_profit_list(take_profit_rate, gradual_take_profit_pace):
    # calculate remain profit with
    remain_profit = take_profit_rate % gradual_take_profit_pace
    # calculate how many steps will be taken
    step_count = take_profit_rate // gradual_take_profit_pace
    step_count = int(step_count)
    # calculate gradual take profit list
    gradual_take_profit_list = []
    for i in range(step_count):
        gradual_take_profit_list.append(gradual_take_profit_pace)
    if remain_profit != 0:
        gradual_take_profit_list.append(remain_profit)
    return gradual_take_profit_list


def genaratetaken_profit_list(gradual_take_profit_list, trade, trade_profit):
    trade_taken_profit = trade_profit
    taken_profit_list = []
    for gradual_take_profit in gradual_take_profit_list:
        trade_taken_profit = trade_taken_profit - gradual_take_profit
        if trade_taken_profit >= 0:
            taken_profit_list.append(gradual_take_profit)
        else:
            return taken_profit_list
    return taken_profit_list



def generate_test_data_list_with_gradual_take_profit(testData, gradual_take_profit_list, trade, trade_profit):
    test_data_list = []
    taken_profit_list = genaratetaken_profit_list(gradual_take_profit_list, trade, trade_profit)
    print(taken_profit_list)
    for gradual_take_profit in gradual_take_profit_list:

        test_data = list(trade)
        test_data[10] = gradual_take_profit
        test_data_list.append(test_data)
    return test_data_list


def calculate_trade_profit(trade):
    if config.use_leverage:
        trade_profit = (float(trade[10]) - 1) / config.leverage_rate
        #round up to 4 decimal places
        trade_profit = round(trade_profit, 4)
    else:
        trade_profit = float(trade[10]) - 1
        trade_profit = round(trade_profit, 4)
    return trade_profit


def make_fresh_trades(testData):
    fresh_trade_list = []
    trade = tradeMaker.makeTrade(testData)
    take_profit_rate = config.take_profit_rate

    if not config.gradual_take_profit:
        fresh_trade_list.append(trade)
        return fresh_trade_list
    if float(trade[10]) < 0:
        fresh_trade_list.append(trade)
        return fresh_trade_list
    trade_profit = calculate_trade_profit(trade)
    gradual_take_profit_pace = config.gradual_take_profit_pace
    gradual_take_profit_list = calculate_gradual_take_profit_list(take_profit_rate, gradual_take_profit_pace)

    if trade_profit < gradual_take_profit_pace:  # if trade profit is less than gradual take profit pace
        fresh_trade_list.append(trade)
        return fresh_trade_list # win below gradual take profit

    # make test_data_list for gradual take profit
    test_data_list = generate_test_data_list_with_gradual_take_profit(testData, gradual_take_profit_list, trade, trade_profit)







def add_fresh_trade_list_to_trade_list(fresh_trade_list, tradeList):
    for fresh_trade in fresh_trade_list:
        tradeList.append(fresh_trade)
    return tradeList


def generateTradeList(testDataList):
    global reset_for_month
    reset_for_month = False
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
            fresh_trade_list = []
            fresh_trade_list = make_fresh_trades(testData)
            tradeList = add_fresh_trade_list_to_trade_list(fresh_trade_list, tradeList)
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

