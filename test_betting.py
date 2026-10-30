
from betting_engine import Player, BettingRound

players = [
    Player("Gaurab", 100),
    Player("Arslan", 100),
    Player("Peter", 100),
]

game = BettingRound(players, boot=1)

game.start()

print("Starting pot:", game.pot)

game.bet(players[0], 5)
game.see_cards(players[1])
game.fold(players[2])

print("\nUpdated pot:", game.pot)

for player in players:
    print(
        player.name,
        "| Balance:", player.bankroll,
        "| Seen:", player.seen,
        "| Folded:", player.folded
    )

print("\nGame history:")
for action in game.history:
    print("-", action)
