
import pandas as pd
import numpy as np
import argparse
from datetime import datetime

arg_parser = argparse.ArgumentParser(description = "Simulate input data")
arg_parser.add_argument("-periods", default = 1000, help = "Period to simulate", type = int)
arg_parser.add_argument("-frequency", default = 5, help = "Frequency of offers (periods between offers)", type = int)
arg_parser.add_argument("-offers_length", default = 2, help = "Number of periods an offer is hold", type = int)
arg_parser.add_argument("-players", default = 1000, help = "Number of player to simulate", type = int)
arg_parser.add_argument("-file_name", help = "Filepath and name where the data will be storage")

class player_class:

    def __init__(self, max_period):
        self.frequency = np.random.randint(2, 50)
        self.quantity = np.random.randint(1, 100)
        self.average_use = np.random.randint(1, max(np.round(self.quantity/2),2))
        price_tolerance = np.random.uniform(-0.8,0.2)
        if price_tolerance <= 0:
            self.price_tolerance = 0
        else:
            self.price_tolerance = np.random.beta(2, 1)
        self.bought_history = {
            "period" : [],
            "quantity" : [],
            "price" : [],
            "total_player_coins" : []
        }
        start_coins = np.random.randint(0, 100) if self.price_tolerance > 0 else 0
        self.coins_by_period = [max(start_coins - (self.average_use * x), 0) for x in range(max_period)]

    def simulate(self, max_period, hist_price):
        if self.price_tolerance == 0:
            return
        period = 0
        while True:
            next_buy = np.random.poisson(self.frequency)
            if period + next_buy >= max_period:
                break
            period += next_buy
            price = hist_price.get_price(period)
            if self.price_tolerance < price:
                 continue

            quantity = np.random.poisson(self.quantity)
            coins = self.coins_by_period[period] + quantity
            self.coins_by_period[period] += quantity
            self.coins_by_period = [self.coins_by_period[p] if p <= period else max(coins - self.average_use, 0) for p in range(max_period)]

            self.bought_history["period"].append(period)
            self.bought_history["quantity"].append(quantity)
            self.bought_history["price"].append(price)
            self.bought_history["total_player_coins"].append(coins)

        return

class price_behaviour:

    def __init__(self, periods, frequency, offers_length):
        self.price_by_period = [1] * periods
        self.frequency = frequency
        self.offers_length = offers_length

    def _generate_offer(self):
        offer = np.random.uniform(0.2,1)
        length = np.random.poisson(self.offers_length)
        return offer, length

    def simulate_prices(self):
        period = 0
        while True:
            offer_period = np.random.poisson(self.frequency)
            if period + offer_period >= len(self.price_by_period):
                break
            offer, lenght = self._generate_offer()
            period += offer_period
            self.price_by_period[period:(period + lenght + 1)] = [offer] * (lenght + 1)

    def get_price(self, period):
        return self.price_by_period[period]

if __name__ == '__main__':

    argv = arg_parser.parse_args()

    prices = price_behaviour(argv.periods, argv.frequency, argv.offers_length)
    prices.simulate_prices()

    data = pd.DataFrame({
        "player_id" : [],
        "period" : [],
        "quantity" : [],
        "price" : [],
        "total_player_coins" : []
    })
    t_start = datetime.now()
    for player_id in range(argv.players):
        t_player = datetime.now()
        player = player_class(argv.periods)
        player.simulate(argv.periods, prices)

        player_data = pd.DataFrame(player.bought_history)
        player_data["player_id"] = player_id
        data = data.append(player_data)
        print("Player", player_id, "proccess time:", datetime.now() - t_player, " - Bought:", (player_data.price * player_data.quantity).sum())

    data.to_csv(argv.file_name, index = False)
    print("Total process time:", datetime.now() - t_start)
