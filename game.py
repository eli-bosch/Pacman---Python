# Name: Assigment 8 Code, Eli Bosch
# Description: Porting A5 to Python
# Date: 4-27-24

import pygame
import time
import json

import pygame.image
import math
from pygame.locals import*
from time import sleep

class Sprite():
	#Constructor
	def __init__(self, x, y, w, h, image):
		#Sprite Default Variables
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.destroyable = False
		self.speed = 5
		self.image = image
		self.frames = 0

	#Getter Methods
	def getRight(self):
		return (self.x + self.w)
	
	def getBottom(self):
		return (self.y + self.h)
	
	def getLeft(self):
		return (self.x)
	
	def getTop(self):
		return (self.y)
	
	def getImage(self):
		return self.image
	
	#Setter Methods
	def setRight(self, left):
		self.x = left - self.w

	def setBottom(self, top):
		self.y = top - self.h

	def setLeft(self, right):
		self. x = right
	
	def setTop(self, bottom):
		self.y = bottom

	def setDestroyable(self):
		self.destroyable = True

	#is Methods and Class ID
	def isPacman(self):
		return False
	
	def isWall(self):
		return False
	
	def isPellet(self):
		return False
	
	def isFruit(self):
		return False
	
	def isGhost(self):
		return False
	
	def isDestroyable(self):
		return self.destroyable
		
	#Collision Methods
	def canCollide(self):
		return False
	
	def collidedBy(self, sprite):
		pass

	#Draw methods
	def loadImage(self, image):
		return pygame.image.load(image)

	def draw(self, view, scroll):
		view.screen.blit(pygame.transform.scale(self.getImage(), (self.w, self.h)), (self.x, self.y - scroll))
  
	#Update Method
	def update(self):
		pass	

#Pacman Class
class Pacman(Sprite):
    #Constructor
	def __init__(self, x, y):
		#Pacman Default Vaibles
		self.direction = 0
		self.animation = 0
		self.moving = False

		pacmanImages = arr = [[0 for i in range(3)] for j in range(4)]

		for i in range(4):
			for j in range(1 , 4):
				pacmanImages[i][j - 1] = self.loadImage(f"images\\pacmanImages\\pacman{((i*3) + j)}.png")

		super().__init__(x, y, 28, 28, pacmanImages) #Sprite Constructor

	#Overrided Methods
	def getImage(self):
		return self.image[self.direction][self.animation] 
	
	def isPacman(self):
		return True
	
	def canCollide(self):
		return True
	
	#Movement Method
	def handleMove(self, d):
		self.moving = True
		self.direction = d

	#Update Methods
	def updateMovement(self):
		if self.moving:
			match self.direction:
				case 0: self.y += self.speed
				case 1: self.x -= self.speed
				case 2: self.y -= self.speed
				case 3: self.x += self.speed
			self.animation = (self.animation + 1) if (self.animation < 2) else 0
			self.moving = False

	def update(self):
		self.updateMovement()


#Wall Class
class Wall(Sprite):
	#Constructor
	def __init__(self, x, y):
		super().__init__(x, y, 30, 30, self.loadImage("Images\\wallImages\\wall.png")) #Sprite Contructor

	#Overridden Methods
	def isWall(self):
		return True

	def collidedBy(self, sprite): #Checks shortest distance to remove collided Sprite
		right = self.getRight() - sprite.getLeft()
		left = sprite.getRight() - self.getLeft()
		up = sprite.getBottom() - self.getTop()
		down = self.getBottom() - sprite.getTop()
		minimum = min(right, left, up, down)

		if(minimum == right):
			sprite.setLeft(self.getRight() + 1)
			if sprite.isFruit(): sprite.ricochet(True, False)
		elif(minimum == left): 
			sprite.setRight(self.getLeft() - 1)
			if sprite.isFruit(): sprite.ricochet(True, False)
		elif(minimum == up): 
			sprite.setBottom(self.getTop() - 1)
			if sprite.isFruit(): sprite.ricochet(False, True)
		elif(minimum == down): 
			sprite.setTop(self.getBottom() + 1)
			if sprite.isFruit(): sprite.ricochet(False, True)

		
#Pellet Class
class Pellet(Sprite):
	#Constructor
	def __init__(self, x, y):
		super().__init__(x, y, 15, 15, self.loadImage("Images\\spriteImages\\pellet.png")) #Sprite contructor

	#Overridden Methods
	def isPellet(self):
		return True

	def collidedBy(self, sprite):
		if sprite.isPacman():
			self.setDestroyable()

#Fruit Class
class Fruit(Sprite):
	#Contructor
	def __init__(self, x, y):
		super().__init__(x, y, 20, 20, self.loadImage("Images\\spriteImages\\fruit1.png")) #Sprite Contructor
		self.speedX = self.speedY = self.speed #Fruit speed variables

	#Override Methods
	def isFruit(self):
		return True

	def collidedBy(self, sprite):
		if sprite.isPacman():
			self.setDestroyable()
	
	def canCollide(self):
		return True

	#Called when removed from Wall
	def ricochet(self, x, y):
		if x:
			self.speedX*=-1
		if y:
			self.speedY*=-1
	
	#Update Methods
	def updateMovement(self):
		self.x += self.speedX
		self.y += self.speedY
	
	def update(self):
		self.updateMovement()

#Ghost Class
class Ghost(Sprite):
	def __init__(self, x, y):
		#Ghost Default variables
		self.state = 0
		self.animation = 0
		self.dead = False

		ghostImages = arr = [[0 for i in range(8)] for j in range(2)]

		for i in range(2):
			for j in range(1 , 9):
				if i == 1: ghostImages[i][j - 1] = self.loadImage(f"images\\spriteImages\\ghost{j}.png")
				else: ghostImages[i][j - 1] = self.loadImage(f"images\\spriteImages\\blinky{j}.png")

		super().__init__(x, y, 28, 28, ghostImages) #Spirte Constructor

	#Overrided Methods
	def isGhost(self):
		return True
	
	def setDestroyable(self):
		if self.dead != True:
			self.dead = True
			self.state = 1
			self.animation = 0

	def getImage(self):
		return self.image[self.state][self.animation] 
	
	def collidedBy(self, sprite):
		if sprite.isPacman(): self.setDestroyable()
	
	#Update Methods
	def updateAnimation(self):
		self.frames+=1

		if self.dead == False and self.frames % 3 == 0:
			if self.animation < 7: self.animation+=1
			else: self.animation = 0
		elif self.frames % 3 == 0:
			if self.animation < 7: self.animation+=1
			else: 
				self.animation = 0
				self.destroyable = True
	
	def update(self):
		self.updateAnimation()

#Model Class
class Model():
    #Constructor
	def __init__(self):
		#Method Default variables
		self.sprites = []
		self.pacman = Pacman(60, 90)
		self.sprites.append(self.pacman)
		self.load()
		
	#Json Methods
	def load(self):
		with open("map.json") as file:
			data = json.load(file)
			self.sprites.clear()
			self.sprites.append(self.pacman)
			#get the list labeled as "lettuces" from the map.json file
			walls = data["WallList"]
			ghosts = data["GhostList"]
			fruits = data["FruitList"]
			pellets = data["PelletList"]
		
		for wall_data in walls:
			self.sprites.append(Wall(wall_data["x-value"], wall_data["y-value"]))

		for ghost_data in ghosts:
			self.sprites.append(Ghost(ghost_data["x-value"], ghost_data["y-value"]))
   
		for fruit_data in fruits:
			self.sprites.append(Fruit(fruit_data["x-value"], fruit_data["y-value"]))
	
		for pellet_data in pellets:
			self.sprites.append(Pellet(pellet_data["x-value"], pellet_data["y-value"]))
   
	def save(self):
		data = {"WallList": [], "PelletList": [], "FruitList": [], "GhostList": []}

		for sprite in self.sprites:
			if sprite.isWall():
				data["WallList"].append({"x-value": sprite.x, "y-value": sprite.y})
			elif sprite.isPellet():
				data["PelletList"].append({"x-value": sprite.x, "y-value": sprite.y})
			elif sprite.isFruit():
				data["FruitList"].append({"x-value": sprite.x, "y-value": sprite.y})
			elif sprite.isGhost():
				data["GhostList"].append({"x-value": sprite.x, "y-value": sprite.y})


		with open("map.json", "w") as file:
			json.dump(data, file)
   
	#Pacman Methods
	def movePacman(self, direction):
		self.pacman.handleMove(direction)

	def getPacman(self):
		return self.pacman
	
	#Sprite Methods
	def addSprite(self, sprite):
		self.sprites.append(sprite)

	def removeSprite(self, x, y):
		for sprite in reversed(self.sprites):
			if(sprite.getRight() > x and sprite.getLeft() < x and sprite.getTop() < y and sprite.getBottom() > y):
				self.sprites.remove(sprite)
				return
	
	#Update methods
	def updateWarping(self, sprite):
		if sprite.canCollide():
			if sprite.getRight() < 10:
				sprite.setLeft(500)
			elif sprite.getLeft() > 500:
				sprite.setRight(10)

	def updateCollision(self, sprite, sprite2):
		if sprite.canCollide() != True:
			return False
		if sprite == sprite2:
			return False
		if sprite.getRight() < sprite2.getLeft():
			return False
		if sprite.getLeft() > sprite2.getRight():
			return False
		if sprite.getTop() > sprite2.getBottom():
			return False
		if sprite.getBottom() < sprite2.getTop():
			return False
		return True	
	
	def updateDestroyable(self, sprite):
		if sprite.isDestroyable():
			self.sprites.remove(sprite)

	def update(self):
		for sprite in self.sprites:
			sprite.update()
			self.updateWarping(sprite)
			self.updateDestroyable(sprite)

			for sprite2 in self.sprites:
				if self.updateCollision(sprite, sprite2):
					sprite2.collidedBy(sprite)

#View Class
class View():
    #Contructor
	def __init__(self, model):
		screen_size = (510, 510)
		#View defalt variables
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.model = model
		self.scroll = 0

	#Update Methods
	def updateScroll(self, pac):
		if pac.getBottom() > 340 + self.scroll:
			self.scroll = pac.getBottom() - 340
		elif pac.getTop() < 170 + self.scroll:
			self.scroll = pac.getTop() - 170 

	def update(self):
		self.screen.fill([0,0,0])

		pac = self.model.getPacman()

		for sprite in self.model.sprites:
			if(sprite != pac):
				sprite.draw(self, self.scroll)	
		pac.draw(self, self.scroll)
		self.updateScroll(pac)
		
		pygame.display.flip()

#Controller Class
class Controller():
    #Contructor
	def __init__(self, model, view):
		#Controller Default Variables
		self.model = model
		self.view = view
		self.keep_going = True
		self.currentMode = 0

	#Handles Mode Selection
	def setEditMode(self, mode):
		match self.currentMode:
			case 0: #Play Mode
				if(mode == 1): self.currentMode = 2
			case 1: #Edit Mode
				if(mode == 1): self.currentMode = 0
				else: self.currentMode = mode
			case 2: #Wall Mode
				if(mode == 1 or mode == self.currentMode): self.currentMode = 0
				else: self.currentMode = mode
			case 3: #Pellet Mode
				if(mode == 1 or mode == self.currentMode): self.currentMode = 0
				else: self.currentMode = mode
			case 4: #Fruit Mode
				if(mode == 1 or mode == self.currentMode): self.currentMode = 0
				else: self.currentMode = mode
			case 5: #Ghost Mode
				if(mode == 1 or mode == self.currentMode): self.currentMode = 0
				else: self.currentMode = mode
			case 6: #Remove Mode
				if(mode == 1 or mode == self.currentMode): self.currentMode = 0
				else: self.currentMode = mode
		print(self.currentMode)
	
	#Update Method
	def update(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE or event.key == K_q:
					self.keep_going = False
			elif event.type == pygame.MOUSEBUTTONDOWN:
				x, y = pygame.mouse.get_pos()
				match self.currentMode: #Checks what to do with the clicks
					case 2: self.model.addSprite(Wall(x, y + self.view.scroll))
					case 3: self.model.addSprite(Pellet(x, y + self.view.scroll))
					case 4: self.model.addSprite(Fruit(x, y + self.view.scroll))
					case 5: self.model.addSprite(Ghost(x, y + self.view.scroll))
					case 6: self.model.removeSprite(x, y + self.view.scroll)
			elif event.type == KEYUP: #Assignms which mode the controller is in
				if event.key == K_e: self.setEditMode(1) #Edit Mode
				elif event.key == K_a: self.setEditMode(2) #Wall Mode
				elif event.key == K_p: self.setEditMode(3) #Pellet Mode
				elif event.key == K_f: self.setEditMode(4) #Fruit Mode
				elif event.key == K_g: self.setEditMode(5) #Ghost Mode
				elif event.key == K_r: self.setEditMode(6) #Remove Mode
				elif event.key == K_s: self.model.save()
				elif event.key == K_l: self.model.load()
			
		keys = pygame.key.get_pressed() #Handles Movement
		if keys[K_LEFT]: self.model.movePacman(1)
		if keys[K_RIGHT]: self.model.movePacman(3)
		if keys[K_UP]: self.model.movePacman(2)
		if keys[K_DOWN]: self.model.movePacman(0)
		


print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m, v)
while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.04)
print("Goodbye")