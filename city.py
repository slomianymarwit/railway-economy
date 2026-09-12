class City():
    def __init__(self, name):
        self.name = name
        self.inventory = {}
        self.daily_consumption = {}
        self.supply_history = {}

    def add_goods(self, good, quantity):
        if quantity <= 0:
            return False
        
        if good not in self.inventory:
            self.inventory[good] = quantity
            return True
        else:
            self.inventory[good] += quantity
            return True

    def remove_goods(self, good, quantity):
        if good not in self.inventory:
            return False

        if quantity <= 0:
            return False

        if quantity > self.inventory[good]:
            return False

        self.inventory[good] -= quantity
        if self.inventory[good] == 0:
            del self.inventory[good]
        return True

    def get_daily_consumption(self, good):
        result = self.daily_consumption.get(good, 0)
        return result

    def set_daily_consumption(self, good, quantity):
        if quantity < 0:
            return False

        if quantity == 0:
            if good in self.daily_consumption:
                del self.daily_consumption[good]
            return True

        self.daily_consumption[good] = quantity
        return True

    def get_days_of_supply(self, good):
        if good not in self.daily_consumption:
            return None
        
        if good not in self.inventory:
            return 0

        return self.inventory[good] / self.daily_consumption[good]

    def get_supply_state(self, good):
        result = self.get_days_of_supply(good)

        if result is None:
            return None
        if result <= 1:
            return "extreme shortage"
        if result <= 3:
            return "shortage"
        if result <= 6:
            return "tight"
        if result <= 10:
            return "normal"
        if result <= 15:
            return "surplus"
        return "heavy surplus"

    def get_supply_multiplier(self, good):
        result = self.get_supply_state(good)

        if result is None:
            return None
        if result == "extreme shortage":
            return 1.50
        if result == "shortage":
            return 1.30
        if result == "tight":
            return 1.15
        if result == "normal":
            return 1.00
        if result == "surplus":
            return 0.85
        return 0.7

    def record_supply_state(self, good):
        supply_scores = {
            "extreme shortage": 1,
            "shortage": 2,
            "tight": 3,
            "normal": 4,
            "surplus": 5,
            "heavy surplus": 6,
        }
        result = self.get_supply_state(good)
        
        if good not in self.inventory and good not in self.daily_consumption:
            score = None
        elif good in self.inventory and good not in self.daily_consumption:
            score = 6
        else:
            score = supply_scores[result]

        if good in self.supply_history and len(self.supply_history[good]) >= 7:
            del self.supply_history[good][0]

        self.supply_history.setdefault(good, []).append(score)
        return True

    def get_average_supply_score(self, good):
        if good not in self.supply_history:
            return None
        
        history = self.supply_history[good]
        filtered_history = []
        for i in history:
            if i is not None:
                filtered_history.append(i)

        if len(filtered_history) > 0:
            average_score = sum(filtered_history) / len(filtered_history)
            return average_score
        else:
            return None

    def get_historical_supply_multiplier(self, good):
        historical_multipliers = {
            1: 1.10,
            2: 1.05,
            3: 1.00,
            4: 1.00,
            5: 0.95,
            6: 0.90,
        }
        average_score = self.get_average_supply_score(good)

        if average_score is None:
            return 1

        if average_score > 4 or average_score < 3:
            score = average_score - int(average_score)
            score = score * 0.05
            historical_supply_multiplier = historical_multipliers[int(average_score)] - score
            return round(historical_supply_multiplier, 3)
        
        return 1