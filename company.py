class Company():
    def __init__(self, name):
        self.name = name
        self.money = 0
        self.all_shares = 1000 #Wszystkie aktualnie wyemitowane udzialy niezaleznie gdzie sie znajduja
        self.shares = self.all_shares #Wyemitowane udzialy posiadane aktualnie przez spolke
        self.shares_price = 100
        self.shareholders = {}
        self.president = None

    def sell_shares(self, buyer, quantity):
        if quantity <= 0:
            return False
        shares_left = self.shares - quantity
        if shares_left >= 0:
            self.shares = shares_left
            self.money += self.shares_price * quantity
            self.shareholders[buyer.name] = self.shareholders.get(buyer.name, 0) + quantity
            
            top_shareholder = max(self.shareholders, key=self.shareholders.get) #Do rozwiazania case gdzie jest remis w ilosci akcji
            if self.shares <= self.all_shares / 2:
                self.president = top_shareholder
            return True
        else:
            return False