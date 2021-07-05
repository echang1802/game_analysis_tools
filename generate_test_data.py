
import pandas as pd
import numpy as np

pd.DataFrame({
    "player_id" : ,
    "datetime" : ,
    "item_type" : ,
    "quantity" : ,
    "price" : ,
    "total_player_item"
})

class player:

    def __init__(self):
        self.frequency = np.random.randint(0, 10)
        self.quantity = np.random.randint(0, 10)

    def simulate(self):
        periods = np.random.poisson(self.frequency, 1000)
        quantity = np.random.poisson(self.quantity, 1000)

if __name__ == '__main__':
