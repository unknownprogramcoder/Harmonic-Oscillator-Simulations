import pygame as py
import random
import math
from matplotlib import pyplot
from tkinter import *

def q():
    py.quit()
    window.destroy()

py.init()
WIDTH = 2000
HEIGHT = 1000
screen = py.display.set_mode((WIDTH,HEIGHT))
py.display.set_caption("Harmonic Oscillator")
FPS = 1200
delta_time = 0.1
window=Tk()
window.title("Setting Values")
window.geometry("160x480+100+100")
window.resizable(0,0)

mass = Scale(window, label="mass", orient="vertical", from_=1, to=100)
mass.set(10)
mass.pack()

k = Scale(window, label="spring constant", orient="vertical", from_=1, to=100)
k.set(90)
k.pack()

b = Scale(window, label="resistance constant", orient="vertical", from_=0, to=20)
b.set(1)
b.pack()
 
w_o = Scale(window, label="drivingforce w", orient="vertical", from_=0, to=10)
w_o.set(0)
w_o.pack()

force = Scale(window, label="drivingforce horizontal", orient="vertical", from_=0, to=3)
force.set(0)
force.pack()


def w_get(k, m):
    return math.sqrt(k/m)
w = 0

def damping_parameter_get(b, m):
    return b / 2*m
beta = 0

text_place = [WIDTH/6, WIDTH/3, WIDTH/2, WIDTH*(2/3), WIDTH*(5/6)]
def draw_text(surf, text, x):
    font = py.font.Font(py.font.match_font('Sans'), 20)
    text_surface = font.render(text, True, (0,0,0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, 10)
    surf.blit(text_surface, text_rect)

window.update()

A = 1

def driving_force(t):
    return A*math.sin((w_o.get()/100)*t)
def periodic_moving(t):
    return 0.5*A*math.sin((0.01)*t)


g_a = 0.3
def gravity(m):
    return m*g_a
class Pin():
    def __init__(self, x, y, radius=10, color=(192,64,64)):
        self.x = x
        self.y = y
        self.v_x = 0.00
        self.v_y = 0
        self.radius = radius
        self.color = color
    def show(self, t, Move=False):
        if Move:
            self.v_x = periodic_moving(t)
        self.x += self.v_x*delta_time
        self.y += self.v_y*delta_time
        py.draw.circle(screen, self.color, (int(WIDTH/2 + 10*self.x), int(HEIGHT/2 - 10*self.y)), self.radius, 0)
        
class Particle():
    def __init__(self, x, y, v_x, v_y, target1, target2, masss, kk, bb, radius=10, color=(255,128,0), min_len=0.1):
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.a_x = 0
        self.a_y = 0 # 이걸 변화시킴.
        self.force_x = 0
        self.force_y = 0
        
        self.radius = radius
        self.color = color
        
        self.mass = mass.get()
        self.k = mass.get()
        self.b = b.get()
        
        self.min_len = min_len
        
        self.target1 = target1
        self.target1_x = None
        self.target1_y = None
        self.distance1_x = None
        self.distance1_y = None
        self.target2 = target2
        self.target2_x = None
        self.target2_y = None
        self.distance2_x = None
        self.distance2_y = None
        self.cos1 = None
        self.sin1 = None
        self.min_len1_x = None
        self.min_len1_y = None
        self.cos2 = None
        self.sin2 = None
        self.min_len2_x = None
        self.min_len2_y = None
    def update_parameters(self):
        self.mass = mass.get()
        self.k = mass.get()
        self.b = b.get()
        if self.target1[0] == 0:
            self.target1_x = pins[self.target1[1]].x
            self.target1_y = pins[self.target1[1]].y
        if self.target1[0] == 1:
            self.target1_x = particles[self.target1[1]].x
            self.target1_y = particles[self.target1[1]].y
        self.distance1_x = self.x - self.target1_x
        self.distance1_y = self.y - self.target1_y
        self.cos1 = self.distance1_x / (math.sqrt(self.distance1_x*self.distance1_x + self.distance1_y*self.distance1_y) + 0.001)
        self.sin1 = self.distance1_y / (math.sqrt(self.distance1_x*self.distance1_x + self.distance1_y*self.distance1_y) + 0.001)
        self.min_len1_x = self.min_len*self.cos1
        self.min_len1_y = self.min_len*self.sin1
        
        if self.target2[0] == 0:
            self.target2_x = pins[self.target2[1]].x
            self.target2_y = pins[self.target2[1]].y
        if self.target2[0] == 1:
            self.target2_x = particles[self.target2[1]].x
            self.target2_y = particles[self.target2[1]].y
        self.distance2_x = self.x - self.target2_x
        self.distance2_y = self.y - self.target2_y
        self.cos2 = self.distance2_x / (math.sqrt(self.distance2_x*self.distance2_x + self.distance2_y*self.distance2_y) + 0.001)
        self.sin2 = self.distance2_y / (math.sqrt(self.distance2_x*self.distance2_x + self.distance2_y*self.distance2_y) + 0.001)
        self.min_len2_x = self.min_len*self.cos2
        self.min_len2_y = self.min_len*self.sin2
    def set_accelation(self, t): # 힘 작용
        
        self.force_x = -self.k*(self.distance1_x-self.min_len1_x) - self.k*(self.distance2_x-self.min_len2_x) - self.b*self.v_x + driving_force(t) + 10*force.get()
        self.a_x = self.force_x / self.mass
        
        self.force_y = -self.k*(self.distance1_y-self.min_len1_y) - self.k*(self.distance2_y-self.min_len2_y) - self.b*self.v_y - gravity(self.mass) 
        self.a_y = self.force_y / self.mass
    def accelate(self):
        self.v_x += self.a_x*delta_time # 미분방정식 오일러 해법 (평균변화율 이용)
        self.v_y += self.a_y*delta_time
    def move(self):
        self.x += self.v_x*delta_time # 미분방정식 오일러 해법 (평균변화율 이용)
        self.y += self.v_y*delta_time
        py.draw.circle(screen, self.color, (int(WIDTH/2 + 10*self.x), int(HEIGHT/2 - 10*self.y)), self.radius, 5)
        py.draw.line(screen, self.color, (int(WIDTH/2 + 10*self.x), int(HEIGHT/2 - 10*self.y)), (int(WIDTH/2 + 10*self.target1_x), int(HEIGHT/2 - 10*self.target1_y)), 1)
        py.draw.line(screen, self.color, (int(WIDTH/2 + 10*self.x), int(HEIGHT/2 - 10*self.y)), (int(WIDTH/2 + 10*self.target2_x), int(HEIGHT/2 - 10*self.target2_y)), 1)


pins = []    
particles = []

pin1 = Pin(-20, 50)
#pin2 = Pin(-20, -50)
particle1 = Particle(-20, 45, 0, 0, (0,0), (1,1), 600, 3.0, 15)
particle2 = Particle(-20, 40, 0, 0, (1,0), (1,2), 600, 3.0, 15)
particle3 = Particle(-20, 35, 0, 0, (1,1), (1,3), 600, 3.0, 15)
particle4 = Particle(-20, 30, 0, 0, (1,2), (1,4), 600, 3.0, 15)
particle5 = Particle(-20, 25, 0, 0, (1,3), (1,5), 600, 3.0, 15)
particle6 = Particle(-20, 20, 0, 0, (1,4), (1,6), 600, 3.0, 15)
particle7 = Particle(-20, 15, 0, 0, (1,5), (1,7), 600, 3.0, 15)
particle8 = Particle(-20, 10, 0, 0, (1,6), (1,8), 600, 3.0, 15)
particle9 = Particle(-20, 5, 0, 0, (1,7), (1,9), 600, 3.0, 15)
particle10 = Particle(-20, 0, 0, 0, (1,8), (1,10), 600, 3.0, 15)
particle11 = Particle(-20, -5, 0, 0, (1,9), (1,11), 600, 3.0, 15)
particle12 = Particle(-20, -10, 0, 0, (1,10), (1,12), 600, 3.0, 15)
particle13 = Particle(-20, -15, 0, 0, (1,11), (1,13), 600, 3.0, 15)
particle14 = Particle(-20, -20, 0, 0, (1,12), (1,14), 600, 3.0, 15)
particle15 = Particle(-20, -25, 0, 0, (1,13), (1,15), 600, 3.0, 15)
particle16 = Particle(-20, -30, 0, 0, (1,14), (1,16), 600, 3.0, 15)
particle17 = Particle(-20, -35, 0, 0, (1,15), (1,17), 600, 3.0, 15)
particle18 = Particle(-20, -40, 0, 0, (1,16), (1,18), 600, 3.0, 15)
particle19 = Particle(-20, -45, 0, 0, (1,17), (1,18), 600, 3.0, 15)

pins.append(pin1)
#pins.append(pin2)
particles.append(particle1)
particles.append(particle2)
particles.append(particle3)
particles.append(particle4)
particles.append(particle5)
particles.append(particle6)
particles.append(particle7)
particles.append(particle8)
particles.append(particle9)
particles.append(particle10)
particles.append(particle11)
particles.append(particle12)
particles.append(particle13)
particles.append(particle14)
particles.append(particle15)
particles.append(particle16)
particles.append(particle17)
particles.append(particle18)
particles.append(particle19)

xlist, ylist = [], []
clock = py.time.Clock()
timetick = 0
py.display.flip()            
running = True
while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
    timetick += 1
    window.update_idletasks()
    window.update()
    
    w = w_get(k.get(), mass.get())
    beta = damping_parameter_get(b.get(), mass.get())
    
    screen.fill((255,255,255))
    
    draw_text(screen, "w= "+str(w), text_place[3])
    draw_text(screen, "beta= "+str(beta), text_place[1])
    draw_text(screen, "w_o= "+str(w_o.get()), text_place[4])
    
    for obj in pins:
        obj.show(timetick, False)
    for obj in particles:    
        obj.update_parameters()
        obj.set_accelation(timetick)
        obj.accelate()
        obj.move()
    
    xlist.append(timetick)
    ylist.append(math.sqrt(particle1.distance1_x**2 + particle1.distance1_y**2))
    py.display.update()
    clock.tick(FPS)

window.destroy()
py.quit()
pyplot.figure(figsize=(25,10))
pyplot.plot(xlist, ylist)
pyplot.xlabel('timetick')
pyplot.ylabel('space')
pyplot.title('oscillator')
pyplot.show() 