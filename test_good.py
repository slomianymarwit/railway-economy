from good import Good
from locomotive import Locomotive
from train import Train
from city import City
import pytest

def test_good_has_name():
    steel = Good("steel", 100)

    assert steel.name == "steel"

def test_city_inventory_can_store_good_object():
    steel = Good("steel", 100)
    detroit = City("Detroit")
    detroit.inventory = {steel: 10}

    assert steel in detroit.inventory

def test_train_cargo_can_store_good_object():
    steel = Good("steel", 100)
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)
    train.cargo = {steel: 1}

    assert steel in train.cargo

def test_goods_with_same_name_are_equal():
    steel1 = Good("steel", 100)
    steel2 = Good("steel", 100)

    assert steel1 == steel2

def test_good_with_same_name_can_access_inventory_entry():
    steel1 = Good("steel", 100)
    steel2 = Good("steel", 100)
    detroit = City("Detroit")
    detroit.inventory = {steel1: 10}

    assert detroit.inventory[steel2] == 10

def test_good_has_base_price():
    steel = Good("steel", 100)

    assert steel.base_price == 100

def test_good_rejects_zero_or_negative_base_price():
    with pytest.raises(ValueError):
        Good("steel", 0)
    with pytest.raises(ValueError):
        Good("steel", -1)