import random

Player_cards = 0
Dealer_cards = 0

Joker = 1
#If the player draws a Joker, the player's score is equal to the dealer's score plus 1
Marksman = 2
#If the player draws a Marksman, the dealer's score is also reduced by 2
Squire = -5
Priest = 0
#If the player draws a Priest, the player's score is equal to 18
Jack = 10
Queen = 10
King = 10
Ace = 11 if Player_cards or Dealer_cards <= 10 else 1
  
# Variables for micro:bit coding
goal_score: int = 21
current_bet: int = 1





while True:
         
    Drawing = input("Would you like to Play?")
    if Drawing == "yes":
        


        # Draw two initial cards for the player
        for _ in range(2):
            number = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace, Squire, Priest, Marksman, Joker])
            
            Player_cards += number
            if number == Priest:
                number = "Knight"
                Player_cards = 18
            elif number == Marksman:
                number = "Marksman"
                Dealer_cards -= 2
            elif number == Joker:
                number = "Joker"
                Player_cards = Dealer_cards + 1

            if number == Jack:
                number = "Jack"
            elif number == Queen:
                number = "Queen"
            elif number == King:
                number = "King"
            elif number == Ace:
                number = "Ace"
            elif number == Squire:
                number = "Squire"

            print("You have drawn a", number, "You have", Player_cards, "points")
            
            # Draw two initial cards for the dealer
            for _ in range(2):
             number = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace, Squire, Priest, Marksman, Joker])
            
            Dealer_cards += number
            if number == Priest:
                number = "Knight"
                Dealer_cards = 18
            elif number == Marksman:
                number = "Marksman"
                Dealer_cards -= 2
            elif number == Joker:
                number = "Joker"
                Dealer_cards = Player_cards + 1

            if number == Jack:
                number = "Jack"
            elif number == Queen:
                number = "Queen"
            elif number == King:
                number = "King"
            elif number == Ace:
                number = "Ace"
            elif number == Squire:
                number = "Squire"
            print("The dealer has drawn a", number, "The dealer has", Dealer_cards, "points")
            
        if Player_cards == 21:
            print("You Win!")
            break
     
    
    if Drawing == "no":
        print("Goodbye!")
        break

   
    
    while True:
        Drawing = input("Would you like to Hit or Stand?")
        
        # Draw a card for the player
        if Drawing.lower() == "hit":
            number = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace, Squire, Priest, Marksman, Joker])
            
            Player_cards += number
            if number == Priest:
                number = "Knight"
                Player_cards = 18
            elif number == Marksman:
                number = "Marksman"
                Dealer_cards -= 2
            elif number == Joker:
                number = "Joker"
                Player_cards = Dealer_cards + 1

            if number == Jack:
                number = "Jack"
            elif number == Queen:
                number = "Queen"
            elif number == King:
                number = "King"
            elif number == Ace:
                number = "Ace"
            elif number == Squire:
                number = "Squire"

            print("You have drawn a", number, "You have", Player_cards, "points")

            if Player_cards > 21:
                print("You have busted!")
                break

            elif Player_cards == 21:
                print("You Win!")
                break
            elif Player_cards < 0:
                print("You have busted!")
                break

        # Draw a card for the dealer
        elif Drawing.lower() == "stand":
            # Draw two initial cards for the dealer
            for _ in range(2):
             number = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace, Squire, Priest, Marksman, Joker])
            
            Dealer_cards += number
            if number == Priest:
                number = "Knight"
                Dealer_cards = 18
            elif number == Marksman:
                number = "Marksman"
                Dealer_cards -= 2
            elif number == Joker:
                number = "Joker"
                Dealer_cards = Player_cards + 1

            if number == Jack:
                number = "Jack"
            elif number == Queen:
                number = "Queen"
            elif number == King:
                number = "King"
            elif number == Ace:
                number = "Ace"
            elif number == Squire:
                number = "Squire"
            print("The dealer has drawn a", number, "The dealer has", Dealer_cards, "points")
            
            while Dealer_cards < 16:
                number = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace, Squire, Priest, Marksman, Joker])
            
            Dealer_cards += number
            if number == Priest:
                number = "Knight"
                Dealer_cards = 18
            elif number == Marksman:
                number = "Marksman"
                Dealer_cards -= 2
            elif number == Joker:
                number = "Joker"
                Dealer_cards = Player_cards + 1


            if number == Jack:
                number = "Jack"
            elif number == Queen:
                number = "Queen"
            elif number == King:
                number = "King"
            elif number == Ace:
                number = "Ace"
            elif number == Squire:
                number = "Squire"

                print("The dealer has drawn a", number, "The dealer has", Dealer_cards, "points")

            if Dealer_cards > 21:
                print("The dealer has busted! You Win!")
                break
            elif 21 >= Dealer_cards > Player_cards:
                print("The dealer wins!")
                break
            elif Dealer_cards == Player_cards:
                print("It's a tie!")
                break
            elif Dealer_cards < Player_cards:
                print("You Win!")
                break
    Player_cards = 0
    Dealer_cards = 0