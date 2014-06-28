# Written by : Diana Low
# Last updated : 21 June 2014
# Coding assignment for Rice University's 
# Fundamentals of Computing course
# Game : "Cookie Clicker"
# Run on codeskulptor.org
"""
Cookie Clicker Simulator
"""

import simpleplot

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(200)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 16.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies=0.0
        self._current_cookies=0.0
        self._current_time=0.0
        self._current_cps=1.0
        self._history=[(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        
        thetext="\nTime: "+str(self._current_time)
        thetext+="\nCurrent Cookies: "+str(self._current_cookies)
        thetext+="\nCPS: "+str(self._current_cps)
        thetext+="\nTotal Cookies: "+str(self._total_cookies)
        return thetext
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        import math
        cookie_difference=cookies-self._current_cookies
        if cookie_difference<=0:
            return 0.0
        else:
            return math.ceil(cookie_difference/self._current_cps)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time>0:
            self._current_time+=time
            self._current_cookies+=self._current_cps*time
            self._total_cookies+=self._current_cps*time
            
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_cookies>=cost:
            self._current_cookies-=cost
            self._current_cps=self.get_cps()+additional_cps
            self._history.append((self._current_time,item_name,cost,self._total_cookies))
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """

    b_info=build_info.clone()
    c_state=ClickerState()
    
    while c_state.get_time()<=duration:
        time_left=duration-c_state.get_time()
        result=strategy(c_state.get_cookies(),c_state.get_cps(),time_left,b_info)
        if result==None:
            break
        else:
            item_cost=b_info.get_cost(result)
            item_cps=b_info.get_cps(result)
                
            time_needed=c_state.time_until(item_cost)
            print time_needed
            if time_needed>time_left:
                break
            else:
                c_state.wait(time_needed)
                c_state.buy_item(result,item_cost,item_cps)
                b_info.update_item(result)
   
    #check for left over time and make cookies
    c_state.wait(time_left)
    if result!=None:
        while c_state.get_cookies()>=b_info.get_cost(result):
            c_state.buy_item(result,b_info.get_cost(result),b_info.get_cps(result))
            b_info.update_item(result)
    return c_state


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def get_sorted_cost(build_info):
    """common function for strategy
    """
    all_items=build_info.build_items()
    costlist=list()
    for dummy_item in all_items:
        costlist.append([build_info.get_cost(dummy_item),build_info.get_cps(dummy_item),dummy_item])
    return sorted(costlist)
    
def strategy_cheap(cookies, cps, time_left, build_info):
    """
    always choose cheapest
    """
    costlist=get_sorted_cost(build_info)[0]
    max_amount=time_left*cps + cookies
    if costlist[0]<=max_amount:
        return costlist[2]
    else: 
        return None

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    always choose expensive
    """
    costlist=get_sorted_cost(build_info)
    current_high=[None,None]
    max_amount=time_left*cps + cookies
    
    for dummy_item in costlist:
        price=dummy_item[0]
        if price<=max_amount and price>current_high[0]:
            current_high=[price,dummy_item[2]]
    return current_high[1]

def strategy_best(cookies, cps, time_left, build_info):
    """
    my best shot?
    """
    costlist=get_sorted_cost(build_info)
    current_high=[costlist[0][0],costlist[0][1],costlist[0][2]]
    cost_per_unit=costlist[0][1]/costlist[0][0]

    for dummy_item in costlist:
        if dummy_item[0]<=0.5*(cookies+time_left*(cps+dummy_item[1])):
            ncost_per_unit=dummy_item[1]/dummy_item[0]
            if ncost_per_unit>cost_per_unit:
                cost_per_unit=ncost_per_unit
                current_high=[dummy_item[0],dummy_item[1],dummy_item[2]]
        else:
            return current_high[2]
                    
    return current_high[2]
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    #history = state.get_history()
    #print history
    #history = [(item[0], item[3]) for item in history]
    #simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    #run_strategy("Cursor", SIM_TIME, strategy_cursor)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    #run_strategy("Expensive", SIM_TIME, strategy_expensive)
    #run_strategy("Best", SIM_TIME, strategy_best)
    
run()