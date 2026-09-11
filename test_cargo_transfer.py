from locomotive import Locomotive
from train import Train
from city import City
from cargo_transfer import transfer_city_to_train, transfer_train_to_city

def test_transfer_city_to_train_moves_goods_between_inventories():
    detroit = City("Detroit")
    detroit.inventory = {"steel": 5}
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 2)

    result = transfer_city_to_train(detroit, train, "steel", 2)

    assert detroit.inventory == {"steel": 3}
    assert train.cargo == {"steel": 2}
    assert result is True

def test_transfer_train_to_city_moves_goods_between_inventories():
    detroit = City("Detroit")
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 2)
    train.cargo = {"steel": 3}

    result = transfer_train_to_city(train, detroit, "steel", 2)

    assert detroit.inventory == {"steel": 2}
    assert train.cargo == {"steel": 1}
    assert result is True

def test_transfer_city_to_train_does_not_change_state_when_train_has_no_capacity():
    detroit = City("Detroit")
    detroit.inventory = {"steel": 5}
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 2)

    result = transfer_city_to_train(detroit, train, "steel", 3)

    assert detroit.inventory == {"steel": 5}
    assert train.cargo == {}
    assert result is False

def test_transfer_city_to_train_does_not_change_state_when_city_has_insufficient_goods():
    detroit = City("Detroit")
    detroit.inventory = {"steel": 1}
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 2)

    result = transfer_city_to_train(detroit, train, "steel", 2)

    assert detroit.inventory == {"steel": 1}
    assert train.cargo == {}
    assert result is False

def test_transfer_city_to_train_does_not_change_state_when_remaining_capacity_is_insufficient():
    detroit = City("Detroit")
    detroit.inventory = {"grain": 5}
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 2)
    train.cargo = {"steel": 1}

    result = transfer_city_to_train(detroit, train, "grain", 2)

    assert detroit.inventory == {"grain": 5}
    assert train.cargo == {"steel": 1}
    assert result is False

def test_transfer_city_to_train_returns_false_when_good_is_not_in_city():
    detroit = City("Detroit")
    detroit.inventory = {"grain": 5}
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 2)

    result = transfer_city_to_train(detroit, train, "steel", 2)

    assert detroit.inventory == {"grain": 5}
    assert train.cargo == {}
    assert result is False

def test_transfer_train_to_city_returns_false_when_good_is_not_on_train():
    detroit = City("Detroit")
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 2)
    train.cargo = {"steel": 2}

    result = transfer_train_to_city(train, detroit, "grain", 2)

    assert detroit.inventory == {}
    assert train.cargo == {"steel": 2}
    assert result is False

def test_transfer_city_to_train_rejects_zero_or_negative_quantity():
    detroit = City("Detroit")
    detroit.inventory = {"steel": 2}
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 2)
    
    result = transfer_city_to_train(detroit, train, "steel", 0)

    assert detroit.inventory == {"steel": 2}
    assert train.cargo == {}
    assert result is False
    
    result = transfer_city_to_train(detroit, train, "steel", -1)

    assert detroit.inventory == {"steel": 2}
    assert train.cargo == {}
    assert result is False

def test_transfer_train_to_city_rejects_zero_or_negative_quantity():
    detroit = City("Detroit")
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 2)
    train.cargo = {"steel": 2}

    result = transfer_train_to_city(train, detroit, "steel", 0)

    assert detroit.inventory == {}
    assert train.cargo == {"steel": 2}
    assert result is False

    result = transfer_train_to_city(train, detroit, "steel", -1)

    assert detroit.inventory == {}
    assert train.cargo == {"steel": 2}
    assert result is False