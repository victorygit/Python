#Importing the things in tkinter, importing the Font class from the font section of it,
# as well as random
from tkinter import *
import random
from tkinter.font import Font
import webbrowser
import os


#Defining the Ship class
class Ship:
    #Defining the constructor function (which uses __init__)
    def __init__(self, ship_num): #It takes a ship number as a parameter.
        #The ship number parameter will define the ship and be set as its 'id' (e.x.
        # ship 1, ship 2, etc.).
        #With every ship object, a list will be created along with it that will store the
        # area that the ship occupies (in terms of grid numbers).
        self.ship_id = ship_num
        self.ship_occupied_area = []
    #Defining the function that will be used to add a grid number to ship area list.
    def append_grid_area(self, grid_num):
        #Adding the passed grid number to the ship area list.
        self.ship_occupied_area.append(grid_num)
    #Defining an accessor method that will return the ship area list.
    def get_grid_area(self):
        return self.ship_occupied_area
    #Defining the function that will print out the ship area list.
    def print_grid_area(self):
        print(self.ship_occupied_area)
    #Defining the function that will clear the ship area list
    def clear_grid_area(self):
        #Using the .clear() function to clear the list
        self.ship_occupied_area.clear()

#Defining the Player class.
class Player:
    #Defining the constructor function (which uses __init__)
    def __init__(self):
        #Upon creating a Player object, two empty lists are created.
        #One will store the ship objects that the Player object has and the other will
        # store the area that those ships occupy (not individually this time).
        self.ships_list = []
        self.occupied_grid_area = []
    #Defining an accessor method that will return the occupied area list
    def get_occupied_area(self):
        return self.occupied_grid_area
    #Defining the function that will print out the occupied area 
    def print_occupied_area(self):
        print(self.occupied_grid_area)
    #Defining the function that will add a ship object and its area list
    def add_ship(self, ship):
        #Adding the ship object into the ships list 
        self.ships_list.append(ship)
        #Looping through its area list and adding them into the occupied area list
        # which stores all ships' areas.
        for item in ship.get_grid_area():
            self.occupied_grid_area.append(item)
    #Defining the function that will print out each ship object's ship id and its area
    # list.
    def print_ships_grid(self):
        for ship in self.ships_list:
            print(ship.ship_id)
            ship.print_grid_area()
    #Defining the function that will clear the occupied area list and ships.
    def clear_grid_list(self):
        #Clearing the occupied area list
        self.occupied_grid_area.clear()
        #Removing each ship object from the ships list.
        for ship in self.ships_list:
            self.ships_list.remove(ship)
    #Defining the function that will clear the occupied area list.
    def clear_occupied_area(self):
        self.occupied_grid_area.clear()
    #Defining the function that will sort the occupied area list and return it back.
    def sort_occupied_area(self):
        self.occupied_grid_area.sort()
        return self.occupied_grid_area

#Defining the constants to be used in the game
CIRCLE_X = 250 #X-coordinate of a circle's top left corner
CIRCLE_Y = 250 #Y-coordinate of a circle's top left corner
EXTENT = 5 #Radius of circle
SIZE = 10 #Diameter of circle
GAME_SIZE = 500 #How big the canvas will be (a.k.a. the height)
#Width and height of each grid block
grid_block_width = 25 
grid_block_height = 25

#Defining a function that will check whether or not the position the user wants to place
# a ship onto is valid. It takes the first circle's top left and bottom right coordinates
# as well as the number of circles and the boolean indicating rotation as parameters.
def check_position(circle_x1, circle_y1, circle_x2, circle_y2, num, rotate_bool):
    #Checking what the rotation boolean is
    if rotate_bool == False:
        #If it is False, then add to the y-coordinates the height of the grid block times
        # the number of circles minus 1 so that you get the top left and bottom right 
        # y-coordinates of the last circle to be drawn.
        last_circle_y1 = circle_y1 + (grid_block_height * (num-1))
        last_circle_y2 = circle_y2 + (grid_block_height * (num-1))
        #Checking if they are bigger than the canvas height/500.
        if last_circle_y1 > GAME_SIZE and last_circle_y2 > GAME_SIZE:
            #If they are, return False
            return False
        else:
            #If they aren't, return True
            return True
    else:
        #If it is True, then add to the x-coordinates the width of the grid block times
        # the number of circles minus 1 so that you get the top left and bottom right 
        # x-coordinates of the last circle to be drawn.
        last_circle_x1 = circle_x1 + (grid_block_width * (num-1))
        last_circle_x2 = circle_x2 + (grid_block_width * (num-1))
        #Checking if they are bigger than the canvas width/250.
        if last_circle_x1 > (GAME_SIZE/2) and last_circle_x2 > (GAME_SIZE/2):
            #If they are, return False
            return False
        else:
            #If they aren't, return True
            return True

#Defining a function that will check whether a grid number/position has been taken
def position_taken(Player, grid_num): #Taking a Player object and grid number as inputs.
    #Checking if the passed grid number if in the Player object's occupied area
    if grid_num in Player.get_occupied_area():
        #If it is, return True
        return True
    else:
        #If it isn't return False.
        return False

#Defining a function that will end the game and program.
def end_game():
    #Importing the sys library and calling the exit() function
    import sys; sys.exit()

#Defining the function that will run the play phase of the game
def hit_or_miss(event):
    #Making the win and lose variables global
    global win, lose
    #Checking if either the win or lose variable is True
    if win == True or lose == True:
        #If one of them is, then return and don't do anything.
        return
    #Checking the position of the mouse.
    if event.y > 250:
        #If the y-coordinate if bigger than 250 (a.k.a. outside of the PC's side of the
        # game board), then return and don't do anything.
        return
    if event.x > 250:
        #If the x-coordinate if bigger than 250 (a.k.a. outside of the PC's side of the
        # game board), then return and don't do anything.
        return
    #If the position if valid, then calculate the grid number through the x and y coordinates of 
    # the mouse.
    grid_number = int(event.y // grid_block_height * int(GAME_SIZE /2 //grid_block_width)  + event.x //grid_block_width)+1
    #Checking if the grid number is in the computer's occupied area list and not already in the 
    # person hit list.
    if grid_number in comp.get_occupied_area() and grid_number not in person_hit_list:
        #If it fits the conditions, then add it to the person hit list.
        person_hit_list.append(grid_number)
        #Through the position of the mouse, calculate the center of the grid block that has been
        # clicked on.
        xc = event.x //grid_block_width * grid_block_width +grid_block_width /2
        yc = event.y //grid_block_height * grid_block_height + grid_block_height /2
        #By subtracting or adding the radius of the circles to the center coordinates, we can get
        # the top left and bottom right coordinates of the circle to be drawn.
        x0, y0 = xc - EXTENT, yc - EXTENT
        x1, y1 = xc + EXTENT, yc + EXTENT
        #Creating an oval/a circle through the above calculated coordinates and making it red to 
        # signify that the person has hit a ship.
        grid_canvas.create_oval(x0,y0,x1,y1,fill='red')
    #Checking if the grid number is not in the computer's occupied area list 
    #Note that here, I am not checking if it's already not in the hit list since they may have just
    # clicked the same spot 2 times in which we don't want to append it into the person miss list.
    elif grid_number not in comp.get_occupied_area():
        #If it is not, then add it into the person miss list.
        person_miss_list.append(grid_number)
        #Through the position of the mouse, calculate the center of the grid block that has been
        # clicked on.
        xc = event.x //grid_block_width * grid_block_width +grid_block_width /2
        yc = event.y //grid_block_height * grid_block_height + grid_block_height /2
        #By subtracting or adding the radius of the circles to the center coordinates, we can get
        # the top left and bottom right coordinates of the circle to be drawn.
        x0, y0 = xc - EXTENT, yc - EXTENT
        x1, y1 = xc + EXTENT, yc + EXTENT
        #Creating an oval/a circle through the above calculated coordinates and making it white to 
        # signify that the person has missed the ships.
        grid_canvas.create_oval(x0,y0,x1,y1,fill='white')
    #Initially setting the while loop condition to be True
    valid_grid = False
    while valid_grid == False:
        #Generating a top left coordinate through the use of random in the range of the person's 
        # side of the canvas.
        comp_grid_x = random.randrange(0,250,25)
        comp_grid_y = random.randrange(250,500,25)
        if comp_grid_x == 250 and comp_grid_y == 500:
            continue
        else:
            valid_grid = True
    grid_x_center = (comp_grid_x * 2 + 25) / 2
    grid_y_center = (comp_grid_y * 2 + 25) / 2
    grid_number = int(grid_y_center // grid_block_height * int(GAME_SIZE /2 //grid_block_width)  + grid_x_center //grid_block_width)+1
    if grid_number in person.get_occupied_area() and grid_number not in comp_hit_list:
        comp_hit_list.append(grid_number)
        grid_canvas.create_text(275,20,fill='red',text='HIT')
        x0, y0 = grid_x_center - EXTENT, grid_y_center - EXTENT
        x1, y1 = grid_x_center + EXTENT, grid_y_center + EXTENT
        grid_canvas.create_oval(x0,y0,x1,y1,fill='red')
    elif grid_number not in person.get_occupied_area():
        comp_miss_list.append(grid_number)
        grid_canvas.create_text(275,20,fill='black',text='MISS')
        x0, y0 = grid_x_center - EXTENT, grid_y_center - EXTENT
        x1, y1 = grid_x_center + EXTENT, grid_y_center + EXTENT
        grid_canvas.create_oval(x0,y0,x1,y1,fill='white')
    global win_window, lose_window
    person_hit_list.sort()
    text_font = Font(size=10)
    if person_hit_list == comp.sort_occupied_area():
        win = True
        win_window = Tk()
        win_window.title('Results')
        # =============== change by Victor
        win_window.iconbitmap('icon/info.ico')
        # ================================
        # =============  Add by Victor        
        win_window.geometry(f'+{root_window.winfo_rootx()+100}+{root_window.winfo_rooty()+ 300}')
        # ==============
        win_label = Label(win_window, font=text_font,text='Congratulations! You have won. \n  Would you like to play again?')
        win_label.grid(row=0, column=0, columnspan=2)
        replay_button = Button(win_window, text='Replay/Rematch', command=restart_game)
        replay_button.grid(row=1, column=0)
        quit_button = Button(win_window, text='Exit', command=end_game)
        quit_button.grid(row=1, column=1)
        win_window.mainloop()
        return
    comp_hit_list.sort()
    if comp_hit_list == person.sort_occupied_area():
        lose = True
        lose_window = Tk()
        lose_window.title('Results')
        # =============  Add by Victor
        lose_window.iconbitmap('icon/info.ico')             
        lose_window.geometry(f'+{root_window.winfo_rootx()+100}+{root_window.winfo_rooty()+ 300}')
        # ==============
        lose_label = Label(lose_window, font=text_font,text='Sorry. You have lost. Would you like to play again?')
        lose_label.grid(row=0,column=0)
        replay_button = Button(lose_window, text='Replay/Rematch', command=restart_game)
        replay_button.grid(row=1, column=0)
        quit_button = Button(lose_window, text='Exit', command=end_game)
        quit_button.grid(row=1,column=1)
        lose_window.mainloop()
        return

def restart_game():
    global win,lose, queue_number, times_clicked, person_hit_list, comp_hit_list
    #global place_ships()
    queue_number = 0
    times_clicked = 0
    person_hit_list = []
    comp_hit_list = []
    place_ships()
    if win == True:
        win_window.destroy()
        win = False
    if lose == True:
        lose_window.destroy()
        lose = False

def play_battleship():
    grid_canvas.bind('<Button-1>', hit_or_miss)


def computer_setup():
    global comp
    play_window.destroy()
    comp = Player()
    queue_number = 0
    while queue_number != max(ship_lengths):
        valid_pos = False
        while valid_pos == False:
            first_circle_x1 = random.randrange(0,250,25)
            first_circle_y1 = random.randrange(0,250,25)
            first_circle_x2 = first_circle_x1 + grid_block_width
            first_circle_y2 = first_circle_y1 + grid_block_height
            bools = [True, False]
            rotate = bools[random.randint(0,1)]
            if queue_number <= len(ship_lengths)-1:
                circle_number = ship_lengths[queue_number]
            else:
                circle_number = 1
                return
            if rotate == True:
                last_circle_x1 = first_circle_x1 + (grid_block_width * (circle_number-1))
                last_circle_x2 = first_circle_x2 + (grid_block_width * (circle_number-1))
                if last_circle_x1 > (GAME_SIZE/2) or last_circle_x2 > (GAME_SIZE/2):
                    continue
                else:
                    break
            else:
                last_circle_y1 = first_circle_y1 + (grid_block_height * (circle_number-1))
                last_circle_y2 = first_circle_y2 + (grid_block_height * (circle_number-1))
                if last_circle_y1 > (GAME_SIZE/2) or last_circle_y2 > (GAME_SIZE/2):
                    continue
                else:
                    break
        first_circle_x_center = (first_circle_x1 + first_circle_x2) / 2
        first_circle_y_center = (first_circle_y1 + first_circle_y2) / 2
        grid_number = int(first_circle_y_center // grid_block_height * int(GAME_SIZE /2 //grid_block_width)  \
        + first_circle_x_center //grid_block_width)+1
        global num_ships
        num_ships += 1
        ship = Ship(num_ships)
        for i in range(0,circle_number):
            position_check = position_taken(comp, grid_number)
            if position_check == False:
                ship.append_grid_area(grid_number)
                if rotate == True:
                    grid_number += 1
                else:
                    grid_number += 10
            else:
                ship.clear_grid_area()
                break
        if position_check == True:
            num_ships -= 1
            continue
        comp.add_ship(ship)
        x0, y0 = first_circle_x_center - EXTENT, first_circle_y_center - EXTENT
        x1, y1 = first_circle_x_center + EXTENT, first_circle_y_center + EXTENT
        if rotate == False:
            #print(circle_number)
            for i in range(0,circle_number):
                grid_canvas.create_oval(x0,y0 + (grid_block_width * i),x1, y1 + (grid_block_width * i), fill='gray', tags='my_tags')
        else:
            for i in range(0,circle_number):
                grid_canvas.create_oval(x0 + (grid_block_height * i),y0,x1 + (grid_block_height * i), y1, fill='gray', tags='my_tags')
        queue_number += 1
    play_battleship()

def exit():
    play_window.destroy()

def right_click(event):
    global rotate_ship
    rotate_ship = not rotate_ship

def left_click(event):

    global times_clicked
    if event.y < 250:
        return
    if event.x > 250:
        return
    times_clicked += 1
    grid_number = int(event.y // grid_block_height * int(GAME_SIZE /2 //grid_block_width)  + event.x //grid_block_width)+1
    global queue_number
    global num_ships
    if queue_number <= len(ship_lengths)-1:
        circle_number = ship_lengths[queue_number]
    else:
        circle_number = 1
        return
    xc = event.x //grid_block_width * grid_block_width +grid_block_width /2
    yc = event.y //grid_block_height * grid_block_height + grid_block_height /2
    x0, y0 = xc - EXTENT, yc - EXTENT
    x1, y1 = xc + EXTENT, yc + EXTENT
    num_ships += 1
    ship = Ship(num_ships)
    valid_position = check_position(x0,y0,x1,y1,circle_number, rotate_ship)
    for i in range(0,circle_number):
        position_check = position_taken(person, grid_number)
        if position_check == False:
            ship.append_grid_area(grid_number)
            if rotate_ship == False:
                grid_number += 10
            else:
                grid_number += 1
        else:
            ship.clear_grid_area()
            break
    if position_check == True or valid_position == False:
        num_ships -= 1
        times_clicked -= 1
        return
    person.add_ship(ship)
    #person.append_grid_num()
    if rotate_ship == False:
        for i in range(0,circle_number):
            grid_canvas.create_oval(x0,y0 + (grid_block_width * i),x1, y1 + (grid_block_width * i), fill='gray', tags='my_tags')
    else:
        for i in range(0,circle_number):
            grid_canvas.create_oval(x0 + (grid_block_height * i),y0,x1 + (grid_block_height * i), y1, fill='gray', tags='my_tags')
    if times_clicked != 3:
        grid_canvas.itemconfigure(circle_list[circle_number-1], state = 'hidden')
    queue_number += 1
    if queue_number == max(ship_lengths):
        global play_window
        play_window = Tk()
        # =============  Add by Victor        
        play_window.geometry(f'+{root_window.winfo_rootx()+100}+{root_window.winfo_rooty()+ 300}')
        play_window.iconbitmap('icon/question.ico')
        # ==============
        play_window.title('Ready to Play')
        play_label = Label(play_window, text='Are you ready to play?')
        play_label.grid(row=0,column=0)
        play_button = Button(play_window, text='Yes', command=computer_setup)
        play_button.grid(row=1, column=0)
        cancel_button = Button(play_window, text='No', command=exit)
        cancel_button.grid(row=1,column=1)
        play_window.mainloop()

def mouse_move(event):
 
    x0, y0 = event.x - EXTENT, event.y - EXTENT
    x1, y1 = event.x + EXTENT, event.y + EXTENT
    if event.y < 250:
        circle_color = 'red'
    else:
        circle_color = 'green'
    global queue_number
    if queue_number <= len(ship_lengths)-1:
        circle_number = ship_lengths[queue_number]
    else:
        circle_number = 1
    if event.x > 250:
        return
    global circle_list
    for i in range(0,circle_number):
        grid_canvas.itemconfig(circle_list[i], fill=circle_color)
    if rotate_ship == False:
        for i in range(0,circle_number):
            grid_canvas.coords(circle_list[i], x0, y0 + (25 * i), x1, y1 + (25 * i))
    else:
        for i in range(0,circle_number):
            grid_canvas.coords(circle_list[i], x0 + (25 * i), y0, x1 + (25 * i), y1)

def clear_ships():
    grid_canvas.delete('my_tags')
    global queue_number, circle_number, circle_list, num_ships, times_clicked
    circle_number = 5
    queue_number = 0
    num_ships = 0
    times_clicked = 0
    person.clear_grid_list()
    place_ships()
    for i in range(0, circle_number):
        grid_canvas.coords(circle_list[i], 500, 500,500, 500)
        grid_canvas.itemconfigure(circle_list[i], state = 'normal')
    reset_window.destroy()

def go_back():
    reset_window.destroy()

def user_reset():
    global reset_window
    reset_window = Tk()
    reset_window.title('Reset Request')
    # =============  Add by Victor       
    reset_window.iconbitmap('icon/question.ico')
    reset_window.geometry(f'+{root_window.winfo_rootx()+100}+{root_window.winfo_rooty()+ 300}')
    # ==============
    reset_label = Label(reset_window, text='Are you sure you want to reset?')
    reset_label.grid(row=0, column=0)
    reset_button = Button(reset_window, text='Yes', command=clear_ships)
    reset_button.grid(row=1,column=0)
    return_button = Button(reset_window, text='No', command=go_back)
    return_button.grid(row=2, column=0)
    reset_window.mainloop()

def place_ships():
    global grid_canvas
    grid_canvas = Canvas(battle_frame, bg='white', width=500, height=500)
    grid_canvas.grid(row=2, column=0)   
    global results_label
    results_label = Label(battle_frame)
    results_label.grid(row=4, column=0)
    global circle_list
    circle_list = []
    #Make this so that the circles are created in a for loop that runs for the biggest number of 
    # circles.
    for i in range(max(ship_lengths)):
        circle = grid_canvas.create_oval(CIRCLE_X, CIRCLE_Y + (SIZE * i), CIRCLE_X + SIZE, CIRCLE_Y + (SIZE * (i + 1)), fill='white',outline='black')
        circle_list.append(circle)
    global person
    person = Player()
    for i in range(0,len(circle_list)):
        length = ship_lengths[i]
        for j in range(0,length):
            grid_canvas.create_oval(250 + (25 * j), 250 + (10 * i), 260 + (25 * j), 260 + (10 * i), fill='green')
    for x in range(0,250,25):
        for y in range(0,250,25):
            grid_canvas.create_rectangle(x,y,x+grid_block_height,y+grid_block_width,outline='black')
    for x in range(0,250,25):
        for y in range(250,500,25):
            grid_canvas.create_rectangle(x,y,x+grid_block_height,y+grid_block_width,outline='black')
    play_button.config(text='Reset', command=user_reset)
    user_manual.grid(row=3,column=0)
    #battle_frame.pack()
    #grid_canvas.pack()
    grid_canvas.create_line(0,250,250,250,width=5)
    grid_canvas.bind('<Motion>', mouse_move)
    grid_canvas.bind('<Button-1>',left_click)
    grid_canvas.bind('<Button-3>', right_click)

def print_instructions():
    '''
    intro_window = Tk()
    intro_window.title('Battleship Instructions')
    instructions_frame = Frame(intro_window, width=500,height=500)
    instructions = Label(instructions_frame, text='Shoot the ships!')
    instructions.grid(row=0,column=0)
    instructions_frame.pack()
    intro_window.mainloop()
    '''    
    webbrowser.open('file://'+dir_path+'/help/HelpDemo.html')

queue_number = 0
times_clicked = 0
num_ships = 0
ship_lengths = [5,4,3,2,2]
comp_miss_list = []
comp_hit_list = []
person_miss_list = []
person_hit_list = []
win = False
lose = False
rotate_ship = False
root_window = Tk()
# =============== change by Victor
root_window.title('Battle Ship')
root_window.iconbitmap('icon/Battleship.ico')
root_window.geometry('600x750')
# ================================
battle_frame = Frame(root_window,width=1000, height=1000)
menu_label = Label(battle_frame, text = 'Welcome to the game Battleship!')
menu_label.grid(row=0, column=0)
play_button = Button(battle_frame, text='Set-Up', command=place_ships)
play_button.grid(row=1, column=0)
user_manual = Button(battle_frame, text='Instructions', command=print_instructions)
user_manual.grid(row=2, column=0)
battle_frame.pack()
dir_path = os.path.dirname(os.path.realpath(__file__))
root_window.mainloop()