from datetime import datetime

class KlineData:
    def __init__(self, opening_timestamp, opening_price, high_price, low_price, closing_price, volume_btc, closing_timestamp, volume_usd, open_orders, taker_buy_volume, taker_sell_volume, open_orders_count):
        self.id = None
        self.opening_timestamp = opening_timestamp
        self.opening_price = opening_price
        self.high_price = high_price
        self.low_price = low_price
        self.closing_price = closing_price
        self.volume_btc = volume_btc
        self.closing_timestamp = closing_timestamp
        self.volume_usd = volume_usd
        self.open_orders = open_orders
        self.taker_buy_volume = taker_buy_volume
        self.taker_sell_volume = taker_sell_volume
        self.open_orders_count = open_orders_count

    def write_my_self(self):
        print("id: " + str(self.id))
        print("opening_timestamp: " + str(self.opening_timestamp))
        print("opening_price: " + str(self.opening_price))
        print("high_price: " + str(self.high_price))
        print("low_price: " + str(self.low_price))
        print("closing_price: " + str(self.closing_price))
        print("volume_btc: " + str(self.volume_btc))
        print("closing_timestamp: " + str(self.closing_timestamp))
        print("volume_usd: " + str(self.volume_usd))
        print("open_orders: " + str(self.open_orders))
        print("taker_buy_volume: " + str(self.taker_buy_volume))
        print("taker_sell_volume: " + str(self.taker_sell_volume))
        print("open_orders_count: " + str(self.open_orders_count))