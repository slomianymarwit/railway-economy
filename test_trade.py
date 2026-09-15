from city import City
from good import Good
from locomotive import Locomotive
from train import Train
from company import Company
from trade import buy_goods, sell_goods
import pytest

def test_buy_goods_transfers_money_and_goods():
    steel = Good("steel", 100)
    detroit = City("Detroit")
    detroit.inventory = {steel: 10}
    detroit.market_prices = {steel: 100}
    locomotive = Locomotive("TierII", 50, 5)
    train = Train("First Train", locomotive, 2)
    train.current_city = detroit
    company = Company("Long Rails")
    company.money = 1000

    result = buy_goods(company, train, detroit, steel, 2)

    assert train.cargo == {steel: 2}
    assert company.money == 800
    assert detroit.inventory == {steel: 8}
    assert result is True

def test_buy_goods_adds_to_existing_cargo():
    steel = Good("steel", 100)
    detroit = City("Detroit")
    detroit.inventory = {steel: 10}
    detroit.market_prices = {steel: 100}
    locomotive = Locomotive("TierII", 50, 5)
    train = Train("First Train", locomotive, 2)
    train.current_city = detroit
    train.cargo = {steel: 1}
    company = Company("Long Rails")
    company.money = 1000

    result = buy_goods(company, train, detroit, steel, 1)

    assert train.cargo == {steel: 2}
    assert company.money == 900
    assert detroit.inventory == {steel: 9}
    assert result is True

def test_buy_goods_returns_false_when_train_is_not_in_city():
    steel = Good("steel", 100)
    detroit = City("Detroit")
    detroit.inventory = {steel: 10}
    detroit.market_prices = {steel: 100}
    locomotive = Locomotive("TierII", 50, 5)
    train = Train("First Train", locomotive, 2)
    company = Company("Long Rails")
    company.money = 1000

    result = buy_goods(company, train, detroit, steel, 1)

    assert train.cargo == {}
    assert company.money == 1000
    assert detroit.inventory == {steel: 10}
    assert result is False

def test_buy_goods_returns_false_when_good_is_not_in_city_inventory():
    steel = Good("steel", 100)
    detroit = City("Detroit")
    detroit.inventory = {}
    detroit.market_prices = {steel: 100}
    locomotive = Locomotive("TierII", 50, 5)
    train = Train("First Train", locomotive, 2)
    train.current_city = detroit
    company = Company("Long Rails")
    company.money = 1000

    result = buy_goods(company, train, detroit, steel, 1)

    assert train.cargo == {}
    assert company.money == 1000
    assert detroit.inventory == {}
    assert result is False

def test_buy_goods_returns_false_when_train_has_insufficient_capacity():
    steel = Good("steel", 100)
    detroit = City("Detroit")
    detroit.inventory = {steel: 10}
    detroit.market_prices = {steel: 100}
    locomotive = Locomotive("TierII", 50, 5)
    train = Train("First Train", locomotive, 2)
    train.current_city = detroit
    company = Company("Long Rails")
    company.money = 1000

    result = buy_goods(company, train, detroit, steel, 3)

    assert train.cargo == {}
    assert company.money == 1000
    assert detroit.inventory == {steel: 10}
    assert result is False

def test_buy_goods_returns_false_when_company_has_insufficient_money():
    steel = Good("steel", 100)
    detroit = City("Detroit")
    detroit.inventory = {steel: 10}
    detroit.market_prices = {steel: 100}
    locomotive = Locomotive("TierII", 50, 5)
    train = Train("First Train", locomotive, 2)
    train.current_city = detroit
    company = Company("Long Rails")
    company.money = 0

    result = buy_goods(company, train, detroit, steel, 1)

    assert train.cargo == {}
    assert company.money == 0
    assert detroit.inventory == {steel: 10}
    assert result is False

@pytest.mark.parametrize("quantity", [0, -1])
def test_buy_goods_returns_false_when_quantity_is_zero_or_negative(quantity):
    steel = Good("steel", 100)
    detroit = City("Detroit")
    detroit.inventory = {steel: 10}
    detroit.market_prices = {steel: 100}
    locomotive = Locomotive("TierII", 50, 5)
    train = Train("First Train", locomotive, 2)
    train.current_city = detroit
    company = Company("Long Rails")
    company.money = 1000

    result = buy_goods(company, train, detroit, steel, quantity)

    assert train.cargo == {}
    assert company.money == 1000
    assert detroit.inventory == {steel: 10}
    assert result is False

def test_buy_goods_returns_false_when_good_has_no_market_price():
    steel = Good("steel", 100)
    detroit = City("Detroit")
    detroit.inventory = {steel: 10}
    detroit.market_prices = {}
    locomotive = Locomotive("TierII", 50, 5)
    train = Train("First Train", locomotive, 2)
    train.current_city = detroit
    company = Company("Long Rails")
    company.money = 1000

    result = buy_goods(company, train, detroit, steel, 1)

    assert train.cargo == {}
    assert company.money == 1000
    assert detroit.inventory == {steel: 10}
    assert result is False

def test_buy_goods_removes_good_from_city_inventory_when_all_stock_is_bought():
    steel = Good("steel", 100)
    detroit = City("Detroit")
    detroit.inventory = {steel: 2}
    detroit.market_prices = {steel: 100}
    locomotive = Locomotive("TierII", 50, 5)
    train = Train("First Train", locomotive, 2)
    train.current_city = detroit
    company = Company("Long Rails")
    company.money = 1000

    result = buy_goods(company, train, detroit, steel, 2)

    assert train.cargo == {steel: 2}
    assert company.money == 800
    assert detroit.inventory == {}
    assert result is True

def test_buy_goods_succeeds_when_company_has_exactly_enough_money():
    steel = Good("steel", 100)
    detroit = City("Detroit")
    detroit.inventory = {steel: 10}
    detroit.market_prices = {steel: 100}
    locomotive = Locomotive("TierII", 50, 5)
    train = Train("First Train", locomotive, 2)
    train.current_city = detroit
    company = Company("Long Rails")
    company.money = 200

    result = buy_goods(company, train, detroit, steel, 2)

    assert train.cargo == {steel: 2}
    assert company.money == 0
    assert detroit.inventory == {steel: 8}
    assert result is True



def test_sell_goods_transfers_money_and_goods():
    steel = Good("steel", 100)
    detroit = City("Detroit")
    detroit.inventory = {}
    detroit.market_prices = {steel: 100}
    locomotive = Locomotive("TierII", 50, 5)
    train = Train("First Train", locomotive, 2)
    train.cargo = {steel: 2}
    train.current_city = detroit
    company = Company("Long Rails")
    company.money = 0

    result = sell_goods(company, train, detroit, steel, 1)

    assert train.cargo == {steel: 1}
    assert company.money == 100
    assert detroit.inventory == {steel: 1}
    assert result is True

def test_sell_goods_adds_to_existing_city_inventory():
    steel = Good("steel", 100)
    detroit = City("Detroit")
    detroit.inventory = {steel: 10}
    detroit.market_prices = {steel: 100}
    locomotive = Locomotive("TierII", 50, 5)
    train = Train("First Train", locomotive, 2)
    train.cargo = {steel: 2}
    train.current_city = detroit
    company = Company("Long Rails")
    company.money = 0

    result = sell_goods(company, train, detroit, steel, 1)

    assert train.cargo == {steel: 1}
    assert company.money == 100
    assert detroit.inventory == {steel: 11}
    assert result is True

def test_sell_goods_returns_false_when_train_is_not_in_city():
    steel = Good("steel", 100)
    detroit = City("Detroit")
    detroit.inventory = {steel: 10}
    detroit.market_prices = {steel: 100}
    locomotive = Locomotive("TierII", 50, 5)
    train = Train("First Train", locomotive, 2)
    train.cargo = {steel: 2}
    train.current_city = None
    company = Company("Long Rails")
    company.money = 0

    result = sell_goods(company, train, detroit, steel, 2)

    assert train.cargo == {steel: 2}
    assert company.money == 0
    assert detroit.inventory == {steel: 10}
    assert result is False

def test_sell_goods_returns_false_when_train_has_insufficient_goods():
    steel = Good("steel", 100)
    detroit = City("Detroit")
    detroit.inventory = {steel: 10}
    detroit.market_prices = {steel: 100}
    locomotive = Locomotive("TierII", 50, 5)
    train = Train("First Train", locomotive, 2)
    train.cargo = {steel: 2}
    train.current_city = detroit
    company = Company("Long Rails")
    company.money = 0

    result = sell_goods(company, train, detroit, steel, 3)

    assert train.cargo == {steel: 2}
    assert company.money == 0
    assert detroit.inventory == {steel: 10}
    assert result is False

def test_sell_goods_returns_false_when_good_is_not_in_train_cargo():
    steel = Good("steel", 100)
    grain = Good("grain", 100)
    detroit = City("Detroit")
    detroit.inventory = {steel: 10}
    detroit.market_prices = {steel: 100}
    locomotive = Locomotive("TierII", 50, 5)
    train = Train("First Train", locomotive, 2)
    train.cargo = {grain: 2}
    train.current_city = detroit
    company = Company("Long Rails")
    company.money = 0

    result = sell_goods(company, train, detroit, steel, 2)

    assert train.cargo == {grain: 2}
    assert company.money == 0
    assert detroit.inventory == {steel: 10}
    assert result is False

@pytest.mark.parametrize("quantity", [0, -1])
def test_sell_goods_returns_false_when_quantity_is_zero_or_negative(quantity):
    steel = Good("steel", 100)
    detroit = City("Detroit")
    detroit.inventory = {steel: 10}
    detroit.market_prices = {steel: 100}
    locomotive = Locomotive("TierII", 50, 5)
    train = Train("First Train", locomotive, 2)
    train.cargo = {steel: 2}
    train.current_city = detroit
    company = Company("Long Rails")
    company.money = 0

    result = sell_goods(company, train, detroit, steel, quantity)

    assert train.cargo == {steel: 2}
    assert company.money == 0
    assert detroit.inventory == {steel: 10}
    assert result is False

def test_sell_goods_returns_false_when_good_has_no_market_price():
    steel = Good("steel", 100)
    detroit = City("Detroit")
    detroit.inventory = {steel: 10}
    detroit.market_prices = {}
    locomotive = Locomotive("TierII", 50, 5)
    train = Train("First Train", locomotive, 2)
    train.cargo = {steel: 2}
    train.current_city = detroit
    company = Company("Long Rails")
    company.money = 0

    result = sell_goods(company, train, detroit, steel, 1)

    assert train.cargo == {steel: 2}
    assert company.money == 0
    assert detroit.inventory == {steel: 10}
    assert result is False

def test_sell_goods_removes_good_from_train_cargo_when_all_stock_is_sold():
    steel = Good("steel", 100)
    detroit = City("Detroit")
    detroit.inventory = {steel: 10}
    detroit.market_prices = {steel: 100}
    locomotive = Locomotive("TierII", 50, 5)
    train = Train("First Train", locomotive, 2)
    train.cargo = {steel: 2}
    train.current_city = detroit
    company = Company("Long Rails")
    company.money = 0

    result = sell_goods(company, train, detroit, steel, 2)

    assert train.cargo == {}
    assert company.money == 200
    assert detroit.inventory == {steel: 12}
    assert result is True