import random

class DeckOfCards:
    # class to represent a deck of playing cards
    suits = ['hearts', 'diamonds', 'clubs', 'spades']
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]

    def __init__(self):
        self.cards = [self.Card(suit, rank) for suit in self.suits for rank in self.ranks]

    def shuffle(self):
        # method to shuffle the deck
        random.shuffle(self.cards)

    class Card:
        # nested class to represent a playing card
        def __init__(self, suit, value):
            self.suit = suit
            self.value = value

        def __str__(self):
            return f"{self.value} of {self.suit}"
