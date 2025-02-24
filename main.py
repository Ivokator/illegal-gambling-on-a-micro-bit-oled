# Constants
INITIAL_POINTS = 10
INITIAL_BET = 1

FACE_CARD_VALUE = 10  # Face cards (J, Q, K) are worth 10

deck: List[number] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
blackjack_goal = 21  # Reset every round

bet = INITIAL_BET
OLED12864_I2C.init(60)


def win_round():
    music.play(music.tone_playable(262, music.beat(BeatFraction.WHOLE)),
        music.PlaybackMode.UNTIL_DONE)

toggle = 0
def change_toggle(toggle):
    global toggle
    if toggle == 0:
        pins.digital_write_pin(DigitalPin.P1, 1)
        pins.digital_write_pin(DigitalPin.P2, 0)
        pins.digital_write_pin(DigitalPin.P3, 0)
        toggle = 1
    elif toggle == 1:
        pins.digital_write_pin(DigitalPin.P1, 0)
        pins.digital_write_pin(DigitalPin.P2, 1)
        pins.digital_write_pin(DigitalPin.P3, 0)
        toggle = 2
    elif toggle == 2:
        pins.digital_write_pin(DigitalPin.P1, 0)
        pins.digital_write_pin(DigitalPin.P2, 0)
        pins.digital_write_pin(DigitalPin.P3, 1)
        toggle = 0
    print(toggle)


def round(n):
    n = n*1
    integer_part = int(n)  # Get the integer part
    decimal_part = n - integer_part  # Get the fractional part
    
    if decimal_part < 0.5:
        return integer_part  # Round down
    else:
        return integer_part + 1  # Round up

def sum(numbers):
    total = 0
    for n in numbers:
        total += n  # Ensure all inputs are converted to floats before summing
    return total

def len(lst):
    count = 0
    for _ in lst:
        count += 1
    return count

def set(lst):
    unique_items = []
    for item in lst:
        if item not in unique_items:
            unique_items.append(item)
    return unique_items

def custom_shuffle(lst: List[number]):
    length = len(lst)
    for i in range(length - 1, 0, -1):
        j = randint(0, i)
        temp  = lst[i]
        lst[i] = lst[j]
        lst[j] = temp

player = {
    "name": "Player",
    "points": INITIAL_POINTS,
    "last_draw": 0,
    "standing": False,
    "invulnerable": False,
}

player_hand: List[number] = []
player_wildcard_deck = [""]
player_placed_wildcards = []

bot = {
    "name": "Bot",
    "points": INITIAL_POINTS,
    "last_draw": 0,
    "standing": False,
    "invulnerable": False,
}

bot_hand: List[number] = []
bot_wildcard_deck = [""]
bot_placed_wildcards = []

"""
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
]
"""

wildcards = [
    {"name": "Justice", "description": "Swap last drawn card with bot."},
    {"name": "Moon", "description": "Change blackjack goal to 17."},
    {"name": "Sun", "description": "Change blackjack goal to 24."},
    {"name": "Death", "description": "Removes opponent's last wildcard."},
    {"name": "Strength", "description": "Both players get a random wildcard."},
    {"name": "The Devil", "description": "Increase bet by 1."},
    {"name": "The Star", "description": "Decrease bet by 1."},
    {"name": "The Fool", "description": "Copy opponent's last wildcard."},
    {"name": "The Magician", "description": "Return last drawn card to deck."},
    {"name": "Temperance", "description": "Average all hand cards."},
    {"name": "The Tower", "description": "Remove all 1s and 2s."},
    {"name": "The High Priestess", "description": "Cannot lose points this round."},
    {"name": "The Chariot", "description": "Reveal opponent's hidden card."},
    {"name": "The Lovers", "description": "Subtract 5 from hand."},
]


def bot_decision_draw(deck: List[int]):
    known_cards = set(player_hand + bot_hand)
    
    remaining_deck = []
    for card in known_cards:
        if card not in deck:
            remaining_deck.append(card)

    if bot_wildcard_deck and randint(0, 10) < 3:
        pass
    elif sum(bot_hand) >= blackjack_goal:
        bot["standing"] = True
        print("Bot stands.")
    else:
        n = 0
        for ncard in remaining_deck:
            if bot_hand + ncard > blackjack_goal:
                n += 1
        bust_chance = n / len(remaining_deck)

        if bust_chance < 0.4:
            bot_draw_card(deck)
            print("Bot hits.")
        else:
            bot["standing"] = True
            print("Bot stands.")


def player_draw_card(deck: List[int]):
    if deck:
        card: number = deck.pop()
        player_hand.append(card)
        player["last_draw"]: number = card
        print(f"Player drew a card")

        if randint(0, 10) < 2:  # 20% chance to get a wildcard on draw
            new_wildcard: string = wildcards._pick_random()['name']
            player_wildcard_deck.append(new_wildcard)
            print(f"You received a wildcard:" + new_wildcard)

def bot_draw_card(deck: List[int]):
    if deck:
        card: number = deck.pop()
        bot_hand.append(card)
        bot["last_draw"] = card
        print(f"Bot drew a card")

        if randint(0, 10) < 2:  # 20% chance to get a wildcard on draw
            new_wildcard: string = wildcards._pick_random()['name']
            bot_wildcard_deck.append(new_wildcard)
            print("Bot received a wildcard: " + new_wildcard)



cards = ['A', '2', '3']

def reset_hands():
    player["last_draw"] = 0
    bot["last_draw"] = 0

    player["standing"] = False
    bot["standing"] = False

    player_hand = []
    bot_hand = []

def play_blackjack():
    global blackjack_goal
    
    while player["points"] > 0 and bot["points"] > 0:
        
        deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
        custom_shuffle(deck)
        reset_hands()

        player_draw_card(deck)
        bot_draw_card(deck)
        bot_draw_card(deck)

        while not (player["standing"] and bot["standing"]):
            # HIT
            
            if input.button_is_pressed(Button.A):
                print("A!")
                player_draw_card(deck)

            # STAND
            elif input.button_is_pressed(Button.B):
                player["standing"] = True

                if randint(0, 10) < 2:  # 20% chance to get a wildcard on draw
                    new_wildcard: string = wildcards._pick_random()['name']
                    player_wildcard_deck.append(new_wildcard)
                    print(f"You received a wildcard:" + new_wildcard)

    if not bot["standing"]:
        bot_decision_draw(deck)




play_blackjack()


index = 0

for card in cards:
    card_to_display = " " + card
    OLED12864_I2C.show_string(index*2, 0, card_to_display, 1)
    index += 1