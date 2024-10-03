# Test dates
start_date = '2024-01-01' # start date of the test ### start date + 1 day
end_date = '2024-09-25' # end date must be one day before from the last date of your data

#warning ### sources  -----------------> start from  -----------------> start_date +1day +1phase ----------------->end_date
#warning ### decision -----------------> start from  -----------------> start date +1day ----------------->end_date -1phase
#warning ### control  -----------------> start from  -----------------> start date +1day  +1phase----------------->end_date

#ortalama negatif hareket : -0.007

starting_bitcoin = 0.003  # starting bitcoin amount

decisionType = "mc_v1_ens_xgb_nn_body_4h" #name of the decision table

# Confidence rate
confidence_rate_include = True  # if True, confidence_rate will be included in the test data
confidence_rate = 0.5   # confidence_rate and above will be included in the test data


stb_trade_print = True  # if True, STB trades will be printed
# short selling
short_selling = True  # if True, short selling will be active

# stop loss
stop_loss = True  # if True, stop loss will be active
stop_loss_rate = 0.03  # stop loss rate
use_different_stop_loss_rate = False  # if True, stop_loss_rate will be different for UP and DOWN decisions
diff_stop_loss_rate_UP = 0.02  # stop loss rate for UP decisions
diff_stop_loss_rate_DOWN = 0.02  # stop loss rate for DOWN decisions

#take profit
take_profit = True  # if True, take profit will be active
take_profit_rate = 0.02 # take profit rate

# leverage
use_leverage = True  # if True, leverage will be active
leverage_rate = 10  # leverage rate


#Montly Test --->> reset start money every month
monthly_test = True #Aylık test yapmak için zorunludur.
monthly_auto_test_results = True  # sadece aylık test sonuçlarını görmek için

# tableList
table_list = [
    "mc_v1_ens_xgb_nn_body_4h",
    #"fi_v1_xgb_body_4h",
    #"fi_v1_ens_xgb_lr_body_4h",
    "fi_v2_xgb_body_4h",
    #"fi_v3_xgb_body_4h",
    "mc_v3_ens_xgb_nn_body_4h", #basarı artısı yetersız
    #"fi_v4_xgb_body_4h",
    "mc_v4_ens_xgb_nn_body_4h",
    #"mc_v4_xgb_body_4h",
    #"fi_v5_xgb_body_4h",
    #"fi_v6_xgb_body_4h",
    "mc_v6_xgb_body_4h"
]

confidence_rate_list = [0.5, 0.55, 0.6]
