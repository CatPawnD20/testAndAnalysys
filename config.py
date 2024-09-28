# Test dates
start_date = '2024-01-01' # start date of the test ### start date + 1 day
end_date = '2024-09-25' # end date must be one day before from the last date of your data

#warning ### sources  -----------------> start from  -----------------> start_date +1day ----------------->end_date
#warning ### decision -----------------> start from  -----------------> start date +1day ----------------->end_date
#warning ### control  -----------------> start from  -----------------> start date +1day ----------------->end_date

starting_bitcoin = 1  # starting bitcoin amount

decisionType = "mc_v1_ens_xgb_nn_body_4h" #name of the decision table

# Confidence rate
confidence_rate_include = False  # if True, confidence_rate will be included in the test data
confidence_rate = 0.6   # confidence_rate and above will be included in the test data


stb_trade_print = False  # if True, STB trades will be printed
# short selling
short_selling = True  # if True, short selling will be active

# stop loss
stop_loss = True  # if True, stop loss will be active
stop_loss_rate = 0.02  # stop loss rate
use_different_stop_loss_rate = False  # if True, stop_loss_rate will be different for UP and DOWN decisions
diff_stop_loss_rate_UP = 0.02  # stop loss rate for UP decisions
diff_stop_loss_rate_DOWN = 0.02  # stop loss rate for DOWN decisions

#take profit
take_profit = True  # if True, take profit will be active
take_profit_rate = 0.06 # take profit rate

# leverage
use_leverage = True  # if True, leverage will be active
leverage_rate = 10  # leverage rate