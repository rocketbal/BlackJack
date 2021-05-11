import random
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}
playing = True

class Card:
    
    # card class to keep all the cards
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:

    def __init__(self):
        self.deck = [] # empty list of cards
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return "The deck has: "+deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


# Keep track of the funds available and place bets
class Chip:

    def __init__(self,amount):
        self.amount = amount
        self.bet = 0

    def place_bet(self,bet):
        if bet > self.amount:
            print('Not enough funds to place the bet')
            print('\n')
            return False
        else:
            self.bet = bet
            print('Bet Placed!')
            print('\n')
            return True
    def win_bet(self):
        self.amount += self.bet

    def lose_bet(self):
        self.amount -= self.bet
        if self.amount < 0:
            print('Not enough funds to continue playing')


# Keep take of player's hand and value of their cards
class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        
    def add_card(self,card):
        self.cards.append(card)
        self.value = self.value + values[card.rank]

        if card.rank == 'Ace':
            self.aces +=1
            
    def adjust_for_aces(self):
        # if the total value is over 21 and I still have an Ace
        # Than change the value of the aces to be 1 from 11
        while self.value > 21 and self.aces:
            self.value -=10
            self.aces -=1

    def __str__(self):
        return self.cards


# Players will place bets
def take_bet(player_chips):
    bet_accepted = False
    # Ensure the bet placed is within player's total amount
    while not bet_accepted:
    # Ensure the bet placed is a valid integer value
        bet_placed = False
        while not bet_placed:
            try:
                temp = int(input('Please enter the amount you would like to bet: '))
                bet_placed = True
            except ValueError: 
                print("Invalid dollar amount, please try again: ")

        bet_accepted = player_chips.place_bet(temp)
        
#Take a hit from the deck of cards
def hit(deck_one,hand):
    hand.add_card(deck_one.deal())
    hand.adjust_for_aces()

# Ask the player if they would like to take a hit or stand
def hit_or_stand(deck,hand):
    global playing
    while True:
        # If player chooses to stand, assign False to global variable player
        status = (input('Would you like to Hit or Stand? Enter H for Hit or S for Stand: ')).upper()

        if status == 'H':
            hit(deck,hand)
        elif status == 'S':
            print("Player Stands Dealer's Turn")
            playing = False
        else:
            print('Sorry, please try again.')
            continue 
        break
#show all of player's cards. For dealer, show all except one card
def show_some(player,dealer):
    
    i = 0
    print("Player's Hand: ")
    while i<len(player.cards):
        print(player.cards[i])
        i+=1
    print('\n')
    
    print("Dealer's Hand: ")
    print("First card Hidden!")
    print(dealer.cards[1])
    print('\n')

#show all of player and dealer's cards
def show_all(player,dealer):
    
    i = 0
    print("Player's Hand: ")
    while i<len(player.cards):
        print(player.cards[i])
        i+=1
    print('\n')
    print(f"Value of Player's hand is: {player.value}")
    
    i = 0
    print("Dealer's Hand: ")    
    while i<(len(dealer.cards)):
        print(dealer.cards[i])
        i+=1
    print('\n')
    print(f"Value of Dealer's hand is: {dealer.value}")

#End of the game scenarios
def player_busts(player,playerchips):
    playerchips.lose_bet()

def player_wins(player,playerchips):
    playerchips.win_bet()

def dealer_busts(dealer,dealerchips):
    dealerchips.lose_bet()

def dealer_wins(dealer,dealerchips):
    dealerchips.win_bet()

def push(player,dealer):
    print('Dealer and player tie! PUSH')


while True:

    print('Welcome to the game of Black Jack!\n')

    # Create and Shuffle the deck
    deck = Deck()
    deck.shuffle()

    # Create a hand for the player and the computer dealer
    player = Hand()
    dealer = Hand()

    #Deal two cards to each player
    hit(deck,player)
    hit(deck,player)
    hit(deck,dealer)
    hit(deck,dealer)

    #Setup player chips
    #Hard coding a value. Potenially could make this a user input
    player_chips = Chip(int(input('Enter an amount of chips you would like to play with: ')))
    dealer_chips = Chip(200)

    #Prompt the Player for their bet
    take_bet(player_chips)

    #Show cards (but keep one dealer card hidden)
    show_some(player,dealer)

    while playing:

        #Prompt for player to Hit or Stand
        hit_or_stand(deck, player)

        #Show cards (but keep one dealer card hidden)
        show_some(player,dealer)

        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player.value > 21:
            player_busts(player,player_chips)
            print('Dealer wins. Player busts\n')
            print('Your current chips total: \n')
            print(player_chips.amount)
            break
        
        # If player hasn't busted, play Dealer's hand until Dealer reaches 17

        if player.value <=21:
            while dealer.value < player.value:
                print('Dealer hits\n')
                hit(deck,dealer)

            show_all(player,dealer)

            if dealer.value > player.value and dealer.value < 21:
                print('Dealer wins. player busts\n')
                dealer_wins(dealer,dealer_chips)
                player_busts(player,player_chips)
                  
            elif dealer.value > 21:
                print('Player wins. The dealer busts\n')
                player_wins(player,player_chips)
                dealer_busts(dealer,dealer_chips)
            elif dealer.value < player.value:
                print('Player wins. The dealer busts\n')
                player_wins(player,player_chips)
                dealer_busts(dealer,dealer_chips)
            else:
                push(player,dealer)
                    

        print('Your current chips total: ')
        print(player_chips.amount)

    new_game = input("Would you like to play another hand? y/n: ")

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print('Thank you for playing!')
        break
        
    


