
from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class Player:
    name: str
    bankroll: Decimal
    folded: bool = False
    seen: bool = False
    total_contributed: Decimal = Decimal("0.00")

    def pay(self, amount):
        """Deduct virtual chips from the player's balance."""
        amount = Decimal(str(amount))

        if amount <= 0:
            raise ValueError("Payment must be positive.")

        if amount > self.bankroll:
            raise ValueError(f"{self.name} has insufficient chips.")

        self.bankroll -= amount
        self.total_contributed += amount
        return amount


@dataclass
class BettingRound:
    players: list[Player]
    boot: Decimal
    pot: Decimal = Decimal("0.00")
    history: list[str] = field(default_factory=list)

    def start(self):
        """Collect the boot amount from every player."""
        self.boot = Decimal(str(self.boot))

        if self.boot <= 0:
            raise ValueError("Boot must be positive.")

        if len(self.players) < 2:
            raise ValueError("At least two players are required.")

        if any(player.bankroll < self.boot for player in self.players):
            raise ValueError("Every player must be able to pay the boot.")

        if self.history or self.pot != 0:
            raise ValueError("This round has already started.")

        for player in self.players:
            self.pot += player.pay(self.boot)

        self.history.append(f"Round started. Pot: {self.pot}")

    def bet(self, player, amount):
        """Add a player's virtual-chip bet to the pot."""
        if not self.history:
            raise ValueError("Start the round first.")

        if player not in self.players:
            raise ValueError("Player is not at this table.")

        if player.folded:
            raise ValueError("Folded players cannot bet.")

        if len(self.active_players()) < 2:
            raise ValueError("The round is already over.")

        paid = player.pay(amount)
        self.pot += paid
        self.history.append(f"{player.name} bet {paid}")
        return paid

    def fold(self, player):
        """Remove a player from the current round."""
        if not self.history:
            raise ValueError("Start the round first.")

        if player not in self.players:
            raise ValueError("Player is not at this table.")

        if player.folded:
            raise ValueError("Player has already folded.")

        if len(self.active_players()) < 2:
            raise ValueError("The round is already over.")

        player.folded = True
        self.history.append(f"{player.name} folded")

    def see_cards(self, player):
        """Mark a player's cards as seen."""
        if not self.history:
            raise ValueError("Start the round first.")

        if player not in self.players or player.folded:
            raise ValueError("Player is not active.")

        player.seen = True
        self.history.append(f"{player.name} viewed their cards")

    def active_players(self):
        return [player for player in self.players if not player.folded]
