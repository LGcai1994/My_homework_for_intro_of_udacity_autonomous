import localizer 
import random
from copy import deepcopy
from matplotlib import pyplot as plt

class Simulation(object):
    #construction function
	def __init__(self, grid, blur, p_hit,start_pos=None):
		"""

		"""
		self.grid = grid
        #initialize beliefs
		self.beliefs = localizer.initialize_beliefs(self.grid)
		self.height = len(grid)
		self.width  = len(grid[0])
		self.blur   = blur
		self.p_hit = p_hit
		self.p_miss = 1.0
		self.incorrect_sense_probability = self.p_miss / (p_hit + self.p_miss)
        #get world colors
		self.colors = self.get_colors()
		self.num_colors = len(self.colors)
		if not start_pos:
			self.true_pose = (int(self.height/2), int(self.width/2))
		else:
			self.true_pose = start_pos
		self.prev_pose = self.true_pose
		self.prepare_visualizer()

        #initialize all the X,Y,P
	def prepare_visualizer(self):
		self.X = []
		self.Y = []
		self.P = []
    
    #count all color types
	def get_colors(self):
		all_colors = []
        #go through all the world(gird) and count the number of colors （prevent double choice)
		for row in self.grid:
			for cell in row:
				if cell not in all_colors:
					all_colors.append(cell)
		return all_colors

    #sense the color and update beliefs
	def sense(self):
        #get sensed color
		color = self.get_observed_color()
		beliefs = deepcopy(self.beliefs)
        #according to the sensed color and update beliefs
		new_beliefs = localizer.sense(color, self.grid, beliefs, self.p_hit, self.p_miss)
		if not new_beliefs or len(new_beliefs) == 0:
			print("NOTE! The robot doesn't have a working sense function at this point.")
			self.beliefs = beliefs
		else:
			self.beliefs = new_beliefs

    #move and update the beliefs
	def move(self, dy, dx):
        #get the new position
		new_y = (self.true_pose[0] + dy) % self.height
		new_x = (self.true_pose[1] + dx) % self.width
        #back up
		self.prev_pose = self.true_pose
		self.true_pose = (new_y, new_x)
		beliefs = deepcopy(self.beliefs)
        #move and update the beliefs
		new_beliefs = localizer.move(dy, dx, beliefs, self.blur)
		self.beliefs = new_beliefs

    #get observed color
	def get_observed_color(self):
        #get ground true color
		y,x = self.true_pose
		true_color = self.grid[y][x]
        #god make his dice
        #for incorrect color, select one
		if random.random() < self.incorrect_sense_probability:
			possible_colors = []
			for color in self.colors:
				if color != true_color and color not in possible_colors:
					possible_colors.append(color)
			color = random.choice(possible_colors)
        #for correct color, make it true
		else:
			color = true_color
		return color
    
#visualize the belifes
	def show_beliefs(self,past_turn=False):
        #copy past turn
		if past_turn:
			X = deepcopy(self.X)
			Y = deepcopy(self.Y)
			P = deepcopy(self.P)
		#delete X,Y,P
		del(self.X[:])
		del(self.Y[:])
		del(self.P[:])
        #unpack beliefs, let x,y,p related to each other
		for y, row in enumerate(self.beliefs):
			for x, belief in enumerate(row):
				self.X.append(x)
				self.Y.append(self.height-y-1) # puts large y ABOVE small y
				self.P.append(5000.0 * belief)
		plt.figure()
        #plot scatter diagram
		if past_turn:
			plt.scatter(X, Y, s=P, alpha=0.3,color="blue")
			plt.scatter([self.prev_pose[1]], [self.height-self.true_pose[0]-1], color='red', marker="*", s=200, alpha=0.3)
		plt.scatter(self.X,self.Y,s=self.P,color="blue")
		plt.scatter([self.true_pose[1]], [self.height-self.true_pose[0]-1], color='red', marker="*", s=200)
		plt.show()
        
    #show belief values
	def show_rounded_beliefs(self):
		for row in self.beliefs:
			for belief in row:
				print("{:0.3f}".format(belief),end=" ")
			print(" ")                
		return
    
    #random move
	def random_move(self):
		dy = random.choice([-1,0,1])
		dx = random.choice([-1,0,1])
		return dy,dx
    
    #object sense and move one step randomly in X and Y direction
	def run(self, num_steps=1):
        #repeat sense and move i times
		for i in range(num_steps):
            #sense the world and update beliefs
			self.sense()
            #decide which way to go
			dy, dx = self.random_move()
            #move and update its beliefs
			self.move(dy,dx)