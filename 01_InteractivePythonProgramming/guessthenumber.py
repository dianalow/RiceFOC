# Written by : Diana Low
# Last updated : 10 April 2014
# Coding assignment for Rice University's 
# Interactive Python Programming course
# Game : "Guess the number"
# Run on codeskulptor.org

import simplegui
import math
import random


# initialize global variables used in your code
guess=0
secretnumber=0
tries=0
currentrange=100

# helper function to start and restart the game
def new_game():
    global counter, tries, secretnumber
    counter=0
    print "\nNew game!"
    secretnumber=random.randrange(0,currentrange)
    tries=int(math.ceil(math.log(currentrange,2)))
    print "Number range: [0-"+str(currentrange)+")\n===================="
    print "Guesses remaining:",tries

# define event handlers for control panel
def range100():
    global currentrange
    currentrange=100
    new_game()
    
def range1000():
    global currentrange
    currentrange=1000
    new_game()
    
def input_guess(guess):
    global tries
    if int(guess)==secretnumber: 
        print "> Bingo, it's "+guess
        new_game()
        return
    elif int(guess)<secretnumber:
        print "> Higher than",guess+"!"
    else : print "> Lower than",guess+"!"
    tries-=1
    
    if tries==0:
        print "Oops! No more chances! The number was",secretnumber
        range100()
        return
    print "Guesses remaining:",tries

# create frame

frame=simplegui.create_frame("Guess the number!",200,200)


# register event handlers for control elements
frame.add_button("Range: [0-100)", range100, 150)
frame.add_button("Range: [0-1000)", range1000, 150)
inp = frame.add_input('Enter your guess', input_guess, 50)


# call new_game and start frame
new_game()


# always remember to check your completed program against the grading rubric
