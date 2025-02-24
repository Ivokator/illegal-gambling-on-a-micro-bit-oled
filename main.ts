//  Constants
let INITIAL_POINTS = 10
let INITIAL_BET = 1
let FACE_CARD_VALUE = 10
//  Face cards (J, Q, K) are worth 10
let deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
let blackjack_goal = 21
//  Reset every round
let bet = INITIAL_BET
OLED12864_I2C.init(60)
function win_round() {
    music.play(music.tonePlayable(262, music.beat(BeatFraction.Whole)), music.PlaybackMode.UntilDone)
}

let toggle = 0
function change_toggle(toggle: number) {
    
    if (toggle == 0) {
        pins.digitalWritePin(DigitalPin.P1, 1)
        pins.digitalWritePin(DigitalPin.P2, 0)
        pins.digitalWritePin(DigitalPin.P3, 0)
        toggle = 1
    } else if (toggle == 1) {
        pins.digitalWritePin(DigitalPin.P1, 0)
        pins.digitalWritePin(DigitalPin.P2, 1)
        pins.digitalWritePin(DigitalPin.P3, 0)
        toggle = 2
    } else if (toggle == 2) {
        pins.digitalWritePin(DigitalPin.P1, 0)
        pins.digitalWritePin(DigitalPin.P2, 0)
        pins.digitalWritePin(DigitalPin.P3, 1)
        toggle = 0
    }
    
    console.log(toggle)
}

function round(n: number): number {
    n = n * 1
    let integer_part = Math.trunc(n)
    //  Get the integer part
    let decimal_part = n - integer_part
    //  Get the fractional part
    if (decimal_part < 0.5) {
        return integer_part
    } else {
        //  Round down
        return integer_part + 1
    }
    
}

//  Round up
function sum(numbers: any[]): number {
    let total = 0
    for (let n of numbers) {
        total += n
    }
    //  Ensure all inputs are converted to floats before summing
    return total
}

function len(lst: any[]): number {
    let count = 0
    for (let _ of lst) {
        count += 1
    }
    return count
}

function set(lst: any[]): any[] {
    let unique_items = []
    for (let item of lst) {
        if (unique_items.indexOf(item) < 0) {
            unique_items.push(item)
        }
        
    }
    return unique_items
}

function custom_shuffle(lst: number[]) {
    let j: number;
    let temp: number;
    let length = len(lst)
    for (let i = length - 1; i > 0; i += -1) {
        j = randint(0, i)
        temp = lst[i]
        lst[i] = lst[j]
        lst[j] = temp
    }
}

let player = {
    "name" : "Player",
    "points" : INITIAL_POINTS,
    "last_draw" : 0,
    "standing" : false,
    "invulnerable" : false,
}

let player_hand : number[] = []
let player_wildcard_deck = [""]
let player_placed_wildcards = []
let bot = {
    "name" : "Bot",
    "points" : INITIAL_POINTS,
    "last_draw" : 0,
    "standing" : false,
    "invulnerable" : false,
}

let bot_hand : number[] = []
let bot_wildcard_deck = [""]
let bot_placed_wildcards = []
/** 
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

 */
let wildcards = [ {
    "name" : "Justice",
    "description" : "Swap last drawn card with bot.",
}
, {
    "name" : "Moon",
    "description" : "Change blackjack goal to 17.",
}
, {
    "name" : "Sun",
    "description" : "Change blackjack goal to 24.",
}
, {
    "name" : "Death",
    "description" : "Removes opponent's last wildcard.",
}
, {
    "name" : "Strength",
    "description" : "Both players get a random wildcard.",
}
, {
    "name" : "The Devil",
    "description" : "Increase bet by 1.",
}
, {
    "name" : "The Star",
    "description" : "Decrease bet by 1.",
}
, {
    "name" : "The Fool",
    "description" : "Copy opponent's last wildcard.",
}
, {
    "name" : "The Magician",
    "description" : "Return last drawn card to deck.",
}
, {
    "name" : "Temperance",
    "description" : "Average all hand cards.",
}
, {
    "name" : "The Tower",
    "description" : "Remove all 1s and 2s.",
}
, {
    "name" : "The High Priestess",
    "description" : "Cannot lose points this round.",
}
, {
    "name" : "The Chariot",
    "description" : "Reveal opponent's hidden card.",
}
, {
    "name" : "The Lovers",
    "description" : "Subtract 5 from hand.",
}
]
function bot_decision_draw(deck: any[]) {
    let n: number;
    let bust_chance: number;
    let known_cards = set(player_hand.concat(bot_hand))
    let remaining_deck = []
    for (let card of known_cards) {
        if (deck.indexOf(card) < 0) {
            remaining_deck.push(card)
        }
        
    }
    if (bot_wildcard_deck && randint(0, 10) < 3) {
        
    } else if (sum(bot_hand) >= blackjack_goal) {
        bot["standing"] = true
        console.log("Bot stands.")
    } else {
        n = 0
        for (let ncard of remaining_deck) {
            if (bot_hand + ncard > blackjack_goal) {
                n += 1
            }
            
        }
        bust_chance = n / len(remaining_deck)
        if (bust_chance < 0.4) {
            bot_draw_card(deck)
            console.log("Bot hits.")
        } else {
            bot["standing"] = true
            console.log("Bot stands.")
        }
        
    }
    
}

function player_draw_card(deck: any[]) {
    let card: number;
    let new_wildcard: string;
    if (deck) {
        card = _py.py_array_pop(deck)
        player_hand.push(card)
        player["last_draw"] = card
        console.log("Player drew a card")
        if (randint(0, 10) < 2) {
            //  20% chance to get a wildcard on draw
            new_wildcard = wildcards._pickRandom()["name"]
            player_wildcard_deck.push(new_wildcard)
            console.log("You received a wildcard:" + new_wildcard)
        }
        
    }
    
}

function bot_draw_card(deck: any[]) {
    let card: number;
    let new_wildcard: string;
    if (deck) {
        card = _py.py_array_pop(deck)
        bot_hand.push(card)
        bot["last_draw"] = card
        console.log("Bot drew a card")
        if (randint(0, 10) < 2) {
            //  20% chance to get a wildcard on draw
            new_wildcard = wildcards._pickRandom()["name"]
            bot_wildcard_deck.push(new_wildcard)
            console.log("Bot received a wildcard: " + new_wildcard)
        }
        
    }
    
}

function reset_hands() {
    player["last_draw"] = 0
    bot["last_draw"] = 0
    player["standing"] = false
    bot["standing"] = false
    let player_hand = []
    let bot_hand = []
}

function play_blackjack() {
    let deck: number[];
    let new_wildcard: string;
    
    while (player["points"] > 0 && bot["points"] > 0) {
        deck = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
        custom_shuffle(deck)
        reset_hands()
        player_draw_card(deck)
        bot_draw_card(deck)
        bot_draw_card(deck)
        while (!(player["standing"] && bot["standing"])) {
            //  HIT
            if (input.buttonIsPressed(Button.A)) {
                console.log("A!")
                player_draw_card(deck)
            } else if (input.buttonIsPressed(Button.B)) {
                //  STAND
                player["standing"] = true
                if (randint(0, 10) < 2) {
                    //  20% chance to get a wildcard on draw
                    new_wildcard = wildcards._pickRandom()["name"]
                    player_wildcard_deck.push(new_wildcard)
                    console.log("You received a wildcard:" + new_wildcard)
                }
                
            }
            
        }
    }
    if (!bot["standing"]) {
        bot_decision_draw(deck)
    }
    
}

play_blackjack()
function main_display() {
    let card_to_display: string;
    let index = 0
    for (let card of player_hand) {
        card_to_display = " " + card
        OLED12864_I2C.showString(index * 2, 0, card_to_display, 1)
        index += 1
    }
    index = 0
    for (let bcard of bot_hand) {
        card_to_display = " " + bcard
        OLED12864_I2C.showString(index * 2, 3, card_to_display, 1)
        index += 1
    }
}

