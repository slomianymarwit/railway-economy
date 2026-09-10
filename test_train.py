from locomotive import Locomotive
from train import Train
from connection import Connection
from city import City
import pytest

def test_create_a_train():
    locomotive1 = Locomotive("TierI", 25, 2)
    locomotive2 = Locomotive("TierI", 50, 4)
    train1 = Train("First Train", locomotive1, 1)
    train2 = Train("Second Train", locomotive2, 1)

    assert train1.locomotive is locomotive1
    assert train1.locomotive.tier == locomotive1.tier
    assert train1.locomotive.speed == locomotive1.speed
    assert train1.locomotive.max_number_of_cars == locomotive1.max_number_of_cars

    assert train2.locomotive is locomotive2
    assert train2.locomotive.tier == locomotive2.tier
    assert train2.locomotive.speed == locomotive2.speed
    assert train2.locomotive.max_number_of_cars == locomotive2.max_number_of_cars

def test_cars_quantity_cant_exceed_cars_limit():
    starting_cars = 1
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, starting_cars)

    result = train.set_cars(3)

    assert train.cars == starting_cars
    assert result is False

def test_cars_quantity_cant_be_lower_than_one():
    starting_cars = 1
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, starting_cars)
    
    result = train.set_cars(0)

    assert train.cars == starting_cars
    assert result is False

def test_cars_quantity_change_if_its_more_than_zero_and_less_than_limit():
    starting_cars = 1
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, starting_cars)

    result = train.set_cars(2)

    assert train.cars == 2
    assert result is True

def test_cant_create_a_train_with_cars_outside_limit():
    locomotive = Locomotive("TierI", 25, 2)

    with pytest.raises(ValueError):
        Train("First Train", locomotive, 999)
    with pytest.raises(ValueError):
        Train("First Train", locomotive, 0)

def test_train_moving_forward():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)
    connection = Connection(None, None, 40)
    train.assign_route([connection])

    train.move()

    assert train.distance_on_connection == 25

def test_train_moving_forward_multiple_turns():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)
    connection = Connection(None, None, 60)
    train.assign_route([connection])

    train.move()
    assert train.distance_on_connection == 25

    train.move()
    assert train.distance_on_connection == 50

def test_train_moving_forward_multiple_turns_and_stop_in_destination():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)
    connection = Connection(None, None, 60)
    train.assign_route([connection])

    train.move()
    assert train.distance_on_connection == 25

    train.move()
    assert train.distance_on_connection == 50

    train.move()
    assert train.distance_on_connection == connection.distance

def test_train_stops_moving_forward_after_reach_destination():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)
    connection = Connection(None, None, 25)
    train.assign_route([connection])

    train.move()
    assert train.distance_on_connection == 25

    train.move()
    assert train.distance_on_connection == 25

def test_train_moving_forward_along_connection():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)
    connection = Connection(None, None, 40)
    train.assign_route([connection])

    train.move()
    assert train.distance_on_connection == 25

    train.move()
    assert train.distance_on_connection == connection.distance

def test_train_moving_forward_along_its_own_connection():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)
    connection = Connection(None, None, 40)
    train.assign_route([connection])

    train.move()
    assert train.distance_on_connection == 25

    train.move()
    assert train.distance_on_connection == train.route[train.current_connection_index].distance

def test_train_try_to_move_without_connection_assigned():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)

    result = train.move()

    assert train.distance_on_connection == 0
    assert result is False

def test_train_try_to_move_when_connection_ended():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)
    connection = Connection(None, None, 40)

    train.assign_route([connection])
    train.move()
    train.move()
    result = train.move()

    assert train.distance_on_connection == 40
    assert result is False

def test_connection_use_city_names():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)
    chicago = City("Chicago")
    detroit = City("Detroit")
    connection = Connection(chicago, detroit, 40)

    train.assign_route([connection])

    assert train.route[train.current_connection_index].start is chicago
    assert train.route[train.current_connection_index].end is detroit

def test_take_second_connection_after_first_with_correct_left_distance_assign():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)
    chicago = City("Chicago")
    detroit = City("Detroit")
    cleveland = City("Cleveland")
    connection1 = Connection(chicago, detroit, 40)
    connection2 = Connection(detroit, cleveland, 60)

    train.assign_route([connection1, connection2])
    assert train.route[train.current_connection_index] is connection1

    train.move()
    train.move()
    train.move()

    assert train.route[train.current_connection_index] is connection2
    assert train.distance_on_connection == 35

def test_completing_more_than_one_connections_in_one_move():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)
    chicago = City("Chicago")
    detroit = City("Detroit")
    cleveland = City("Cleveland")
    connection1 = Connection(chicago, detroit, 10)
    connection2 = Connection(detroit, cleveland, 10)
    connection3 = Connection(cleveland, chicago, 60)

    train.assign_route([connection1, connection2, connection3])
    train.move()

    assert train.route[train.current_connection_index] is connection3
    assert train.distance_on_connection == 5

def test_train_ends_exactly_at_the_end_of_the_connection_and_is_assigned_the_next_one():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)
    chicago = City("Chicago")
    detroit = City("Detroit")
    cleveland = City("Cleveland")
    connection1 = Connection(chicago, detroit, 25)
    connection2 = Connection(detroit, cleveland, 50)

    train.assign_route([connection1, connection2])
    result = train.move()

    assert train.route[train.current_connection_index] is connection2
    assert train.distance_on_connection == 0
    assert result is True

def test_move_returns_false_when_train_already_reached_route_end():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)
    chicago = City("Chicago")
    detroit = City("Detroit")
    cleveland = City("Cleveland")
    connection1 = Connection(chicago, detroit, 25)
    connection2 = Connection(detroit, cleveland, 10)

    train.assign_route([connection1, connection2])
    train.move()
    result = train.move()

    assert train.route[train.current_connection_index] is connection2
    assert train.distance_on_connection == 10
    assert result is True

    result = train.move()
    assert result is False

def test_assign_route_returns_false_for_disconnected_route():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)
    chicago = City("Chicago")
    detroit = City("Detroit")
    cleveland = City("Cleveland")
    boston = City("Boston")
    connection1 = Connection(chicago, detroit, 25)
    connection2 = Connection(boston, cleveland, 10)

    result = train.assign_route([connection1, connection2])

    assert train.route is None
    assert train.distance_on_connection == 0
    assert result is False

def test_assign_route_accepts_continuous_route():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)
    chicago = City("Chicago")
    detroit = City("Detroit")
    cleveland = City("Cleveland")
    connection1 = Connection(chicago, detroit, 25)
    connection2 = Connection(detroit, cleveland, 10)

    result = train.assign_route([connection1, connection2])

    assert train.route == [connection1, connection2]
    assert train.distance_on_connection == 0
    assert result is True

def test_assign_route_returns_false_for_empty_route():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)

    result = train.assign_route([])

    assert train.route is None
    assert train.distance_on_connection == 0
    assert result is False

def test_assign_route_accepts_single_connection():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)
    chicago = City("Chicago")
    detroit = City("Detroit")
    connection1 = Connection(chicago, detroit, 25)

    result = train.assign_route([connection1])

    assert train.route == [connection1]
    assert train.distance_on_connection == 0
    assert result is True

def test_move_stops_at_planned_stop_and_does_not_use_remaining_distance():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)
    chicago = City("Chicago")
    detroit = City("Detroit")
    cleveland = City("Cleveland")
    connection1 = Connection(chicago, detroit, 10)
    connection2 = Connection(detroit, cleveland, 40)

    train.stops = [detroit]
    train.assign_route([connection1, connection2])
    result = train.move()

    assert train.current_city is detroit
    assert train.distance_on_connection == 0
    assert train.current_connection_index == 1
    assert result is True

def test_move_does_not_set_current_city_when_passing_through_city():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)
    chicago = City("Chicago")
    detroit = City("Detroit")
    cleveland = City("Cleveland")
    connection1 = Connection(chicago, detroit, 10)
    connection2 = Connection(detroit, cleveland, 40)

    train.assign_route([connection1, connection2])
    result = train.move()

    assert train.current_city is None
    assert train.distance_on_connection == 15
    assert train.current_connection_index == 1
    assert result is True

def test_move_returns_false_when_train_is_stopped_at_planned_stop():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)
    chicago = City("Chicago")
    detroit = City("Detroit")
    cleveland = City("Cleveland")
    connection1 = Connection(chicago, detroit, 10)
    connection2 = Connection(detroit, cleveland, 40)

    train.stops = [detroit]
    train.assign_route([connection1, connection2])
    result = train.move()

    assert train.current_city is detroit
    assert train.distance_on_connection == 0
    assert train.current_connection_index == 1
    assert result is True

    result = train.move()

    assert train.current_city is detroit
    assert train.distance_on_connection == 0
    assert train.current_connection_index == 1
    assert result is False

def test_depart_allows_train_to_continue_route():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)
    chicago = City("Chicago")
    detroit = City("Detroit")
    cleveland = City("Cleveland")
    connection1 = Connection(chicago, detroit, 10)
    connection2 = Connection(detroit, cleveland, 40)

    train.stops = [detroit]
    train.assign_route([connection1, connection2])
    result = train.move()

    assert train.current_city is detroit
    assert train.distance_on_connection == 0
    assert train.current_connection_index == 1
    assert result is True

    train.depart()
    result = train.move()

    assert train.current_city is None
    assert train.distance_on_connection == 25
    assert train.current_connection_index == 1
    assert result is True

def test_depart_clears_current_city():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)
    detroit = City("Detroit")

    train.current_city = detroit
    train.depart()
    train.move()

    assert train.current_city is None

def test_train_starts_with_empty_cargo():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)

    assert train.cargo == {}

def test_train_cannot_load_more_carloads_than_number_of_cars():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 1)

    assert train.cargo <= train.cars

def test_load_cargo_adds_carloads_to_train():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 2)

    result = train.load_cargo("steel", 1)

    assert train.cargo == {"steel": 1}
    assert result is True

def test_train_cannot_load_more_carloads_than_number_of_cars():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 2)

    result = train.load_cargo("steel", 3)

    assert train.cargo == {}
    assert result is False

def test_load_cargo_adds_to_existing_good_quantity():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 2)

    train.load_cargo("steel", 1)
    train.load_cargo("steel", 1)

    assert train.cargo == {"steel": 2}

def test_load_cargo_cannot_exceed_remaining_train_capacity():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 2)
    train.cargo = {"steel": 2}

    train.load_cargo("steel", 1)

    assert train.cargo == {"steel": 2}

def test_load_cargo_rejects_zero_or_negative_quantity():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 2)

    result = train.load_cargo("steel", 0)

    assert train.cargo == {}
    assert result is False

    result = train.load_cargo("steel", -1)

    assert train.cargo == {}
    assert result is False

def test_load_cargo_accepts_quantity_equal_to_remaining_capacity():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 2)
    train.cargo = {"steel": 1}

    result = train.load_cargo("steel", 1)

    assert train.cargo == {"steel": 2}
    assert result is True

def test_failed_load_cargo_does_not_change_existing_cargo():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 2)
    train.cargo = {"steel": 1}

    result = train.load_cargo("grain", 2)

    assert train.cargo == {"steel": 1}
    assert result is False

def test_unload_cargo_reduces_carload_quantity():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 2)
    train.cargo = {"steel": 2}

    result = train.unload_cargo("steel", 1)

    assert train.cargo == {"steel": 1}
    assert result is True

def test_unload_cargo_removes_good_when_quantity_reaches_zero():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 2)
    train.cargo = {"steel": 1}

    result = train.unload_cargo("steel", 1)

    assert train.cargo == {}
    assert result is True

def test_unload_cargo_cannot_remove_more_than_train_carries():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 2)
    train.cargo = {"steel": 1}

    result = train.unload_cargo("steel", 2)

    assert train.cargo == {"steel": 1}
    assert result is False

def test_unload_cargo_rejects_zero_or_negative_quantity():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 2)
    train.cargo = {"steel": 1}

    result = train.unload_cargo("steel", 0)

    assert train.cargo == {"steel": 1}
    assert result is False

    result = train.unload_cargo("steel", -1)
    
    assert train.cargo == {"steel": 1}
    assert result is False

def test_unload_cargo_returns_false_when_good_is_not_on_train():
    locomotive = Locomotive("TierI", 25, 2)
    train = Train("First Train", locomotive, 2)
    train.cargo = {"steel": 1}

    result = train.unload_cargo("grain", 1)

    assert train.cargo == {"steel": 1}
    assert result is False