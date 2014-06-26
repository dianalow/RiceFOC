# Written by : Diana Low
# Last updated : 18 April 2014
# Coding assignment for Rice University's 
# Interactive Python Programming course
# Game : "Stopwatch"
# Run on codeskulptor.org

import simplegui
import time
import math

# define global variables
points = 0 
clicks = 0
width = 300
height = 200
position = [width/2,height/2]
rtime = "0:00.0"
prevtime=""

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    rtime=int(round(t))
    seconds=rtime%10
    rmins=(rtime-seconds)/10
    if rmins>59:
        minutes=rmins%60
        hours=(rmins-minutes)/60
    else: 
        hours=0
        minutes=rmins
    if len(str(minutes))==1: minutes=str(0)+str(minutes)
    return(str(hours)+":"+str(minutes)+"."+str(seconds))
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def cstart():
    global starttime
    timer.start()
    starttime = time.time()
    
def cstop():
    global points, clicks, prevtime
    if timer.is_running():
        prevtime=rtime
        if rtime[-1]=="0": points+=1
        clicks+=1

def creset():
    global rtime, points, clicks, prevtime
    timer.stop()
    rtime, points, clicks, prevtime = "0:00.0",0,0,""

# define event handler for timer with 0.1 sec interval
def tick():
    global rtime
    runtime = time.time() - starttime
    rtime=format(runtime*10)

# define draw handler
def draw(canvas):
    canvas.draw_text(rtime,position,36,"White")
    canvas.draw_text(str(points)+"/"+str(clicks),[200,50],36,"Green")
    canvas.draw_text("Previous attempt: "+prevtime,[50,150],20,"Red")
    
# create frame
frame = simplegui.create_frame("Stopwatch",width,height)

# register event handlers
frame.add_button("Start", cstart)
frame.add_button("Stop", cstop)
frame.add_button("Reset", creset)
timer = simplegui.create_timer(100,tick)
frame.set_draw_handler(draw)
# start frame
frame.start()

# Please remember to review the grading rubric
