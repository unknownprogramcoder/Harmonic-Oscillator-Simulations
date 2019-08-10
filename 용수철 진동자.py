import pygame as py
import random
import math
from matplotlib import pyplot
from tkinter import *
def q():
    py.quit()
    window.destroy()


py.init()
WIDTH = 800
HEIGHT = 800
screen = py.display.set_mode((WIDTH,HEIGHT))
py.display.set_caption("Harmonic Oscillator")
FPS = 60

window=Tk()
window.title("Setting Values")
window.geometry("160x480+100+100")
window.resizable(0,0)

mass = Scale(window, label="mass", orient="vertical", from_=1, to=500)
mass.set(4)
mass.pack()
k = Scale(window, label="spring constant", orient="vertical", from_=1, to=100)
k.set(1)
k.pack()
def w_get(k, m):
    return math.sqrt(k/m)
w = 0
def damping_parameter_get(b, m):
    return b / 2*m
beta = 0
b = Scale(window, label="resistance constant", orient="vertical", from_=0, to=20)
b.set(0)
b.pack()
 
w_o = Scale(window, label="drivingforce w", orient="vertical", from_=0, to=10)
w_o.set(0)
w_o.pack()


text_place = [WIDTH/6, WIDTH/3, WIDTH/2, WIDTH*(2/3), WIDTH*(5/6)]
def draw_text(surf, text, x):
    font = py.font.Font(py.font.match_font('Sans'), 20)
    text_surface = font.render(text, True, (0,0,0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, 10)
    surf.blit(text_surface, text_rect)

window.update()

A = 5
def driving_force(t):
    return A*math.sin((w_o.get()/10)*t)
class Particle():
    def __init__(self, x, y, v_x, v_y, color):
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y
        self.a_x = 0
        self.a_y = 0 # 이걸 변화시킴.
        self.force_x = 0
        self.force_y = 0
        self.radius = 10
        self.color = color
        self.ypos = HEIGHT/2
    def set_accelation(self, t):
        self.force_y = -k.get()*self.y - b.get()*self.v_y + driving_force(t)
        self.a_y = self.force_y / mass.get()
    def accelate(self):
        self.v_x += self.a_x
        self.v_y += self.a_y
    def move(self):
        self.x += self.v_x
        self.y += self.v_y
        self.xpos = WIDTH/2 - 10*self.x
        self.ypos = HEIGHT/2 - 10*self.y
        py.draw.circle(screen, self.color, (int(self.xpos), int(self.ypos)), self.radius, 0)
        
object1 = Particle(0, A, 0, 0, (255, 0, 255))

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
    object1.set_accelation(timetick)
    object1.accelate()
    object1.move()
    xlist.append(timetick)
    ylist.append(object1.y)
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