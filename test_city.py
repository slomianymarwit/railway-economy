from city import City

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