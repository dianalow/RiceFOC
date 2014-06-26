# Written by : Diana Low
# Last updated : 9 April 2014
# Coding assignment for Rice University's 
# Interactive Python Programming course
# Game : Scissors, Paper, Spock
# Run on codeskulptor.org

def name_to_number(name):
    if(name=="rock"): return 0
    elif(name=="Spock"): return 1
    elif(name=="paper"): return 2
    elif(name=="lizard"): return 3
    elif(name=="scissors"): return 4
    else: print "Invalid name!"

def number_to_name(number):
    if(number==0): return "rock"
    elif(number==1): return "Spock"
    elif(number==2): return "paper"
    elif(number==3): return "lizard"
    elif(number==4): return "scissors"
    else: print "Invalid number!"
    

def rpsls(player_choice): 
    import random
    print ""
    print "Player chooses",player_choice
    pn=name_to_number(player_choice)
    cn=random.randrange(0,5)
    cc=number_to_name(cn)
    print "Computer chooses",cc
    
    diffnum=(pn-cn)%5
    
    if(diffnum==0): print "Player and computer tie!"
    elif(diffnum<=2): print "Player wins!"
    else: print "Computer wins!"
        
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

