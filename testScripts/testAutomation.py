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
    confidence_rate_list = config.confidence_rate_list
    table_list = prepare_test_table_list()
    table_count = len(table_list)

    SetDict = make_set_dict(dataTupleList, confidence_rate_list, table_list)

    with open('auto_test_results.csv', 'w') as f:
        # Write headers for each set
        headers = []
        for confidence_rate in confidence_rate_list:
            headers.extend([f'Table ({confidence_rate})', f'Win Count ({confidence_rate})', f'Win Rate ({confidence_rate})', f'Lose Count ({confidence_rate})', f'Lose Rate ({confidence_rate})', f'Last Money ({confidence_rate})'])
        f.write(','.join(headers) + '\n')

        # Write data for each table
        for i in range(table_count):
            row = []
            for confidence_rate in confidence_rate_list:
                dataTuple = SetDict[confidence_rate][i]
                formatted_last_money = f'"{dataTuple[5]:,}"'
                row.extend([dataTuple[0], dataTuple[1], dataTuple[2], dataTuple[3], dataTuple[4], formatted_last_money])
            f.write(','.join(map(str, row)) + '\n')

    print('Auto Test Results are written to auto_test_results.csv')

