import config
from testScripts import tradeMaker, testMaker


def prepare_test_table_list():
    table_list = config.table_list
    return table_list

def make_auto_test():
    table_list = prepare_test_table_list()
    confidence_rate_list = config.confidence_rate_list
    dataTupleList = []
    for confidence_rate in confidence_rate_list:
        config.confidence_rate = confidence_rate
        for table in table_list:
            config.decisionType = table
            print(f'Testing {table} with confidence rate {confidence_rate}')
            tradeList = testMaker.doTest()
            winCount = tradeMaker.winningTradeCount(tradeList)
            loseCount = tradeMaker.losingTradeCount(tradeList)
            winRate = 100 * winCount / (winCount + loseCount)
            loseRate = 100 * loseCount / (winCount + loseCount)
            lastMoney = tradeMaker.lastMoney(tradeList)
            dataTuple = (table, winCount, winRate, loseCount, loseRate, lastMoney)
            dataTupleList.append(dataTuple)
    return dataTupleList


def make_set_dict(dataTupleList, confidence_rate_list, table_list):
    # pick first table_count elements from dataTupleList and set them as first SET
    # pick next table_count elements from dataTupleList and set them as second SET
    # there will be confidence_count SETs
    # each SET will have table_count elements

    SetDict = {}
    for i in range(len(confidence_rate_list)):
        SetDict[confidence_rate_list[i]] = dataTupleList[i*len(table_list):(i+1)*len(table_list)]
    return SetDict


def write_auto_test():
    dataTupleList = make_auto_test()
    #write the results to a file with header
    #writeTo cvs
    confidence_rate_list = config.confidence_rate_list
    confidence_count = len(confidence_rate_list)
    table_list = prepare_test_table_list()
    table_count = len(table_list)

    SetDict = make_set_dict(dataTupleList, confidence_rate_list, table_list)

    #write the results to a file with header
    #write this sets to a cvs file
    # write each set side by side
    # use headers for each set
    # use table names as rows
    # make csv Tables for each SET

    with open('auto_test_results.csv', 'w') as f:
        f.write('table,')
        for confidence_rate in confidence_rate_list:
            f.write(f'winCount_{confidence_rate},winRate_{confidence_rate},loseCount_{confidence_rate},loseRate_{confidence_rate},lastMoney_{confidence_rate},')
        f.write('\n')
        for table in table_list:
            f.write(f'{table},')
            for confidence_rate in confidence_rate_list:
                dataTuple = SetDict[confidence_rate][table_list.index(table)]
                f.write(f'{dataTuple[1]},{dataTuple[2]},{dataTuple[3]},{dataTuple[4]},{dataTuple[5]},')
            f.write('\n')