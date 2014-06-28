# Written by : Diana Low
# Last updated : 14 June 2014
# Coding assignment for Rice University's 
# Principles of Computing course
# Game : "2048"
# Run on codeskulptor.org

"""
Clone of 2048 game.
"""

import poc_2048_gui        
import random
# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
   
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    result=[0]*len(line)
    merged=[False]*len(line)
    #print line
    for dummy_i in line:
        if dummy_i!=0:
            for dummy_j in range(0,len(result)):
                if result[dummy_j]==0:
                    if dummy_j>0:
                        if result[dummy_j-1]==dummy_i and not merged[dummy_j-1]:
                            result[dummy_j-1]=result[dummy_j-1]+dummy_i
                            merged[dummy_j-1]=True
                            break
                        else:
                            result[dummy_j]=dummy_i
                            break
                    else:
                        result[dummy_j]=dummy_i
                        break                   
    return result

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self.grid_height=grid_height
        self.grid_width=grid_width
        self.grid=[]
        self.direction={}
        self.direction[UP]=[]
        self.direction[DOWN]=[]
        self.direction[LEFT]=[]
        self.direction[RIGHT]=[]
        
        for dummy_row in range(0,self.grid_height):
            self.direction[LEFT].append((dummy_row,0))
            self.direction[RIGHT].append((dummy_row,self.grid_width-1))
            
        for dummy_col in range(0,self.grid_width):
            self.direction[UP].append((0,dummy_col))
            self.direction[DOWN].append((self.grid_height-1,dummy_col))
            
        self.reset()

    
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        new_grid=[]
        for dummy_rows in range(0,self.grid_height):
            new_grid.append([0]*self.grid_width)
        self.grid=new_grid
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        grid_string='# Current grid #\n'
        for dummy_row in range(0,self.grid_height):
            grid_string+=str(self.grid[dummy_row])+'\n'
        return grid_string

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.grid_height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.grid_width
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        tile_change=False
        
        if direction==UP or direction==DOWN: 
            index_length=self.grid_height
        else : 
            index_length=self.grid_width
        
        init_tiles=self.direction[direction]
        offset=list(OFFSETS[direction])

        for dummy_it in init_tiles:
            temp_list=[]
            #print '###',dummy_it
            tile_pos=list(dummy_it)
            temp_list.append(self.get_tile(tile_pos[0],tile_pos[1]))
            for dummy_index in range(0,index_length-1):                
                tile_pos[0]+=offset[0]
                tile_pos[1]+=offset[1]
                #print tile_pos
                temp_list.append(self.get_tile(tile_pos[0],tile_pos[1]))
            #print temp_list
            merged_list=merge(temp_list)
            tile_pos=list(dummy_it)
            for dummy_index in range(0,index_length):
                curr_value=self.get_tile(tile_pos[0],tile_pos[1])
                if curr_value!=merged_list[dummy_index]:
                    tile_change=True
                    self.set_tile(tile_pos[0],tile_pos[1],merged_list[dummy_index])
                tile_pos[0]+=offset[0]
                tile_pos[1]+=offset[1]
            
        if tile_change:
            self.new_tile()
                
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # check current grid for empty places
        # and then choose one from that
        empty_spaces=[]
        for dummy_row in range(0,self.grid_height):
            for dummy_col in range(0,self.grid_width):
                if self.grid[dummy_row][dummy_col]==0:
                    empty_spaces.append((dummy_row,dummy_col))

        if empty_spaces!=[]:
            grid_space=random.choice(empty_spaces)
            grid_value=random.choice([2]*9+[4])
            self.set_tile(grid_space[0],grid_space[1],grid_value)
        else : 
            grid_space=None
        
        
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        self.grid[row][col]=value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        return self.grid[row][col]

poc_2048_gui.run_gui(TwentyFortyEight(5, 4))
