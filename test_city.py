from city import City
from good import Good
import pytest

def test_city_starts_with_empty_inventory():
    detroit = City("Detroit")

    assert detroit.inventory == {}

def test_add_goods_increases_city_inventory():
    detroit = City("Detroit")

    result = detroit.add_goods("steel", 3)

    assert detroit.inventory == {"steel": 3}
    assert result is True

def test_add_goods_increases_existing_good_quantity():
    detroit = City("Detroit")
    detroit.inventory = {"steel": 3}
    
    result = detroit.add_goods("steel", 2)

    assert detroit.inventory == {"steel": 5}
    assert result is True

def test_add_goods_rejects_zero_or_negative_quantity():
    detroit = City("Detroit")
    detroit.inventory = {"steel": 3}

    result = detroit.add_goods("steel", 0)

    assert detroit.inventory == {"steel": 3}
    assert result is False

    result = detroit.add_goods("steel", -1)

    assert detroit.inventory == {"steel": 3}
    assert result is False

def test_remove_goods_reduces_city_inventory():
    detroit = City("Detroit")
    detroit.inventory = {"steel": 3}

    result = detroit.remove_goods("steel", 1)

    assert detroit.inventory == {"steel": 2}
    assert result is True

def test_remove_goods_removes_good_when_quantity_reaches_zero():
    detroit = City("Detroit")
    detroit.inventory = {"steel": 3}

    result = detroit.remove_goods("steel", 3)

    assert detroit.inventory == {}
    assert result is True

def test_remove_goods_cannot_remove_more_than_city_has():
    detroit = City("Detroit")
    detroit.inventory = {"steel": 1}

    result = detroit.remove_goods("steel", 3)

    assert detroit.inventory == {"steel": 1}
    assert result is False

def test_remove_goods_returns_false_when_good_is_not_in_inventory():
    detroit = City("Detroit")
    detroit.inventory = {"steel": 1}

    result = detroit.remove_goods("grain", 1)

    assert detroit.inventory == {"steel": 1}
    assert result is False

def test_remove_goods_rejects_zero_or_negative_quantity():
    detroit = City("Detroit")
    detroit.inventory = {"steel": 1}

    result = detroit.remove_goods("steel", 0)

    assert detroit.inventory == {"steel": 1}
    assert result is False

    result = detroit.remove_goods("steel", -1)

    assert detroit.inventory == {"steel": 1}
    assert result is False

def test_city_add_goods_accepts_good_object():
    detroit = City("Detroit")
    steel = Good("steel", 100)

    result = detroit.add_goods(steel, 1)

    assert detroit.inventory[steel] == 1
    assert result is True

def test_city_starts_with_empty_daily_consumption():
    detroit = City("Detroit")

    assert detroit.daily_consumption == {}

def test_set_daily_consumption_for_good():
    detroit = City("Detroit")
    steel = Good("steel", 100)

    result = detroit.set_daily_consumption(steel, 2)

    assert detroit.daily_consumption == {steel: 2}
    assert result is True

def test_missing_good_has_zero_daily_consumption():
    detroit = City("Detroit")
    steel = Good("steel", 100)

    result = detroit.get_daily_consumption(steel)

    assert result == 0

def test_set_daily_consumption_rejects_negative_quantity():
    detroit = City("Detroit")
    steel = Good("steel", 100)

    result = detroit.set_daily_consumption(steel, -1)

    assert detroit.daily_consumption == {}
    assert result is False

def test_set_daily_consumption_zero_removes_good():
    detroit = City("Detroit")
    steel = Good("steel", 100)
    detroit.daily_consumption = {steel: 1}

    result = detroit.set_daily_consumption(steel, 0)

    assert detroit.daily_consumption == {}
    assert result is True

def test_set_daily_consumption_replaces_existing_value():
    detroit = City("Detroit")
    steel = Good("steel", 100)
    detroit.daily_consumption = {steel: 1}

    result = detroit.set_daily_consumption(steel, 2)

    assert detroit.daily_consumption == {steel: 2}
    assert result is True

def test_set_daily_consumption_zero_when_good_is_missing():
    detroit = City("Detroit")
    steel = Good("steel", 100)
    detroit.daily_consumption = {}

    result = detroit.set_daily_consumption(steel, 0)

    assert detroit.daily_consumption == {}
    assert result is True

def test_get_days_of_supply_returns_inventory_divided_by_daily_consumption():
    detroit = City("Detroit")
    steel = Good("steel", 100)
    detroit.inventory ={steel: 10}
    detroit.daily_consumption = {steel: 2}

    result = detroit.get_days_of_supply(steel)

    assert result == 5

def test_get_days_of_supply_preserves_fractional_days():
    detroit = City("Detroit")
    steel = Good("steel", 100)
    detroit.inventory ={steel: 5}
    detroit.daily_consumption = {steel: 2}

    result = detroit.get_days_of_supply(steel)

    assert result == 2.5

def test_get_days_of_supply_returns_none_when_good_is_not_consumed():
    detroit = City("Detroit")
    steel = Good("steel", 100)
    detroit.inventory = {steel: 10}

    result = detroit.get_days_of_supply(steel)

    assert result is None

def test_get_days_of_supply_returns_zero_when_consumed_good_has_no_inventory():
    detroit = City("Detroit")
    steel = Good("steel", 100)
    detroit.inventory = {}
    detroit.daily_consumption = {steel: 2}

    result = detroit.get_days_of_supply(steel)

    assert result == 0

def test_get_supply_state_returns_none_when_good_is_not_consumed():
    detroit = City("Detroit")
    steel = Good("steel", 100)
    detroit.inventory = {steel: 2}

    result = detroit.get_supply_state(steel)
    assert result == None

def test_get_supply_state_returns_extreme_shortage_for_one_day_or_less():
    detroit = City("Detroit")
    steel = Good("steel", 100)
    detroit.inventory = {steel: 0}
    detroit.daily_consumption = {steel: 2}

    result = detroit.get_supply_state(steel)
    assert result == "extreme shortage"

    detroit.inventory = {steel: 2}
    result = detroit.get_supply_state(steel)
    assert result == "extreme shortage"

def test_get_supply_state_returns_shortage_for_two_to_three_days():
    detroit = City("Detroit")
    steel = Good("steel", 100)
    detroit.inventory = {steel: 4}
    detroit.daily_consumption = {steel: 2}

    result = detroit.get_supply_state(steel)
    assert result == "shortage"

    detroit.inventory = {steel: 6}
    result = detroit.get_supply_state(steel)
    assert result == "shortage"

def test_get_supply_state_returns_tight_for_four_to_six_days():
    detroit = City("Detroit")
    steel = Good("steel", 100)
    detroit.inventory = {steel: 8}
    detroit.daily_consumption = {steel: 2}

    result = detroit.get_supply_state(steel)
    assert result == "tight"

    detroit.inventory = {steel: 12}
    result = detroit.get_supply_state(steel)
    assert result == "tight"

def test_get_supply_state_returns_normal_for_seven_to_ten_days():
    detroit = City("Detroit")
    steel = Good("steel", 100)
    detroit.inventory = {steel: 14}
    detroit.daily_consumption = {steel: 2}

    result = detroit.get_supply_state(steel)
    assert result == "normal"

    detroit.inventory = {steel: 20}
    result = detroit.get_supply_state(steel)
    assert result == "normal"

def test_get_supply_state_returns_surplus_for_eleven_to_fifteen_days():
    detroit = City("Detroit")
    steel = Good("steel", 100)
    detroit.inventory = {steel: 22}
    detroit.daily_consumption = {steel: 2}

    result = detroit.get_supply_state(steel)
    assert result == "surplus"

    detroit.inventory = {steel: 30}
    result = detroit.get_supply_state(steel)
    assert result == "surplus"

def test_get_supply_state_returns_heavy_surplus_above_fifteen_days():
    detroit = City("Detroit")
    steel = Good("steel", 100)
    detroit.inventory = {steel: 31}
    detroit.daily_consumption = {steel: 2}

    result = detroit.get_supply_state(steel)
    assert result == "heavy surplus"

    detroit.inventory = {steel: 40}
    result = detroit.get_supply_state(steel)
    assert result == "heavy surplus"

@pytest.mark.parametrize(
    "inventory, daily_consumption, expected_multiplier",
    [
        (1, 1, 1.50),
        (2, 1, 1.30),
        (4, 1, 1.15),
        (7, 1, 1.00),
        (11, 1, 0.85),
        (16, 1, 0.70),
    ],
)

def test_get_supply_multiplier_returns_multiplier_for_supply_state(inventory, daily_consumption, expected_multiplier):
    detroit = City("Detroit")
    steel = Good("steel", 100)
    detroit.inventory = {steel: inventory}
    detroit.daily_consumption = {steel: daily_consumption}

    result = detroit.get_supply_multiplier(steel)

    assert result == expected_multiplier

def test_record_supply_state_adds_score_to_history():
    detroit = City("Detroit")
    steel = Good("steel", 100)
    detroit.inventory = {steel: 4}
    detroit.daily_consumption = {steel: 2}

    result = detroit.record_supply_state(steel)
    assert detroit.supply_history == {steel: [2]}
    assert result is True

def test_record_supply_state_removes_oldest_entry_when_history_is_full():
    detroit = City("Detroit")
    steel = Good("steel", 100)
    detroit.inventory = {steel: 4}
    detroit.daily_consumption = {steel: 2}
    detroit.supply_history = {steel: [1, 1, 1, 1, 1, 1, 1]}

    result = detroit.record_supply_state(steel)
    assert detroit.supply_history == {steel: [1, 1, 1, 1, 1, 1, 2]}
    assert result is True

def test_record_supply_state_records_none_for_inactive_market():
    detroit = City("Detroit")
    steel = Good("steel", 100)
    grain = Good("grain", 60)
    detroit.inventory = {steel: 4}
    detroit.daily_consumption = {steel: 2}

    result = detroit.record_supply_state(grain)
    assert detroit.supply_history == {grain: [None]}
    assert result is True

def test_record_supply_state_records_heavy_surplus_when_inventory_exists_without_consumption():
    detroit = City("Detroit")
    steel = Good("steel", 100)
    detroit.inventory = {steel: 4}

    result = detroit.record_supply_state(steel)
    assert detroit.supply_history == {steel: [6]}
    assert result is True

def test_supply_history_preserves_inactive_turns():
    detroit = City("Detroit")
    steel = Good("steel", 100)
    detroit.inventory = {steel: 4}

    for i in range(2):
        result = detroit.record_supply_state(steel)
    assert detroit.supply_history == {steel: [6, 6]}
    assert result is True

    detroit.inventory = {}
    for i in range(2):
        result = detroit.record_supply_state(steel)
    assert detroit.supply_history == {steel: [6, 6, None, None]}
    assert result is True

    detroit.inventory = {steel: 4}
    for i in range(2):
        result = detroit.record_supply_state(steel)
    assert detroit.supply_history == {steel: [6, 6, None, None, 6, 6]}
    assert result is True

def test_get_average_supply_score_ignores_inactive_turns():
    detroit = City("Detroit")
    steel = Good("steel", 100)
    detroit.supply_history = {steel: [6, 6, None, None, 6, 6]}

    result = detroit.get_average_supply_score(steel)

    assert result == 6

def test_get_average_supply_score_returns_none_when_history_has_no_active_turns():
    detroit = City("Detroit")
    steel = Good("steel", 100)
    detroit.supply_history = {steel: [None, None, None, None]}

    result = detroit.get_average_supply_score(steel)

    assert result == None

def test_get_average_supply_score_returns_none_when_good_has_no_history():
    detroit = City("Detroit")
    steel = Good("steel", 100)

    result = detroit.get_average_supply_score(steel)

    assert result == None

def test_historical_supply_multiplier_interpolates_fractional_score():
    detroit = City("Detroit")
    steel = Good("steel", 100)
    detroit.supply_history = {steel: [5, 6]}

    result = detroit.get_historical_supply_multiplier(steel)

    assert result == 0.925

def test_historical_supply_multiplier_returns_neutral_when_no_active_history():
    detroit = City("Detroit")
    steel = Good("steel", 100)
    detroit.supply_history = {steel: [None, None, None, None]}

    result = detroit.get_historical_supply_multiplier(steel)

    assert result == 1