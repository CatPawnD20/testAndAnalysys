# Test dates
start_date = '2024-07-01'
end_date = '2024-08-09'
starting_bitcoin = 1  # starting bitcoin amount

decisionType = "MC_V1_ENS_XGB_NN_BODY_4H" #name of the decision table

# Confidence rate
confidence_rate_include = False  # if True, confidence_rate will be included in the test data
confidence_rate = 0.5   # confidence_rate and above will be included in the test data

# STB decision conversion
stb_decision_conversion = False  # if True, STB decisions will be converted to buy/sell decisions
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