from good import Good
from locomotive import Locomotive
from train import Train
from city import City

def test_good_has_name():
    steel = Good("steel")

    assert steel.name == "steel"

def test_city_inventory_can_store_good_object():
    steel = Good("steel")
    detroit = City("Detroit")
    detroit.inventory = {steel: 10}

    assert steel in detroit.inventory

def test_train_cargo_can_store_good_object():
    steel = Good("steel")
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)
    train.cargo = {steel: 1}

    assert steel in train.cargo

def test_goods_with_same_name_are_equal():
    steel1 = Good("steel")
    steel2 = Good("steel")

    assert steel1 == steel2

def test_good_with_same_name_can_access_inventory_entry():
    steel1 = Good("steel")
    steel2 = Good("steel")
    detroit = City("Detroit")
    detroit.inventory = {steel1: 10}

    assert detroit.inventory[steel2] == 10