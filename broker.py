class Broker:
    shares = 0
    money = 0
    count = 0

    buy_amt = 0
    sell_amt = 0
    buy_share = 0
    sell_share = 0

    def __init__(self):
        pass
    def buy(self, amt, price):
        amt_shares = amt
        self.money -= amt_shares*price
        self.shares = self.shares+amt_shares
        self.buy_share+=1
        self.buy_amt += amt_shares*price
    def sell(self, amt, price):
        amt_shares = amt
        if self.shares - amt_shares >= 0:
            self.money += amt_shares*price
            self.shares -= amt_shares
            self.sell_share+=1
            self.sell_amt += amt_shares*price
    def show_money(self):
        print("Money remaining:", self.money)
    def show_remaining_shares(self):
        print("Remaining shares:",self.shares)
    def show_buy_and_sell_shares(self):
        print(f"Buy shares: {self.buy_share} | Sell share: {self.sell_share}")
    def show_returns(self, share_rem_value):
        print("Returns:", (self.money+ self.shares*share_rem_value)/self.buy_amt*100)

