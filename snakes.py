"""This is a Simple Game of Snakes for exclusively windows platform.

TASKS:
    try to create more obstacles and different modes
    make it platform independent(for pc only)
    try to give snake a better shape
    try different styles for the platform
    add more music
    try to change panel_ratio
    sort out memory problem if any
    fix how fast would the steep should be in dlay()
    try to make the timer more beautiful if possible


problems that will/may occur:
    counter wouldn't stop if two bigfood comes and we eat the last one
    memory can be optimised
    someone may be unable to see the .py or anything else
    someone may be able to score a 6 digit no.
"""

import turtle
import time
from math import sqrt
from random import randint
from os.path import exists
import winsound



#create some necessary functions
def distance(point_1, point_2):#think if it can be avoided
    '''returns the distance betwwen two points'''
    return sqrt((float(point_1[0])-float(point_2[0]))**2+(float(point_1[1])-float(point_2[1]))**2)

def dlay(score):
    '''returns time(in seconds) of delay between two moves
    of the snake according to the score'''
    highest_delay = .3
    steep = 1
    return steep/(steep*score+1/highest_delay)



# create classes for Snake, Food, Big food, obstacles and pen
class Snake:
    '''Creates a snake object of given width and wall type
    '''

    def __init__(self, width=0, Type='box'):
        if not width: width = 2*border_width
        self.turned = False
        self.width, self.length = width, width*3
        self.last = time.time()
        self.fed = []
        self.eaten = [0, 0]# 0 to count small foods, 1 to count big foods
        self.score = 0
        self.delay = .3
        self.tlist = [][:]
        self.head = turtle.Turtle('circle')
        self.head.pu()
        self.head.color('green')
        self.head.shapesize(self.width/20, self.width/20, 0)
        self.head.speed(0)
        for _ in range(2):
            self.tlist.append(self.head.stamp())
            self.head.fd(self.width)
        self.pos_list = [(0, 0), (width, 0), (2*width, 0)][:]

    def move(self):
        """Moves the snake 1 step forward
        """
        if time.time() - self.last >= self.delay:
            self.tlist.append(self.head.stamp())
            self.head.fd(self.width)
            self.head.clearstamp(self.tlist.pop(0))
            self.pos_list.append(self.head.pos())
            del self.pos_list[0]
            self.turned = False
            self.last = time.time()

    def eat(self, foods):
        """Makes the snake eat if food is available"""
        for food in foods:
            if food.sight.pos() in Food.coords \
               and self.head.distance(*food.sight.pos()) < border_width/2:
                self.score += food.score
                food.newfood()
                self.delay = dlay(sum(self.eaten))
                self.head.shapesize(self.width/20, self.width/20, 5)
                self.fed.append((self.head.stamp(), self.head.pos()))
                self.head.shapesize(self.width/20, self.width/20, 0)

            if self.fed and distance(self.pos_list[0], self.fed[0][1]) < border_width/2:
                st, posi = self.fed.pop(0)
                self.pos_list = [posi]+self.pos_list
                self.tlist = [st]+self.tlist

    def up(self):
        """Turns the snake North"""
        if music: winsound.PlaySound('beep.wav', winsound.SND_ASYNC)
        if self.head.heading() in (0, 180) and not self.turned:
            self.head.seth(90)
            self.turned = True

    def down(self):
        """Turns the snake South"""
        if music: winsound.PlaySound('beep.wav', winsound.SND_ASYNC)
        if self.head.heading() in (0, 180) and not self.turned:
            self.head.seth(270)
            self.turned = True

    def right(self):
        """Turns the Snake East"""
        if music: winsound.PlaySound('beep.wav', winsound.SND_ASYNC)
        if self.head.heading() in (90, 270) and not self.turned:
            self.head.seth(0)
            self.turned = True

    def left(self):
        """Turns the snake West"""
        if music: winsound.PlaySound('beep.wav', winsound.SND_ASYNC)
        if self.head.heading() in (90, 270) and not self.turned:
            self.head.seth(180)
            self.turned = True

    def dead(self):
        """Checks if the snake is dead"""
        for i in self.pos_list[:-1]:
            if self.head.distance(*i) <= 5: return True
        x, y = self.head.pos()
        if abs(x) > max_x+.1 or abs(y) > max_y+.1: return True
        return False


class Food:
    """Creates a Food object for a Snake to eat"""
    coords = list()
    size_ratio = 1
    lifetime = float('inf')
    score = 1
    def __init__(self, snake, ratio=1):
        self.timer = time.time()
        self.last = time.time()
        self.snake = snake
        self.size = self.snake.width
        self.sight = turtle.Turtle(shape='circle', visible=False)
        self.sight.color('yellow')
        self.sight.shapesize(ratio*snake.width/25, ratio*snake.width/25, 0)
        self.sight.pu()
        self.sight.speed(0)
        self.sight.goto(self.new_cor())
        Food.coords.append(self.sight.pos())
        self.sight.showturtle()

    def blink(self, delay=.5):
        """Makes the food blink"""
        if time.time() - self.last >= delay:
            self.sight.color('yellow')
            self.last = time.time()
        elif time.time() - self.last >= delay/2:
            self.sight.color('cyan')

    def new_cor(self):
        """Changes co-ordnates of the food"""
        x0, y0 = round(max_x/(2*border_width)), round((max_y/(2*border_width)))
        while True:
            x, y = (2*border_width)*randint(-x0, x0), (2*border_width)*randint(-y0, y0)
            if all([max(0, distance((x, y), i)-border_width/2) for i in self.snake.pos_list] +
                   [max(0, distance((x, y), i)-border_width/2) for i in Food.coords]): break
        return x, y

    def newfood(self):
        """creates new food"""
        self.sight.hideturtle()
        self.snake.eaten[0] += 1
        del Food.coords[Food.coords.index(self.sight.pos())]
        self.sight.goto(self.new_cor())
        Food.coords.append(self.sight.pos())
        self.sight.showturtle()

    def vanish(self):
        """Makes the food vanish"""
        del foods[foods.index(self)]
        self.sight.reset()
        self.sight.hideturtle()

    def decrease_life(self):
        """decreases the lifetime of the food
        Useful for the bigfoods to vanish"""
        self.lifetime -= (time.time()-self.timer)
        self.timer = time.time()
        if self.lifetime <= 0:
            self.vanish()
        if self.score != 1:
            self.score = max(int(2*Bigfood.score/Bigfood.lifetime),
                             int(self.lifetime*Bigfood.score/Bigfood.lifetime))


class Bigfood(Food):
    """A special kind of food object with finite lifetime and bigger points decreasing with time"""
    size_ratio = 1.5
    total = 0
    lifetime = 5
    score = 100

    def newfood(self):
        """Vanishes bigfood after the timer stops
        over-writes the function for Food"""
        self.vanish()
        self.snake.eaten[1] += 1


class Tictic():
    """creates a virtual timer in form of a turtle finishing a race"""
    lifetime = Bigfood.lifetime
    started = False
    def __init__(self):
        self.turt = turtle.Turtle(shape='turtle', visible=False)
        self.turt.pu()
        self.turt.goto(-15*border_width, -max_y-5*border_width)
        self.turt.pd()
        self.turt.color('lime')
        self.turt.width(border_width*1.5)
        self.turt.shapesize(border_width/5, border_width/5)

    def set(self):
        """resets the timer"""
        self.vanish()
        self.turt.seth(0)
        self.turt.fd(border_width*30)
        self.turt.lt(180)
        self.turt.color('red', 'orange')
        self.turt.showturtle()
        self.started = True
        self.timer = time.time()

    def run(self):
        """simulates the timer after it starts"""
        if self.started:
            self.lifetime -= (time.time()-self.timer)
            self.timer = time.time()
            self.turt.setx(-15*border_width+30*border_width*self.lifetime/Bigfood.lifetime)
            if self.lifetime <= 0: self.vanish()

    def vanish(self):
        """lets the timer vanish after time(i.e. when the turtle travels the whole distance)"""
        self.lifetime = Bigfood.lifetime
        self.started = False
        self.turt.hideturtle()
        self.turt.clear()
        self.turt.pu()
        self.turt.goto(-15*border_width, -max_y-5*border_width)
        self.turt.pd()
        self.turt.color('lime')
        self.turt.width(border_width*1.5)
        self.turt.shapesize(border_width/5, border_width/5)


class Obstacle:
    """Creates Obstacles for the snake depending on the mode of the game.
    If the snake hits any of them, it dies."""
    def __init__(self, Type='box'):
        if Type == 'box':
            self.brick = turtle.Turtle(visible=False)
            self.brick.pu()
            self.brick.color('red')
            self.brick.width(border_width)
            self.brick.speed(0)
            self.brick.goto(-(max_x+3*border_width/2), -(max_y+3*border_width/2))
            self.brick.pd()
            for _ in range(2):
                self.brick.fd(2*max_x+3*border_width)
                self.brick.lt(90)
                self.brick.fd(2*max_y+3*border_width+.1)
                self.brick.lt(90)



#lets mix-up OOP and functional programming
def pen():
    """Creates a pen that writes down texts"""
    t = turtle.Turtle(visible=False)
    t.color(['black', 'white'][wn.bgcolor() == 'black'])
    t.speed(0)
    t.pu()
    return t


def write_down(cords, pen, color, arg, move=False,
               align="left", font=("Arial", 8, "normal")):
    """writes down text with pen in the place, font and allignment as wanted"""
    pen.pu()
    pen.goto(*cords)
    pen.pd()
    pen.color(color)
    pen.write(arg, move, align, font)
    pen.pu()



# functions for initiating the screen
def screenOn(window_width=900, panel_ratio=1.616, night_mode=True):
    """Creates the turtle window and sets basic parameters"""
    global wn, border_width, max_x, max_y
    wn = turtle.Screen()
    wn.title("Snakes")
    wn.bgcolor(['white', 'black'][night_mode])
    wn.setup(width=window_width, height=window_width/panel_ratio)
    real_ratio, parts = (2, 1), 2*10   #parts must be divisible by 2
    xblocks, yblocks = real_ratio[0]*parts, real_ratio[1]*parts
    border_width = (wn.window_width()*(1-.1))/(2*xblocks)
    max_x, max_y = xblocks*border_width, yblocks*border_width
    wn.listen()
    constant_args()


def constant_args():
    """Writes down all the texts that would be constant to the board"""
    cpen = pen()
    write_down((wn.window_width()/2-6.8*border_width, -wn.window_height()/2+border_width),
               cpen, 'grey', '#Sarthack', font=("Arial", max(1, int(border_width)), "normal"))

    write_down((0, max_y+3*border_width), cpen, 'red', 'SNAKES',
               align='center', font=("Arial", int(3*border_width), "bold underline"))

    write_down((8*border_width, (max_y+3*border_width)), cpen, 'yellow', ' .py',
               align='left', font=("Arial", max(1, int(border_width)), "bold"))

    write_down((-wn.window_width()/2+border_width, -wn.window_height()/2+border_width),
               cpen, 'grey', "Press 'h' for help",
               font=("Arial", max(1, int(border_width)), "normal"))

    write_down((-max_x-1*border_width, (max_y+2.5*border_width)), cpen, 'lime', 'Snake Master:',
               align='left', font=("Arial", max(1, int(1.2*border_width)), "normal"))

    write_down((28*border_width, (max_y+2.5*border_width)), cpen, 'lime', 'Score:',
               font=("Arial", max(1, int(1.2*border_width)), "normal"))


def navigations(snake):
    """Sets up basic navigation system for key inputs"""
    wn.onkeypress(snake.up, 'Up')
    wn.onkeypress(snake.left, 'Left')
    wn.onkeypress(snake.down, 'Down')
    wn.onkeypress(snake.right, 'Right')
    wn.onkeypress(snake.up, 'w')
    wn.onkeypress(snake.left, 'a')
    wn.onkeypress(snake.down, 's')
    wn.onkeypress(snake.right, 'd')



#scores update
def update_score():
    """Updates the score-board each time the snakes eats a food"""
    global snake, scorer
    scorer.clear()
    write_down((max_x+1*border_width, (max_y+2*border_width)), scorer, 'Yellow',
               f'{snake.score:0=4d}', align='right',
               font=("Arial", max(1, int(2*border_width)), "bold"))


def update_highest(file, score):
    """Updates High scores after each game is over"""
    fin = open(file)
    prev = fin.read().strip('\n').split('\n')
    fin.close()
    tups = makeTups(prev)
    if  len(tups) < 5 or score > tups[-1][0]:
        name = wn.textinput("NEW HIGH SCORE", "Enter your name : ")
        if name in (None, ''): name = 'user'
        tups.append((score, '<'+name+'>'))
        tups.sort(reverse=True)
    fin = open(file, 'w')
    fin.write(makelist(tups))
    fin.close()
    highest_writer.clear()
    wn.listen()
    write_down((-23*border_width, (max_y+2.5*border_width)), highest_writer, 'gold',
               strHigh('snakes_highests.txt'), align='center',
               font=("Arial", max(1, int(1.5*border_width)), "bold"))


def makeTups(l):
    """makes tuples of highscore holders with their corresponding scores"""
    t = []
    if l == ['']: return t
    for i in l:
        for index in range(len(i)-1, -1, -1):
            if i[index] == ' ': break
        t.append((int(i[index+1:]), i[:index]))
    return t


def makelist(t):
    """makes list of strings to write down the high score holders in corresponding file"""
    l = list()
    for i in t[:5]:
        l.append(i[1]+' '+str(i[0]))
    return '\n'.join(l)


def strHigh(file, highest_only=True):
    """takes string form of high scores from the file
    if file doesn't exists creates one"""
    if exists(file): fin = open(file)
    else:
        fin = open(file, 'x')
        fin.close()
        return ''
    if highest_only:
        s = fin.readline().strip()
        if len(s) > 14:
            for index in range(len(s)-1, -1, -1):
                if s[index] == ' ': break
            s = s[:10-len(s)+index]+'...> '+s[index+1:]
    else: s = fin.read()
    fin.close()
    return s


def clear_records():
    """clears memory by deleting unnecessary records from the previous game"""
    global snake, foods, vpen
    snake.head.reset()
    (snake.score, snake.eaten)
    for food in foods: food.sight.reset()
    Bigfood.total = 0
    tic.vanish()
    vpen.clear()
    scorer.clear()



#main game
def newGame(paused=False):
    """The core structure of the game:
    Starts, pauses, resumes and restarts the game with key inputs"""
    try:
        global snake, foods, obs, vpen, started, pause, tic
        vpen.clear()
        scorer.clear()

        if (not started and not pause and paused) or\
           (started == pause == paused == False) or \
           (started and pause and not paused):
            """u started a new game after loosing last one
            or, this is ur first game
            or, u just restarted the game after pausing the previous game
                (pressed enter after space / h)"""

            started = True
            if pause:
                pause = False
                clear_records()
            del wn._turtles[5:]
            snake = Snake()
            foods = [Food(snake)]
            obs = Obstacle()
            navigations(snake)

        # to avoid restart if I accidentally press enter in the middle of a game
        elif not started or pause or not paused: return

        for food in foods: food.timer = time.time()# for not loosing bigfood
        tic.timer = time.time()# same for timer
        while not pause:
            wn.update()
            for food in foods: food.blink()
            snake.move()
            snake.eat(foods)
            if len(foods) == 1: tic.vanish()
            b, r = divmod(snake.eaten[0], 5)
            if r == 0 and b == 1+Bigfood.total:
                foods.append(Bigfood(snake, 1.5))
                Bigfood.total += 1
                tic.set()
            tic.run()
            update_score()
            for food in foods: food.decrease_life()
            if snake.dead():
                clear_records()
                write_down((0, 0), vpen, 'red', f'   YOU LOST\nYour Score: {snake.score}\n',
                           align='center', font=("Arial", max(1, int(3*border_width)), "normal"))
                write_down((0, 0), vpen, 'green', 'Hit Enter to Restart',
                           align='center', font=("Arial", max(1, int(1.5*border_width)), "normal"))
                started = False
                update_highest('snakes_highests.txt', snake.score)
                break
        if not started: return #returns when you die(to avoid being stuck on this func forever)

        turtle.mainloop()
        #if paused by any way, stops at the current situation
        #(flow of execution stays on this func forever)

    except Exception: pass #handles error when u leave the window


# button functions
def wait():
    """Pauses the game"""
    if started:
        global pause, vpen
        pause = not pause
        if pause:
            write_down((0, 5*border_width), vpen, 'orange', 'Paused\n',
                       align='center', font=("Arial", max(1, int(4*border_width)), "normal"))
            write_down((0, 0), vpen, 'green', 'Press space to continue\n',
                       align='center', font=("Arial", max(1, int(2*border_width)), "normal"))
            write_down((0, -2*border_width), vpen, 'orange', 'Press Enter to restart\n',
                       align='center', font=("Arial", max(1, int(1.5*border_width)), "normal"))
        else:
            newGame(True)


def Help():
    """Pauses a current game to show the controls and features"""
    global pause, vpen, started
    vpen.clear()
    if started: pause = True
    write_down((0, 14*border_width), vpen, 'aqua', 'HELP',
               align='center', font=("Arial", max(1, int(3*border_width)), "bold underline"))
    write_down((0, -15*border_width), vpen, 'orange',
               ("'Up' or 'w' to face the snake North    'Down' or 's' to face the snake South"+\
                "\n\n'Left' or 'a' to face the snake West      'Right' or 'd' to face the snake East"+\
                "\n\n'space' to pause / continue the game"+' '*14+"'enter' to start a new game"+\
                "\n\n'p' to see all High Scores"+' '*17+"'SHIFT' + 'r' to reset the High Scores"+\
                "\n\nPress 'm' for sound on/off"+' '*19+"Press 'b' to turn night mode on/off"),
               align='center', font=("Arial", max(1, int(1.8*border_width)), "normal"))


def highScores():
    """Writes down the High Scores after pressing 'p'
    """
    global pause, vpen, started
    vpen.clear()
    if started: pause = True
    write_down((0*border_width, 8*border_width), vpen, 'purple', 'All High Scores:',
               align='right', font=("Arial", max(1, int(2.5*border_width)), "bold underline"))
    write_down((0*border_width, -10*border_width), vpen, 'cyan', strHigh('snakes_highests.txt', 0),
               align='center', font=("Arial", max(1, int(2*border_width)), "normal"))


def nightMode():
    """Changes Background to black or white"""
    wn.bgcolor(['white', 'black'][wn.bgcolor() == 'white'])


def reSet():
    """resets all high scores"""
    fin = open('snakes_highests.txt', 'w')
    fin.close()
    highest_writer.clear()
    write_down((-12*border_width, (max_y+2.5*border_width)), highest_writer, 'gold',
               strHigh('snakes_highests.txt'), align='right',
               font=("Arial", max(1, int(2*border_width)), "bold"))


def muSic():
    """controls music allowance"""
    global music
    music = not music
    if music: winsound.PlaySound('beep.wav', winsound.SND_ASYNC)



# __main__ starts Here On:
#initializing the screen
screenOn(window_width=900)
wn.tracer(0)

#create pens
vpen = pen()
scorer = pen()
highest_writer = pen()

#initialize the variables
pause = False
started = False
music = True

#write down initial values of
write_down((0, 0), vpen, 'green', 'Hit enter to Start',
           align='center', font=("Arial", max(1, int(3*border_width)), "normal"))

write_down((-23*border_width, (max_y+2.5*border_width)), highest_writer, 'gold',
           strHigh('snakes_highests.txt'), align='center',
           font=("Arial", max(1, int(1.5*border_width)), "bold"))

tic = Tictic()

#create button responses
wn.onkeypress(newGame, 'Return')
wn.onkeypress(wait, 'space')
wn.onkeypress(Help, 'h')
wn.onkeypress(highScores, 'p')
wn.onkeypress(nightMode, 'b')
wn.onkeypress(reSet, 'R')
wn.onkeypress(muSic, 'm')

#end up in mainloop
turtle.mainloop()