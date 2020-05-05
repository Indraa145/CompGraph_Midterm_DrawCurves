import pygame
from sys import exit
import numpy as np
import math

width = 800
height = 600
pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)

screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("CompGraph_Midterm - Indra Imanuel Gunawan - 20195118")

# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pts = []
knots = []
count = 0
# screen.blit(background, (0,0))
screen.fill(WHITE)

# https://kite.com/python/docs/pygame.Surface.blit
clock = pygame.time.Clock()

def clearAndRedraw():
    #print("tes")
    #pygame.draw.rect(screen, WHITE, (0,0,590,height))
    screen.fill(WHITE)
    #Line and rects
    for i in range(count - 1):
        pygame.draw.line(screen, GREEN, pts[i], pts[i+1], 3)
    for i in range(count):
        pygame.draw.rect(screen, BLUE, (pts[i][0] - margin, pts[i][1] - margin, 2 * margin, 2 * margin), 5)

    #Buttons
    lagrangeButton.draw(screen, (0, 0, 0))
    bezierButton.draw(screen, (0, 0, 0))
    hermiteButton.draw(screen, (0, 0, 0))
    cubicSplineButton.draw(screen, (0, 0, 0))

    #Text
    if buttonCheck == 1:
        curveType = "Curve Type: Lagrange"
    elif buttonCheck == 2 or buttonCheck == -1:
        curveType = "Curve Type: Bezier"
    elif buttonCheck == 3:
        curveType = "Curve Type: Piecewise cubic hermite"
    else:
        curveType = "Curve Type: Cubic spline"

    font = pygame.font.Font("freesansbold.ttf", 22)
    curveText = font.render(curveType, True, BLACK)
    screen.blit(curveText, (5,5))

#Bezier
def bezier():
    clearAndRedraw()
    N = len(pts)
    n = N-1
    for t in np.arange(0, 1, 0.01):
        z = np.zeros(2)
        for i in range(N):
            z += np.dot((math.factorial(n)/(math.factorial(i)*math.factorial(n-i)))
                        *((1-t)**(n-i))*(t**i),pts[i])

        pygame.draw.circle(screen, RED, z.astype(int), 3)

#Hermite Cubic
def hermiteCubic():
    clearAndRedraw()
    N = len(pts)
    n = N-1
    z = np.array(pts)
    c = 0.5
    for t in np.arange(0, 1, 0.01):
        h1 = (2*(t**3)) - (3*(t**2)) + 1
        h2 = (-2 * (t**3)) + (3*(t**2))
        h3 = (t**3) - (2*(t**2)) + t
        h4 = (t**3) - (t**2)
        for i in np.arange(0, n, 1):
            if i==0:
                tangent2 = z[i+2] - z[i]
                tangent1 = np.zeros(2)
                tan2 = np.dot(c, tangent2)
            elif (i > 0) and (i < n-1):
                tan1 = z[i+1] - z[i-1]
                tangent2 = z[i+2] - z[i]
                tangent1 = np.dot(c, tan1)
                tan2 = np.dot(c, tangent2)
            else:
                tan1 = z[i+1]-z[i-1]
                tangent1 = np.dot(c,tan1)
                tan2 = np.zeros(2)

            c_h = np.dot(h1, pts[i]) + np.dot(h2, pts[i+1]) + np.dot(h3, tangent1) + np.dot(h4, tan2)
            pygame.draw.circle(screen, RED, c_h.astype(int), 3)

#Cubic Spline
def cubicSpline():
    clearAndRedraw()
    N = len(pts)
    n = N-1

    trid = np.identity(N)*4 + np.diag(np.ones(n), 1) + np.diag(np.ones(n), -1)
    trid[0][0] = 2
    trid[n][n] = 2

    z = np.array(pts)
    r = np.zeros((N,2))
    for i in range(N):
        if i == 0:
            r[i] = z[1]-z[0]
        elif i > 0 and i < n:
            r[i] = z[i+1]-z[i-1]
        else:
            r[i] = z[i] - z[i-1]

    w = np.linalg.inv(trid).dot(3*r)

    for t in np.arange(0, 1, 0.01):
        for i in range(n):
            a = z[i]
            b = w[i]
            c = np.dot(3, (z[i+1] - z[i]))-np.dot(2, w[i])-w[i+1]
            d = np.dot(2, (z[i]-z[i+1]))+w[i]+w[i+1]
            yt = a + b*t + c*t*t + d*t*t*t
            pygame.draw.circle(screen, RED, yt.astype(int), 3)

#Lagrange
def lagrange():
    clearAndRedraw()
    for t in np.arange(0, len(pts)-1, 0.01):
        ptPlt = np.zeros(2, float)
        for i in np.arange(0, len(pts), 1):
            num, den = 1, 1
            for j in np.arange(0, len(pts), 1):
                if j != i:
                    num = num * (t - j)
                    den = den * (i - j)
            ptPlt = ptPlt + np.dot(pts[i], num/den)
        pygame.draw.circle(screen, RED, ptPlt.astype(int), 3)

def drawPolylines(color='GREEN', thick=3):
    if (count < 2): return
    for i in range(count - 1):
        pygame.draw.line(screen, color, pts[i], pts[i+1], thick)
    for i in range(count):
        pygame.draw.rect(screen, BLUE, (pts[i][0] - margin, pts[i][1] - margin, 2 * margin, 2 * margin), 5)
        if(count > 2):
            if buttonCheck == 1:
                lagrange()
            elif buttonCheck == 2 or buttonCheck == -1:
                bezier()
            elif buttonCheck == 3:
                hermiteCubic()
            else:
                cubicSpline()

#Button Class
class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

# Loop until the user clicks the close button.
done = False
pressed = 0
margin = 6
old_pressed = 0
old_button1 = 0
old_button3 = 0

selectedPoint = -1
lagrangeButton = button((255,165,0),650,100,120,70,"Lagrange")
bezierButton = button((0,255,0),650,200,120,70,"Bezier")
hermiteButton = button((255,255,0),650,300,120,70,"Hermite")
cubicSplineButton = button((255,255,255),650,400,120,70,"Cubic Spline")
buttonCheck = -1
while not done:
    lagrangeButton.draw(screen, (0, 0, 0))
    bezierButton.draw(screen, (0, 0, 0))
    hermiteButton.draw(screen, (0, 0, 0))
    cubicSplineButton.draw(screen, (0, 0, 0))

    time_passed = clock.tick(30)

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pressed = -1
            if count > 2:
                if lagrangeButton.isOver(pos):
                    buttonCheck = 1
                    lagrange()
                elif bezierButton.isOver(pos):
                    buttonCheck = 2
                    bezier()
                elif hermiteButton.isOver(pos):
                    buttonCheck = 3
                    hermiteCubic()
                elif cubicSplineButton.isOver(pos):
                    buttonCheck = 4
                    cubicSpline()
        elif event.type == pygame.MOUSEBUTTONUP:
            pressed = 1
        elif event.type == pygame.QUIT:
            done = True
        else:
            pressed = 0

    button1, button2, button3 = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    pt = [x, y]

    if old_pressed == -1 and pressed == 1 and old_button1 == 1 and button1 == 0:
        #Mouse click
        if x < 590:
            pts.append(pt)
            count += 1
            pygame.draw.rect(screen, BLUE, (pt[0] - margin, pt[1] - margin, 2 * margin, 2 * margin), 5)
            # print("Mouse is clicked")
            # print("len:" + repr(len(pts)) + " mouse x:" + repr(x) + " y:" + repr(y) + " button:" + repr(
            #     button1) + repr(button3) + " old button:" + repr(old_button1) + repr(old_button3) +" pressed:" + repr(pressed) + " old pressed:" + repr(old_pressed) + " add pts ...")
    elif old_pressed == -1 and pressed == -1 and old_button1 == 1 and button1 == 1:
        #Mouse hold
        #print("Mouse is hold")
        for i in range(len(pts)):
            if((math.isclose(x, pts[i][0], rel_tol=0.05)) and (math.isclose(y, pts[i][1], rel_tol=0.05))):
                print("You selected point "+str(i))
                selectedPoint = i
    elif old_pressed == 0 and pressed == 0 and old_button1 == 1 and button1 == 1:
        #Mouse hold while moving
        if selectedPoint != -1:
            print("You are moving point "+str(selectedPoint))
            #redraw
            #pygame.draw.rect(screen, WHITE, (0,0,590,height))
            screen.fill(WHITE)
            pts[selectedPoint][0] = x
            pts[selectedPoint][1] = y
    elif old_pressed == 1 and pressed == 1 and old_button1 == 0 and button1 == 0:
        #print("Mouse is released")
        selectedPoint = -1
    elif old_pressed == -1 and pressed == 1 and old_button3 == 1 and button3 == 0:
        #Right mouse
        #print("Right mouse is clicked")
        for i in range(len(pts)):
            if((math.isclose(x, pts[i][0], rel_tol=0.05)) and (math.isclose(y, pts[i][1], rel_tol=0.05))):
                print("You deleted point "+str(i))
                del pts[i]
                count -= 1
                #pygame.draw.rect(screen, WHITE, (0,0,590,height))
                screen.fill(WHITE)
                break
    # else:
    #     print("len:" + repr(len(pts)) + " mouse x:" + repr(x) + " y:" + repr(y) + " button:" + repr(
    #         button1) + repr(button3) + " old button:" + repr(old_button1) + repr(old_button3) + " pressed:" + repr(pressed) + " old pressed:" + repr(old_pressed))

    if len(pts) > 1:
        drawPolylines(GREEN, 3)

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.update()
    old_button1 = button1
    old_pressed = pressed
    old_button3 = button3

pygame.quit()