# Written by : Diana Low
# Last updated : 21 April 2014
# Coding assignment for Rice University's 
# Interactive Python Programming course
# Game : "Pong"
# Run on codeskulptor.org

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos=[WIDTH/2,HEIGHT/2]
ball_vel=[0,0]
paddle1_pos=paddle2_pos=HEIGHT/2
paddle1_vel=paddle2_vel=0
score1=score2=0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    #middle of table spawn
    ball_pos=[WIDTH/2,HEIGHT/2]
    
    #generate random horizontal and vertical velocity
    #pixels per second, so divide by 60
    horizontal_vel=random.randrange(120, 240)/60
    vertical_vel=random.randrange(60, 180)/60
    
    #velocity of the ball should be upwards and towards the right
    if direction: 
        ball_vel=[horizontal_vel,-vertical_vel]
    else: 
        ball_vel=[-horizontal_vel,-vertical_vel]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1=score2=0
    paddle1_pos=paddle2_pos=HEIGHT/2
    paddle1_vel=paddle2_vel=0
    spawn_ball(RIGHT)
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel  
    global ball_dir
    
    # ball movement
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1] 
   
    # ball bouncing off top or bottom walls
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT-1-BALL_RADIUS:
        ball_vel[1]=-ball_vel[1]
        
    # test if ball touches gutter

    # 1. right gutter, paddle2
    if ball_pos[0]>= (WIDTH-1-BALL_RADIUS)-PAD_WIDTH:
        # if within paddle reflect and increase vel 
        # if not,update score and spawn
        if ball_pos[1]>=paddle2_pos-HALF_PAD_HEIGHT and ball_pos[1]<=paddle2_pos+HALF_PAD_HEIGHT:
            ball_vel[0]=-ball_vel[0]*1.1
        else: 
            score1+=1
            spawn_ball(LEFT)
    # 1. left gutter, paddle1
    elif ball_pos[0]<=BALL_RADIUS+PAD_WIDTH:
        if ball_pos[1]>=paddle1_pos-HALF_PAD_HEIGHT and ball_pos[1]<=paddle1_pos+HALF_PAD_HEIGHT:
            ball_vel[0]=-ball_vel[0]*1.1
        else: 
            score2+=1
            spawn_ball(RIGHT)
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    # update only when within vertical boundaries
    if paddle1_pos-HALF_PAD_HEIGHT+paddle1_vel>=0 and paddle1_pos+HALF_PAD_HEIGHT+paddle1_vel<=HEIGHT :
        paddle1_pos+=paddle1_vel
    if paddle2_pos-HALF_PAD_HEIGHT+paddle2_vel>=0 and paddle2_pos+HALF_PAD_HEIGHT+paddle2_vel<=HEIGHT: 
        paddle2_pos+=paddle2_vel
    
    # draw paddles
    canvas.draw_line([HALF_PAD_WIDTH,paddle1_pos-HALF_PAD_HEIGHT],[HALF_PAD_WIDTH,paddle1_pos+HALF_PAD_HEIGHT],PAD_WIDTH,"Red")
    canvas.draw_line([WIDTH-HALF_PAD_WIDTH,paddle2_pos-HALF_PAD_HEIGHT],[WIDTH-HALF_PAD_WIDTH,paddle2_pos+HALF_PAD_HEIGHT],PAD_WIDTH,"Yellow")
    
    # draw scores
    canvas.draw_text(str(score1), [WIDTH/2-50, 50], 50, "Red")
    canvas.draw_text(str(score2), [WIDTH/2+25, 50], 50, "Yellow")  

def keydown(key):
    global paddle1_vel, paddle2_vel
    #paddle velocity
    pad_vel=5
    
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel = -pad_vel
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel = pad_vel
        
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel = -pad_vel
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel = pad_vel
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    #stops the paddle from moving
    paddle1_vel=0
    paddle2_vel=0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
reset_button = frame.add_button('Restart', new_game, 100)

# start frame
new_game()
frame.start()
