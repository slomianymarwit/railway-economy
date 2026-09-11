def transfer_city_to_train(city, train, good, quantity):
    if quantity <= 0:
        return False

    if quantity > train.cars - sum(train.cargo.values()):
        return False

    if good not in city.inventory:
        return False

    if quantity > city.inventory[good]:
        return False
    
    city.remove_goods(good, quantity)
    train.load_cargo(good, quantity)
    return True

def transfer_train_to_city(train, city, good, quantity):
    if quantity <= 0:
        return False

    if good not in train.cargo:
        return False
    
    if quantity > train.cargo[good]:
        return False
    
    train.unload_cargo(good, quantity)
    city.add_goods(good, quantity)
    return True