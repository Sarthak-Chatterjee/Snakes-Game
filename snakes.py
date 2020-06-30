from math import log
import turtle
import time
from random import randint
from math import sqrt
from os.path import exists
import winsound


def distance(t1,t2):#think if it can be avoided
    return sqrt((float(t1[0])-float(t2[0]))**2+(float(t1[1])-float(t2[1]))**2)

def dlay(score):
    limit = 20
    highest_delay = .3
    steep = 1
    return steep/(steep*score+1/highest_delay)#its best, just fix how fast would the steep should be

class Snake():
    
    def __init__(self, width = 0, Type = 'box'):
        if width: self.width = width
        else:width = 2*border_width
        self.turned = False
        self.width,self.length = width,width*3
        self.last = time.time()
        self.fed = []
        self.eaten = 0#for score
        self.delay = .3
        self.tlist = [][:]
        self.head = turtle.Turtle('circle')
        self.head.pu()
        self.head.color('green')
        self.head.shapesize(self.width/20,self.width/20,0)
        self.head.speed(0)
        for i in range(2):
            self.tlist.append(self.head.stamp())
            self.head.fd(self.width)
        self.pos_list = [(0,0),(width,0),(2*width,0)][:]
            
    def move(self):
        if time.time() - self.last >= self.delay:
            self.tlist.append(self.head.stamp())
            self.head.fd(self.width)
            self.head.clearstamp(self.tlist.pop(0))
            self.pos_list.append(self.head.pos())
            del self.pos_list[0]
            self.turned = False
            self.last = time.time()
            
    def eat(self,food):
        if self.head.distance(*food.sight.pos()) < border_width/2:
            food.newfood()
            self.eaten+=1
            self.delay = dlay(self.eaten)
            self.head.shapesize(self.width/20,self.width/20,5)
            self.fed.append((self.head.stamp(),self.head.pos()))
            self.head.shapesize(self.width/20,self.width/20,0)
            
        if self.fed and distance(self.pos_list[0],self.fed[0][1]) <border_width/2:
            st,posi = self.fed.pop(0)
            self.pos_list = [posi]+self.pos_list
            self.tlist = [st]+self.tlist

    def up(self):
        winsound.PlaySound('C:/Users/sarth/Downloads/beep.wav',winsound.SND_ASYNC)
        if self.head.heading() in (0,180) and not self.turned:
            self.head.seth(90)
            self.turned = True

    def down(self):
        winsound.PlaySound('C:/Users/sarth/Downloads/beep.wav',winsound.SND_ASYNC)
        if self.head.heading() in (0,180) and not self.turned:
            self.head.seth(270)
            self.turned = True

    def right(self):
        winsound.PlaySound('C:/Users/sarth/Downloads/beep.wav',winsound.SND_ASYNC)
        if self.head.heading() in (90,270) and not self.turned:
            self.head.seth(0)
            self.turned = True

    def left(self):
        winsound.PlaySound('C:/Users/sarth/Downloads/beep.wav',winsound.SND_ASYNC)
        if self.head.heading() in (90,270) and not self.turned:
            self.head.seth(180)
            self.turned = True

    def dead(self):
        for i in self.pos_list[:-1]:
            if self.head.distance(*i)<=5: return True
        x,y = self.head.pos()
        if abs(x) > max_x+.1 or abs(y) > max_y+.1: return True
        return False


    

class Food():
    
    def __init__(self,snake):
        self.last = time.time()
        self.snake = snake
        self.size = self.snake.width
        self.sight = turtle.Turtle(shape = 'circle',visible = False)
        self.sight.color('yellow')
        self.sight.shapesize(snake.width/25,snake.width/25,0)
        self.sight.pu()
        self.sight.speed(0)
        self.sight.goto(self.new_cor())
        self.sight.showturtle()
        
    def blink(self,delay = .5):
        if time.time() - self.last >= delay:
            self.sight.color('yellow')
            self.last = time.time()
        elif time.time() - self.last >= delay/2:
            self.sight.color('cyan')

    def new_cor(self):
        x0,y0 = round(max_x/(2*border_width)),round((max_y/(2*border_width)))
        while True:
            x,y = (2*border_width)*randint(-x0,x0),(2*border_width)*randint(-y0,y0)
            if not (0 in [max(0,distance((x,y),i)-border_width/2) for i in self.snake.pos_list] or (x,y) == self.sight.pos()): break
        return x,y

    def newfood(self):
        self.sight.hideturtle()
        self.sight.goto(self.new_cor())
        self.sight.showturtle()

        

class Obstacle:

    def __init__(obstacle,Type = 'box'):

        if Type == 'box':
            obstacle.brick = turtle.Turtle(visible = False)
            obstacle.brick.pu()
            obstacle.brick.color('red')
            obstacle.brick.width(border_width)
            obstacle.brick.speed(0)
            obstacle.brick.goto(-(max_x+3*border_width/2),-(max_y+3*border_width/2))
            obstacle.brick.pd()
            for i in range(2):
                obstacle.brick.fd(2*max_x+3*border_width)
                obstacle.brick.lt(90)
                obstacle.brick.fd(2*max_y+3*border_width+.1)
                obstacle.brick.lt(90)

            


def pen():
    t = turtle.Turtle(visible = False)
    t.color(['black','white'][wn.bgcolor() == 'black'])
    t.speed(0)
    t.pu()
    return t


def write_down(cords, pen, color, arg, move=False, align="left", font=("Arial", 8, "normal")):
    pen.pu()
    pen.goto(*cords)
    pen.pd()
    pen.color(color)
    pen.write(arg, move, align, font)
    pen.pu()


def screenOn(window_width = 900,panel_ratio = 1.616,night_mode = False): # future plans to change panel_ratio
    global wn, border_width, max_x, max_y
    wn = turtle.Screen()
    wn.title("Snakes by Sarthack")
    wn.bgcolor(['white','black'][night_mode])
    wn.setup(width = window_width,height = window_width/panel_ratio)
    real_ratio,parts = (2,1),2*10   #parts must be divisible by 2
    xblocks,yblocks = real_ratio[0]*parts,real_ratio[1]*parts
    border_width = (wn.window_width()*(1-.1))/(2*xblocks)
    max_x,max_y = xblocks*border_width,yblocks*border_width
    wn.listen()
    constant_args()

 


def constant_args():
    cpen = pen()
    
    write_down((wn.window_width()/2-6.8*border_width,-wn.window_height()/2+border_width),cpen,'grey','#Sarthack',font=("Arial", max(1,int(border_width)), "normal"))
    write_down((0,max_y+3*border_width),cpen,'red','SNAKES',align = 'center',font=("Arial", int(3*border_width), "bold underline"))
    write_down((8*border_width,(max_y+3*border_width)),cpen,'lime',' .py',align = 'left',font=("Arial", max(1,int(border_width)), "normal"))
    write_down((-wn.window_width()/2+border_width,-wn.window_height()/2+border_width),cpen,'grey',"Press 'h' for help",font=("Arial", max(1,int(border_width)), "normal"))


    write_down((-max_x-1*border_width,(max_y+3*border_width)),cpen,'lime','Snake Master:',align = 'left',font=("Arial", max(1,int(1.2*border_width)), "normal"))
    write_down((28*border_width,(max_y+3*border_width)),cpen,'lime','Score:',font=("Arial", max(1,int(1.2*border_width)), "normal"))
    

def navigations(snake):
    wn.onkeypress(snake.up, 'Up')
    wn.onkeypress(snake.left, 'Left')
    wn.onkeypress(snake.down, 'Down')
    wn.onkeypress(snake.right, 'Right')
    wn.onkeypress(snake.up, 'w')
    wn.onkeypress(snake.left, 'a')
    wn.onkeypress(snake.down, 's')
    wn.onkeypress(snake.right, 'd')

def update_score():
    global snake,score
    score.clear()
    write_down((max_x+1*border_width,(max_y+2*border_width)),score,'Yellow','{0:0=5d}'.format(snake.eaten),align = 'right',font=("Arial", max(1,int(2*border_width)), "bold"))

def update_highest(file,score):
    try:
        fin = open(file)
        prev = fin.read().strip('\n').split('\n')
        fin.close()
        tups = makeTups(prev)
        print(tups)
        if  len(tups)<5 or score>tups[-1][0]:
            name = wn.textinput("NEW HIGH SCORE", "Enter your name : ")
            if (name == None) or name == '': name = 'user'
            tups.append((score,'<'+name+'>'))
            tups.sort(reverse = True)
        fin = open(file,'w')
        fin.write(makelist(tups))
        fin.close()
        highests.clear()
        wn.listen()
        write_down((-21*border_width,(max_y+2.5*border_width)),highests,'gold',strHigh('snakes_highests.txt'),align = 'center',font=("Arial", max(1,int(1.5*border_width)), "bold"))
    except:
        turtle.mainloop()

def makeTups(l):
    t = []
    if l == ['']: return t
    for i in l:
        for index in range(len(i)-1,-1,-1):
            if i[index] == ' ': break
        t.append((int(i[index+1:]),i[:index]))
    return t

def makelist(t):
    l = list()
    for i in t[:5]:
        l.append(i[1]+' '+str(i[0]))
    print('in makelist: ',l)
    return '\n'.join(l)

def strHigh(file,highest_only = True):
    if exists(file):fin = open(file)
    else:
        fin = open(file,'x')
        fin.close()
        return ''
    if highest_only:
        s = fin.readline().strip()
        if len(s)>14:
            for index in range(len(s)-1,-1,-1):
                if s[index] == ' ': break
            s = s[:10-len(s)+index]+'...> '+s[index+1:]
        
    else: s = fin.read()
    fin.close()
    return s


def clear_records():
    global snake,food,vpen
    snake.head.reset()
    food.sight.reset()
    vpen.clear()
    score.clear()

def newGame(paused = False):
    try:
        global snake,food,obs,vpen,started,pause
        vpen.clear()
        score.clear()
    ##    print(started,pause,paused)

        if (started == False and pause == False and paused == True) or\
           (started ==  pause == paused == False) or \
           (started == True and pause == True and paused == False):
               
            ''' u started a new game after loosing last one
            or, this is ur first game
            or, u just restarted the game after pausing the previous game  (pressed enter after space / h)
            '''

            
            started = True
            if pause:
                pause = False
                clear_records()
            del wn._turtles[2:]
            snake = Snake()
            food = Food(snake)
            obs = Obstacle()
            navigations(snake)

        elif not(started == True and pause == False and paused == True):
            return
        
        while not pause:
            wn.update()
            food.blink()
            snake.eat(food)
            update_score()
            snake.move()
            snake.eat(food)
            update_score()
            if snake.dead():
                clear_records()
                write_down((0,0),vpen,'red','  YOU LOST\nYour Score: {}\n'.format(snake.eaten),align = 'center',font=("Arial", max(1,int(3*border_width)), "normal"))
                write_down((0,0),vpen,'green','Press Enter to Restart'.format(snake.eaten),align = 'center',font=("Arial", max(1,int(1.5*border_width)), "normal"))
                started = False
                print('here in new game before updating highscore')
                update_highest('snakes_highests.txt',snake.eaten)
                break
        print('ended',started,pause,paused)
        if started == False:
            print('bye bye')
            return
        turtle.mainloop()
    except:
        pass




def wait():
    if started:
        global pause,vpen
        pause = not pause
        if pause:
            write_down((0,5*border_width),vpen,'orange','Paused\n',align = 'center',font=("Arial", max(1,int(4*border_width)), "normal"))
            write_down((0,0),vpen,'green','Press space to continue\n',align = 'center',font=("Arial", max(1,int(2*border_width)), "normal"))
            write_down((0,-2*border_width),vpen,'orange','Press Enter to restart\n',align = 'center',font=("Arial", max(1,int(1.5*border_width)), "normal"))

        else:
            newGame(True)


def Help():
    global pause,vpen,started
    vpen.clear()
    if started:
        pause = True
    write_down((0,14*border_width),vpen,'aqua','HELP',align = 'center',font=("Arial", max(1,int(3*border_width)), "bold underline"))
    write_down((0,-15*border_width),vpen,'orange',"'Up' to face the snake North                'Down' to face the snake South\n\n'Left' to face the snake West                  'Right' to face the snake East\n\n'space' to pause / continue the game         'enter' to start a new game\n\nPress 'p' to see all High Scores        Press 'r' to reset the High Scores\n\nPress 'm' for sound on/off              Press 'b' to turn night mode on/off",align = 'center',font=("Arial", max(1,int(1.8*border_width)), "normal"))

def highScores():
    global pause,vpen,started
    vpen.clear()
    if started:
        pause = True
    write_down((0*border_width,8*border_width),vpen,'purple','All High Scores:',align = 'right',font=("Arial", max(1,int(2.5*border_width)), "bold underline"))
    write_down((0*border_width,-10*border_width),vpen,'cyan',strHigh('snakes_highests.txt',0),align = 'center',font=("Arial", max(1,int(2*border_width)), "normal"))

def nightMode():
    wn.bgcolor(['white','black'][wn.bgcolor() == 'white'])
    
def reSet():
    fin = open('snakes_highests.txt','w')
    fin.close()
    highests.clear()
    write_down((-12*border_width,(max_y+2.5*border_width)),highests,'gold',strHigh('snakes_highests.txt'),align = 'right',font=("Arial", max(1,int(2*border_width)), "bold"))

screenOn(window_width = 900)
wn.tracer(0)
vpen = pen()
score = pen()
highests =  pen()
pause = False
started = False
music = True
write_down((0,0),vpen,'green','Press enter to Start',align = 'center',font=("Arial", max(1,int(3*border_width)), "normal"))
write_down((-24*border_width,(max_y+2.5*border_width)),highests,'gold',strHigh('snakes_highests.txt'),align = 'center',font=("Arial", max(1,int(1.5*border_width)), "bold"))
wn.onkeypress(newGame,'Return')
wn.onkeypress(wait,'space')
wn.onkeypress(Help,'h')
wn.onkeypress(highScores,'p')
wn.onkeypress(nightMode,'b')
wn.onkeypress(reSet,'R')
turtle.mainloop()


'''TASKS:
add music and m button
try to accelerate the snake with the score increasing
try to create more obstacles and different modes
try to give snake a better shape
try different styles for the platform
'''
