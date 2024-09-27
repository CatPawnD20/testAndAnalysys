from databaseScripts.classes.klineBased.KlineData import KlineData

class OneMinuteKline(KlineData):
    def __init__(self, opening_timestamp, opening_price, high_price, low_price, closing_price, volume_btc,
                 closing_timestamp, volume_usd, open_orders, taker_buy_volume, taker_sell_volume, open_orders_count):

        # KlineData sınıfının __init__ metodunu çağırarak miras alınan özellikleri ayarla
        super().__init__(opening_timestamp, opening_price, high_price, low_price, closing_price, volume_btc,
                 closing_timestamp, volume_usd, open_orders, taker_buy_volume, taker_sell_volume, open_orders_count)