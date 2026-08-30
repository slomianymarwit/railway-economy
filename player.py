from company import Company

class Player():
    def __init__(self, name, money):
        self.name = name
        self.money = money

    def buy_shares(self, company:Company, quantity):
        total_price = company.shares_price * quantity
        if total_price > self.money:
            return False

        result = company.sell_shares(self, quantity)
        if result:
            self.money -= total_price
        return result
    
    def sell_shares(self, company:Company, quantity):
        total_price = company.shares_price * quantity
        pass
        # Na ta chwile nie ma nikogo kto by te akcje kupil - moze trzeba dodac market albo zlecenia kupna od "malych graczy/innych spolek"

    def shares_in(self, company:Company):
        shares_quantity = company.shareholders.get(self.name, 0)
        return shares_quantity