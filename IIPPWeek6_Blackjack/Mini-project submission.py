
'''
http://www.codeskulptor.org/#user44_g0C0D8uwlz_1.py
'''
# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

    def draw_back(self, canvas, pos):
        card_loc = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])
        canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0] + 1, pos[1] + CARD_BACK_CENTER[1] + 1], CARD_BACK_SIZE)
# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.list_of_cards = []
        
        
        
    def __str__(self):
        # return a string representation of a hand
        output = ""
        for card in self.list_of_cards:
            output += ("Card suit: " + card.get_suit() + ', ' + "Card_rank: " + card.get_rank() + '.\n')
        return output

    def add_card(self, card):
        # add a card object to a hand
        self.list_of_cards.append(card)
            

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        hand_value = 0
        ace = False
        for card in self.list_of_cards:
            rank = card.get_rank()
            if 'A' == rank:
                ace = True
            hand_value += VALUES[card.get_rank()]
        if ace == False:
            return hand_value
        elif hand_value + 10 <= 21:
            return hand_value + 10
        else:
            return hand_value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.list_of_cards:
            pos[0] = pos[0] + CARD_SIZE[0] + 30
            card.draw(canvas, pos)



        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck_of_cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck_of_cards.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.deck_of_cards)


    def deal_card(self):
        # deal a card object from the deck
        return self.deck_of_cards.pop()

    def __str__(self):
        # return a string representing the deck
        output = ''
        for card in self.deck_of_cards:
            output += (card.get_suit() + card.get_rank() + ';') 
        return output



#define event handlers for buttons
def deal():
    global outcome, in_play, message, score
    global deck, player_hand, dealer_hand
    if in_play == True:
        score -= 1
    in_play = True
    
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    dealer_hand = Hand()
    
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())

    message = "Hit or Stand?"
    outcome = ""


def hit():
    global outcome, score, message, in_play
    # replace with your code below
 
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
    if player_hand.get_value() <= 21:
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() > 21:
            outcome = "You have busted."
            score -= 1
            message = "New Deal?"
            in_play = False



def stand():
    # replace with your code below

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score
    global score, dealer_print, in_play, outcome, message
    dealer_print = True
    if in_play:
        if player_hand.get_value() > 21:
            score -=1
            outcome = "You have busted"
        else:
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(deck.deal_card())
            
            if dealer_hand.get_value() > 21:
                score += 1
                outcome = "Dealer busted, player win!"
            elif dealer_hand.get_value() >= player_hand.get_value():
                score -= 1
                outcome = "Dealer win!"
            else:
                score += 1
                outcome = "Player win!"
        
        message = "New Deal?"
        in_play = False


# draw handler
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    
    canvas.draw_text("BLACKJACK", (150, 70), 50, "Aqua")
    canvas.draw_text("Dealer", (36, 185), 30, "Black")
    canvas.draw_text("Player", (36, 385), 30, "Black")
    canvas.draw_text("Score " + str(score), (450, 115), 30, "Black")
    canvas.draw_text(outcome, (235, 385), 30, "Black")
    canvas.draw_text(message, (235, 185), 30, "Black")

    dealer_hand.draw(canvas, [-65, 200])
    player_hand.draw(canvas, [-65, 400])

    if in_play:
        dealer_hand.list_of_cards[0].draw_back(canvas, [36, 199])



# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()

# remember to review the gradic rubric