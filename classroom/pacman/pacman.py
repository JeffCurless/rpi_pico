'''
    PACMAN - A clone
    
    Authors: Todd P, Andrew W

'''
import time
import math
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_RGB565

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_RGB565)
display.set_backlight(0.8)

width, height = display.get_bounds()

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

black = display.create_pen(0,0,0)
white = display.create_pen(255,255,255)
yellow = display.create_pen(255,255,0)
yell_whit = display.create_pen(253, 253, 150)
red = display.create_pen(255, 0, 0)
cyan = display.create_pen(0, 255, 255)
blue = display.create_pen(0,0,255)
pink = display.create_pen(255, 192, 203)
orange = display.create_pen(255, 140, 0)

tile_color = display.create_pen(0,0,125)
tile_size = 9
piece_size = 4

#  0 = lane, 1 = wall, 2 = only ghost can pass through, 3 = forced turn, 4 = choice turn, 5 = force turn up
board = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,3,0,0,0,4,0,0,0,4,0,0,0,3,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,1,3,0,4,0,0,0,4,0,3,1,0,1],
    [1,0,1,0,1,1,1,1,1,1,1,0,1,0,1],
    [1,4,0,4,4,0,3,1,3,0,4,4,0,4,1],
    [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
    [1,0,1,1,0,1,0,1,0,1,0,1,1,0,1],
    [1,4,0,0,4,1,3,4,3,1,4,0,0,4,1],
    [1,0,1,1,0,1,1,0,1,1,0,1,1,0,1],
    [1,3,3,1,4,0,0,4,0,0,4,1,3,3,1],
    [1,1,0,1,0,1,1,2,1,1,0,1,0,1,1],
    [0,0,4,0,4,1,6,5,6,1,4,0,4,0,0],
    [1,1,0,1,0,1,1,1,1,1,0,1,0,1,1],
    [1,3,3,1,4,0,0,4,0,0,4,1,3,3,1],
    [1,0,1,1,0,1,1,0,1,1,0,1,1,0,1],
    [1,0,1,3,4,0,0,4,0,0,4,3,1,0,1],
    [1,0,1,0,1,1,1,0,1,1,1,0,1,0,1],
    [1,0,1,0,1,1,1,0,1,1,1,0,1,0,1],
    [1,4,0,4,0,4,0,4,0,4,0,4,0,4,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,1,3,0,4,0,0,0,4,0,3,1,0,1],
    [1,0,1,0,1,1,1,1,1,1,1,0,1,0,1],
    [1,3,0,4,0,0,0,0,0,0,0,4,0,3,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ]

pellets = []

# [0] = Pacman,  [1] = Inky (Red), [2] = Blinky (Blue), [3] = Pinky (Pink), [4] = Clyde (Orange)
character_cords = [(),(),(),(),()]

def clear():
    display.set_pen(black)
    display.clear()

# detects if button is pressed for getting out of the homescreen
def detect_button(start):
    if button_a.read():
        start = True
    if button_b.read():
        start = True
    if button_x.read():
        start = True
    if button_y.read():
        start = True
    return start

# homecsreen animation
def homescreen(highscore):
    start = False
    start = detect_button(start)
    if not start:
        display.set_pen(black)
        display.rectangle(0,0,width,height)
        display.update()
        time.sleep(0.5)
    start = detect_button(start)
    display.set_pen(white)
    display.text('Highscore: '+str(highscore),width//2 -62,height-height//9)
    display.update()
    if not start:
        display.set_pen(red)
        display.circle(width//4,height//4,10)
        display.update()
        time.sleep(1)
    start = detect_button(start)
    if not start:
        display.set_pen(pink)
        display.circle(width//4,height//4+30,10)
        display.update()
        time.sleep(1)
    start = detect_button(start)
    if not start:
        display.set_pen(cyan)
        display.circle(width//4,height//4+60,10)
        display.update()
        time.sleep(1)
    start = detect_button(start)
    if not start:
        display.set_pen(orange)
        display.circle(width//4,height//4+90,10)
        display.update()
        time.sleep(1)
    start = detect_button(start)
    if not start:
        display.set_pen(white)
        display.text('Blinky',width//2,height//4-8)
        display.update()
        time.sleep(1)
    start = detect_button(start)
    if not start:
        display.text('Pinky',width//2,height//4+22)
        display.update()
        time.sleep(1)
    start = detect_button(start)
    if not start:
        display.text('Inky',width//2,height//4+52)
        display.update()
        time.sleep(1)
    start = detect_button(start)
    if not start:
        display.text('Clyde',width//2,height//4+82)
        display.update()
        time.sleep(2)
    start = detect_button(start)
    if not start:
        display.set_pen(black)
        display.rectangle(0,0,width,height)
        display.update()
        time.sleep(0.5)
    start = detect_button(start)
    if not start:
        display.set_pen(yellow)
        display.circle(width//2, height//2, 10)
        display.update()
        time.sleep(1)
    start = detect_button(start)
    if not start:
        display.set_pen(white)
        display.text('Pacman',width//2 - 32,height//2 + 20)
        display.update()
        time.sleep(2)
    if start:
        display.set_pen(white)
        display.text('Starting...',width//2 -62,height-height//5)
        display.update()
        time.sleep(1.25)
    return start  

# draw board, blue = wall
def draw_board(color):
    for i in range(25): 
        for j in range(15):
            x_cord = tile_size * j
            y_cord = tile_size * i
            if board[i][j] == 1:
                display.set_pen(color)
                display.rectangle(x_cord, y_cord, tile_size, tile_size)
            elif board[i][j] == 2:
                display.set_pen(white)
                display.rectangle(x_cord, y_cord, tile_size, tile_size//3)

# initially create the pellets
def create_pellets():
    for i in range(25): 
        for j in range(15):
            x_cord = tile_size * j
            y_cord = tile_size * i
            if board[i][j] == 0 or board[i][j] == 3 or board[i][j] == 4:
                pellets.append((j, i))

# draw the pellets not eaten on the screen
def draw_pellets():
    for pellet in pellets:
        x_cord = tile_size * pellet[0]
        y_cord = tile_size * pellet[1]
        display.set_pen(yell_whit)
        display.rectangle(x_cord + 4, y_cord + 4, 1, 1)

# delete eaten pellets from pellets list
def update_pellets():
    pellets_eaten = []
    for i in range(len(pellets)):
        if character_cords[0] == pellets[i]:
            pellets_eaten.append(i)
    if len(pellets_eaten) != 0:
        del pellets[pellets_eaten[0]]
        
# /////////////////////////////////////////////////////////////////////////////////////////////////////////
class Pacman_brains:
    def __init__(self):
        self.pac_x = width//2
        self.pac_y = 147
        self.pac_speed = 9
        self.direction = ''
        character_cords[0] = (7,16)
    
    # direction you want pacman to go
    def direct_pacman(self):
        if button_a.read():
            self.direction = 'up'
        elif button_b.read():
            self.direction = 'down'
        elif button_x.read():
            self.direction = 'right'
        elif button_y.read():
            self.direction = 'left' 
    
    def move_pacman(self):
        # grid coordinates (0-14, 0-24)
        current_x = character_cords[0][0]
        current_y = character_cords[0][1]
        
        # teleportation for when you go off the screen left/right
        if character_cords[0] == (14, 12) and self.direction == 'right':
            self.pac_x = 5
            current_x = 0
        elif character_cords[0] == (0, 12) and self.direction == 'left':
            self.pac_x = 130
            current_x = 14
        
        # make sure that new Pacman position isn't inside of a wall, update coordinates/position on grid
        else:
            if self.direction == 'up' and board[current_y - 1][current_x] != 1:
                self.pac_y -= self.pac_speed
                current_y -= 1
            elif self.direction == 'down'and board[current_y + 1][current_x] != 1 and board[current_y + 1][current_x] != 2:
                self.pac_y += self.pac_speed
                current_y += 1
            elif self.direction == 'right' and board[current_y][current_x + 1] != 1:
                self.pac_x += self.pac_speed
                current_x += 1
            elif self.direction == 'left' and board[current_y][current_x - 1] != 1:
                self.pac_x -= self.pac_speed
                current_x -= 1
        
        # fully update coordinates/position on grid
        character_cords[0] = (current_x,current_y)
    
    def draw_pacman(self):
        display.set_pen(yellow)
        display.circle(self.pac_x, self.pac_y, piece_size)
        return self.direction

class Ghost_brains:
    def __init__(self, color, x, y, cords, cord_num, direction):
        self.color = color
        self.ghost_x = x
        self.ghost_y = y
        self.direction = direction
        self.target = 'skip'
        self.cord_num = cord_num
        self.count = 0
        self.slow_move = 0
        character_cords[self.cord_num] = cords
    
    # set target to outside ghost house then sets it as pacman's coordinates
    def direct_red(self):
        if self.count == 0:
            self.target = (7, 12)
            self.count += 1
        else:
            self.target = character_cords[0]
    
    # blue's target tile is caculated in 3 steps.
    # 1. take position that is 2 tiles in front of pacman
    # 2. find direct distance from red's position to the position in step 1
    # 3. double that distance to find teh target tile
    def direct_blue(self, pac_direction):
        pac_x = character_cords[0][0]
        pac_y = character_cords[0][1]
        red_x = character_cords[1][0]
        red_y = character_cords[1][1]
        if pac_direction == 'up':
            pac_y -= 2
        elif pac_direction == 'down':
            pac_y += 2
        elif pac_direction == 'left':
            pac_x -= 2
        elif pac_direction == 'right':
            pac_x += 2
        a = pac_x - red_x
        b = pac_y - red_y
        self.target = (pac_x + a, pac_y + b)

    # target square 4 tiles ahead of pacman
    def direct_pink(self, pac_direction):
        target_x = character_cords[0][0]
        target_y = character_cords[0][1]
        if pac_direction == 'up':
            target_y -= 4
        elif pac_direction == 'down':
            target_y += 4
        elif pac_direction == 'right':
            target_x += 4
        elif pac_direction == 'left':
            target_x -= 4
        self.target = (target_x, target_y)
    
    # target pacman if farther than 6 tiles away, flee if too close
    def direct_orange(self):
        current_x = character_cords[self.cord_num][0]
        current_y = character_cords[self.cord_num][1]
        pac_x = character_cords[0][0]
        pac_y = character_cords[0][1]
        a = pac_x - current_x
        b = pac_y - current_y
        c = math.sqrt(a**2 + b**2)
        if c > 6:
            self.target = character_cords[0]
        else:
            self.target = (0, 26)

    def move_ghost(self):
        current_x = character_cords[self.cord_num][0]
        current_y = character_cords[self.cord_num][1]
        target_x = self.target[0]
        target_y = self.target[1]
        
        if self.slow_move == 0:
            # teleportation at sides of screen
            if character_cords[self.cord_num] == (14, 12) and self.direction == 'right':
                self.ghost_x = 5
                current_x = 0  
            elif character_cords[self.cord_num] == (0, 12) and self.direction == 'left':
                self.ghost_x = 130
                current_x = 14
            
            # force ghost outside of ghost house
            elif board[current_y][current_x] == 2 or board[current_y][current_x] == 5:
                self.direction = 'up'
            
            # if tile is 3 then ghost can only go in one direction
            elif board[current_y][current_x] == 3:
                if board[current_y - 1][current_x] != 1 and self.direction != 'down':
                    self.direction = 'up'
                elif board[current_y + 1][current_x] != 1 and self.direction != 'up':
                    self.direction = 'down'
                elif board[current_y][current_x - 1] != 1 and self.direction != 'right':
                    self.direction = 'left'
                elif board[current_y][current_x + 1] != 1 and self.direction != 'left':
                    self.direction = 'right'
            
            elif board[current_y][current_x] == 4:
                possible_paths = []
                
                # put possible positions in a list
                if board[current_y - 1][current_x] != 1 and self.direction != 'down':
                    possible_paths.append(['up',(current_y - 1, current_x)])  
                if board[current_y + 1][current_x] != 1 and self.direction != 'up':
                    possible_paths.append(['down',(current_y + 1, current_x)])       
                if board[current_y][current_x + 1] != 1 and self.direction != 'left':
                    possible_paths.append(['right',(current_y, current_x + 1)])      
                if board[current_y][current_x - 1] != 1 and self.direction != 'right':
                    possible_paths.append(['left',(current_y, current_x - 1)])
                    
                # find direct distance from possible next positions to pacman's position (use hypotenuse)
                for i in range(len(possible_paths)):
                    a = target_x - possible_paths[i][1][1]
                    b = target_y - possible_paths[i][1][0]
                    c = math.sqrt(a**2 + b**2)
                    possible_paths[i].append(c)
                
                # find shortest hypotenuse
                for i in range(len(possible_paths)):
                    if i == 0:
                        shortest_path = (possible_paths[i][0],possible_paths[i][2])
                        
                    elif possible_paths[i][2] < shortest_path[1]:
                        shortest_path = (possible_paths[i][0],possible_paths[i][2])
                
                # set direction to the tile that has the shortest hypotenuse to pacman
                self.direction = shortest_path[0]
                    
        # makes ghosts move slower than pacman           
        if self.slow_move == 0:
            if self.direction == 'up':
                self.ghost_y -= 4
                #current_y -= 1
            elif self.direction == 'down':
                self.ghost_y += 4
                #current_y += 1
            elif self.direction == 'left':
                self.ghost_x -= 4
                #current_x -= 1
            elif self.direction == 'right':
                self.ghost_x += 4
                #current_x += 1
            self.slow_move = 1
        
        else:
            if self.direction == 'up':
                self.ghost_y -= 5
                current_y -= 1
            elif self.direction == 'down':
                self.ghost_y += 5
                current_y += 1
            elif self.direction == 'left':
                self.ghost_x -= 5
                current_x -= 1
            elif self.direction == 'right':
                self.ghost_x += 5
                current_x += 1
            self.slow_move = 0
        
        # update ghost coordinates
        character_cords[self.cord_num] = (current_x, current_y)

    def draw_ghost(self):
        display.set_pen(self.color)
        display.circle(self.ghost_x, self.ghost_y, piece_size)
        
# ////////////////////////////////////////////////////////////////////////////////////////////

# condense pacman and ghost code
def pacman_handler(pacman):
    pacman.direct_pacman()
    pacman.move_pacman()
    pac_direction = pacman.draw_pacman()
    update_pellets()
    return pac_direction

def ghost_handler(ghosts, pac_direction, active_ghost):
    for i in range(4):
        if active_ghost:
            if i == 0:
                ghosts[i].direct_red()
            elif i == 1:
                ghosts[i].direct_blue(pac_direction)
            elif i == 2:
                ghosts[i].direct_pink(pac_direction)
            elif i == 3:
                ghosts[i].direct_orange()
            ghosts[i].move_ghost()
        ghosts[i].draw_ghost()

# resets screen after a death, resets all pellets if all lives are lost
def setup_screen(hit):
    pacman = Pacman_brains()
    red_ghost = Ghost_brains(red, width//2, 103, (7, 11), 1, '')
    blue_ghost = Ghost_brains(cyan, width//2 - 9, 112, (6, 12), 2, 'right')
    pink_ghost = Ghost_brains(pink, width//2, 112, (7, 12), 3, '')
    orange_ghost = Ghost_brains(orange, width//2 + 9, 112, (8, 12), 4, 'left')
    ghosts = [red_ghost,blue_ghost,pink_ghost,orange_ghost]
    active_ghost = False
    if not hit:
        create_pellets()
    return pacman,ghosts,active_ghost

# draws the lives (self-explanitory)
def draw_lives(lives):
    display.set_pen(yellow)
    if lives >= 1:
        display.circle(width//7,height - piece_size-2,piece_size)
    if lives >= 2:
        display.circle(width//7+(piece_size*3),height - piece_size-2,piece_size)
    if lives >= 3:
        display.circle(width//7+(piece_size*6),height - piece_size-2,piece_size)

# sets up the variables
pacman,ghosts, active_ghost = setup_screen(False)
lives = 3
screens_cleared = 0
highscore = 8

start = False
# actual running of code
while True:
    if not start:
        start = homescreen(highscore)
        continue
    
    time.sleep(0.14)  # pseudo fps
    clear()
    draw_board(tile_color)
    draw_pellets()
    pac_direction = pacman_handler(pacman)
    ghost_handler(ghosts, pac_direction, active_ghost)
    
    # does begin game until player input is given
    if pac_direction != '':
        active_ghost = True
    
    # win state
    if len(pellets) == 0:
        for i in range(7):
            draw_board(white)
            display.update()
            time.sleep(0.15)
            draw_board(tile_color)
            display.update()
            time.sleep(0.15)
        pellets = []
        pacman,ghosts, active_ghost = setup_screen(False)
        lives = 3
        screens_cleared += 1
        if screens_cleared > highscore:
            highscore = screens_cleared
    
    # hit detection (ghost)
    for i in range(1,5):
        if character_cords[0] == character_cords[i]:
            time.sleep(1)
            pacman,ghosts, active_ghost = setup_screen(True)
            lives -= 1
    
    # all lives lost
    if lives == -1:
        time.sleep(1)
        pellets = []
        pacman,ghosts, active_ghost = setup_screen(False)
        lives = 3
        screens_cleared = 0
        start = False
                    
    draw_lives(lives)
    
    # numbers of screens cleared
    display.set_pen(white)
    display.text(str(screens_cleared),width//2+50,height-14)
    
    display.update()