###### WELCOME TO THIS POINT IN POLYGON TEST ALGORITHM ! ######



# STEP 1: IMPORT MODULES NEEDED #

import numpy as np
import matplotlib.pyplot as plt # import the needed library



# STEP 2: CREATE PYTHON OBJECT CLASSES #


# 1. The first object we are creating is a parent geometry class, that I call Geom
class Geom(object):
    """A parent class for all geometry classes"""
    # Method to get the start point of the object
    def getStartPoint(self): 
        return self.coords[0]
    # Method to get the end point of the object
    def getEndPoint(self):
        return self.coords[-1]
    # Method to get the number of points the object comprises
    def getNumPoints(self):
        return self.coords.shape[0]
    # Method to add a point to the object
    def addPoint(self, point):
        self.coords = np.vstack([self.coords, point])
    # Method to get the length of the object
    def length(self):
        return self.len()
    #Method to create a Minimum Bouding Box and obtain its coordinates
    #Based on: https://stackoverflow.com/questions/20808393/python-defining-a-minimum-bounding-rectangle ; Author: user3115802 ; Date:27/12/2013
    def boundingBox(self):
        if len(polygon.coords) == 0:
            raise ValueError("Can't compute bounding box of empty list")
        self.min_x, self.min_y = np.amin(polygon.coords, axis=0) #Minimum points for x and y
        self.max_x, self.max_y = np.amax(polygon.coords, axis=0) #Maximum points for x and y
        self.minbr = Polygon([(self.min_x, self.min_y), (self.max_x, self.min_y), (self.max_x, self.max_y), (self.min_x, self.max_y)])
##      self.minbr.addPoint(self.minbr.coords[0]) #Repeat first point to close the polygon
        return self.minbr.coords
    #Method to test if an array of points are inside or outside minimum bounding box
    def insideBoundingBox(self, points):
        for i in points:
            if self.min_x  <= i[0] <= self.max_x and  self.min_y <= i[1] <= self.max_y: #Point lying on a boundary are considered inside the minimum bounding box
                return 1
                print "Inside Bounding Box"
            else:
                return 0
                print "Outside Bounding Box"
                

# 2. Point class based on example class provided in Moodle but changed to be a 2D point class
class Point(Geom):
    """A simple point class"""
    # initiating the class
    def __init__(self, x=0, y=0):
        self.__coords = np.array([x,y], dtype=float)
        self.__coords.shape = (1,2)
    # Adding a getter: returns value of x
    @property
    def x(self):
        return self.__coords[0,0]
    # Adding a getter: returns value of y
    @property
    def y(self):
        return self.__coords[0,1]
    # Adding a setter to edit value of x
    @x.setter
    def x(self, x):
        self.__coords[0,0] = x
    # Adding a setter to edit value of y
    @y.setter   
    def y(self, y):
        self.__coords[0,1] = y
    # Adding a getter: returns coordinates [x,y] of the points
    @property
    def coords(self):
        return self.__coords
    #Here I prevent the user from using the Geom method addPoint on Point objects
    def addPoint(self, point):
        return "Can't add a point to a point"



# 3. Line class based on example class provided on Moodle
class Line(Geom):
    """A simple line class"""
    # initiating the class: a line is defined by an array of points
    def __init__(self, points = None):
        if points is None:
            self.__coords = None
        else:
            self.__coords = np.vstack(points)
    # Adding a getter: returns coordinates of the Line object as an array of its points'[x,y] coordinates
    @property
    def coords(self):
        return self.__coords
    # Adding a setter: returns the coordinates
    @coords.setter
    def coords(self, points):
        self.__coords = np.vstack(points)
    # Adding the Geom addPoint method and dealing with special case: when the line is empty
    def addPoint(self, point):
        if self.__coords is None:
            self.__coords = point
            self.__coords.shape = (1,2)
        else:
            self.__coords = np.vstack([self.__coords, point])
        


# 4. Polygon class built from Moodle example and enriched with a few functions
class Polygon(Line, Geom): # Polygons inherit from both Geom and Line classes
    """A fancy polygon class with quite a few built-in functions"""
    # A Polygon is defined as a Line that starst and ends with the same point
    def getEndPoint(self):
        return self.getStartPoint()
    # Create a method to ask the Polygon directly if it contains any given point or coordinates [x,y]
    def pointInPoly(self, x, y):
        if self.insideBoundingBox == 0: #if the tested point is outside the bounding box it is definitely outside the polygon
            return "Your point is outside the polygon"
        else:
            #Using winding number algorithm. Modified, based on:
            #https://gis.stackexchange.com/questions/170264/python-point-in-polygon-boundary-and-vertex-check-ray-casting
            #I first need to extract polygon coords to test and format them as a list
            
            poly = self.coords.tolist()
    
            # Let's first check if the point is a vertex, in other words if it is part of the points defining the polygon
            if ([x,y]) in poly: 
                return "Your point is one of the polygon's vertices"
    
            # If not, I check if the point is on one of the polygon's edges (boundaries). 
            # There are three different cases I need to look at: horizontal, vertical and slopy boundaries
            for i in range(len(poly)):
                p1 = None
                p2 = None
                if i==0:
                    p1 = poly[0]
                    p2 = poly[1]
                else:
                    p1 = poly[i-1]
                    p2 = poly[i]
                if p1[1] == p2[1] and p1[1] == y and x > min(p1[0], p2[0]) and x < max(p1[0], p2[0]):
                    return "Your point lies on a horizontal boundary" #In this case, the point lies on a horizontal boundary (same y value)
                
                elif p1[0] == p2[0] and p1[0] == x and y > min(p1[1], p2[1]) and y < max(p1[1], p2[1]):
                    return "Your point lies on a vertical boundary" #In that case, the point lies on a vertical boundary (same x value)
    
                else:
                    if y!=p1[1]:
                        if p1[1] != p2[1] and p1[0] != p2[0] and ((p2[0]-p1[0])/(p2[1]-p1[1]) == (x-p1[0])/(y-p1[1]))  and x< p2[0] and x>p1[0]:
                            return "Your point lies on a boundary slope" #And here, the point lies on a boundary slope (point lies on the line 
                                            #defined by p1 and p2 AND it's between these two points, so it's on the segment that links p1 and p2)
                            break
            #Now that I have dealt with boundaries and won't get false positives, let's test if the point lies within the polygon
            # For this we use the winding number algorithm 
            n = len(poly)
            inside = False #I start with the premise that the point is outside
        
            p1x,p1y = poly[0] #I iterate through all edges of the polygon (defined as two consecutive points defining the polygon)
            for i in range(n+1):
                p2x,p2y = poly[i % n]
                if y > min(p1y,p2y): #if the tested point lies above the lowest of the two vertices,
                    if y <= max(p1y,p2y): # and if it lies below the highest of the two vertices
                        if x <= max(p1x,p2x): #and if it lies before the furthest of the two vertices
                            if p1y != p2y: #then if the edge is not horizontal
                                xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x #I calculate the winding number of our point with respect to this polygon
                            if p1x == p2x or x <= xints: #if the boundary is vertical or our point's x is lower than the winding number
                                inside = not inside #in that case the point is outside
                p1x,p1y = p2x,p2y #close the loop
    
            if inside: return "Your point is inside the polygon"
            else: return "Your point is outside the polygon"
 
            
    
# STEP 3: CODING THE USER SCRIPT #

# Print welcome message
print """
Hi there!

Welcome to this exciting Point in Polygon test. Just feed me a polygon and try 
any point you want, I'll tell you if your point is inside outside, or on your
polygon's boundary. And because I'm fancy like that, I'll also tell you where on
that boundary: vertex, horizontal boundary, vertical boundary or boundary slope.



To start with, I'm going to need a polygon input. I read CSV files that give me
your polygon's points coordinates. Careful, x coordinates should be in the 1st 
column and y coordinates in the 2nd.


Now it's your turn to play. Please enter here the path to your polygon's CSV
file. This path consists in the path to your folder + a backslash + your file's 
name + .csv 
(For instance: C:\Users\Me\Documents\Python\Coursework\Data\testPoly.csv)
"""

# Load the polygon data. The user has to input the path to the file. I added some
# basic error handling. Based on:
# https://stackoverflow.com/questions/11126012/read-csv-and-separate-by-column
try:
    str = raw_input("Please enter your path here and press enter: ")
    f = open(str, "r+")
except:
    print """
Uh oh.... It looks like this file can't be read. Please make sure you entered the
path to a .csv file. Remember: your path shouldn't contain any apostrophe, and 
you should be using backslashes. Another common errorcould be an aditional space
at the begining of your path. 

""" 
    str = raw_input("Please try again:")
    f = open(str, "r+")

# Read the polygon points from the user CSV file as a list
# based on: https://stackoverflow.com/questions/37585038/i-need-to-get-tuples-of-x-y-coordinates-from-a-file-and-add-it-to-a-list
with open (str, "r+") as imput:
    polyPointsList = [tuple(int(i)for i in line.strip().split(",")) for line in imput]
    X, Y = zip(*polyPointsList)


# Create the polygon from the points 
pg1 = Polygon(polyPointsList)

# Print the polygon's coordinates
print """

Thank you! Let me read you your polygon's coordinates:
"""

print (pg1.coords)

# Introduce the point testing section
print """

Now that your polygon is ready, let's play with it and test any point you'd like.
I accept float values and even negative numbers (Try!):

"""

# Here I start a loop so that the user can repeatedly key in point coordinates 
# for as long as he wants to test new points. Based on:
# https://stackoverflow.com/questions/12557376/python-repeat-program-while-true
def pointTest():
    # The user defines a point. I added some error handling:
    # based on: https://docs.python.org/2.7/tutorial/errors.html
    try:
        testPoint_X = float(raw_input("Please key in your point's X coordinate and press enter: "))
    except:
        print "Uh oh... I can only read numbers!"
        testPoint_X = float(raw_input("Please try again. Make sure it's a number! Key in your number and press enter:"))
        
    try:
        testPoint_Y = float(raw_input("Please key in your point's Y coordinate and press enter: "))
    except:
        print "Uh oh... I can only read numbers!"
        testPoint_Y = float(raw_input("Please try again. Make sure it's a number! Key in your number and press enter:"))
    
        print """
        Now I'll tell you if your point lies within, outside or on your polygon's boundaries
        """
    
# I ask this question just to build up the suspense :)
    try:
        raw_input(""""
Shall we take a look?
Press any key: 

            """)
# And of course some error handling, just in case         
    except:
        print "Hmmm strange! Then maybe not THAT key. Just press enter:"
    
    


# Plot the polygon and the point, labelled and titled properly
        
    plt.fill(X,Y, "c") # Create a plot object with the X and Y coordinates of the polygon fil
    plt.xlabel ("X coordinates") # Add the X label
    plt.ylabel("Y coordinates") # Add the Y label
    plt.title ("Your polygon and your point")
    plt.plot([testPoint_X],[testPoint_Y],"k+") # plot the test point user defined as a red point
    plt.show() # Show the plot in a plot wondow
    
    

# Print the results of the point in polygon test (method built-in the polygon class)
    print """
There you go !
"""
    print (pg1.pointInPoly(testPoint_X, testPoint_Y))
    

#If the user wants to test more points he doesn't have to relaunch the whole script. This loops 
# simply allows them to keep testing as long as they want and exit the loop when they're done.

def testAgain():
    return raw_input("""

Do you want to try again? If so, type yes, otherwise press any other key : 
                         """).lower() == "yes"

while True:
    pointTest()
    if not testAgain(): break

# Message displayed when the loop is broken 
print """

Thank you for testing this Point in Polygon algorithm. 
Goodbye!
"""




###### THE END ######
