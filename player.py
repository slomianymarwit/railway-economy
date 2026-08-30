from company import Company

class Player():
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.shares = {}
        self.owned_companies = []

    def buy_shares(self, company:Company, quantity):
        total_price = company.shares_price * quantity
        if total_price > self.money:
            False
        else:
            if company.sell_shares(self, quantity):
                self.money -= total_price
                self.shares[company.name] = self.shares.get(company.name, 0) + quantity
                # Ponizszy krok moze powinien byc osobna funkcja uruchamiana niezaleznie od akcji graczy - tutaj jedynie akcja kupna moze spowodowac zmiane przypisanych spolek jako posiadanych
                if company.president == self.name:
                    self.owned_companies.append(company.name) #Jesli inny gracz aktywuje spolke swoim kupnem akcji ta dostnie prezesa ale nie zostanie ona przypisana do nieaktywnego gracza - do rozwiazania
                else:
                    try:
                        self.owned_companies.remove(company.name) #Jesli inny gracz uzyska wiekszosc % akcji w spolce ta zmieni wlasciciela ale nieatywny gracz nie straci jej ze swojej listy wlasnosci - do rozwiazania
                    except:
                        pass
    
    def sell_shares(self, company:Company, quantity):
        total_price = company.shares_price * quantity
        pass
        # Na ta chwile nie ma nikogo kto by te akcje kupil - moze trzeba dodac market albo zlecenia kupna od "malych graczy/innych spolek"