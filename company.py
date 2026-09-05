class Company():
    def __init__(self, name):
        self.name = name
        self.money = 0
        self.all_shares = 1000 #Wszystkie aktualnie wyemitowane udzialy niezaleznie gdzie sie znajduja
        self.shares = self.all_shares #Wyemitowane udzialy posiadane aktualnie przez spolke
        self.shares_price = 100
        self.shareholders = {}
        self.president = None
        self.is_floated = False

    def sell_shares(self, buyer, quantity):
        if quantity <= 0:
            return False
        shares_left = self.shares - quantity
        if shares_left >= 0:
            self.shares = shares_left
            self.money += self.shares_price * quantity
            self.shareholders[buyer.name] = self.shareholders.get(buyer.name, 0) + quantity
            
            self._update_company_after_share_sale()
            return True
        else:
            return False
        
    def _update_company_after_share_sale(self):
        highest_quantity = max(self.shareholders.values())
        top_shareholders = [shareholder for shareholder, quantity in self.shareholders.items() if quantity == highest_quantity]
        if self.shares <= self.all_shares / 2:
            self.is_floated = True

            if len(top_shareholders) == 1:
                self.president = top_shareholders[0]
            elif self.shares == self.all_shares / 2:
                self.president = None
            elif self.president in top_shareholders:
                pass
            else:
                self.president = top_shareholders[0]