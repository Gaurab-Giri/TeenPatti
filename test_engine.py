import unittest
from game_engine import Card, evaluate_hand, compare_hands, deal_hands, estimate_win_rate

def hand(*tokens):
    return [Card(x[0], x[1]) for x in tokens]

class EngineTests(unittest.TestCase):
    def test_categories(self):
        examples = [
            (hand('AC','AD','AH'), 6),
            (hand('AS','2S','3S'), 5),
            (hand('4C','5D','6H'), 4),
            (hand('2H','5H','9H'), 3),
            (hand('KC','KD','2H'), 2),
            (hand('2C','6D','9H'), 1),
        ]
        for cards, category in examples:
            self.assertEqual(evaluate_hand(cards)[0], category)
    def test_order(self):
        self.assertEqual(compare_hands(hand('AC','AD','AH'), hand('KC','KD','KH')), 1)
        self.assertEqual(compare_hands(hand('AS','2S','3S'), hand('QS','KS','AS')), 1)
    def test_deal_unique(self):
        cards = [card for h in deal_hands(10) for card in h]
        self.assertEqual(len(cards), len(set(cards)))
    def test_probability(self):
        result = estimate_win_rate(hand('AC','AD','AH'), opponents=3, trials=100, seed=1)
        self.assertEqual(result, 1.0)

if __name__ == '__main__':
    unittest.main()
