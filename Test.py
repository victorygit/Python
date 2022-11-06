from pickle import TRUE
import tkinter as tk
from tkinter import ALL
from xml.sax import SAXNotRecognizedException
from xml.sax.handler import DTDHandler

# Constants
CIRCLE1_X = 250
CIRCLE1_Y = 250
SIZE = 10  # Height and width of the two "circle" Canvas objects.
EXTENT = SIZE // 2  # Their height and width as measured from center.
CIRCLE2_X = 250 + SIZE
CIRCLE2_Y = 250


def _create_circle(self, x, y, r, **kwargs):
	return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

class Ship_Class:

	def __init__(self, id) -> None:
		self.ship_id = id
		self.ship_occupied_grid = []
		sinked = False
		__total_ship_art = 0
		__hitted_ship_part = 0

	def append_shipgrid(self,number):
		self.ship_occupied_grid.append(number)
	def print_shipgrid(self):
		print(self.ship_occupied_grid)

class Player_Class:
	total_ship = 0
	sinked_ship = 0
	occupied_grid = []
	
	def __init__(self) -> None:
		self.ship_list = []

	def append_grid(self,number):
		self.occupied_grid.append(number)
		
	def print_grid(self):
		print(self.occupied_grid)
	def append_ship(self,ship):
		self.ship_list.append(ship)
		print("ship added")
	def print_ship(self):		
		for ship in self.ship_list:	
			print(ship.ship_id)
			ship.print_shipgrid()


root = tk.Tk()

#Grid
GAME_SIZE = 500 # height of the game window in pixels, width is half of this
GRID_SIZE = 10 # how many blocks each player's grid
MAX_PLAYERS = 2
SHIP_LENGTHS = [5, 4, 3, 3, 2]
QUEUE_BLOCK_SIZE = 16
frame = tk.Frame(root, width=1000, height=1000, background="bisque")
frame.pack()
c = tk.Canvas(frame, width=int(GAME_SIZE / 2), height=GAME_SIZE)
#c.pack(fill=BOTH, expand=1)
c_placement_queue = tk.Canvas(frame, width=int(GAME_SIZE / 2), height=(len(SHIP_LENGTHS) * QUEUE_BLOCK_SIZE))
#canvas_placement_queue.pack(fill=Y)
c.create_circle = _create_circle
c.pack()
c_placement_queue.pack()
c.update()
grid_block_height = int(c.winfo_height() / 2 / GRID_SIZE)
grid_block_width = int(c.winfo_width() / GRID_SIZE)
#print(grid_block_height,grid_block_width)
for p in range(MAX_PLAYERS, 0, -1):
	for y in range(int(GAME_SIZE / 2 * (p - 1)) - 1, int(GAME_SIZE / 2 * p) + 1, grid_block_height):
		# for x in range(int(GAME_SIZE * .25), int(GAME_SIZE * .75), self.grid_block_width):
		for x in range(0, int(GAME_SIZE / 2) + 1, grid_block_width):
			# print("placing grid block {}".format((x, y, x + self.grid_block_width, y + self.grid_block_height)))
			c.create_rectangle(x, y, x + grid_block_width, y + grid_block_height)
# draw the queue
for i in range(0, len(SHIP_LENGTHS)):
	y = QUEUE_BLOCK_SIZE * i + 5
	# for x in range(int(GAME_SIZE * .25), int(GAME_SIZE * .75), self.grid_block_width):
	for x in range(0, grid_block_width * SHIP_LENGTHS[i], grid_block_width):
		# print("placing grid block {}".format((x, y, x + self.grid_block_width, y + self.grid_block_height)))
		c_placement_queue.create_oval(x+10, y, x + 10+SIZE, y + SIZE, fill = "green")
		print(x,y)


# draw a thicker line in the middle between the player's boards
c.create_line(0, int(GAME_SIZE / 2), int(GAME_SIZE / 2), int(GAME_SIZE / 2), width=3)
MiddlePoint = int(GAME_SIZE / 2)
circle_color = 'white'
circle_list = []
circle1 = c.create_oval(CIRCLE1_X, CIRCLE1_Y,
                        CIRCLE1_X + SIZE, CIRCLE1_Y + SIZE,fill = circle_color)
circle2 = c.create_oval(CIRCLE2_X, CIRCLE2_Y,
                             CIRCLE2_X + SIZE, CIRCLE2_Y + SIZE, fill = circle_color)
circle3 = c.create_oval(CIRCLE2_X+SIZE, CIRCLE2_Y,
                             CIRCLE2_X + SIZE * 2, CIRCLE2_Y + SIZE, fill = circle_color)
circle4 = c.create_oval(CIRCLE2_X+SIZE, CIRCLE2_Y,
                             CIRCLE2_X + SIZE * 2, CIRCLE2_Y + SIZE, fill = circle_color)
circle5 = c.create_oval(CIRCLE2_X+SIZE, CIRCLE2_Y,
                             CIRCLE2_X + SIZE * 2, CIRCLE2_Y + SIZE, fill = circle_color)
circle_list.append(circle1)
circle_list.append(circle2)
circle_list.append(circle3)
circle_list.append(circle4)
circle_list.append(circle5)
queue_number = 0
circle_numer = SHIP_LENGTHS[0]
global boat_rotation
boat_rotation = False
ship_count = 0
# Player
me = Player_Class()
computer = Player_Class()
#pos1 = c.coords(circle1)
#pos2 = c.coords(circle2)

#c.move(circle1, 250-pos1[0], 250-pos1[2])
#c.move(circle2, 250-pos1[0], 250-pos1[2])


def move_circles(event):
	#c.delete(ALL)
	# Move two "circle" widgets so they're centered at event.x, event.y.
	x0, y0 = event.x - EXTENT, event.y - EXTENT
	x1, y1 = event.x + EXTENT, event.y + EXTENT
	if y0 < MiddlePoint:
		circle_color = 'red'
	else:
		circle_color = 'green'
	global queue_number
	if queue_number <= len(SHIP_LENGTHS)-1:
		circle_numer = SHIP_LENGTHS[queue_number]
	else:
		circle_numer = 1
	
	for i in range(0,circle_numer):
		c.itemconfig(circle_list[i], fill=circle_color)
	
	
	if boat_rotation == False:
		for i in range(0,circle_numer):
			c.coords(circle_list[i], x0+grid_block_width * i , y0, x1+grid_block_width * i, y1)	
	else:
		for i in range(0,circle_numer):
			c.coords(circle_list[i], x0, y0+grid_block_height * i, x1, y1+grid_block_height * i)


	
def on_Rightclick(event):
	global boat_rotation 
	boat_rotation = not boat_rotation

def on_Click(event):
	#x0, y0 = event.x - EXTENT, event.y - EXTENT
	#x1, y1 = event.x + EXTENT, event.y + EXTENT
	#grid center
	if event.y < MiddlePoint:
		return
	xc= event.x //grid_block_width * grid_block_width +grid_block_width /2
	yc = event.y //grid_block_height * grid_block_height + grid_block_height /2
	r = 5
	x0, y0 = xc-r, yc-r
	x1, y1 = xc+r, yc+r
	# Get the grid number
	grid_number = int(event.y // grid_block_height * int(GAME_SIZE /2 //grid_block_width)  + event.x //grid_block_width)+1
	# create ship
	global ship_count
	global queue_number
	if queue_number < len(SHIP_LENGTHS):
		ship_count = ship_count + 1
		globals()[f"ship{str(ship_count)}"] = Ship_Class(ship_count)
		me.append_ship(globals()[f"ship{str(ship_count)}"])
		circle_numer = SHIP_LENGTHS[queue_number]
		if boat_rotation == False:
			for i in range(0,circle_numer):
				c.create_oval(x0 + grid_block_width * i,y0,x1+ grid_block_width * i,y1,fill= 'grey')	
				me.append_grid(grid_number + i)	
				globals()[f"ship{str(ship_count)}"].append_shipgrid(grid_number + i)
			
		else:
			for i in range(0,circle_numer):
				c.create_oval(x0,y0 + grid_block_height * i,x1,y1 + grid_block_height * i,fill= 'grey')	
				# create ship
				me.append_grid(grid_number + i * int(GAME_SIZE /2 //grid_block_width))
				globals()[f"ship{str(ship_count)}"].append_shipgrid(grid_number + i * int(GAME_SIZE /2 //grid_block_width))
		me.print_grid()
		me.print_ship()
		queue_number = queue_number + 1


c.bind('<Motion>', move_circles)
c.bind("<Button-1>", on_Click)
c.bind("<Button-3>", on_Rightclick)
root.mainloop()