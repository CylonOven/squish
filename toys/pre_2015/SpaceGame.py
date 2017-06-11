#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2012 Tonis <Tonis@PLUTO>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import random
import math

def makeGrid(x,y):
	grid= []
	for x in range(x):
		grid.append([None] * y)
	return grid
	
def makeSolidGrid(x,y):
	grid= []
	for x in range(x):
		grid.append([" "] * y)
	return grid

def drawGrid(grid):
	print("%s%s%s" %('/','-' * (len(grid)), '\\'))
	for y in range(len(grid[0])):
		print("%s%s%s" %('|',getRow(grid, y),'|'))		
	print("%s%s%s" %('\\','-' * (len(grid)), '/'))

def copyGrid(grid):#returns a new list identical to grid
	newGrid = []
	for x in range(len(grid)):
		newGrid.append([])
		for y in range(len(grid[0])):
			newGrid[x].append(grid[x][y])
	return newGrid
	
def LayerGrids(bottomGrid,layerList):#Returns a new grid, of bottemGrid with [layers]
	#[layers] = [[(x,y),grid_to_be_layered],ect]
	finalGrid = copyGrid(bottomGrid)
	for layer in layerList:
		drawObject(finalGrid, [layer[0],layer[1]],layer[2])
	return finalGrid
	
def getRow(grid, yRow):#returns string of the row y of grid
	row = ''
	for x in range(len(grid)):
		if grid[x][yRow] == None:
			row += ' '
			continue
		row += grid[x][yRow]
	return row

def getLineList(pointA,pointB):#Returns a list of points forming a line between pointA and B
	if pointA == pointB:
		return []
	linedist = getDistance(pointA,pointB)
	steps =  [(pointB[0]-pointA[0]) / linedist  ,  (pointB[1]-pointA[1]) / linedist]
	lineList = [pointA]
	x = pointA[0]
	y = pointA[1]
	while True:
		x += steps[0]
		y += steps[1]
		if pointA[0] <= pointB[0] and pointA[1] <= pointB[1]:
			if round(x) >= pointB[0] and round(y) >= pointB[1]:
				lineList.append(pointB)
				break
		elif pointA[0] >= pointB[0] and pointA[1] <= pointB[1]:
			if round(x) <= pointB[0] and round(y) >= pointB[1]:
				lineList.append(pointB)
				break
		elif pointA[0] <= pointB[0] and pointA[1] >= pointB[1]:
			if round(x) >= pointB[0] and round(y) <= pointB[1]:
				lineList.append(pointB)
				break
		elif pointA[0] >= pointB[0] and pointA[1] >= pointB[1]:
			if round(x) <= pointB[0] and round(y) <= pointB[1]:
				lineList.append(pointB)
				break
		
		if [round(x),round(y)] not in lineList:
			lineList.append((round(x),round(y)))
			
	return lineList
	
	
	

def getNeighbours(pointA,galaxy):#returns a list of neighbours for pointA, uses galaxy[CONNECTIONS]
	neighbours = []
	for A,B in galaxy["CONNECTIONS"]:
		if pointA == A:
			neighbours.append([getDistance(pointA, B),B])
		if pointA == B:
			neighbours.append([getDistance(pointA, A),A])
	neighbours.sort()
	for i in range(len(neighbours)):
		neighbours[i] = neighbours[i][1]  
	return neighbours
	
	
	
def makeconnections(galaxy,):#Returns a list of line endpoints, that form a map.
	connections = []
	for pointA in galaxy["PLANETLIST"]:
		for pointB in getClosestPoints(pointA,galaxy["PLANETLIST"],galaxy["NUM_CLOSEST"]):
			if (pointA,pointB) not in connections and (pointB,pointA) not in connections:
				connections.append((pointA,pointB)) #only adds to the atlus if the line is not present
	return connections





def drawString(grid, xy, string, CLR):#will draw string on grid starting at xy. CLR = center of xy right of xy, left of xy.
	string = str(string)
	
	if CLR.upper()[0] == "L":
		shift = -len(string) +1
	elif CLR.upper()[0] == "C":
		shift = - round(len(string)/2)
	else:
		shift = 0
	
	#If the string is too long and will not fit,
	if shift+len(string)+xy[0] >= len(grid):
		shift -=   shift+len(string)+xy[0] - len(grid)
	if shift+xy[0] < 0:
		shift += abs(shift +xy[0])
	if xy[1] < 0 or xy[1] >= len(grid[1]):
		return None
	#edit the board
	for letter in string:
		if letter == "&":
			shift += 1
			continue
		grid[xy[0]+shift][xy[1]] = letter
		shift += 1 #change shfit so we edit a new tile as we go.

def drawObject(board, xy, string ):#draws multiline string on grid, if object goes over, does not draw. XY is top left corner of object
	x = xy[0]
	y = xy[1]
	xShift = 0
	yShift = 0
	
	if type(string) == str:
		for letter in string:
			if letter == "\n":
				yShift += 1
				xShift = 0
				continue
			elif x+xShift >= len(board) or y+yShift >= len(board[0]): #if ojbect falls off right or bottom side.
				xShift += 1
			elif x+xShift < 0 or y+yShift < 0: #if object starts off the top or left side
				xShift += 1
			else:
				board[x+xShift][y+yShift]=letter
				xShift += 1
	elif type(string) == list:
		for X in range(len(string)):
			yShift = 0
			for Y in range(len(string[0])):
				if x+xShift >= len(board) or y+yShift >= len(board[0]): #if ojbect falls off right or bottom side.
					yShift += 1
				elif x+xShift < 0 or y+yShift < 0: #if object starts off the top or left side
					yShift += 1
				elif string[X][Y] == None: #if there is nothing in the tile to be added,
					yShift += 1
				else:
					board[x+xShift][y+yShift]=string[X][Y]
					yShift += 1 
			xShift +=1
			
def makeStringIntoGrid(string): #Given a multiline (or single line) sring will return a grid version of it.
	grid = [[None]]
	x = 0
	y = 0
	for letter in string:
		if letter == "\n":
			y += 1
			x = 0
		if x >= len(grid):
			grid.append([None]*(y+1))
		if y >= len(grid[x]):
			for X in range(len(grid)):
				grid[X].append(None)

			continue
		grid[x][y]= letter
		x += 1
	return grid
		


	
def isWholeGalaxy(galaxy):#Returns true if there no unconnected planets.
	visitedPlanets = [galaxy["PLANETLIST"][0]]
	for planet in visitedPlanets:
		for neighbours in galaxy[planet]["NEIGHBOURS"]:
			if neighbours in visitedPlanets:
				continue
			visitedPlanets.append(neighbours)
	for planet in galaxy["PLANETLIST"]:
		if planet not in visitedPlanets:
			return False
			
	return True
				
	
def getRoute(galaxy,pointA,pointB):#Returns a list of points that make up the shortest route between pointA&B
	#CURRENTLY DOES NOT FIND SHORTEST ROUTE, JUST THE FIRST ONE THAT POPS UP! Make it so it will run untill it's looking for pointB's neibours, then break.
	#then go though each pointB in routeTree, calculating dist, return shortest route.
	reachedPoint=False
	skipList = [pointA]
	routeTree = [[pointA, None]]
	if pointA == pointB:
		return [pointA]
	for parent in routeTree:
		if parent[0] == pointB:
			break
		for point in galaxy[parent[0]]["NEIGHBOURS"]:
			if point == pointB:
				routeTree.append([point,parent[0]])
			if point in skipList and point != pointB:
				continue
			skipList.append(point)
			routeTree.append([point,parent[0]])
			
			
		#~ if routeTree[-1][0] == pointB:
			#~ break
	routeList = []
	routeTree.reverse()
	
	#Forms a list of possible routes from pointA > pointB, using routeTree
	for point,parent in routeTree:
		if point != pointB:
			continue
		route = [point,parent]
		while route[-1] != pointA:
			for nextpoint,parrent in routeTree:
				if nextpoint == route[-1]:
					route.append(parrent)
					break
		route.reverse()
		routeList.append(route)
		
	#finds the shortest route
	bestDistance = None 
	bestRoute = None
	for route in routeList:
		distance = 0
		for stop in range(len(route)):
			if stop == len(route) -1:
				continue
			distance += getDistance(route[stop],route[stop+1])
		
		if bestDistance == None or distance < bestDistance:
			bestDistance = distance
			bestRoute = route
	return bestRoute 
	
def getRouteOverlay(pointA,pointB):
	route =  getRoute(galaxy,pointA,pointB)
	lineOverLay = makeGrid(len(galaxy["BOARD"]),len(galaxy["BOARD"][0]))
	distance = 0
	for stop in range(len(route)):
		if stop == len(route)-1:
			break
		distance += getDistance(route[stop],route[stop+1])
		if (route[stop],route[stop+1]) in galaxy["CONNECTIONS"]:
			line=getLineList(route[stop],route[stop+1])
		elif (route[stop+1],route[stop]) in galaxy["CONNECTIONS"]:
			line=getLineList(route[stop+1],route[stop])
		for point in line:
			drawString(lineOverLay, point, 'O', 'R')
	return [[lineOverLay],distance]
	
		
		
def getClosestPoints(pointA,pointList,places):#returns a list of the N closest points of pointA
	closest = []
	for i in range(places):
		closest.append([None,9999])#Creates the highscores for closest planets
	for pointB in pointList:
		if pointB == pointA: # Point A is not Point A´s neighbour
			continue
		distance = getDistance(pointA,pointB)
		for i in range(len(closest)): 
			if distance < closest[i][1]:#Checking if the current pointB is closer than any of the current closest
				closest.insert(i,[pointB, distance])
				del(closest[-1])#Pushing down the list of scores, knocking the last place off the list.
				break#Once we find where it is in the highscore list, we go onto the next pointB

	for i in range(len(closest)):
			 closest[i]=closest[i][0]#Alter the list, removing the distances./
			 if closest[i] == None:
				 del(closest[i])
	return closest
	
	
	
	
	
	
	
	#Returns a list of strings that corispond with lineList to form a ascii line of /\-and |s
	#stringList = ['A']
	#for i in range(len(lineList)):
		#if i == len(lineList) - 1:
			#stringList.append('B')
			#return stringList
		#if lineList[i+1][0]==lineList[i][0]+1 and lineList[i+1][1]==lineList[i][1]+1 or lineList[i+1][0]==lineList[i][0]-1 and lineList[i+1][1]==lineList[i][1]-1:
			#stringList.append('\\')
		#elif lineList[i+1][0]==lineList[i][0]-1 and lineList[i+1][1]==lineList[i][1]+1 or lineList[i+1][0]==lineList[i][0]+1 and lineList[i+1][1]==lineList[i][1]-1:
			#stringList.append('/')
		#elif lineList[i+1][0]==lineList[i][0] and lineList[i+1][1]==lineList[i][1]+1 or lineList[i+1][0]==lineList[i][0] and lineList[i+1][1]==lineList[i][1]-1:
			#stringList.append('|')
		#elif lineList[i+1][0]==lineList[i][0]+1 and lineList[i+1][1]==lineList[i][1] or lineList[i+1][0]==lineList[i][0]-1 and lineList[i+1][1]==lineList[i][1]:
			#stringList.append('-')

def generateGalaxy(X,Y,density,neighbours):#generates Galaxy. (board, planet density)
	
	while True:
		
		galaxy = {}
		galaxy["BOARD"] = makeGrid(X,Y)
		galaxy["PLANETLIST"] = []
		while len(galaxy["PLANETLIST"]) <= len(galaxy["BOARD"])*len(galaxy["BOARD"][0])/density: 
		#the last number is the number of tiles for each planet. lower the number higher the planet density
		#will loop untill the correct ratio of space/planets is acheived
			x = random.choice(range(len(galaxy["BOARD"])))
			y= random.choice(range(len(galaxy["BOARD"][0])))
			#print(planet,round(len(grid)*len(grid[0])/100), len(planetList))
			#Moves the planet away from the border if it's too close
			if x - 2 <= 0:
				x = 2
			if x + 2 >= len(galaxy["BOARD"]):
				x = len(galaxy["BOARD"]) - 2
			if y - 2 <= 0:
				y = 2
			if y + 2 >= len(galaxy["BOARD"][0]):
				y = len(galaxy["BOARD"][0]) - 2
			
			validPlanet = True
			
			for otherPlanets in galaxy["PLANETLIST"]: # Makes sure the chosen star far enough apart
				dist = getDistance([x,y],otherPlanets)
				if random.randrange(13) >= round(dist)-3: #The closer something is to another point, the highter chance of rejection
					validPlanet = False
			if validPlanet == True:
				galaxy["PLANETLIST"].append((x,y))
		
		galaxy["NUM_CLOSEST"] = neighbours
		NAMES = ['Nagano', 'Johnny', 'Swope', 'Coelum', 'Kornev', 'Yoneta', 'Divis', 'Legia', 'Lambey', 'Takase', 'Emicka', 'Guido', 'Donald', 'Daishi', 'Goethe', 'Takeda', 'Adonis', 'Ruth', 'Iruma', 'Mie', 'Hoder', 'Cromer', 'Tycho', 'Zachia', 'Pleso', 'Atala', 'Liroma', 'Brod', 'Ceske', 'Osip', 'Mora', 'Ubels', 'Tone', 'Troja', 'Saale', 'Jeans', 'Hiroo', 'Karoji', 'Hoyo', 'Saji', 'Aeria', 'Melosh', 'NEAT', 'Lugano', 'Turgot', 'Hodler', 'Yanaka', 'Payton', 'Hapke', 'Dufu', 'Paton', 'Glauke', 'Thekla', 'Kuga', 'Leung', 'Samra', 'Pafuri', 'Gangda', 'Sayany', 'Pales', 'Giclas', 'Leifer', 'Bali', 'Holic', 'Berger', 'Huia', 'Rop', 'Madrid', 'Serio', 'Makio', 'Perun', 'Kepler', 'Ewers', 'Ute', 'Aenna', 'Dibaj', 'Inge', 'ASP', 'ASCII', 'Kaler', 'Khege', 'Wanach', 'Schwob', 'Laban', 'Rozgaj', 'Jessop', 'Kamil', 'Bombig', 'Wade', 'Dakota', 'Renate', 'Andrea', 'Swasey', 'Soldan', 'Barlow', 'Tunica', 'Ekholm', 'Reiz', 'Kusaka', 'Elois']
		galaxy["CONNECTIONS"] = makeconnections(galaxy)
		
		for x,y in galaxy["PLANETLIST"]:
			galaxy[(x,y)] = {"NAME":random.choice(NAMES), "NEIGHBOURS" : getNeighbours((x,y),galaxy,), "RATING":0, "XY":(x,y)}
			NAMES.remove(galaxy[(x,y)]["NAME"])
			if len(NAMES) == 0:
				NAMES = ['Trebic', 'Yunnan', 'Doren', 'Kobe', 'Harris', 'Franke', 'Pest', 'Hera', 'Silvo', 'Perdix', 'Valina', 'Palmen', 'Zajic', 'Kajov', 'Ahau', 'Akayu', 'Asimov', 'Bohmia', 'Ticha', 'Saito', 'Mieke', 'Tairov', 'Emma', 'Radaly', 'Sykes', 'Pirko', 'Volta', 'Valdaj', 'Mopaku', 'Kitezh', 'Troska', 'Petit', 'Part', 'House', 'Echo', 'Pelcak', 'Warner', 'Benbow', 'Gifu', 'Shair', 'Eluard', 'San', 'Berko', 'Mann', 'Lysa', 'Mayumi', 'Enescu', 'Ypres', 'Otto', 'Polino', 'Arlon', 'Maik', 'Fermi', 'Jagras', 'Green', 'Smiley', 'Shaim', 'Pagnol', 'Yumi', 'Kursk', 'Louise', 'Luguhu', 'Vydra', 'Tobata', 'Larbro', 'Suess', 'Rowan', 'Neuvo', 'Letzel', 'Inca', 'Hegel', 'Warhol', 'Testa', 'Isora', 'Haruna', 'Scotti', 'Franz', 'Nanon', 'Hedwig', 'Falce', 'Chaka', 'Paola', 'Ivory', 'Haolei', 'Aldaz', 'Urania', 'Stunzi', 'The', 'Yalta', 'Van', 'Hopf', 'Takei', 'Reich', 'Gautam', 'Ikuo', 'Pfaff', 'Celik', 'Gase', 'Yulong', 'Forum', 'Cosima', 'Hippo', 'Hube', 'Lie', 'Udinsk', 'Carus', 'Pitman', 'Stooke', 'Jeter', 'Jara', 'Dehant', 'Yeti', 'Loa', 'Ripero', 'Fox', 'Delila', 'Kurtz', 'Capys', 'Atluri', 'Otila', 'Sivers', 'Mila', 'Aisha', 'Rauch', 'Metis', 'Heard', 'Olea', 'Mork', 'Cahill', 'Tyson', 'Raahe', 'Oertli', 'Kiuchi', 'Iwabu', 'Peitho', 'Penzel', 'Dahir', 'Hyogo', 'Bressi', 'Diebel', 'Ceva', 'Labnow', 'Somov', 'IRAS', 'Tarter', 'Sushko', 'Ashley', 'Aude', 'Young', 'Braude', 'Morden', 'Ivanka', 'Hajos', 'Bligh', 'Hoyt', 'Grygar', 'Dusek', 'Bernes', 'Premt', 'Defoy', 'Iruma', 'Eri', 'Ella', 'Yocum', 'Peter', 'Zagar', 'Orlik', 'Onoda', 'Mustel', 'Ganz', 'James', 'Frigga', 'Tatsuo', 'Mould', 'Bottke', 'Keiko', 'Leewei', 'Hajdu', 'Tanner', 'Plaut', 'Kirov', 'Alona', 'Yanaka', 'Hrabal', 'Pohl', 'Banzan', 'Yvette', 'Franck', 'Pire', 'Totoro', 'Grote', 'Zelter', 'Ciney', 'Ubuntu', 'Sofue', 'Onsen', 'Lewis', 'Burney', 'Cruces', 'Bruges', 'Haken', 'Brno', 'Hybris', 'Mach', 'Gomyou', 'Bihoro', 'Stobbe', 'Fassel', 'Batten', 'Heindl', 'Stino', 'Sicoli', 'Harel', 'Mali', 'Downs', 'Tyle', 'Galois', 'Hnath', 'Martak', 'Feijth', 'Heyler', 'Tabei', 'Festin', 'Edmond', 'Hrozny', 'Slavov', 'Rukl', "L'Obel", 'Abetti', 'Danjon', 'Utkin', 'Donna', 'Alkon', 'Rhone', 'Abbe', 'Stalle', 'Sambre', 'Boyce', 'Beck', 'Ibsen', 'Schade', 'Fermat', 'Sierks', 'Sobey', 'Minox', 'Piso', 'Zelia', 'Lopez', 'Frisia', 'Bilbo']
		
		### REJECTS GALAXY IF THERE ARE DISCONNECTED POINTS!
		if not isWholeGalaxy(galaxy):
			continue
		
		###Values planets by traffic
		
		globalRating = 0
		ratings = []
		for pointA in galaxy["PLANETLIST"]:
			for pointB in galaxy["PLANETLIST"]:
				if pointA == pointB:
					continue
				route = getRoute(galaxy, pointA, pointB)
				
				for planet in route:
					if planet == pointA:
						continue
					galaxy[planet]["RATING"] += 1
					globalRating += 1
		for planet in galaxy["PLANETLIST"]:
			ratings.append(galaxy[planet]["RATING"])
		ratings.sort()
		galaxy["RATINGS"] = ratings
		galaxy["GLOBALRATING"] = globalRating
		galaxy["AVERAGERATING"]= globalRating/len(galaxy["PLANETLIST"])
		
		###Generates Planet trade resourses:
		#good list
		tradeGoodList = "Luxuary Food,Food Bars,Raw metals,High-Tech goods,Trade good 1,Trade good 2,Trade good 3,Trade good 4,Trade good 5,Trade good 6,Trade good 7".split(',')
		#creates empty data to be filled in
		for planet in galaxy["PLANETLIST"]:
			galaxy[planet]["TRADE"] = []
			for tradeGood in tradeGoodList:
				galaxy[planet]["TRADE"].append({'NAME':tradeGood,"BUY":0,"SELL":0, "QUANTATY":0})
		
		###Draws galaxy onto galaxy["BOARD"]fasjf
		###Draws names to galaxy["NAME OVERLAY"]
		###Draws cords to galaxy["XY OVERLAY"]
		
		#lines
		for pointA,pointB in galaxy["CONNECTIONS"]:
			for x,y in getLineList(pointA,pointB):
				if (x,y) == pointA or (x,y) == pointB:
					continue
				galaxy["BOARD"][x][y] = '.'
		#planets
		galaxy["NAME OVERLAY"] = makeGrid(X,Y)
		galaxy["XY OVERLAY"] = makeGrid(X,Y)
		for planet in galaxy["PLANETLIST"]:
			galaxy["BOARD"][planet[0]][planet[1]] = str(int( galaxy[planet]["RATING"] / (ratings[-1]/10+1) ))
			#Draws on Oversays
			drawString(galaxy["NAME OVERLAY"], [planet[0],planet[1]-1], galaxy[planet]["NAME"], "C")				
			drawString(galaxy["XY OVERLAY"], [planet[0],planet[1]-1], str(galaxy[planet]["XY"]), "C")

		break
	return galaxy
	
		

def getDistance(pointA, pointB):
	#returns a [xAxisDif,yAxisDif,lineDist]
	difs = [abs(pointA[0] - pointB[0]) , abs(pointA[1] - pointB[1])] 
	linedist = math.sqrt(difs[0]**2 + difs[1]**2)
	return linedist

		

def generateChoiceMenu(options):
	mainMenu = {"GRID" : makeGrid(77,3) , "OPTIONS":[]}
	for choice in options:
		mainMenu["OPTIONS"].append(choice)
	
	###Calculate the spaceing for text
	textSize = 0
	for text in mainMenu["OPTIONS"]:
		textSize+=len(text["NAME"])
	spaceing = round((len(mainMenu["GRID"])-textSize)/(len(mainMenu["OPTIONS"])+1))
	
	
	x = spaceing
	for text in  mainMenu["OPTIONS"]:
		text["OBJECTS"]=[]
		drawString(mainMenu["GRID"],[x,1], text["NAME"] ,"R")
		text["OBJECTS"].append([x-3,1,">>>%s<<<"%(text["NAME"])])
		x += spaceing + len(text["NAME"])
	return mainMenu
	
def generateBuyMenu(art,text,items,leftkey, rightkey): #A menu with art and text, with selectable items. Each item has it's own overlay, 
	
	page = makeSolidGrid(77,40)
	drawObject(page,(1,round(len(page[0])/2)+1),generateTextBox((round(len(page)/2)-1,round(len(page[0])/2)-2),text))
	drawObject(page,(1,1),generateArtBox((round(len(page)/2)-1,round(len(page[0])/2)-1),art))
	drawObject(page,(round(len(page)/2)+1,1),generateArtBox((round(len(page)/2)-1,round(len(page[0]))-2),""))

	
	Menu = {"GRID" : page , "OPTIONS":items}
	#~ for item in items:
		#~ Menu["ITEMS"].append(item)
	
	###Calculate the spaceing for text
	spaceing = round( (len(page[0])-2)/ len(items) )
	y = spaceing +1
	x = round( len(Menu["GRID"])/4*3)
	for item in  Menu["OPTIONS"]:
		item["OBJECTS"] = []
		if "TEXT" in item:
			item["OBJECTS"].append(drawObject(overlay,(1,round(len(page[0])/2)+1),generateTextBox((round(len(page)/2)-1,round(len(page[0])/2)-2),text)))
		if "ART" in item:
				item["OBJECTS"].append( drawObject(overlay,(1,1),generateArtBox((round(len(page)/2)-1,round(len(page[0])/2)-1),item['ART'])))
		#WHAT?
		drawObject(Menu["GRID"],(x-len(str(item[leftkey])),y), "%s %s"%(item[leftkey], item[rightkey]))
		item["OBJECTS"].append([x-len(str(item[leftkey]))-3,y, ">>>%s %s<<<"%(item[leftkey], item[rightkey]) ])
		#item["END"] = (x+len(str(item[rightkey]))+1,y)
		y += spaceing
		#item["GRID"] = Menu["GRID"]
	return Menu	
	
	
	
def generateInfoBox(size,contents,leftKEY, rightKEY):#Retuns a rect(size) with contents[key] evenly spaced
	#Make the Box and the border
	infoBox = makeSolidGrid(size[0],size[1])
	for x in range(len(infoBox)):
		infoBox[x][0] = '-'
		infoBox[x][len(infoBox[0])-1] = '-'
	for y in range(len(infoBox[0])):
		infoBox[0][y] = '|'
		infoBox[len(infoBox)-1][y] = '|'
	infoBox[0][0] = '/'
	infoBox[len(infoBox)-1][0] = '\\'
	infoBox[0][len(infoBox[0])-1] = '\\'
	infoBox[len(infoBox)-1][len(infoBox[0])-1] = '/'
	
	spaceing = round( (len(infoBox[0])/ len(contents) )) 
	y = spaceing
	x = round( len(infoBox)/2)
	print(spaceing,(len(infoBox[0]) -len(contents)) / len(contents))
	for item in contents:
		drawString(infoBox, (x-1,y), item[leftKEY] ,"L")
		drawString(infoBox, (x+1,y), item[rightKEY], "R")
		y += spaceing
		
	return infoBox
	
def generateTextBox(size, string):#Returns a grid with the object in the center,
	#Make the Box
	Box = makeSolidGrid(size[0],size[1])
	#For eaze of code, make another grid that will have the text printed on it,
	#then draw that grid onto the first.
	textBox = makeSolidGrid(size[0]-2,size[1]-2)
	string = string.split()
	x,y = [1,0]
	for word in string:
		if word == "_LB_":
			x = 1
			y += 1
			continue 
		if len(word) + x >= len(textBox):
			x = 1
			y += 1
		if y >= len(textBox[0]):
			break
		drawString(textBox,(x,y),word,"r")
		x += len(word) +1
	print((len(textBox[0])-y) /2)
	drawObject(Box,(1,round((len(textBox[0])-y) /2)+1),textBox)
	print(round((len(textBox[0])-y) /2))
	
	#Draw the border on the box.
	for x in range(len(Box)):
		Box[x][0] = '-'
		Box[x][len(Box[0])-1] = '-'
	for y in range(len(Box[0])):
		Box[0][y] = '|'
		Box[len(Box)-1][y] = '|'
	Box[0][0] = '/'
	Box[len(Box)-1][0] = '\\'
	Box[0][len(Box[0])-1] = '\\'
	Box[len(Box)-1][len(Box[0])-1] = '/'
	
	return Box
	
def generateArtBox(size,art):
	#Make the Box and the border
	Box = makeSolidGrid(size[0],size[1])
	for x in range(len(Box)):
		Box[x][0] = '-'
		Box[x][len(Box[0])-1] = '-'
	for y in range(len(Box[0])):
		Box[0][y] = '|'
		Box[len(Box)-1][y] = '|'
	Box[0][0] = '/'
	Box[len(Box)-1][0] = '\\'
	Box[0][len(Box[0])-1] = '\\'
	Box[len(Box)-1][len(Box[0])-1] = '/'
	
	#Turns the art into a grid.
	if type(art) == str:
		artGrid = makeStringIntoGrid(art)
	else:
		artGrid = art

	#draw the art so it's centered in the Box
	x = round((len(Box)-2 - len(artGrid)) /2)
	y = round((len(Box[0])-2 - len(artGrid[0])) /2)

	drawObject(Box,(x,y),artGrid)
	
	return Box
	
#~ def inputReaction(selection):
	#~ if "ROUTE" in selection:
drawGrid(makeStringIntoGrid("""xxxx
xxxxx
OOO"""))		
page = makeSolidGrid(77,40)
drawObject(page,(1,round(len(page[0])/2)+1),generateTextBox((round(len(page)/2)-1,round(len(page[0])/2)-2),"They lied to us, they said that this world would be new start, fresh ground. But nothing grows in the soil here but the native plant, prickle vines. Named after their sharp thorns that stick to clothing. They wouldn't be that bad excpet they grow like fire, feilds of the stuff have to be cut back each day to prevent them getting into our crops. Their seeds are just everywhere, if you try to grow anything in soil that hasen't been treated, the vines just grow insted.  The only reason this collany exists is the mine. All we do is export the iron ore to other planets. Life is cold and boring. I wish I could afford to leave this planet. But maybe I should be thankful, I hear that some of the other new colonised planets have it even worse."))
drawObject(page,(1,1),generateArtBox((round(len(page)/2)-1,round(len(page[0])/2)-1),"""  O  
/ / \\
OOOOO"""))
drawObject(page,(round(len(page)/2)+1,1),generateArtBox((round(len(page)/2)-1,round(len(page[0]))-2),"XXX"))
drawGrid(page)



galaxy = generateGalaxy(77,40,70,3)

player = {"CASH":0, "PLANET": galaxy[random.choice(galaxy["PLANETLIST"])],"SHIP": None,"CARGO": []}
planet = player["PLANET"]
print(planet)
drawGrid(generateInfoBox([40,30],player["PLANET"]["TRADE"],"NAME","BUY"))

#~ #["Galaxy"],["View Planet"],["Ship Maintinace"],]

#galaxy Menu
galaxyMenu = generateChoiceMenu([
{"NAME":"Planet Names", "SCREEN": LayerGrids(galaxy["BOARD"],[[0,0, galaxy["NAME OVERLAY"]]]), "ROUTE": None},
{"NAME":"Cordinates", "SCREEN": LayerGrids(galaxy["BOARD"],[[0,0, galaxy["XY OVERLAY"]]]), "ROUTE": None}])


#Trade Screen
tradeMenu = generateBuyMenu("ART GOES HERE!","Welcome to the Trading house. If you want to buy a good, just tell me how much.",planet["TRADE"],"NAME","BUY")
#planetSide menu
planetView = makeGrid(77,10)

drawString(planetView,(45,5), "PLANET VIEW SCEEN, IN PROGRESS", "C")
PlanetMenu = generateChoiceMenu([{"NAME":"Trade", "SCREEN": tradeMenu["GRID"], "SUBMENU" : tradeMenu},
{"NAME":"Mission", "SCREEN": planetView} ])




#shipyard menu
ShipyardView = makeGrid(77,10)
drawString(ShipyardView,(45,5), "SHIPYARD SCEEN, IN PROGRESS", "C")
ShipyardMenu = generateChoiceMenu([{"NAME":"Repair", "SCREEN": ShipyardView},{"NAME":"The Garage", "SCREEN": ShipyardView}
,{"NAME":"Ship Dealer", "SCREEN": ShipyardView},{"NAME":"Weapon Dealer", "SCREEN": ShipyardView}])

#Options Menu
optionsView = makeGrid(77,10)
drawString(optionsView,(45,5), "OPTIONS SCEEN, IN PROGRESS", "C")
optionsMenu = generateChoiceMenu([{"NAME":"Save-Quit", "SCREEN": optionsView}])


mainMenu = generateChoiceMenu([{"NAME":"The Bridge","SCREEN":galaxy["BOARD"],"SUBMENU": galaxyMenu},
 {"NAME":"Planet Side","SCREEN":planetView,"SUBMENU": PlanetMenu},
 {"NAME":"Ship Yard","SCREEN":ShipyardView,"SUBMENU": ShipyardMenu},
 {"NAME":"Game Options","SCREEN":optionsView,"SUBMENU": optionsMenu}])
#~ 


menuList = [mainMenu]
menuScreens = [None]
while True:
	
	journey = []
	currentMenu = menuList[-1]
	
	for selected in currentMenu["OPTIONS"]:#Cycles the options in current menu
	
		if "SCREEN" in selected:
			drawGrid(selected["SCREEN"])
		currentMenuScreen = LayerGrids(currentMenu["GRID"],selected["OBJECTS"])
		menuScreens[-1]=(currentMenuScreen)
		
		for i in range(1,len(menuScreens)+1):
			drawGrid(menuScreens[-i])
		
		selection = input()
		for m in range(30):
			print()
		if bool(selection):
			if "SUBMENU" in selected:
				menuList.append(selected["SUBMENU"])
				menuScreens.append(None)
				break
			elif "ROUTE" in selected:
				for x in galaxy["PLANETLIST"]:
					if selection == galaxy[x]["NAME"] or selection == galaxy[x]["XY"]:
						selection = galaxy[x]["XY"]
						break
				if selection in galaxy["PLANETLIST"]:					
					print(player["PLANET"], selection)
					routeOverlay, distance = getRouteOverlay(player["PLANET"]["XY"],selection)
					drawGrid(LayerGrids(selected["SCREEN"],[[0,0,routeOverlay]+selected["OBJECTS"]]))
					input()
					for i in range(1,len(menuList)+1):
						drawGrid(menuList[-i]["GRID"])
					print('ROUTE MAPPED: TOTAL DISTANCE:',round(distance),"BEGEN JOURNEY?")
					if input().upper().startswith("Y"):
						journey = [player["PLANET"]["XY"],selection,distance]
				
				pass #Here we will figure out how to travel #After accepting the route, would break out of this loop into the combat/travle game.

	
	if bool(journey):
		break
	
	if not bool(selection):
		if len(menuList) != 1:
			del(menuList[-1])
			del(menuScreens[-1])
	
print("JOURNEY COMMENCE!")
		
#while Trgue:
	#for x in range(len(grid)):
		#for y in range(len(grid[0])):
			#drawLine(grid,[30,30],[x,y], '*')
			#drawGrid(grid)
			#drawLine(grid,[30,30],[x,y], ' ')
	
