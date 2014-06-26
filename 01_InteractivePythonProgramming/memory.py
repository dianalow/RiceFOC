# Written by : Diana Low
# Last updated : 29 April 2014
# Coding assignment for Rice University's 
# Interactive Python Programming course
# Game : "Memory"
# Run on codeskulptor.org

import simplegui
import random

font_size=40
font_color="White"

#use card images
image_list=['http://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Playing_card_heart_A.svg/200px-Playing_card_heart_A.svg.png',
           'http://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Playing_card_club_2.svg/200px-Playing_card_club_2.svg.png',
           'http://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Playing_card_diamond_3.svg/200px-Playing_card_diamond_3.svg.png',
           'http://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Playing_card_club_4.svg/200px-Playing_card_club_4.svg.png',
           'http://upload.wikimedia.org/wikipedia/commons/5/52/Playing_card_heart_5.svg',
           'http://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Playing_card_spade_6.svg/200px-Playing_card_spade_6.svg.png',
           'http://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Playing_card_diamond_7.svg/200px-Playing_card_diamond_7.svg.png',
           'http://upload.wikimedia.org/wikipedia/commons/thumb/e/eb/Playing_card_club_8.svg/200px-Playing_card_club_8.svg.png']

#initialize images
image_map={}
for n,i in enumerate(image_list):
    image = simplegui.load_image(i)
    image_map[n+1]=image
    
# helper function to initialize globals
def new_game():
    global numbers, exposed, state, firstcard, secondcard,turns
    state = 0
    numbers=range(1,9)+range(1,9)
    random.shuffle(numbers)
    exposed = [False]*16 #all 16 cards hidden
    firstcard=[0,0]
    secondcard=[0,0]
    turns=0
    label.set_text('Turns ='+str(turns))
    
# define event handlers
def mouseclick(pos):
    global state, firstcard, secondcard,turns
    
    #just consider the x location
    #since every card differs by 50px, 
    #we take the multiples of 50 as the index    
    xpos=list(pos)[0]/50
    
    if not exposed[xpos]:
        if state == 0:
            state = 1
            turns+=1
            firstcard=[numbers[xpos],xpos] #keep card number,index
            label.set_text('Turns ='+str(turns))
        elif state == 1:
            state = 2
            secondcard=[numbers[xpos],xpos] #keep card number,index
        else:
            state = 1
            turns+=1
            if firstcard[0]!=secondcard[0]: #compare number
                #check if exposed (by index!!!!)
                exposed[firstcard[1]]=False 
                exposed[secondcard[1]]=False
            # records the new click as firstcard of new turn and increment turn
            firstcard=[numbers[xpos],xpos]
            label.set_text('Turns ='+str(turns))
        exposed[xpos]=True
        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for pos,n in enumerate(numbers):
        if exposed[pos]:
            #canvas.draw_text(str(n), [(50*pos)+50/3,100*2/3], font_size, font_color) #text version
            canvas.draw_image(image_map[n], [100,125], [200,250], [(50*pos)+25, 50], [50,100]) #image version
        else:
            canvas.draw_polygon([[50*pos, 0], [(50*pos)+50, 0], [(50*pos)+50, 100], [50*pos, 100]], 1, 'Black', 'Green')

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()