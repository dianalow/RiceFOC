# Written by : Diana Low
# Last updated : 9 May 2014
# Coding assignment for Rice University's 
# Interactive Python Programming course
# Game : "Blackjack"
# Run on codeskulptor.org

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
bust=False
outcome = "Hit or Stand?"
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
        
# define hand class
class Hand:
    def __init__(self):
        self.cards=[]

    def __str__(self):
        output="Hand contains "
        for i in self.cards:
            output+=str(i)+" "
        return output

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        value=0
        hasAce=False
        for i in self.cards:
            value+=VALUES[i.get_rank()]
            if i.get_rank()=='A': hasAce=True
        if hasAce:
            if value+10<=21: return value+10
            else : return value
        else : return value
   
    def draw(self, canvas, pos):
        for n,i in enumerate(self.cards):
            i.draw(canvas,[pos[0]+CARD_SIZE[0]*n,pos[1]]) 
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards=[]
        for i in SUITS:
            for j in RANKS:
                self.cards.append(Card(i,j))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        dealed=self.cards.pop()
        return dealed
    
    def __str__(self):
        output="Deck contains "
        for i in self.cards:
            output+=str(i)+" "
        return output

#define event handlers for buttons
def deal():
    global outcome, in_play,player,dealer,deck,score
    if in_play:
        score-=1
    outcome="Hit or Stand?"
    #create deck and shuffle
    deck=Deck()
    deck.shuffle()
    
    #create player and dealer hands
    player=Hand()
    dealer=Hand()
    
    #deal cards to player and dealer
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    in_play = True

def hit():
    global in_play,score,player,outcome
    if in_play:
        player.add_card(deck.deal_card())
        if player.get_value()>21 : 
            in_play=False
            outcome="You have busted! New deal?"
            bust=True
            score-=1
    else:
        outcome="Game is over! New deal?"

def stand():
    global in_play,dealer,player,score,outcome
    if in_play:
        while dealer.get_value()<17:
            dealer.add_card(deck.deal_card())
        if dealer.get_value()<=21:
            if player.get_value()<=dealer.get_value():
                outcome="Dealer wins!"
                score-=1
            else: 
                outcome="Player wins!"
                score+=1
        else: 
            outcome="Dealer busts!"
            score+=1
        in_play=False
    else : 
        if bust: outcome="You have busted!"
        else : outcome="Game is over!"
    outcome+=" New deal?"

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("BLACK", (100, 50), 50, 'Black')
    canvas.draw_text("JACK", (270, 50), 50, 'Red')
    canvas.draw_text("(dealer wins ties)", (170, 80), 25, 'White')
    canvas.draw_text("Dealer", (30, 200), 30, 'White')
    canvas.draw_text("Player", (30, 500), 30, 'White')
    #card = Card("S", "A")
    dealer.draw(canvas, [150, 150])
    player.draw(canvas, [150, 450])
    canvas.draw_text(outcome, (100, 350), 40, 'White')
    canvas.draw_text("Score: "+str(score), (400, 120), 40, 'White')
    if in_play:canvas.draw_image(card_back, (CARD_BACK_CENTER[0],CARD_BACK_CENTER[1]), CARD_BACK_SIZE, [150 + CARD_BACK_CENTER[0], 150 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)

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