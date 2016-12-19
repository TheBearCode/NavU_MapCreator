from graphics import *
import sys
from xml.etree.ElementTree import *
import struct
import imghdr

#Get dimensions of a PNG
def get_image_size(fname):
	with open(fname, 'rb') as fhandle:
		head = fhandle.read(24)
		if len(head) != 24:
			return
		check = struct.unpack('>i', head[4:8])[0]
		if check != 0x0d0a1a0a:
			return
		width, height = struct.unpack('>ii', head[16:24])
		return [width, height]

#Parse current nodes from XML
def parseXML():
	file = open("node_data.xml", "r")
	tree = parse(file)
	elem = tree.getroot()
	build = elem.getchildren()[0]
	bn = build.getchildren()
	for i in bn:
		iden = i.findtext("id")
		if iden[0:3] != "HP3" and iden[0:2] != "C3" and iden[0:2] != "S3":
			continue
		newNode = Node()
		newNode.id = iden
		newNode.pos = Vector(float(i.findtext("positionx")), float(i.findtext("positiony")))
		for j in i.findall("connection"):
			newNode.cons.append(j.text)
		nodes.append(newNode)
		
#Simple 2D vector class
class Vector:
	x = 0
	y = 0
	
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y
		
	def __str__(self):
		return ("My x is: " + str(round(self.x,6)) + ", and my y is: " + str(round(self.y,6)))
		
	def __add__(self, other):
		return Vector(self.x + other.x, self.y + other.y)
		
	def __sub__(self, other):
		return Vector(self.x - other.x, self.y - other.y)
		
	def __mul__(self, other):
		return Vector(self.x * other.x, self.y * other.y)
		
	def __truediv__(self, other):
		return Vector(self.x / other.x, self.y / other.y)
		
	def dist(self, other):
		return ((other.x - self.x)**2 + (other.y - self.y)**2)**0.5

#Node data class
class Node:
	pos = Vector()
	id = "What am I"
	cons = []
	rad = 5
	fillC = 'red'
	lineC = 'green'
	
	def __init__(self, pos=Vector(), id=""):
		self.pos = pos
		self.id = id
		self.cons = []
		
	def __eq__(self, other):
		if self.id == other.id:
			return True
		return False
		
	def __ne__(self, other):
		return not (self == other)
		
	def draw(self):
		setFill(self.fillC)
		setColor(self.fillC)
		ellipse(self.pos.x * imgDim.x, self.pos.y * imgDim.y, self.rad, self.rad)
		
		if (self.pos*imgDim).dist(mouse) <= self.rad:
			if self not in tNodes:
				tNodes.append(self)
			for i in nodes:
				if i.id in self.cons:
					setColor(self.lineC)
					setWidth(2)
					line(self.pos.x * imgDim.x + self.rad/2, self.pos.y * imgDim.y + self.rad/2, \
						 i.pos.x * imgDim.x + self.rad/2, i.pos.y * imgDim.y + self.rad/2)
		else:
			if self in tNodes:
				tNodes.remove(self)
		
#Attempt to load necessary data, exits program if invalid arguments are passed by the user
try:
	img = loadImage(str(sys.argv[1]))
	imgDim = Vector(get_image_size(str(sys.argv[1]))[0], get_image_size(str(sys.argv[1]))[1])
	#imgDim = Vector(int(sys.argv[2]), int(sys.argv[3]))
except:
	close()
	exit("Well fuck")
	
wDim = Vector(imgDim.x + 200, imgDim.y)
resize(wDim.x, wDim.y)
setAutoUpdate(False)

tNodes = []
nodes = []
activeNode = Node()

parseXML()

while not closed():
	clear()
	drawImage(img, 0, 0)
	mouse = Vector(mouseX(), mouseY())
	
	setColor('black')
	text(0, 0, str(mouse/imgDim), "nw")
	
	if leftButtonPressed():
		if mouse.x <= imgDim.x:
			activeNode = Node(mouse)
		else:
			print("incoming")
			
		
	for node in nodes:
		node.draw()
		
	for i in range(len(tNodes)):
		setColor('black')
		text(0, 17*i + 17, tNodes[i].id, "nw")
	
	sleep(0.01)
	




