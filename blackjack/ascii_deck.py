"""
ascii_deck.py

Provides functions to render playing cards as ASCII art.
- create_card_join(): for side-by-side card rendering
- create_card_solo(): for single card display
"""

__all__ = ["create_card_join", "create_card_solo", "ranks", "suits"]

ranks = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
suits = ["♠","♡","♣","♢"]

# Used for displaying multiple cards side by side in ASCII art.
def create_card_join(card):
    rank, suit = card
    return ("+---------+",
f"|{rank:<2}       |",
"|         |",
f"|    {suit}    |",
"|         |",
f"|       {rank:>2}|",
"+---------+")

# Used for displaying a single card in ASCII art (e.g., the dealer's hand while he has a hidden card).       
def create_card_solo(card):
     rank, suit = card
     return ("+---------+\n"
f"|{rank:<2}       |\n"
"|         |\n"
f"|    {suit}    |\n"
"|         |\n"
f"|       {rank:>2}|\n"
"+---------+")

if __name__ == "__main__":
    print(create_card_solo(("A","♠")))