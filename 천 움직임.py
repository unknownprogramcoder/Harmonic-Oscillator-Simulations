import pygame as py
import random
import math
from matplotlib import pyplot
from tkinter import *

def q():
    py.quit()
    window.destroy()

py.init()
WIDTH = 1000
HEIGHT = 1000
screen = py.display.set_mode((WIDTH,HEIGHT))
py.display.set_caption("Harmonic Oscillator")
FPS = 1200
delta_time = 0.1
window=Tk()
window.title("Setting Values")
window.geometry("160x480+100+100")
window.resizable(0,0)

mass = Scale(window, label="mass", orient="vertical", from_=1, to=10000)
mass.set(1)
mass.pack()

k = Scale(window, label="spring constant", orient="vertical", from_=1, to=100)
k.set(40)
k.pack()

b = Scale(window, label="resistance constant", orient="vertical", from_=0, to=20)
b.set(10)
b.pack()
 
w_o = Scale(window, label="drivingforce w", orient="vertical", from_=0, to=10)
w_o.set(5)
w_o.pack()

force = Scale(window, label="drivingforce horizontal", orient="vertical", from_=0, to=10)
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

A = 15

def driving_force(t):
    return A*math.sin((w_o.get()/100)*t)
def periodic_moving(t):
    return 0.2*A*math.cos((0.01)*t)

g_a = 10
def gravity(m):
    return m*g_a
class Pin():
    def __init__(self, x, y, radius=10, color=(192,64,64)):
        self.x = x
        self.y = y
        self.v_x = 0
        self.v_y = 0
        self.radius = radius
        self.color = color
    def show(self, t, Move=False):
        if Move:
            self.x += periodic_moving(t)*delta_time
        py.draw.circle(screen, self.color, (int(WIDTH/2 + 10*self.x), int(HEIGHT/2 - 10*self.y)), self.radius, 0)
        
class Particle():
    def __init__(self, x, y, v_x, v_y, target1, target2, target3, target4, masss, kk, bb, radius=10, color=(255,128,0), min_len=10):
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
        self.k = k.get()
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
        self.target3 = target3
        self.target3_x = None
        self.target3_y = None
        self.distance3_x = None
        self.distance3_y = None
        self.target4 = target4
        self.target4_x = None
        self.target4_y = None
        self.distance4_x = None
        self.distance4_y = None
        self.cos1 = None
        self.sin1 = None
        self.min_len1_x = None
        self.min_len1_y = None
        self.cos2 = None
        self.sin2 = None
        self.min_len2_x = None
        self.min_len2_y = None
        self.cos3 = None
        self.sin3 = None
        self.min_len3_x = None
        self.min_len3_y = None
        self.cos4 = None
        self.sin4 = None
        self.min_len4_x = None
        self.min_len4_y = None
        
    def update_parameters(self):
        self.mass = mass.get()
        self.k = k.get()
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
        
        if self.target3[0] == 0:
            self.target3_x = pins[self.target3[1]].x
            self.target3_y = pins[self.target3[1]].y
        if self.target3[0] == 1:
            self.target3_x = particles[self.target3[1]].x
            self.target3_y = particles[self.target3[1]].y
        self.distance3_x = self.x - self.target3_x
        self.distance3_y = self.y - self.target3_y
        self.cos3 = self.distance3_x / (math.sqrt(self.distance3_x*self.distance3_x + self.distance3_y*self.distance3_y) + 0.001)
        self.sin3 = self.distance3_y / (math.sqrt(self.distance3_x*self.distance3_x + self.distance3_y*self.distance3_y) + 0.001)
        self.min_len3_x = self.min_len*self.cos3
        self.min_len3_y = self.min_len*self.sin3
        
        if self.target4[0] == 0:
            self.target4_x = pins[self.target4[1]].x
            self.target4_y = pins[self.target4[1]].y
        if self.target4[0] == 1:
            self.target4_x = particles[self.target4[1]].x
            self.target4_y = particles[self.target4[1]].y
        self.distance4_x = self.x - self.target4_x
        self.distance4_y = self.y - self.target4_y 
        self.cos4 = self.distance4_x / (math.sqrt(self.distance4_x*self.distance4_x + self.distance4_y*self.distance4_y) + 0.001)
        self.sin4 = self.distance4_y / (math.sqrt(self.distance4_x*self.distance4_x + self.distance4_y*self.distance4_y) + 0.001)
        self.min_len4_x = self.min_len*self.cos4
        self.min_len4_y = self.min_len*self.sin4
        
    def set_accelation(self, t): # 힘 작용
        
        self.force_x = -self.k*(self.distance1_x-self.min_len1_x) - self.k*(self.distance2_x-self.min_len2_x) - self.k*(self.distance3_x-self.min_len3_x) - self.k*(self.distance4_x-self.min_len4_x) - self.b*self.v_x + driving_force(t) + 5*force.get()
        self.a_x = self.force_x / self.mass
        
        self.force_y = -self.k*(self.distance1_y-self.min_len1_y) - self.k*(self.distance2_y-self.min_len2_y) - self.k*(self.distance3_y-self.min_len3_y) - self.k*(self.distance4_y-self.min_len4_y) - self.b*self.v_y - gravity(self.mass) 
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
        py.draw.line(screen, self.color, (int(WIDTH/2 + 10*self.x), int(HEIGHT/2 - 10*self.y)), (int(WIDTH/2 + 10*self.target3_x), int(HEIGHT/2 - 10*self.target3_y)), 1)
        py.draw.line(screen, self.color, (int(WIDTH/2 + 10*self.x), int(HEIGHT/2 - 10*self.y)), (int(WIDTH/2 + 10*self.target4_x), int(HEIGHT/2 - 10*self.target4_y)), 1)


pins = []    
particles = []

pin0 = Pin(-20, 20) 
pin1 = Pin(20, 20)
#pin2 = Pin(20, -20)
#pin3 = Pin(-20, -20)

# 인데

#particle0 = Particle(-10, 20, 0, 0, (0,0), (1,1), (1,4), (1,0), 600, 3.0, 15)
#particle1 = Particle(0, 20, 0, 0, (1,0), (1,2), (1,5), (1,1), 600, 3.0, 15)
#particle2 = Particle(10, 20, 0, 0, (0,1), (1,1), (1,6), (1,2), 600, 3.0, 15)
pin2 = Pin(-10, 20)
pin3 = Pin(0, 20)
pin4 = Pin(10, 20)
#여러 개 바꾸려면 귀찮아서 이렇게 편법으로 pin을 particles 배열 안에 넣음 ㅠ
particle3 = Particle(-20, 10, 0, 0, (0,0), (1,4), (1,8), (1,3), 600, 3.0, 15)
particle4 = Particle(-10, 10, 0, 0, (1,3), (1,0), (1,5), (1,9), 600, 3.0, 15)
particle5 = Particle(0, 10, 0, 0, (1,4), (1,6), (1,1), (1,10), 600, 3.0, 15)
particle6 = Particle(10, 10, 0, 0, (1,5), (1,7), (1,2), (1,11), 600, 3.0, 15)
particle7 = Particle(20, 10, 0, 0, (0,1), (1,6), (1,12), (1,7), 600, 3.0, 15)

particle8 = Particle(-20, 0, 0, 0, (1,3), (1,9), (1,13), (1,8), 600, 3.0, 15)
particle9 = Particle(-10, 0, 0, 0, (1,8), (1,4), (1,10), (1,14), 600, 3.0, 15)
particle10 = Particle(0, 0, 0, 0, (1,9), (1,5), (1,11), (1,15), 600, 3.0, 15)
particle11 = Particle(10, 0, 0, 0, (1,10), (1,6), (1,12), (1,16), 600, 3.0, 15)
particle12 = Particle(20, 0, 0, 0, (1,11), (1,7), (1,17), (1,12), 600, 3.0, 15)

particle13 = Particle(-20, -10, 0, 0, (1,13), (1,8), (1,14), (1,13), 600, 3.0, 15)
particle14 = Particle(-10, -10, 0, 0, (1,13), (1,9), (1,15), (1,18), 600, 3.0, 15)
particle15 = Particle(0, -10, 0, 0, (1,14), (1,10), (1,16), (1,19), 600, 3.0, 15)
particle16 = Particle(10, -10, 0, 0, (1,15), (1,11), (1,17), (1,20), 600, 3.0, 15)
particle17 = Particle(20, -10, 0, 0, (1,17), (1,16), (1,12), (1,17), 600, 3.0, 15)

particle18 = Particle(-10, -20, 0, 0, (1,18), (1,14), (1,19), (1,18), 600, 3.0, 15)
particle19 = Particle(0, -20, 0, 0, (1,18), (1,15), (1,20), (1,19), 600, 3.0, 15)
particle20 = Particle(10, -20, 0, 0, (1,20), (1,19), (1,16), (1,20), 600, 3.0, 15)
particle21 = Particle(-20, -20, 0, 0, (1,13), (1,18), (1,21), (1,21), 600, 3.0, 15)
particle22 = Particle(20, -20, 0, 0, (1,17), (1,20), (1,22), (1,22), 600, 3.0, 15)

pins.append(pin0)
pins.append(pin1)
#pins.append(pin2)
#pins.append(pin3)

particles.append(pin2)
particles.append(pin3)
particles.append(pin4)
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
particles.append(particle20)
particles.append(particle21)
particles.append(particle22)

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
    for obj in particles[0:3]: #실질적으로 pin들어있는 부분 ㅠ
        obj.show(timetick, False) 
    for obj in particles[3:]:    
        obj.update_parameters()
        obj.set_accelation(timetick)
        obj.accelate()
        obj.move()
    xlist.append(timetick)
    ylist.append(math.sqrt(particle3.distance1_x**2 + particle3.distance1_y**2))
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