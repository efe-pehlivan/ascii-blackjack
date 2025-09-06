"""
blackjack.py

A console-based Blackjack game featuring ASCII card graphics.
Play against a dealer and try to reach 21 without going over.

Features:
- Start with 10,000 credits.
- Bet any amount per hand; enter 0 to leave the table and cash out.
- Choose between 6 to 8 decks; reshuffles automatically when the deck is low.
- Player actions: Hit, Stand, or Double Down.
- Dealer always stands on soft 17.
- Blackjack (Ace + 10-value card as the initial hand) pays 3:2 *if the player wins*.
- If both player and dealer have Blackjack, the result is a push.
- Ties (equal totals) return the bet (no gain or loss).
- Hands displayed using side-by-side ASCII art for clarity.
- Dealer's second card remains hidden until the player's turn is over.
- Hand values shown after each action to aid decision-making.
- Realistic pacing with short delays to simulate card dealing.
- Robust input validation and informative error messages.
- Cards are drawn randomly from a finite, non-repeating deck.
- The game starts with a low deck, which is reshuffled when it runs low again.
"""
try:
    from ascii_deck import *
except ImportError:
    print("Error: 'ascii_deck.py' module not found. Please make sure it exists in the same directory as 'blackjack.py'.")
    exit()
import random
import time

credits = 10000
deck = []
deck_number = 0

def draw_card():
    return deck.pop(random.randrange(len(deck)))

# Displays cards in hand side by side using ASCII art.
def show_hand(hand):
     ascii_cards = [create_card_join(card) for card in hand]
     for i in range(7):
          print(' '.join(line[i] for line in ascii_cards))

# Calculates total hand value, adjusting for Aces if needed.
def points(hand):
     value=0
     aces=0
     for rank, suit in hand:
          if rank == "A":
               value += 11
               aces += 1
          elif rank == "J":
               value += 10
          elif rank == "Q":
               value += 10
          elif rank == "K":
               value += 10
          else:
               value+=int(rank)
     while value > 21 and aces > 0:
      value -= 10
      aces -= 1
     return value

# Returns True if the hand is a Blackjack (21 with two cards).
def is_blackjack(hand):
    return points(hand) == 21 and len(hand) == 2

# Messages are inline to simplify flow and allow scenario-specific responses.
def play():
    global multiplier
    global bet
    while points(player_hand) < 21:
        x = input("What do you want to do? (Hit = 1 Double = 2 Stand = 3)\n")
        if x == "1":
            player_hand.append(draw_card())
            if points(player_hand) > 21:
                print(f"Dealer's Hand: {points(dealer_hand)} (Dealer always stands on soft 17.)")
                show_hand(dealer_hand)
                print(f"----------------------------------VS---------------------------------- DEALER WON {bet}")
                show_hand(player_hand)
                print(f"Your Hand: {points(player_hand)}")
                return "dealer"
            elif points(player_hand) == 21:
                print(f"Dealer's Hand: {points(dealer_hand)} (Dealer always stands on soft 17.)")
                show_hand(dealer_hand)
                print("----------------------------------VS----------------------------------")
                show_hand(player_hand)
                print(f"Your Hand: {points(player_hand)}")
                return dealer_plays()
            else:
                print(f"Dealer's Hand: {dealer_hand[0][0]} (Second card is hidden. Dealer stands on soft 17.)")
                print(create_card_solo(dealer_hand[0]))
                print("----------------------------------VS----------------------------------")
                show_hand(player_hand)
                print(f"Your Hand: {points(player_hand)}")

        elif x == "2":
            if bet * 2 > credits:
                print("Not enough credits to double down.")
                continue
            player_hand.append(draw_card())
            bet *= 2
            if points(player_hand) > 21:
                print(f"Dealer's Hand: {points(dealer_hand)} (Dealer always stands on soft 17.)")
                show_hand(dealer_hand)
                print(f"----------------------------------VS---------------------------------- DEALER WON {bet}")
                show_hand(player_hand)
                print(f"Your Hand: {points(player_hand)}")
                return "dealer"
            else:
                return dealer_plays()
            
        elif x == "3":
            return dealer_plays()
        else:
            print("Invalid input. Please enter 1, 2, or 3.")
    # BLACKJACK! or not?
    if is_blackjack(player_hand) and not is_blackjack(dealer_hand):
        multiplier = 1.5
        print(f"Dealer's Hand: {points(dealer_hand)} (Dealer always stands on soft 17.)")
        show_hand(dealer_hand)
        print(f"----------------------------------VS---------------------------------- PLAYER WON {bet*multiplier}!")
        show_hand(player_hand)
        print(f"Your Hand: {points(player_hand)}")
        return "player"
    elif is_blackjack(player_hand) and is_blackjack(dealer_hand):
        print(f"Dealer's Hand: {points(dealer_hand)} (Dealer always stands on soft 17.)")
        show_hand(dealer_hand)
        print("----------------------------------VS---------------------------------- PUSH")
        show_hand(player_hand)
        print(f"Your Hand: {points(player_hand)}")
        return "push"

def dealer_plays():
    global multiplier
    while points(dealer_hand) < 17:
        print(f"Dealer's Hand: {points(dealer_hand)} (Dealer always stands on soft 17.)")
        show_hand(dealer_hand)
        print("----------------------------------VS----------------------------------")
        show_hand(player_hand)
        print(f"Your Hand: {points(player_hand)}")
        dealer_hand.append(draw_card())
        time.sleep(3)
    if points(dealer_hand) > 21:
        print(f"Dealer's Hand: {points(dealer_hand)} (Dealer always stands on soft 17.)")
        show_hand(dealer_hand)
        print(f"----------------------------------VS---------------------------------- PLAYER WON {bet*multiplier}!")
        show_hand(player_hand)
        print(f"Your Hand: {points(player_hand)}")
        return "player"
    elif points(dealer_hand) > points(player_hand):
        print(f"Dealer's Hand: {points(dealer_hand)} (Dealer always stands on soft 17.)")
        show_hand(dealer_hand)
        print(f"----------------------------------VS---------------------------------- DEALER WON {bet}")
        show_hand(player_hand)
        print(f"Your Hand: {points(player_hand)}")
        return "dealer"
    elif points(dealer_hand) < points(player_hand):
        print(f"Dealer's Hand: {points(dealer_hand)} (Dealer always stands on soft 17.)")
        show_hand(dealer_hand)
        print(f"----------------------------------VS---------------------------------- PLAYER WON {bet*multiplier}!")
        show_hand(player_hand)
        print(f"Your Hand: {points(player_hand)}")
        return "player"
    else:
        print(f"Dealer's Hand: {points(dealer_hand)} (Dealer always stands on soft 17.)")
        show_hand(dealer_hand)
        print("----------------------------------VS---------------------------------- PUSH")
        show_hand(player_hand)
        print(f"Your Hand: {points(player_hand)}")
        return "push"
    

def blackjack():
    global player_hand, dealer_hand, bet, multiplier, credits, deck, deck_number

    dealer_hand = []
    player_hand = []

    # Reshuffle when the deck is low.
    if len(deck) < 50:
        print("Deck is low. Shuffling deck...", end='', flush=True)
        for i in range(10):
            time.sleep(1)
            print('.', end='', flush=True)
        print()
        deck = [(rank,suit) for rank in ranks for suit in suits] * deck_number

    while True:
        try:
            bet = int(input("Bet amount: "))
            if bet>credits:
                print(f"Bet can't be higher than credits. You have {credits} credits.")
                continue
            elif bet<0:
                print("Bet must be positive.")
                continue
            elif bet == 0:
                print(f"You left the table with {credits} credits.")
                exit()
            break
        except ValueError:
            print("Please enter a valid number.")
    
    
    multiplier = 1

    # Simulates card dealing delay.
    print("Dealing cards...", end="", flush=True)
    for i in range(3):
        print(".", end="", flush=True)
        time.sleep(1)
    print() # Moves cursor to the next line after dealing animation.

    player_hand.append(draw_card())
    player_hand.append(draw_card())
    dealer_hand.append(draw_card())
    dealer_hand.append(draw_card())


    print(f"Dealer's Hand: {dealer_hand[0][0]} (Second card is hidden. Dealer stands on soft 17.)")
    print(create_card_solo(dealer_hand[0]))
    print("----------------------------------VS----------------------------------")
    show_hand(player_hand)
    print(f"Your Hand: {points(player_hand)}")

    result = play()

    # Update credits based on outcome.
    if result == "player":
        credits += bet*multiplier
    elif result == "dealer":
        credits -= bet
    # Else, it is a push. No one wins, no one cries.
    print(f"\nCredits left: {credits}")

if __name__ == "__main__":
    
    print("Welcome to ASCII Blackjack!\n")
    time.sleep(1)
    print(f"Starting with {credits} credits.")
    time.sleep(1)

    while True:
        try:
            deck_number = int(input("How many decks do you want to play with? "))
            if 6 <= deck_number <= 8:
                break
            print("Deck number must be between 6 and 8.")

        except ValueError:
            print("Enter a valid number.")

    while credits > 0:
        blackjack()
    else:
        print("No credits left. The house always wins.")
        time.sleep(2)