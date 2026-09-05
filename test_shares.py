from company import Company
from player import Player

def test_player_can_buy_shares():
    starting_money = 5000
    shares_quantity = 10
    player = Player("Test Player", starting_money)
    company = Company("Test Company")
    starting_shares_price = company.shares_price

    result = player.buy_shares(company, shares_quantity)

    assert player.money == starting_money - starting_shares_price * shares_quantity
    assert player.shares_in(company) == shares_quantity
    assert company.shares == company.all_shares - shares_quantity
    assert company.money == starting_shares_price * shares_quantity
    assert result is True


def test_player_cannot_buy_shares_without_enough_money():
    starting_money = 900
    shares_quantity = 10
    player = Player("Test Player", starting_money)
    company = Company("Test Company")

    result = player.buy_shares(company, shares_quantity)

    assert player.money == starting_money
    assert player.shares_in(company) == 0
    assert company.shares == company.all_shares
    assert company.money == 0
    assert result is False

def test_player_cannot_buy_more_shares_than_company_have():
    starting_money = 1000000
    player = Player("Test Player", starting_money)
    company = Company("Test Company")
    shares_quantity = company.all_shares + 1

    result = player.buy_shares(company, shares_quantity)

    assert player.money == starting_money
    assert player.shares_in(company) == 0
    assert company.shares == company.all_shares
    assert company.money == 0
    assert result is False

def test_player_cannot_buy_negative_number_of_shares():
    starting_money = 5000
    player = Player("Test Player", starting_money)
    company = Company("Test Company")
    shares_quantity = -10

    result = player.buy_shares(company, shares_quantity)

    assert player.money == starting_money
    assert player.shares_in(company) == 0
    assert company.shares == company.all_shares
    assert company.money == 0
    assert result is False

def test_player_cannot_buy_zero_shares():
    starting_money = 5000
    player = Player("Test Player", starting_money)
    company = Company("Test Company")
    shares_quantity = 0

    result = player.buy_shares(company, shares_quantity)

    assert player.money == starting_money
    assert player.shares_in(company) == 0
    assert company.shares == company.all_shares
    assert company.money == 0
    assert result is False

def test_company_changing_president():
    starting_money = 500000
    player1 = Player("Test Player1", starting_money)
    player2 = Player("Test Player2", starting_money)
    company = Company("Test Company")

    player1.buy_shares(company, 250)
    player2.buy_shares(company, 350)

    assert company.president == player2.name

    player1.buy_shares(company, 200)

    assert company.president == player1.name

def test_company_floats_after_50_percent_of_shares_are_sold():
    starting_money = 500000
    player = Player("Test Player", starting_money)
    company = Company("Test Company")

    player.buy_shares(company, 499)
    assert company.president is None

    player.buy_shares(company, 1)
    assert company.president == player.name

    player.buy_shares(company, 1)
    assert company.president == player.name

def test_player_can_check_number_of_shares_owned_in_company():
    starting_money = 500000
    player = Player("Test Player", starting_money)
    company = Company("Test Company")

    assert player.shares_in(company) == 0

    player.buy_shares(company, 100)
    assert player.shares_in(company) == 100

def test_tie_for_the_position_of_president():
    starting_money = 500000
    player1 = Player("Test Player1", starting_money)
    player2 = Player("Test Player2", starting_money)
    company = Company("Test Company")

    player2.buy_shares(company, 250)
    player1.buy_shares(company, 350)
    assert company.president == player1.name

    player2.buy_shares(company, 100)
    assert company.president == player1.name

    player2.buy_shares(company, 1)
    assert company.president == player2.name

def test_company_has_no_president_when_top_shareholders_are_tied():
    starting_money = 500000
    player1 = Player("Test Player1", starting_money)
    player2 = Player("Test Player2", starting_money)
    company = Company("Test Company")

    player2.buy_shares(company, 250)
    player1.buy_shares(company, 250)
    assert company.president is None

def test_single_shareholder_becomes_president_at_float_threshold():
    starting_money = 500000
    player = Player("Test Player", starting_money)
    company = Company("Test Company")

    player.buy_shares(company, 500)
    assert company.president == player.name

def test_company_has_floated_but_doesnt_have_president():
    starting_money = 500000
    player1 = Player("Test Player1", starting_money)
    player2 = Player("Test Player2", starting_money)
    company = Company("Test Company")

    player2.buy_shares(company, 250)
    player1.buy_shares(company, 250)
    assert company.is_floated is True
    assert company.president is None

def test_company_is_floated_after_50_percent_of_shares_are_sold():
    starting_money = 500000
    player = Player("Test Player", starting_money)
    company = Company("Test Company")

    player.buy_shares(company, 499)
    assert company.is_floated is False

    player.buy_shares(company, 1)
    assert company.is_floated is True

def test_floated_company_has_president_and_tie_in_shares_doesnt_change_that():
    starting_money = 500000
    player1 = Player("Test Player1", starting_money)
    player2 = Player("Test Player2", starting_money)
    company = Company("Test Company")

    player2.buy_shares(company, 250)
    player1.buy_shares(company, 255)
    assert company.president == player1.name

    player2.buy_shares(company, 5)
    assert company.president == player1.name

def test_first_tied_shareholder_becomes_president_after_float_threshold_is_exceeded():
    starting_money = 500000
    player1 = Player("Test Player1", starting_money)
    player2 = Player("Test Player2", starting_money)
    player3 = Player("Test Player3", starting_money)
    company = Company("Test Company")

    player1.buy_shares(company, 250)
    player2.buy_shares(company, 250)
    assert company.president is None

    player3.buy_shares(company, 1)
    assert company.president == player1.name