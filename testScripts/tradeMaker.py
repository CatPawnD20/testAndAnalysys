import csv
import decimal
from decimal import Decimal, ROUND_DOWN

import config

starting_bitcoin = config.starting_bitcoin
before_bitcoin = 0
before_cash = 0


def calculateAfterBtc(trade_before_cash, trade_before_btc, trade_starting_price, trade_decision,
                      is_stop_loss_active, stop_loss_rate, use_different_stop_loss_rate, diff_stop_loss_rate_UP,
                      max_opposite_price_move_rate_tuple,trade_max_profit_rate_tuple,is_take_profit_active,take_profit_rate):
    if trade_before_cash == 0:
        trade_before_cash = Decimal(trade_before_btc) * Decimal(trade_starting_price)
    trade_after_btc = 0
    if is_take_profit_active and is_stop_loss_active:
        if max_opposite_price_move_rate_tuple[0] >= stop_loss_rate and trade_max_profit_rate_tuple[0] >= take_profit_rate:
            if max_opposite_price_move_rate_tuple[1] < trade_max_profit_rate_tuple[1]:
                #use stop loss
                if trade_decision == 'UP':
                    trade_after_btc = 0
                elif trade_decision == 'DOWN':
                    trade_after_btc = 0
            else :
                #use take profit
                if trade_decision == 'UP':
                    trade_btc = trade_before_cash / trade_starting_price
                    trade_after_btc = trade_btc
                elif trade_decision == 'DOWN':
                    trade_after_btc = 0
        elif max_opposite_price_move_rate_tuple[0] >= stop_loss_rate and trade_max_profit_rate_tuple[0] < take_profit_rate:
            #use stop loss
            if trade_decision == 'UP':
                trade_after_btc = 0
            elif trade_decision == 'DOWN':
                trade_after_btc = 0
        elif max_opposite_price_move_rate_tuple[0] < stop_loss_rate and trade_max_profit_rate_tuple[0] >= take_profit_rate:
            #use take profit
            if trade_decision == 'UP':
                trade_btc = trade_before_cash / trade_starting_price
                trade_after_btc = trade_btc
            elif trade_decision == 'DOWN':
                trade_after_btc = 0
        else:
            #no take profit no stop loss
            if trade_decision == 'UP':
                trade_btc = trade_before_cash / trade_starting_price
                trade_after_btc = trade_btc
            elif trade_decision == 'DOWN':
                trade_after_btc = 0
    elif is_take_profit_active and not is_stop_loss_active:
        if trade_max_profit_rate_tuple[0] >= take_profit_rate:
            if trade_decision == 'UP':
                trade_btc = trade_before_cash / trade_starting_price
                trade_after_btc = trade_btc
            elif trade_decision == 'DOWN':
                trade_after_btc = 0
        else:
            if trade_decision == 'UP':
                trade_btc = trade_before_cash / trade_starting_price
                trade_after_btc = trade_btc
            elif trade_decision == 'DOWN':
                trade_after_btc = 0
    elif not is_take_profit_active and is_stop_loss_active:
        if max_opposite_price_move_rate_tuple[0] >= stop_loss_rate:
            if trade_decision == 'UP':
                trade_after_btc = 0
            elif trade_decision == 'DOWN':
                trade_after_btc = 0
        else:
            if trade_decision == 'UP':
                trade_btc = trade_before_cash / trade_starting_price
                trade_after_btc = trade_btc
            elif trade_decision == 'DOWN':
                trade_after_btc = 0
    elif not is_take_profit_active and not is_stop_loss_active:
        if trade_decision == 'UP':
            trade_btc = trade_before_cash / trade_starting_price
            trade_after_btc = trade_btc
        elif trade_decision == 'DOWN':
            trade_after_btc = 0


    #if trade_decision == 'UP':
    #    if is_stop_loss_active:
    #        if max_opposite_price_move_rate_tuple >= stop_loss_rate:
    #            trade_after_btc = 0
    #        else:
    #            trade_btc = trade_before_cash / trade_starting_price
    #            trade_after_btc = trade_btc
    #    else:
    #        trade_btc = trade_before_cash / trade_starting_price
    #        trade_after_btc = trade_btc
    #elif trade_decision == 'DOWN':
    #    trade_after_btc = 0
    return trade_after_btc


def calculateAfterCash(trade_before_cash, trade_before_btc, trade_starting_price, trade_decision,
                       is_stop_loss_active, stop_loss_rate, use_different_stop_loss_rate, trade_ending_price,
                       max_opposite_price_move_rate_tuple, diff_stop_loss_rate_DOWN, is_short_selling_active,diff_stop_loss_rate_UP,trade_max_profit_rate_tuple,is_take_profit_active,take_profit_rate):
    trade_after_cash = 0
    if trade_decision == 'STB':
        if trade_before_cash != 0:
            trade_after_cash = trade_before_cash
        else:
            trade_after_cash = trade_before_btc * trade_ending_price
        return trade_after_cash
    else:
        if is_take_profit_active and is_stop_loss_active:
            if max_opposite_price_move_rate_tuple[0] >= stop_loss_rate and trade_max_profit_rate_tuple[0] >= take_profit_rate:
                if max_opposite_price_move_rate_tuple[1] < trade_max_profit_rate_tuple[1]:
                    # use stop loss
                    if trade_decision == 'UP':
                        trade_after_cash = trade_before_cash * Decimal(str((1 - stop_loss_rate)))
                    elif trade_decision == 'DOWN':
                        if trade_before_btc == 0:
                            trade_before_btc = trade_before_cash / trade_starting_price
                        if not is_short_selling_active:
                            trade_after_cash = trade_before_btc * trade_starting_price
                            return trade_after_cash
                        value = 1 - stop_loss_rate
                        value = Decimal(str(value))
                        trade_cash = trade_before_btc * trade_starting_price
                        trade_after_cash = trade_cash * value
                else:
                    # use take profit
                    if trade_decision == 'UP':
                        trade_after_cash = trade_before_cash * Decimal(str((1 + take_profit_rate)))
                    elif trade_decision == 'DOWN':
                        if trade_before_btc == 0:
                            trade_before_btc = trade_before_cash / trade_starting_price
                        if not is_short_selling_active:
                            trade_after_cash = trade_before_btc * trade_starting_price
                            return trade_after_cash
                        value = 1 + take_profit_rate
                        value = Decimal(str(value))
                        trade_cash = trade_before_btc * trade_starting_price
                        trade_after_cash = trade_cash * value

            elif max_opposite_price_move_rate_tuple[0] >= stop_loss_rate and trade_max_profit_rate_tuple[0] < take_profit_rate:
                # use stop loss
                if trade_decision == 'UP':
                    trade_after_cash = trade_before_cash * Decimal(str((1 - stop_loss_rate)))
                elif trade_decision == 'DOWN':
                    if trade_before_btc == 0:
                        trade_before_btc = trade_before_cash / trade_starting_price
                    if not is_short_selling_active:
                        trade_after_cash = trade_before_btc * trade_starting_price
                        return trade_after_cash
                    value = 1 - stop_loss_rate
                    value = Decimal(str(value))
                    trade_cash = trade_before_btc * trade_starting_price
                    trade_after_cash = trade_cash * value

            elif max_opposite_price_move_rate_tuple[0] < stop_loss_rate and trade_max_profit_rate_tuple[0] >= take_profit_rate:
                # use take profit
                if trade_decision == 'UP':
                    trade_after_cash = trade_before_cash * Decimal(str((1 + take_profit_rate)))
                elif trade_decision == 'DOWN':
                    if trade_before_btc == 0:
                        trade_before_btc = trade_before_cash / trade_starting_price
                    if not is_short_selling_active:
                        trade_after_cash = trade_before_btc * trade_starting_price
                        return trade_after_cash
                    value = 1 + take_profit_rate
                    value = Decimal(str(value))
                    trade_cash = trade_before_btc * trade_starting_price
                    trade_after_cash = trade_cash * value

            else:
                # no take profit no stop loss
                if trade_decision == 'UP':
                    trade_after_cash = 0
                elif trade_decision == 'DOWN':
                    if trade_before_btc == 0:
                        trade_before_btc = trade_before_cash / trade_starting_price
                    if not is_short_selling_active:
                        trade_after_cash = trade_before_btc * trade_starting_price
                        return trade_after_cash
                    trade_cash = trade_before_btc * trade_starting_price
                    borrowed_btc = trade_cash / trade_starting_price
                    returned_cash = borrowed_btc * trade_ending_price
                    dif = trade_cash - returned_cash
                    trade_after_cash = trade_cash + dif

        elif is_take_profit_active and not is_stop_loss_active:
            if trade_max_profit_rate_tuple[0] >= take_profit_rate:
                # use take profit
                if trade_decision == 'UP':
                    trade_after_cash = trade_before_cash * Decimal(str((1 + take_profit_rate)))
                elif trade_decision == 'DOWN':
                    if trade_before_btc == 0:
                        trade_before_btc = trade_before_cash / trade_starting_price
                    if not is_short_selling_active:
                        trade_after_cash = trade_before_btc * trade_starting_price
                        return trade_after_cash
                    value = 1 + take_profit_rate
                    value = Decimal(str(value))
                    trade_cash = trade_before_btc * trade_starting_price
                    trade_after_cash = trade_cash * value

            else:
                # no take profit no stop loss
                if trade_decision == 'UP':
                    trade_after_cash = 0
                elif trade_decision == 'DOWN':
                    if trade_before_btc == 0:
                        trade_before_btc = trade_before_cash / trade_starting_price
                    if not is_short_selling_active:
                        trade_after_cash = trade_before_btc * trade_starting_price
                        return trade_after_cash
                    trade_cash = trade_before_btc * trade_starting_price
                    borrowed_btc = trade_cash / trade_starting_price
                    returned_cash = borrowed_btc * trade_ending_price
                    dif = trade_cash - returned_cash
                    trade_after_cash = trade_cash + dif

        elif not is_take_profit_active and is_stop_loss_active:
            if max_opposite_price_move_rate_tuple[0] >= stop_loss_rate:
                # use stop loss
                if trade_decision == 'UP':
                    trade_after_cash = trade_before_cash * Decimal(str((1 - stop_loss_rate)))
                elif trade_decision == 'DOWN':
                    if trade_before_btc == 0:
                        trade_before_btc = trade_before_cash / trade_starting_price
                    if not is_short_selling_active:
                        trade_after_cash = trade_before_btc * trade_starting_price
                        return trade_after_cash
                    value = 1 - stop_loss_rate
                    value = Decimal(str(value))
                    trade_cash = trade_before_btc * trade_starting_price
                    trade_after_cash = trade_cash * value
            else:
                # no take profit no stop loss
                if trade_decision == 'UP':
                    trade_after_cash = 0
                elif trade_decision == 'DOWN':
                    if trade_before_btc == 0:
                        trade_before_btc = trade_before_cash / trade_starting_price
                    if not is_short_selling_active:
                        trade_after_cash = trade_before_btc * trade_starting_price
                        return trade_after_cash
                    trade_cash = trade_before_btc * trade_starting_price
                    borrowed_btc = trade_cash / trade_starting_price
                    returned_cash = borrowed_btc * trade_ending_price
                    dif = trade_cash - returned_cash
                    trade_after_cash = trade_cash + dif

        elif not is_take_profit_active and not is_stop_loss_active:
            # no take profit no stop loss
            if trade_decision == 'UP':
                trade_after_cash = 0
            elif trade_decision == 'DOWN':
                if trade_before_btc == 0:
                    trade_before_btc = trade_before_cash / trade_starting_price
                if not is_short_selling_active:
                    trade_after_cash = trade_before_btc * trade_starting_price
                    return trade_after_cash
                trade_cash = trade_before_btc * trade_starting_price
                borrowed_btc = trade_cash / trade_starting_price
                returned_cash = borrowed_btc * trade_ending_price
                dif = trade_cash - returned_cash
                trade_after_cash = trade_cash + dif
    return trade_after_cash


def calculate_max_opposite_price_move_rate(testDataDailyTuple, trade_decision,is_stop_loss_active):
    priceHourlyTupleList = testDataDailyTuple[6]
    max_opposite_price_move_rate = 0
    max_opposite_price_move_rate_time = -1
    if not is_stop_loss_active:
        return (max_opposite_price_move_rate, max_opposite_price_move_rate_time)
    if trade_decision == 'UP':
        for priceHourlyTuple in priceHourlyTupleList:
            if priceHourlyTuple[1] > priceHourlyTuple[6]:
                current_opposite_price_move_rate = (priceHourlyTuple[1] - priceHourlyTuple[6]) / priceHourlyTuple[1] # para ters tarafa ne kadar oynamış
                if current_opposite_price_move_rate > max_opposite_price_move_rate:
                    max_opposite_price_move_rate = current_opposite_price_move_rate
                    max_opposite_price_move_rate_time = priceHourlyTuple[0].time().hour
    elif trade_decision == 'DOWN':
        for priceHourlyTuple in priceHourlyTupleList:
            if priceHourlyTuple[1] < priceHourlyTuple[5]:
                current_opposite_price_move_rate = (priceHourlyTuple[5] - priceHourlyTuple[1]) / priceHourlyTuple[1]
                if current_opposite_price_move_rate > max_opposite_price_move_rate:
                    max_opposite_price_move_rate = current_opposite_price_move_rate
                    max_opposite_price_move_rate_time = priceHourlyTuple[0].time().hour
    max_opposite_price_move_rate_tuple = (max_opposite_price_move_rate, max_opposite_price_move_rate_time)
    return max_opposite_price_move_rate_tuple



def calculate_result_rate(trade_before_cash, trade_before_btc, trade_after_cash, trade_after_btc,
                          trade_starting_price, trade_ending_price, trade_decision, trade_max_opposite_price_move_rate_tuple,
                          is_stop_loss_active, stop_loss_rate, is_short_selling_active, trade_max_profit_rate_tuple, is_take_profit_active, take_profit_rate):
    result_rate = 0
    if is_take_profit_active and is_stop_loss_active:
        if trade_max_opposite_price_move_rate_tuple[0] >= stop_loss_rate and trade_max_profit_rate_tuple[0] >= take_profit_rate:
            if trade_max_opposite_price_move_rate_tuple[1] < trade_max_profit_rate_tuple[1]:
                # use stop loss
                if trade_decision == 'UP':
                    result_rate = stop_loss_rate
                    if result_rate < 1:
                        result_rate = -result_rate
                    result_rate = Decimal(str(result_rate))
                    decimal.getcontext().rounding = decimal.ROUND_HALF_UP
                    result_rate = result_rate.quantize(decimal.Decimal('0.00001'))
                    return result_rate

                elif trade_decision == 'DOWN':
                    if not is_short_selling_active:
                        result_rate = 0
                        return result_rate
                    else:
                        result_rate = stop_loss_rate
                        if result_rate < 1:
                            result_rate = -result_rate
                        result_rate = Decimal(str(result_rate))
                        decimal.getcontext().rounding = decimal.ROUND_HALF_UP
                        result_rate = result_rate.quantize(decimal.Decimal('0.00001'))
                        return result_rate
            else:
                # use take profit
                if trade_decision == 'UP':
                    result_rate = take_profit_rate
                    if result_rate < 1:
                        result_rate = result_rate
                    result_rate =1 + Decimal(str(result_rate))
                    decimal.getcontext().rounding = decimal.ROUND_HALF_UP
                    result_rate = result_rate.quantize(decimal.Decimal('0.00001'))
                    return result_rate

                elif trade_decision == 'DOWN':
                    if not is_short_selling_active:
                        result_rate = 0
                        return result_rate
                    else:
                        result_rate = take_profit_rate
                        if result_rate < 1:
                            result_rate = result_rate
                        result_rate =1 + Decimal(str(result_rate))
                        decimal.getcontext().rounding = decimal.ROUND_HALF_UP
                        result_rate = result_rate.quantize(decimal.Decimal('0.00001'))
                        return result_rate
        elif trade_max_opposite_price_move_rate_tuple[0] >= stop_loss_rate and trade_max_profit_rate_tuple[0] < take_profit_rate:
            # use stop loss
            if trade_decision == 'UP':
                result_rate = stop_loss_rate
                if result_rate < 1:
                    result_rate = -result_rate
                result_rate = Decimal(str(result_rate))
                decimal.getcontext().rounding = decimal.ROUND_HALF_UP
                result_rate = result_rate.quantize(decimal.Decimal('0.00001'))
                return result_rate
            elif trade_decision == 'DOWN':
                if not is_short_selling_active:
                    result_rate = 0
                    return result_rate
                else:
                    result_rate = stop_loss_rate
                    if result_rate < 1:
                        result_rate = -result_rate
                    result_rate = Decimal(str(result_rate))
                    decimal.getcontext().rounding = decimal.ROUND_HALF_UP
                    result_rate = result_rate.quantize(decimal.Decimal('0.00001'))
                    return result_rate

        elif trade_max_opposite_price_move_rate_tuple[0] < stop_loss_rate and trade_max_profit_rate_tuple[0] >= take_profit_rate:
            # use take profit
            if trade_decision == 'UP':
                result_rate = take_profit_rate
                if result_rate < 1:
                    result_rate = result_rate
                result_rate =1 + Decimal(str(result_rate))
                decimal.getcontext().rounding = decimal.ROUND_HALF_UP
                result_rate = result_rate.quantize(decimal.Decimal('0.00001'))
                return result_rate

            elif trade_decision == 'DOWN':
                if not is_short_selling_active:
                    result_rate = 0
                    return result_rate
                else:
                    result_rate = take_profit_rate
                    if result_rate < 1:
                        result_rate = result_rate
                    result_rate =1 + Decimal(str(result_rate))
                    decimal.getcontext().rounding = decimal.ROUND_HALF_UP
                    result_rate = result_rate.quantize(decimal.Decimal('0.00001'))
                    return result_rate

        else:
            # no take profit no stop loss
            if trade_decision == 'UP':
                if trade_after_cash == 0:
                    result_rate = trade_after_btc * trade_ending_price / trade_before_cash
                else:
                    result_rate = trade_after_cash / trade_before_cash
            elif trade_decision == 'DOWN':
                if trade_before_cash == 0:
                    trade_before_cash = trade_before_btc * trade_starting_price
                result_rate = trade_after_cash / trade_before_cash

            if result_rate < 1:
                result_rate = 1 - result_rate
                result_rate = -result_rate
            result_rate = Decimal(str(result_rate))
            decimal.getcontext().rounding = decimal.ROUND_HALF_UP
            result_rate = result_rate.quantize(decimal.Decimal('0.00001'))
    elif is_take_profit_active and not is_stop_loss_active:
        if trade_max_profit_rate_tuple[0] >= take_profit_rate:
            # use take profit
            if trade_decision == 'UP':
                result_rate = take_profit_rate
                if result_rate < 1:
                    result_rate = result_rate
                result_rate =1 + Decimal(str(result_rate))
                decimal.getcontext().rounding = decimal.ROUND_HALF_UP
                result_rate = result_rate.quantize(decimal.Decimal('0.00001'))
                return result_rate

            elif trade_decision == 'DOWN':
                if not is_short_selling_active:
                    result_rate = 0
                    return result_rate
                else:
                    result_rate = take_profit_rate
                    if result_rate < 1:
                        result_rate = result_rate
                    result_rate =1 + Decimal(str(result_rate))
                    decimal.getcontext().rounding = decimal.ROUND_HALF_UP
                    result_rate = result_rate.quantize(decimal.Decimal('0.00001'))
                    return result_rate

        else:
            # no take profit no stop loss
            if trade_decision == 'UP':
                if trade_after_cash == 0:
                    result_rate = trade_after_btc * trade_ending_price / trade_before_cash
                else:
                    result_rate = trade_after_cash / trade_before_cash
            elif trade_decision == 'DOWN':
                if trade_before_cash == 0:
                    trade_before_cash = trade_before_btc * trade_starting_price
                result_rate = trade_after_cash / trade_before_cash

            if result_rate < 1:
                result_rate = 1 - result_rate
                result_rate = -result_rate
            result_rate = Decimal(str(result_rate))
            decimal.getcontext().rounding = decimal.ROUND_HALF_UP
            result_rate = result_rate.quantize(decimal.Decimal('0.00001'))
    elif not is_take_profit_active and is_stop_loss_active:
        if trade_max_opposite_price_move_rate_tuple[0] >= stop_loss_rate:
            # use stop loss
            if trade_decision == 'UP':
                result_rate = stop_loss_rate
                if result_rate < 1:
                    result_rate = -result_rate
                result_rate = Decimal(str(result_rate))
                decimal.getcontext().rounding = decimal.ROUND_HALF_UP
                result_rate = result_rate.quantize(decimal.Decimal('0.00001'))
                return result_rate

            elif trade_decision == 'DOWN':
                if not is_short_selling_active:
                    result_rate = 0
                    return result_rate
                else:
                    result_rate = stop_loss_rate
                    if result_rate < 1:
                        result_rate = -result_rate
                    result_rate = Decimal(str(result_rate))
                    decimal.getcontext().rounding = decimal.ROUND_HALF_UP
                    result_rate = result_rate.quantize(decimal.Decimal('0.00001'))
                    return result_rate
        else:
            # no take profit no stop loss
            if trade_decision == 'UP':
                if trade_after_cash == 0:
                    result_rate = trade_after_btc * trade_ending_price / trade_before_cash
                else:
                    result_rate = trade_after_cash / trade_before_cash
            elif trade_decision == 'DOWN':
                if trade_before_cash == 0:
                    trade_before_cash = trade_before_btc * trade_starting_price
                result_rate = trade_after_cash / trade_before_cash

            if result_rate < 1:
                result_rate = 1 - result_rate
                result_rate = -result_rate
            result_rate = Decimal(str(result_rate))
            decimal.getcontext().rounding = decimal.ROUND_HALF_UP
            result_rate = result_rate.quantize(decimal.Decimal('0.00001'))
    elif not is_take_profit_active and not is_stop_loss_active:
        # no take profit no stop loss
        if trade_decision == 'UP':
            if trade_after_cash == 0:
                result_rate = trade_after_btc * trade_ending_price / trade_before_cash
            else:
                result_rate = trade_after_cash / trade_before_cash
        elif trade_decision == 'DOWN':
            if trade_before_cash == 0:
                trade_before_cash = trade_before_btc * trade_starting_price
            result_rate = trade_after_cash / trade_before_cash

        if result_rate < 1:
            result_rate = 1 - result_rate
            result_rate = -result_rate
        result_rate = Decimal(str(result_rate))
        decimal.getcontext().rounding = decimal.ROUND_HALF_UP
        result_rate = result_rate.quantize(decimal.Decimal('0.00001'))

    return result_rate
def calculate_trade_state(result_rate, is_stop_loss_active, stop_loss_rate, trade_decision,is_short_selling_active,is_take_profit_active,take_profit_rate):
    trade_state = ''
    if trade_decision == 'STB':
        trade_state = 'NO TRADE STB'
        return trade_state
    if not is_short_selling_active:
        if trade_decision == 'DOWN':
            trade_state = 'NO TRADE'
            return trade_state
    if not is_stop_loss_active and not is_take_profit_active:
        if result_rate > 0:
            trade_state = 'WIN DeActive Stop Loss and DeActive Take Profit'
        elif result_rate < 0:
            trade_state = 'LOSS DeActive Stop Loss and DeActive Take Profit'
        else:
            trade_state = 'DRAW DeActive Stop Loss and DeActive Take Profit'
    elif is_stop_loss_active and not is_take_profit_active:
        if result_rate > 0:
            trade_state = 'WIN and DeActive Take Profit'
        elif result_rate < 0:
            if result_rate == -Decimal(str(stop_loss_rate * config.leverage_rate)):
                trade_state = 'Stop Loss and DeActive Take Profit'
            else:
                trade_state = 'LOSS Below Stop Loss and DeActive Take Profit'
        else:
            trade_state = 'DRAW'
    elif not is_stop_loss_active and is_take_profit_active:
        if result_rate > 0:
            if result_rate >= 1 + Decimal(str(take_profit_rate * config.leverage_rate)):
                trade_state = 'Win Take Profit and DeActive Stop loss'
            else:
                trade_state = 'Win Below Take Profit and DeActive Stop loss'
        elif result_rate < 0:
            trade_state = 'LOSS and DeActive Stop loss'
        else:
            trade_state = 'DRAW'

    else:
        if result_rate > 0:
            sonuc = Decimal((take_profit_rate * float(config.leverage_rate)))
            sonuc =  sonuc.quantize(Decimal('0.001'), rounding=ROUND_DOWN)
            if result_rate >= 1 + sonuc:
                trade_state = 'Win Take Profit'

            else:
                trade_state = 'Win Below Take Profit'
        elif result_rate < 0:
            if result_rate <= -Decimal(str(stop_loss_rate*config.leverage_rate)).quantize(Decimal('0.001'), rounding=ROUND_DOWN):
                trade_state = 'Stop Loss'
            else:
                trade_state = 'LOSS Below Stop Loss'
        else:
            trade_state = 'DRAW'
    return trade_state


def useLeverageBTC(trade_after_btc, result_rate):
    leverage_rate = config.leverage_rate
    if trade_after_btc == 0:
        return trade_after_btc
    if leverage_rate == 0:
        return trade_after_btc
    if leverage_rate == 1:
        return trade_after_btc
    if result_rate >= 1:
        trade_after_btc = trade_after_btc / result_rate
        result_rate = result_rate - 1
        result_rate = result_rate * leverage_rate
        result_rate = result_rate + 1
        trade_after_btc = trade_after_btc * result_rate
    else:
        result_rate = -result_rate
        result_rate = 1 - result_rate
        trade_after_btc = trade_after_btc / result_rate
        result_rate = result_rate - 1
        result_rate = result_rate * leverage_rate
        result_rate = -result_rate
        negatif = trade_after_btc * result_rate
        trade_after_btc = trade_after_btc - negatif
        result_rate = -result_rate

    return trade_after_btc


def useLeverageResultRate(result_rate):
    leverage_rate = config.leverage_rate
    if leverage_rate == 0:
        return result_rate
    if leverage_rate == 1:
        return result_rate
    if result_rate >= 1:
        result_rate = result_rate - 1
        result_rate = result_rate * leverage_rate
        result_rate = result_rate + 1
    else:
        result_rate = result_rate * leverage_rate
    return result_rate


def useLeverageCash(trade_after_cash, result_rate):
    leverage_rate = config.leverage_rate
    if result_rate == 1 or result_rate == -1:
        return trade_after_cash
    if leverage_rate == 0:
        return trade_after_cash
    if leverage_rate == 1:
        return trade_after_cash
    if result_rate >= 1:
        trade_after_cash = trade_after_cash / result_rate
        result_rate = result_rate - 1
        result_rate = result_rate * leverage_rate
        result_rate = result_rate + 1
        trade_after_cash = trade_after_cash * result_rate
    else:
        result_rate = -result_rate
        result_rate = 1 - result_rate
        trade_after_cash = trade_after_cash / result_rate
        result_rate = result_rate - 1
        result_rate = result_rate * leverage_rate
        result_rate = -result_rate
        negatif = trade_after_cash * result_rate
        trade_after_cash = trade_after_cash - negatif
        result_rate = -result_rate
    return trade_after_cash


def calculate_trade_max_profit_rate(testDataDailyTuple, trade_decision,is_take_profit_active):
    priceHourlyTupleList = testDataDailyTuple[6]
    max_profit_rate = 0
    max_profit_rate_time = -1
    if not is_take_profit_active:
        return (max_profit_rate, max_profit_rate_time)
    if trade_decision == 'UP':
        for priceHourlyTuple in priceHourlyTupleList:
            if priceHourlyTuple[5] > priceHourlyTuple[1]:
                current_profit_rate = (priceHourlyTuple[5] - priceHourlyTuple[1]) / priceHourlyTuple[1]
                if current_profit_rate > max_profit_rate:
                    max_profit_rate = current_profit_rate
                    max_profit_rate_time = priceHourlyTuple[0].time().hour
    elif trade_decision == 'DOWN':
        for priceHourlyTuple in priceHourlyTupleList:
            if priceHourlyTuple[1] > priceHourlyTuple[6]:
                current_profit_rate = (priceHourlyTuple[1] - priceHourlyTuple[6]) / priceHourlyTuple[1]
                if current_profit_rate > max_profit_rate:
                    max_profit_rate = current_profit_rate
                    max_profit_rate_time = priceHourlyTuple[0].time().hour
    max_profit_tuple = (max_profit_rate, max_profit_rate_time)
    return max_profit_tuple


def doTrade(testDataDailyTuple, before_cash_1, before_bitcoin_1, is_stop_loss_active, stop_loss_rate,
            is_short_selling_active, use_different_stop_loss_rate, diff_stop_loss_rate_UP, diff_stop_loss_rate_DOWN,is_take_profit_active,take_profit_rate):
    # trade has these elements: date, decision, confidence_rate,before_cash,before_btc,
    # starting_price, ending_price,after_cash,after_btc,result_rate, stop_loss_rate, max_opposite_price_move_rate ,
    # trade_state

    is_leverage_active = config.use_leverage
    trade = []
    trade_id = testDataDailyTuple[0]
    trade_date = testDataDailyTuple[1]
    trade_decision = testDataDailyTuple[3]
    trade_confidence_rate = testDataDailyTuple[4]
    trade_before_cash = before_cash_1
    trade_before_btc = Decimal(before_bitcoin_1)
    trade_starting_price = Decimal(testDataDailyTuple[2])
    trade_ending_price = testDataDailyTuple[5]
    trade_max_profit_rate_tuple = calculate_trade_max_profit_rate(testDataDailyTuple, trade_decision,is_take_profit_active)
    trade_max_opposite_price_move_rate_tuple = calculate_max_opposite_price_move_rate(testDataDailyTuple, trade_decision,is_stop_loss_active)
    if trade_decision == 'UP':
        if is_stop_loss_active:
            if use_different_stop_loss_rate:
                stop_loss_rate = diff_stop_loss_rate_UP
            else:
                stop_loss_rate = stop_loss_rate
    if trade_decision == 'DOWN':
        if is_stop_loss_active:
            if use_different_stop_loss_rate:
                stop_loss_rate = diff_stop_loss_rate_DOWN
            else:
                stop_loss_rate = stop_loss_rate
    trade_after_btc = calculateAfterBtc(trade_before_cash, trade_before_btc, trade_starting_price, trade_decision,
                                        is_stop_loss_active, stop_loss_rate, use_different_stop_loss_rate,
                                        diff_stop_loss_rate_UP, trade_max_opposite_price_move_rate_tuple,trade_max_profit_rate_tuple,is_take_profit_active,take_profit_rate)

    trade_after_cash = calculateAfterCash(trade_before_cash, trade_before_btc, trade_starting_price, trade_decision,
                                          is_stop_loss_active, stop_loss_rate, use_different_stop_loss_rate,
                                          trade_ending_price,
                                          trade_max_opposite_price_move_rate_tuple, diff_stop_loss_rate_DOWN,
                                          is_short_selling_active,diff_stop_loss_rate_UP,trade_max_profit_rate_tuple,is_take_profit_active,take_profit_rate)
    result_rate = calculate_result_rate(before_cash_1, before_bitcoin_1, trade_after_cash, trade_after_btc,
                                        trade_starting_price, trade_ending_price,trade_decision,trade_max_opposite_price_move_rate_tuple,
                                        is_stop_loss_active, stop_loss_rate,is_short_selling_active,trade_max_profit_rate_tuple,is_take_profit_active,take_profit_rate)
    if is_leverage_active:
        trade_after_btc = useLeverageBTC(trade_after_btc,result_rate)
        trade_after_cash = useLeverageCash(trade_after_cash,result_rate)
        result_rate = useLeverageResultRate(result_rate)


    trade_state = calculate_trade_state(result_rate,is_stop_loss_active, stop_loss_rate,trade_decision,is_short_selling_active,is_take_profit_active,take_profit_rate)
    trade.append(trade_id) #0
    trade.append(trade_date) #1
    trade.append(trade_decision) #2
    trade.append(trade_confidence_rate) #3
    trade.append(trade_before_cash) #4
    trade.append(trade_before_btc) #5
    trade.append(trade_starting_price) #6
    trade.append(trade_ending_price) #7
    trade.append(trade_after_cash) #8
    trade.append(trade_after_btc) #9
    trade.append(format(result_rate, '.4f')) #10
    trade.append(format(trade_max_opposite_price_move_rate_tuple[0], '.4f')) #11rate
    trade.append(format(trade_max_opposite_price_move_rate_tuple[1])) #12time
    trade.append(format(trade_max_profit_rate_tuple[0], '.4f'))  # 13rate
    trade.append(format(trade_max_profit_rate_tuple[1]))  # 14time
    trade.append(trade_state) #15
    global before_cash
    global before_bitcoin
    before_cash = trade_after_cash
    before_bitcoin = trade_after_btc
    return trade


def makeTrade(testDataDailyTuple):
    before_cash1 = before_cash
    before_bitcoin1 = before_bitcoin
    is_stop_loss_active = config.stop_loss
    stop_loss_rate = config.stop_loss_rate
    is_short_selling_active = config.short_selling
    use_different_stop_loss_rate = config.use_different_stop_loss_rate
    diff_stop_loss_rate_UP = 0
    diff_stop_loss_rate_DOWN = 0
    is_take_profit_active = config.take_profit
    take_profit_rate = config.take_profit_rate
    if testDataDailyTuple[3] == 'STB':
        if before_cash1 == 0 and before_bitcoin1 == 0:
            before_cash1 = Decimal(starting_bitcoin) * Decimal(testDataDailyTuple[2])
            before_bitcoin1 = 0
        else:
            if before_bitcoin1 == 0:
                before_cash1 = before_cash1
            else:
                before_cash1 = before_bitcoin1 * testDataDailyTuple[2]
                before_bitcoin1 = 0

        trade = doTrade(testDataDailyTuple, before_cash1, before_bitcoin1, is_stop_loss_active, stop_loss_rate,
                        is_short_selling_active, use_different_stop_loss_rate, diff_stop_loss_rate_UP,
                        diff_stop_loss_rate_DOWN,is_take_profit_active,take_profit_rate)

        return trade

    if use_different_stop_loss_rate:
        diff_stop_loss_rate_UP = config.diff_stop_loss_rate_UP
        diff_stop_loss_rate_DOWN = config.diff_stop_loss_rate_DOWN

    if before_cash1 == 0 and before_bitcoin1 == 0:
        if is_short_selling_active:
            if testDataDailyTuple[3] == 'UP':
                before_cash1 = Decimal(starting_bitcoin) * testDataDailyTuple[2]
                before_bitcoin1 = 0
            elif testDataDailyTuple[3] == 'DOWN':
                before_cash1 = 0
                before_bitcoin1 = starting_bitcoin
        else:
            if testDataDailyTuple[3] == 'UP':
                before_cash1 = starting_bitcoin * testDataDailyTuple[2]
                before_bitcoin1 = 0
            elif testDataDailyTuple[3] == 'DOWN':
                before_cash1 = starting_bitcoin * testDataDailyTuple[2]
                before_bitcoin1 = 0
    else:
        if testDataDailyTuple[3] == 'UP':
            if before_bitcoin1 == 0:
                before_cash1 = before_cash1
            else:
                before_cash1 = before_bitcoin1 * testDataDailyTuple[2]
                before_bitcoin1 = 0
        elif testDataDailyTuple[3] == 'DOWN':
            if before_cash1 == 0:
                before_cash1 = 0
                before_bitcoin1 = before_bitcoin1
            else:
                before_bitcoin1 = 0
                before_cash1 = before_cash1
    trade = doTrade(testDataDailyTuple, before_cash1, before_bitcoin1, is_stop_loss_active, stop_loss_rate,
                    is_short_selling_active, use_different_stop_loss_rate, diff_stop_loss_rate_UP,
                    diff_stop_loss_rate_DOWN,is_take_profit_active,take_profit_rate)
    return trade


def calculate_before_total(param, param1, param2):
    if param == 0:
        return param1 * param2
    else:
        return param


def calculate_after_total(param, param1, param2):
    if param == 0:
        return param1 * param2
    else:
        return param


def makeReadableTrade(trade):
    readableTrade = []
    readableTrade.append(trade[0])  # 0 id
    readableTrade.append(trade[1])  # 1 date
    readableTrade.append(trade[2])  # 2 decision
    readableTrade.append(trade[3])  # 3 confidence_rate
    before_total = calculate_before_total(trade[4], trade[5], trade[6])
    readableTrade.append(trade[6])  # 4 starting_price
    readableTrade.append(trade[7])  # 5 ending_price
    readableTrade.append(before_total) # 6 before_total
    after_total = calculate_after_total(trade[8], trade[9], trade[7])
    readableTrade.append(after_total) # 7 after_total
    readableTrade.append(trade[10])  # 8 result_rate
    readableTrade.append(trade[11])  # 10 max_opposite_price_move_rate
    readableTrade.append(trade[12])
    readableTrade.append(trade[13])
    readableTrade.append(trade[14])
    readableTrade.append(trade[15])

    return readableTrade


def makeReadableTradeList(tradeList):
    readableTradeList = []
    for trade in tradeList:
        readableTrade = makeReadableTrade(trade)
        readableTradeList.append(readableTrade)
    return readableTradeList


def printTradeList(readableTradeList):
    # CSV dosyası açılıyor ve yazma modunda açılıyor ('w' modu)
    with open('trade_list.csv', mode='w', newline='', encoding='utf-8') as file:
        # CSV yazıcı oluşturuluyor
        writer = csv.writer(file)
        is_stb_trade_print = config.stb_trade_print
        # Sütun başlıkları yazılıyor
        headers = ['id', 'date', 'decision', 'confidence_rate', 'starting_price', 'ending_price', 'before_total',
                   'after_total', 'result_rate', 'max_opposite_price_move_rate', 'max_opposite_price_move_rate_time', 'max_take_profit_rate', 'take_profit_rate_time', 'trade_state', 'control_state']
        writer.writerow(headers)

        # Verilen ticaret listesi satır satır yazdırılıyor
        for trade in readableTradeList:
            if not is_stb_trade_print:
                if trade[2] == 'STB':
                    continue
            writer.writerow([
                trade[0],
                trade[1],
                trade[2],
                trade[3],
                trade[4],
                trade[5],
                trade[6],
                trade[7],
                trade[8],
                trade[9],
                trade[10],
                trade[11],
                trade[12],
                trade[13],
                trade[14]

            ])


def controlTrade(trade):
    if trade[2] == 'STB':
        if trade[6] == trade[7]:
            if Decimal(trade[8]) == 1 or Decimal(trade[8]) == 0:
                return True
    if Decimal(trade[8]) >= 0:
        say1 = round(trade[7] / trade[6], 4)
        say2 = round(Decimal(trade[8]), 4)
        if say1 == say2:
            return True
        say2 = say2 - Decimal(0.0001)
        say2 = round(say2, 4)
        if say1 == say2:
            return True
        else:
            return False

    if Decimal(trade[8]) < 0 and Decimal(trade[8]) > -1:
        say1 = round(trade[7] / trade[6], 4)
        say2 = round(Decimal(trade[8]), 4)
        say1 = say1 - 1
        say2 = say2
        if say1 == say2:
            return True
        say2 = say2 + Decimal(0.0001)
        say2 = round(say2, 4)
        if say1 == say2:
            return True
        else:
            return False
    if Decimal(trade[8]) == -1:
        if trade[7] == 0:
            return True
        else:
            return False

def controlTradeList(readableTradeList):
    for trade in readableTradeList:
        is_trade_OK = controlTrade(trade)
        if is_trade_OK:
            trade.append('OK')
        else:
            trade.append('ERROR')
    return readableTradeList
