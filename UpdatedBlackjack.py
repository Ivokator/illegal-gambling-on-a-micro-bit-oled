import random
from typing import List, Callable

# Constants
INITIAL_POINTS = 10
INITIAL_BET = 1

FACE_CARD_VALUE = 10  # Face cards (J, Q, K) are worth 10

deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
blackjack_goal = 21  # Reset every round

# Wildcard system
class Wildcard:
    def __init__(self, name: str, description: str, effect: Callable, stays_on_table: bool = False):
        self.name = name
        self.description = description
        self.effect = effect
        self.stays_on_table = stays_on_table

def switch_last_draw(player, bot):
    """Switch the last drawn card between player and bot."""
    if player.last_draw and bot.last_draw:
        player.last_draw, bot.last_draw = bot.last_draw, player.last_draw
        print("Switched last drawn cards!")

def change_goal_to_17(player, bot):
    """Change the blackjack goal to 17."""
    global blackjack_goal
    blackjack_goal = 17
    print("Blackjack goal is now 17!")

def change_goal_to_24(player, bot):
    """Change the blackjack goal to 24."""
    global blackjack_goal
    blackjack_goal = 24
    print("Blackjack goal is now 24!")

def remove_last_wildcard(player, bot):
    """Removes opponent's last placed wildcard, reverting its effects."""
    if bot.placed_wildcards:
        bot.placed_wildcards.pop()
        print("Opponent's last wildcard has been removed!")

def give_random_wildcards(player, bot):
    """Gives both players a random wildcard that is not added to their permanent deck."""
    player_wildcard = random.choice(wildcards)
    bot_wildcard = random.choice(wildcards)
    player.placed_wildcards.append(player_wildcard)
    bot.placed_wildcards.append(bot_wildcard)
    print(f"Player received temporary wildcard: {player_wildcard.name}")
    print(f"Bot received temporary wildcard: {bot_wildcard.name}")

def increase_bet(player, bot):
    """Increases the bet by one."""
    global bet
    bet += 1
    print("Bet increased by 1!")

def decrease_bet(player, bot):
    """Decreases the bet by one."""
    global bet
    bet = max(1, bet - 1)
    print("Bet decreased by 1!")

def copy_last_wildcard(player, bot):
    """Copies the opponent's last placed wildcard and uses it."""
    if bot.placed_wildcards:
        copied_wildcard = bot.placed_wildcards[-1]
        copied_wildcard.effect(player, bot)
        print(f"Copied and used {copied_wildcard.name}!")

def return_last_drawn_card(player, bot):
    """Places the last drawn card back into the deck."""
    if player.last_draw:
        deck.append(player.last_draw)
        player.hand.remove(player.last_draw)
        print("Last drawn card returned to the deck!")

def average_hand(player, bot):
    """Takes the average of all cards in hand and assigns that number to all cards."""
    if player.hand:
        avg_value = round(sum(player.hand) / len(player.hand))
        player.hand = [avg_value] * len(player.hand)
        print("All cards in hand changed to the average value!")

def remove_low_values(player, bot):
    """Removes 1s and 2s from the deck."""
    global deck
    deck = [card for card in deck if card > 2]
    print("All 1s and 2s removed from the deck!")

def make_player_invulnerable(player, bot):
    """User does not lose points this round."""
    player.invulnerable = True
    print("You are invulnerable this round!")

def reveal_hidden_card(player, bot):
    """Reveals the bot's hidden card."""
    print(f"Bot's hidden card: {bot.hand[0]}")

def subtract_five_from_hand(player, bot):
    """Subtracts 5 from the user's hand."""
    player.hand = [max(0, card - 5) for card in player.hand]
    print("5 subtracted from your hand!")

def reveal_bot_wildcards(player, bot):
    """Reveals the bot's wildcard hand."""
    if bot.wildcard_deck:
        print("Bot's wildcards:", ', '.join([wc.name for wc in bot.wildcard_deck]))
    else:
        print("Bot has no wildcards.")

wildcards = [
    Wildcard("Switch Last Draw", "Swap last drawn card with bot's.", switch_last_draw),
    Wildcard("Moon", "Change blackjack goal to 17.", change_goal_to_17, True),
    Wildcard("Sun", "Change blackjack goal to 24.", change_goal_to_24, True),
    Wildcard("Death", "Removes opponent's last wildcard.", remove_last_wildcard),
    Wildcard("Strength", "Both players get a random wildcard.", give_random_wildcards),
    Wildcard("The Devil", "Increase bet by 1.", increase_bet, True),
    Wildcard("Cautious", "Decrease bet by 1.", decrease_bet, True),
    Wildcard("The Fool", "Copy opponent's last wildcard.", copy_last_wildcard),
    Wildcard("The Magician", "Return last drawn card to deck.", return_last_drawn_card),
    Wildcard("Temperance", "Average all hand cards.", average_hand),
    Wildcard("The High Priestess", "Remove all 1s and 2s.", remove_low_values),
    Wildcard("Justice", "Cannot lose points this round.", make_player_invulnerable, True),
    Wildcard("The Chariot", "Reveal opponent's hidden card.", reveal_hidden_card),
    Wildcard("The Lovers", "Subtract 5 from hand.", subtract_five_from_hand, True),
    Wildcard("The Hierophant", "Reveal opponent's wildcards.", reveal_bot_wildcards)
]

# Add feature to display wildcard table and reset it after each round
player_placed_wildcards: list = []
bot_placed_wildcards: list = []

def clear_wildcard_table():
    global player_placed_wildcards, bot_placed_wildcards
    player_placed_wildcards.clear()
    bot_placed_wildcards.clear()
class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand: list = []
        self.points = INITIAL_POINTS
        self.last_draw : int
        self.wildcard_deck: list = []
        self.standing = False

    def reset_hand(self):
        self.hand = []
        self.last_draw = None
        self.standing = False

    def draw_card(self, deck: List[int]):
        if deck:
            card = deck.pop()
            self.hand.append(card)
            self.last_draw = card
            print(f"{self.name} drew a card")
            if random.random() < 0.2:  # 20% chance to get a wildcard on draw
                new_wildcard = random.choice(wildcards)
                self.wildcard_deck.append(new_wildcard)
                print(f"You received a wildcard: {new_wildcard.name}")

    def play_wildcard(self, wildcard, opponent):
        print(f"{self.name} played wildcard: {wildcard.name}")
        wildcard.effect(self, opponent)
        self.wildcard_deck.remove(wildcard)

class Bot(Player):
    def __init__(self, difficulty: int):
        super().__init__("Bot")
        self.difficulty = difficulty

    def make_decision(self, deck: List[int], player):
        known_cards = set(player.hand + self.hand)
        remaining_deck = [card for card in deck if card not in known_cards]
        
        if self.wildcard_deck and random.random() < 0.3:  # 30% chance to use a wildcard
            wildcard = random.choice(self.wildcard_deck)
            self.play_wildcard(wildcard, player)
        elif sum(self.hand) >= blackjack_goal:
            self.standing = True
            print("Bot stands.")
        else:
            bust_chance = sum(1 for card in remaining_deck if sum(self.hand) + card > blackjack_goal) / len(remaining_deck)
            if bust_chance < 0.4:  # Only hit if there's a low chance of busting
                self.draw_card(deck)
                print("Bot hits.")
            else:
                self.standing = True
                print("Bot stands.")

# Game loop setup
def play_game(difficulty):
    global blackjack_goal
    player = Player("You")
    bot = Bot(difficulty)
    bet = INITIAL_BET
    
    while player.points > 0 and bot.points > 0:
        blackjack_goal = blackjack_goal  # Reset goal every round
        deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]  # Reset deck each round
        random.shuffle(deck)
        player.reset_hand()
        bot.reset_hand()
        
        player.draw_card(deck)
        bot.draw_card(deck)
        bot.draw_card(deck)  # Bot gets a second card immediately
        
        while not (player.standing and bot.standing):
            print(f"\nYour hand: {player.hand} (Total: {sum(player.hand)})")
            print("Bot's hand: [?] + " + str(bot.hand[1:]))  # Hide the first bot card
            print(str(player.wildcard_deck), "\n")
            if not player.standing:
                action = input("Do you want to (d)raw a card, (s)tand, or (w)ildcard? ").lower()
                if action == 'd':
                    player.draw_card(deck)
                elif action == 's':
                    player.standing = True
                    if random.random() < 0.2:  # 20% chance to get a wildcard on stand
                        new_wildcard = random.choice(wildcards)
                        player.wildcard_deck.append(new_wildcard)
                        print(f"You received a wildcard: {new_wildcard.name}")
                elif action == 'w' and player.wildcard_deck:
                    print("Choose a wildcard to play:")
                    for i, wc in enumerate(player.wildcard_deck):
                        print(f"{i+1}. {wc.name}: {wc.description}")
                    choice = int(input("Enter the number of the wildcard: ")) - 1
                    if 0 <= choice < len(player.wildcard_deck):
                        player.play_wildcard(player.wildcard_deck[choice], bot)
            
            if not bot.standing:
                bot.make_decision(deck, player)
        
        print(f"Bot's full hand: {bot.hand} (Total: {sum(bot.hand)})")
        
        if sum(player.hand) > blackjack_goal:
            print("You busted! Bot wins the round.")
            player.points -= bet
            bot.points += bet
        elif sum(bot.hand) > blackjack_goal:
            print("Bot busted! You win the round.")
            bot.points -= bet
            player.points += bet
        else:
            if sum(player.hand) > sum(bot.hand):
                print("You win the round!")
                player.points += bet
                bot.points -= bet
            else:
                print("Bot wins the round!")
                player.points -= bet
                bot.points += bet
        
        bet += 1
        print(f"Your points: {player.points} | Bot points: {bot.points}\n")
    
    print("Game over!")

def main_menu():
    print("Welcome to Blackjack Variant!")
    difficulty = int(input("Select bot difficulty (1-4): "))
    play_game(difficulty)

if __name__ == "__main__":
    main_menu()
