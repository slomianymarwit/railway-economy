from city import City
from company import Company
from train import Train
from good import Good

def buy_goods(company:Company, train:Train, city:City, good:Good, quantity):
    if train.current_city is not city:
        return False

    if quantity <= 0:
        return False

    if good not in city.inventory:
        return False

    if city.inventory[good] < quantity:
        return False

    remaining_capacity = train.cars - sum(train.cargo.values())
    if remaining_capacity < quantity:
        return False

    if good not in city.market_prices:
        return False
    
    if company.money < city.market_prices[good] * quantity:
        return False

    price = city.market_prices[good] * quantity
    company.money -= price
    city.remove_goods(good, quantity)
    train.load_cargo(good, quantity)
    return True

def sell_goods(company:Company, train:Train, city:City, good:Good, quantity):
    if train.current_city is not city:
        return False
    
    if quantity <= 0:
        return False

    if good not in train.cargo:
        return False

    if train.cargo[good] < quantity:
        return False

    if good not in city.market_prices:
        return False

    price = city.market_prices[good] * quantity
    company.money += price
    train.unload_cargo(good, quantity)
    city.add_goods(good, quantity)
    return True