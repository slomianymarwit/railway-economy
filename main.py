from player import Player
from company import Company

player1 = Player("Marcin", 500000)
player2 = Player("Bogdan", 500000)
fast_rails = Company("Fast rails")
happy_trains = Company("Happy Trains")

players = [player1, player2]
companies = [fast_rails, happy_trains]

def give_info():
    for player in players:
        print(f"""{player.name}:
    Money: {player.money};   Shares: {player.shares}""")
    for company in companies:
        print(f"""{company.name}:
    Money: {company.money};   Shares: {company.shares};   Shareholders: {company.shareholders};   President: {company.president}""")
    print("--------------------------------")

# give_info()
# player1.buy_shares(fast_rails, 100)
# player2.buy_shares(fast_rails, 10)
# give_info()
# player1.buy_shares(happy_trains, 50)
# player2.buy_shares(fast_rails, 410)
# give_info()
# player1.buy_shares(fast_rails, 400)
# player2.buy_shares(fast_rails, 2)
# give_info()
# player1.buy_shares(happy_trains, 201)
# player2.buy_shares(happy_trains, 250)
# give_info()
# player2.buy_shares(happy_trains, 1)
# give_info()

player2.buy_shares(fast_rails, 200)
give_info()
player1.buy_shares(fast_rails, 310)
give_info()
player2.buy_shares(fast_rails, 350)
give_info()