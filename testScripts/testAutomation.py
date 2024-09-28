import config
from testScripts import tradeMaker, testMaker


def prepare_test_table_list():
    table_list = config.table_list
    return table_list

def make_auto_test():
    table_list = prepare_test_table_list()
    dataTupleList = []
    for table in table_list:
        config.decisionType = table
        print(table)
        tradeList = testMaker.doTest()
        winCount = tradeMaker.winningTradeCount(tradeList)
        loseCount = tradeMaker.losingTradeCount(tradeList)
        winRate = 100 * winCount / (winCount + loseCount)
        loseRate = 100 * loseCount / (winCount + loseCount)
        lastMoney = tradeMaker.lastMoney(tradeList)
        dataTuple = (table, winCount, winRate, loseCount, loseRate, lastMoney)
        dataTupleList.append(dataTuple)

    return dataTupleList

def write_auto_test():
    dataTupleList = make_auto_test()
    #write the results to a file with header
    #writeTo cvs
    with open('auto_test_results.csv', 'w') as f:
        f.write('Decision Table,Winning Trade Count,Winning Trade Rate (%),Losing Trade Count,Losing Trade Rate (%),Last Money\n')
        for dataTuple in dataTupleList:
            f.write(f'{dataTuple[0]},{dataTuple[1]},{dataTuple[2]},{dataTuple[3]},{dataTuple[4]},{dataTuple[5]}\n')
