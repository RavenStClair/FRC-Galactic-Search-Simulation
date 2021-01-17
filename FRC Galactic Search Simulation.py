import pygame
import math
import random
import time
import os
import fractions
"""This is a to-scale simulation for simulating math and logic associated with making the robot for 2021 work.
    all values entered are converted by "factor" into feet, and the field is scaled down. The relative locations and dimensions of
    all aspects of the field and goals are accurate, and the speed of the game may be set to simulate ftps."""
crashed = False
DISPLAY_WIDTH = 900
DISPLAY_HEIGHT = 450
field = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))


LockID = False
clickables_clicked = [0]
mouseup = True
drag_conditional = False
Click = False

factor = 30
WHITE = (255,255,255)
blue_missed = (74,134,232)
red_missed=(225,124,124)
BLUE_LIGHT = (94, 166, 247)
coordinates = [(12.5,2.5),(10,2.5),(5,2.5),(2.5,2.5),
               (10,5),(5,5),
               (12.5,7.5),(10,7.5),(7.5,7.5),(5,7.5),(2.5,7.5),
               (12.5,10),(10,10),(5,10),(2.5,10),
               (10,12.5),(5,12.5),
               (12.5,15),(10,15),(5,15),(2.5,15),
               (12.5,17.5), (10,17.5), (5,17.5), (2.5,17.5),
               (12.5,20),(10,20),(5,20),(2.5,20),
               (12.5,22.5),(10,22.5),(7.5,22.5),(5,22.5),(2.5,22.5),
               (12.5,25),(10,25),(5,25),(2.5,25),
               (10,27.5), (5,27.5)]

      
def scale_ft(value):
    return value * factor
def scale_in(value):
    return math.round(value/12*factor)
def rectoffier(offset,value):
    return factor*(value-2.5/2)
class draw_field:
    def field_default():
        for mark in coordinates:
            y = factor*(mark[0]-2.5/24)
            x= factor * (mark[1]-2.5/24)
            rec = pygame.Rect(x,y,factor*2.5/12,factor*2.5/12)
            pygame.draw.rect(field,(0,0,0), rec)
        

    
    

    
        
class BOT:
    def __init__(self,l,w):
        self.L = l
        self.W =w
        self.center = (2.5*factor,7.5*factor)
        self.a = l/2
        self.o=w/2
        self.speed=0
        self.color = (10,59,0)
        self.angle = 0
        self.dim = (self.a,self.o)
        self.h = math.sqrt(self.a**2+self.o**2)
        self.ang_v = 0
        self.dr = 0
        self.ar = 0
        self.dx = 0
        self.dv = 0
        self.v0 = 0
        self.dy = 0
        self.dp = 0
        self.in_mot = 0
        self.trapcounter = 0
    def reset_all(self):
        l = self.L
        w= self.W
        self.center = (2.5*factor,7.5*factor)
        self.a = l/2
        self.o=w/2
        self.speed=0
        self.color = (10,59,0)
        self.angle = 0
        self.dim = (self.a,self.o)
        self.h = math.sqrt(self.a**2+self.o**2)
        self.ang_v = 0
        self.dr = 0
        self.ar = 0
        self.dx = 0
        self.dv = 0
        self.v0 = 0
        self.dy = 0
        self.dp = 0
        self.in_mot = 0
        self.trapcounter = 0
    def display(self):
        """calculate locations of corners of robot based on robot width, height, and rotation.
            a modified form could be used to determine how far each encoder must move to reach a
            given location"""
        """I am not explaining the math here, as it is easy to understand with diagrams but hard to put into words"""
        p1 = self.center[0]+self.h*(math.cos(math.pi+math.acos(self.a/self.h)-self.angle))
        p2=self.center[1]+self.h*(math.sin(math.asin(self.o/self.h)+math.pi-self.angle))
        
        p3 = self.center[0]+self.h*(math.cos(math.acos(self.a/self.h)-self.angle))
        p4=self.center[1]+self.h*(math.sin(math.asin(self.o/self.h)-self.angle))
        
        p5 = self.center[0]+self.h*(math.cos(math.acos((self.a)/self.h)-self.angle-math.pi/2))
        p6 = self.center[1]+self.h*(math.sin(math.asin(self.o/self.h)-self.angle-math.pi/2))
        
        p7 = self.center[0]+self.h*(math.cos(math.acos(self.a/self.h)-self.angle-3*math.pi/2))
        p8 = self.center[1]+self.h*(math.sin(math.asin(self.o/self.h)-self.angle-3*math.pi/2))
        
        pygame.draw.polygon(field,self.color,((p1,p2),(p5,p6),(p3,p4),(p7,p8)))
    def set_angle(self,angle):
        self.angle = angle
    def get_angle(self):
        return self.angle
    def get_pos(self):
        return self.center
    def set_pos(self, pos):
        self.center = pos
    def traprad(self,rad,ti, dt,c0):
        t = pygame.time.get_ticks()-ti
        av = rad/dt
        if t < dt:
            self.dr = av*t
        self.set_angle(c0+self.dr)
    def traptang(self,dx,ti,dt,v0, c0):
        t = pygame.time.get_ticks()-ti
        v = dx/dt
        if t < dt:
            self.dp = v*t
            self.in_mot = 1
        else:
            self.in_mot = 2
        self.dx = self.dp*math.cos(-self.angle)
        self.dy = self.dp*math.sin(-self.angle)
        self.set_pos((c0[0]+self.dx, c0[1]+self.dy))
    def traptan_r(self):
        self.in_mot = 0
    def get_r_err(self,c):
        return -math.atan(((15-c[1])*factor-self.get_pos()[1])/((c[0])*factor-self.get_pos()[0]))
    def get_p_err(self, c):
        return math.sqrt((c[0]*factor-self.get_pos()[0])**2+((15-c[1])*factor-self.get_pos()[1])**2)
        
        
        



B = BOT(2*factor,2*factor) 

class Galactic_Search:
    """because "Placement of the ROBOT is not considered signalling", we can put the robot at B1 when it is taking
        RedB, D1 when it is taking BlueB, "C1" when it is taking RedA, and "E1" when it is taking BlueC. The robot can then use a limelight to measure
        the distance between itself and the ball furthest from it, and complete its routine based on the distance
        the ball is. This could also set it up for the maximum efficiency."""
    def __init__(self):
        self.pos = (0,0)
        self.points = []
        self.color = (0,0,0)
        self.game = 99
        self.state = 0
        self.C3 = (7.5,7.5)
        self.A6 = (15,12.5)
        self.D5 = (12.5,5)
        self.D6 = (15,5)
        self.B8 = (17.5, 10)
        self.D10 = (25,5)
        self.E6 = (15,2.5)
        self.B7 = (17.5,10)
        self.C9 =(22.5,7.5)
        self.B3 = (7.5,10)
        self.option = None
        self.t_angle =0
        self.sub_counter = 0
        self.counter = 0
        self.ti = pygame.time.get_ticks()
        self.dt = 0
        self.t_d = 0
        self.endpoint = (0,0)
        self.game = 0

    
    def reset_all(self):
        self.pos = (0,0)
        self.points = []
        self.color = (0,0,0)
        self.game = 99
        self.state = 0
        self.C3 = (7.5,7.5)
        self.A6 = (15,12.5)
        self.D5 = (12.5,5)
        self.D6 = (15,5)
        self.B8 = (17.5, 10)
        self.D10 = (25,5)
        self.E6 = (15,2.5)
        self.B7 = (17.5,10)
        self.C9 =(22.5,7.5)
        self.B3 = (7.5,10)
        self.option = None
        self.t_angle =0
        self.sub_counter = 0
        self.counter = 0
        self.ti = pygame.time.get_ticks()
        self.dt = 0
        self.t_d = 0
        self.endpoint = (0,0)
        self.game = 0
    def reset1(self,cord):
         self.t_angle = B.get_r_err(cord)
         self.sub_counter=1
         self.ti = pygame.time.get_ticks()
         print("reset")
    def turnToTarget(self):
        if ((abs(self.t_angle-B.get_angle())%2*math.pi)>0.1):
                    B.traprad(self.t_angle-B.get_angle(),self.ti,250,B.get_angle())
        else:
            self.sub_counter = 2
    def setPath(self,cord):
        self.t_d =B.get_p_err(cord)
        self.ti = pygame.time.get_ticks()
        B.traptan_r()
        self.sub_counter = 3
        self.pos = B.get_pos()
    def executePath(self):
        if B.in_mot != 2:
            B.traptang(self.t_d, self.ti, 700,0,self.pos)
        else:
            self.counter = self.counter+1
            self.sub_counter = 0
    def acquire_target(self,cord):
        if self.sub_counter == 0:
            self.reset1(cord)
        elif self.sub_counter == 1:
            self.turnToTarget()
        elif self.sub_counter == 2:
            self.setPath(cord)
        elif self.sub_counter == 3:
            self.executePath()
    def runPathX(self, speed,cord,c0=B.get_pos()):
        self.endpoint = (30,cord[2][1])   
        if self.counter <=2:
            self.acquire_target(cord[self.counter])
        if self.counter == 3:
            self.acquire_target(self.endpoint)        
    def pathARed(self):
        self.points = [self.C3, self.D5, self.A6]
        self.color = red_missed
        self.game = 0
    def pathABlue(self):
        self.points = [self.E6,self.B7,self.C9]
        self.color = blue_missed
        self.game = 1
    def pathBRed(self):
        self.points = [self.B3,self.D5, self.B7]
        self.color = red_missed
        self.game = 2
    def pathBBlue(self):
        self.points = [self.D6, self.B7, self.D10]
        self.color = blue_missed
        self.game = 3
    def randomize(self):
        draw_field.field_default()
        if self.state ==0:
            self.option = random.choice([self.pathBBlue,self.pathBRed,self.pathARed,self.pathABlue])
            self.state = 1
        self.option()
        for p in self.points:
            pygame.draw.circle(field,self.color, (p[0]*factor,(15-p[1])*factor),3/12*factor)
        Galactic_Search.runPathX(self,10,self.points)
    def set_game(self,state):
        self.game = state
    def run(self):
        draw_field.field_default()
        if self.game == 0:
            self.option = self.pathARed
        elif self.game ==1:
            self.option = self.pathABlue
        elif self.game == 2:
            self.option = self.pathBRed
        elif self.game == 3:
            self.option = self.pathBBlue
        self.option()
        for p in self.points:
            pygame.draw.circle(field,self.color, (round(p[0]*factor),round((15-p[1]))*factor),round(3/12*factor))
        Galactic_Search.runPathX(self,20,self.points)
        
            
            
pygame.init()
THAT_ONE_TITLE = pygame.font.SysFont("dubai", 40)
BUTTON_TEXT= pygame.font.SysFont("dubai", 20)
def fontText(text,font = BUTTON_TEXT,color = WHITE):
    return font.render(text, True, color)


        


                                               
    

class Mouse_Magic:
    def __init__(self):
        self.drag = False
        self.down = False
        self.dragging = False
        self.click = False
        self.press = False
        self.release = False
    def Drag(self,event):
         if event.type == pygame.MOUSEBUTTONDOWN:
             self.drag = True
             self.dragging = False
             return False
         elif event.type == pygame.MOUSEBUTTONUP:
             self.drag = False
             self.dragging = False
             return False
         elif event.type==pygame.MOUSEMOTION and self.drag:
             self.dragging = True
             return True
    def hover(self, in_place, event):
        if in_place:
            if event.type ==pygame.MOUSEBUTTONDOWN:
                self.down = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.down = False
            if not self.down:
                return True
            else:
                return False
        else:
            return False
    def Click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.press = True
            self.click = False
            return False
        elif event.type == pygame.MOUSEMOTION:
            self.press = False
            return False
        elif event.type == pygame.MOUSEBUTTONUP and self.press == True:
            self.click = True
            print("Clicked!")
            return True
        else:
            return False
            
    def mousex(self):
        return pygame.mouse.get_pos()[0]
    
    def mousey(self):
        return pygame.mouse.get_pos()[1]
    
    def mouse_in_rect(self,x,y,w,h):
        if Mouse_Magic.mousex(self)>(x+w) or Mouse_Magic.mousex(self) < x or Mouse_Magic.mousey(self)>y+h or Mouse_Magic.mousey(self) < y:
            return False
        else:
            return True

    def mouseUp(self, event):
        global mouseup
        if event.type == pygame.MOUSEBUTTONUP:
            mouseup=True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouseup = False

    def mouse_drag_to_click_zone(self, x,y,w,h,event, DC  = drag_conditional):
        if not Mouse_Magic.mouse_in_rect(self, x,y,w,h):
            if event.type == pygame.MOUSEBUTTONDOWN:
                DC = True
                return drag_conditional
            else:
                DC = False
                return DC
        else:
            return DC

G = Galactic_Search()
MM = Mouse_Magic()
  

class master:
    def __init__(self):
        self.choice = True
        self.startMessage = THAT_ONE_TITLE.render("Select a Simulation", True, WHITE)
        self.RECT_HEIGHT = 150
        self.RECT_WIDTH = 150
        self.buttons = [fontText("Path A: Red"), fontText("Path A: Blue"), fontText("Path B: Red"), fontText("Path B: Blue")]
    def run(self, event):
        if self.choice == True:
            field.fill((0, 68, 150))
            field.blit(self.startMessage, (300, 100))
            for i in range(0,4):
                pygame.draw.rect(field,BLUE_LIGHT, pygame.Rect(75+200*i,200,self.RECT_WIDTH,self.RECT_HEIGHT))
                field.blit(self.buttons[i], (80+205*i,250))
                if MM.Click(event) and MM.mouse_in_rect(75+200*i,200,self.RECT_WIDTH,self.RECT_HEIGHT):
                    print(G.option)
                    G.set_game(i)
                    self.choice = False
                    
        else:
            G.run()
            B.display()
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_ESCAPE):
                    self.choice = True
                    B.reset_all()
                    G.reset_all()
                
    
C = master() 
while not crashed:
    for event in pygame.event.get():
        MM.Click(event)
        if event.type == pygame.QUIT:
            crashed = True
      field.fill(WHITE)
      C.run(event)
    """G.randomize()"""
    """B.display()"""

    pygame.display.flip()
pygame.quit()
