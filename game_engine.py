from dataclasses import dataclass
from collections import Counter
from itertools import combinations
import random

RANKS = '23456789TJQKA'
SUITS = 'CDHS'
RANK_VALUE = {rank: i + 2 for i, rank in enumerate(RANKS)}
CATEGORY_NAMES = {1: 'High Card', 2: 'Pair', 3: 'Color', 4: 'Sequence', 5: 'Pure Sequence', 6: 'Trail'}

@dataclass(frozen=True)
class Card:
    rank: str
    suit: str

    def __post_init__(self):
        if self.rank not in RANKS or self.suit not in SUITS:
            raise ValueError('Invalid card')

    def __str__(self):
        return f'{self.rank}{self.suit}'


def new_deck():
    return [Card(rank, suit) for suit in SUITS for rank in RANKS]


def sequence_strength(values):
    """Standard house default: A-2-3 highest, A-K-Q second, then K-Q-J ... 4-3-2."""
    ranks = set(values)
    if ranks == {14, 2, 3}:
        return 15
    if ranks == {14, 13, 12}:
        return 14
    ordered = sorted(ranks)
    if len(ranks) == 3 and ordered[2] - ordered[0] == 2:
        return ordered[2]
    return None


def evaluate_hand(cards):
    if len(cards) != 3 or len(set(cards)) != 3:
        raise ValueError('A hand must contain three different cards')
    values = [RANK_VALUE[card.rank] for card in cards]
    counts = Counter(values)
    flush = len({card.suit for card in cards}) == 1
    straight = sequence_strength(values)
    if len(counts) == 1:
        return (6, values[0])
    if flush and straight is not None:
        return (5, straight)
    if straight is not None:
        return (4, straight)
    if flush:
        return (3, *sorted(values, reverse=True))
    if 2 in counts.values():
        pair = next(value for value, count in counts.items() if count == 2)
        kicker = next(value for value, count in counts.items() if count == 1)
        return (2, pair, kicker)
    return (1, *sorted(values, reverse=True))


def compare_hands(first, second):
    a, b = evaluate_hand(first), evaluate_hand(second)
    return (a > b) - (a < b)


def deal_hands(player_count, rng=None):
    if not 2 <= player_count <= 17:
        raise ValueError('Player count must be between 2 and 17')
    rng = rng or random.Random()
    deck = new_deck()
    rng.shuffle(deck)
    return [deck[i * 3:(i + 1) * 3] for i in range(player_count)]


def estimate_win_rate(hand, opponents=1, trials=3000, seed=None):
    if not 1 <= opponents <= 16:
        raise ValueError('Opponents must be between 1 and 16')
    if trials < 1:
        raise ValueError('Trials must be positive')
    if len(hand) != 3 or len(set(hand)) != 3:
        raise ValueError('Choose three unique cards')
    rng = random.Random(seed)
    remaining = [card for card in new_deck() if card not in hand]
    score = 0.0
    our_score = evaluate_hand(hand)
    for _ in range(trials):
        draw = rng.sample(remaining, 3 * opponents)
        opponents_scores = [evaluate_hand(draw[i * 3:(i + 1) * 3]) for i in range(opponents)]
        best = max([our_score, *opponents_scores])
        if our_score == best:
            score += 1 / (1 + sum(other == best for other in opponents_scores))
    return score / trials
