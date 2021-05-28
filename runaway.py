#! /bin/python3
import pygame,math,pickle,random
from random import randrange
pygame.font.init()
pygame.time.delay(100)
print("booting system")
pygame.time.delay(900)

from enum import Enum

pic1=pygame.image.load("assets/story_pic_1.png")
pic2=pygame.image.load("assets/story_pic_2.png")
pic3=pygame.image.load("assets/story_pic_3.png")
pic4=pygame.image.load("assets/story_pic_4.png")
pic5=pygame.image.load("assets/story_pic_5.png")
pic_cow_run = pygame.image.load("assets/cowontherun.png")
pic_cow_hurt =pygame.image.load("assets/hurtcowontherun.png")
pic_butcher= pygame.image.load("assets/butcher.png")
background = pygame.image.load("assets/background.png")
PMage = pygame.image.load("assets/mage.png")
PPuddle = pygame.image.load("assets/puddle.png")
LA = pygame.image.load("assets/LArrow.png")
RA = pygame.image.load("assets/RArrow.png")
UA = pygame.image.load("assets/UArrow.png")
DA = pygame.image.load("assets/DArrow.png")
arch = pygame.image.load("assets/archer.png")
CP = pygame.image.load("assets/coin.png")
CP = pygame.transform.scale(CP,(20,20))
#Menu Job is used to decide where to go when menu closes
class MenuJob(Enum):
    quit = 0
    play = 1
    story = 2


def overlap(a,b):
    if a.left > b.right:
        return False
    if a.top > b.bottom:
        return False
    if b.left > a.right:
        return False
    if b.top > a.bottom:
        return False

    return True

class MyOb:
    def __init__(self,x,y,speedx,speedy):
        self.r = pygame.Rect(x,y,100,100)
        self.speedx = speedx
        self.speedy = speedy
        self.col = (0,0,0)
        self.dead = False

    def draw(self,screen):
        pygame.draw.rect(screen,self.col,self.r)

    def time_step(self, world):
        self.move(self.speedx,self.speedy)
        if self.r.right > world.width: self.speedx =abs(self.speedx) * -1
        if self.r.left < 0: self.speedx =abs(self.speedx)
        if self.r.bottom > world.width: self.speedy =abs(self.speedy)*-1
        if self.r.top <0:self.speedy=abs(self.speedy)

    def move(self,x,y):
        self.r = self.r.move(x,y)

class Person(MyOb):
    def __init__(self,x,y):
        super().__init__(x,y,3,3)
        self.r = pic_cow_run.get_rect()
        self.r = self.r.move(100,400)
        self.col = (155,0,0)
        self.invun = 0
        self.HP = 3

    def draw(self,screen):
        if self.invun > 0:
            screen.blit(pic_cow_hurt,self.r)
        else:
            screen.blit(pic_cow_run,self.r)

class Arrow(MyOb):
    def __init__(self,pos,direction):
        self.pos = pos
        if direction <1.5:
            self.pic = LA
        elif direction <2.5:
            self.pic = RA
        elif direction <3.5:
            self.pic = UA
        elif direction <4.5:
            self.pic = DA

class Puddle(MyOb):
    def __init__(self,x,y):
        super().__init__(x,y,0,0)
        self.pic = PPuddle
        self.x = x
        self.y = y
        self.r = self.pic.get_rect().move(x,y)
        self.tp = "p"
        self.lt = 20

    def time_step(self,world):
        self.lt -=0.05
        if self.lt <= 0:
            self.dead = True

    def draw(self,screen):
        screen.blit(self.pic,self.r)
class Mage(MyOb):
    def __init__(self,pic,x,y,speedx,speedy):
        super().__init__(x,y,speedx,speedy)
        self.pic = pic
        self.r = pic.get_rect().move(x,y)
        self.tp ="m"

    def draw(self,screen):
        screen.blit(self.pic,self.r)

    def pour(self,obs):

        c = randrange(1,500)
        if c < 3.5:
            obs.append(Puddle(self.r.x,self.r.y))

class Butcher(MyOb):
    def __init__(self,x,y,speedx,speedy):
        super().__init__(x,y,speedx,speedy)
        self.r = pic_butcher.get_rect().move(x,y)
        self.tp = "b"


    def draw(self,screen):
        self.invun = 0
        self.HP = 3
        screen.blit(pic_butcher,self.r)

class World:
    def __init__(self,width,hight):
        self.width = width
        self.hight = hight
        self.score = 0
        self.obs = []
    def draw(self,screen):
        screen.blit(background,(0,0))

class Coin:
    def __init__(self,x,y):
        self.r = CP.get_rect().move(x,y)
        self.pic = CP
        self.tp = "c"
        self.dead = False
        self.tbd = 100

    def draw(self,screen):
        screen.blit(self.pic,self.r)

    def time_step(self,it):
        self.tbd -= 1
        if self.tbd < 0.5:
            self.dead = True
        pass
def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def message_display(screen,text,font):

    largeText = pygame.font.SysFont(font,20)
    TextSurf, TextRect = text_objects(text, largeText)
    #TextRect.center = ((display_width/2),(display_height/2))
    screen.blit(TextSurf, TextRect)







#  Initial setup
screen =  pygame.display.set_mode((500,500))
pygame.display.set_caption("runaway")

def story():
        piclist = [pic1,pic2,pic3,pic4,pic5]
        for pic in piclist:
            screen.blit(pic,(0,0))
            pygame.display.flip()
            swichinue = True
            while swichinue:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        swichinue = not swichinue
def game():
    wor = World(500,500)
    n = 3

    while n > 0.5:
        c = randrange(0.0,3.0)
        if c > 1.3:
            wor.obs += [Butcher(randrange(1,300),randrange(1,300),randrange(1,3),randrange(1,3))]
        else:
            wor.obs += [Mage(PMage,randrange(1,300),randrange(1,300),randrange(1,3),randrange(1,3))]
        n -= 1
    me = Person(400,400)
    pause = False
    second = 0
    HP = 3
    invun = 0
    tbne = 100.5

    while True:
        pygame.time.delay(50)


        if not pause:
            second += 0.05
            wor.score += 0.05
            tbne -= 0.5
            for ob in wor.obs:
                #score depleter
                if overlap(me.r,ob.r) and ob.tp != "c":wor.score -= 0.1
            if me.speedy>5 or me.speedy<-5:wor.score -= 0.1
            if me.speedx>5 or me.speedx<-5:wor.score -= 0.1

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Checks if the red button in the corner of the window is clicked
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_q:
                    return wor.score
                if event.key == pygame.K_SPACE:
                    pause = not pause
            if event.type == pygame.KEYDOWN:
                dx,dy = 0,0
                if event.key == pygame.K_q:
                    return 0
                if event.key == pygame.K_DOWN:
                    dy = 6
                if event.key == pygame.K_UP:
                    dy = -6
                if event.key == pygame.K_LEFT:
                    dx = -6
                if event.key == pygame.K_RIGHT:
                    dx = 6
                me.speedx += dx
                me.speedy += dy
                if me.speedx > 9:
                    me.speedx = 9
                if me.speedy > 9:
                    me.speedy = 9
                if me.speedx < -9:
                    me.speedx = -9
                if me.speedy < -9:
                    me.speedy = -9
        if not pause:
            if tbne <= 0:
                choose = randrange(0,10)
                if 3.5 < choose < 4.5:
                    wor.obs += [Mage(PMage,randrange(1,30),randrange(1,30),randrange(1,3),randrange(1,3))]
                else:
                    wor.obs += [Butcher(randrange(1,30),randrange(1,30),randrange(1,3),randrange(1,3))]
                tbne = 100.5
            coinadd = random.randint(1,40)
            if coinadd <1.5:
                wor.obs += [Coin(random.randint(1,480),random.randint(1,480))]
            timestep_game(me,wor)
            if me.HP == 0:
                return wor.score
        draw_game(me,wor,pause)

def draw_game(me,wor,pause):
    # draw stuff
    wor.draw(screen)
    for ob in wor.obs:
        ob.draw(screen)
    me.draw(screen)
    if not pause:message_display(screen,"score = {}  HP = {}".format(math.floor(wor.score),me.HP),'unbatimato')
    else:message_display(screen,"score = {}  HP = {}  Paused  speed = {},{}".format(math.floor(wor.score),me.HP,me.speedx,-me.speedy),'unbatimato')
    pygame.display.flip()

def timestep_game(me,wor):
    for ob in wor.obs:
        ob.time_step(wor)

    me.time_step(wor)


            #ps

    for ob_a in wor.obs:
        tp_a = ob_a.tp
        if tp_a == "p" or tp_a == "c":
            for ob_b in wor.obs:
                if overlap(ob_a.r,ob_b.r):
                    if ob_a.tp == "p" and ( ob_b.tp == "b" or ob_b.tp =="c"):
                        ob_b.dead = True
                        ob_a.dead = True
                    if ob_a.tp == "c" and ob_b.tp != "c":
                        ob_a.dead = True

        elif tp_a == "m":
            ob_a.pour(wor.obs)

    #kill Objects
    wor.obs = [x for x in wor.obs if not x.dead ]


    if me.invun >0:
        me.invun -=1

    #kill me
    for ob in wor.obs:
        if overlap(me.r,ob.r):
            if ob.tp == "c":
                ob.dead= True
                wor.score += 5
            elif me.invun <= 0:
                me.HP = me.HP -1
                if ob.tp == "p":ob.dead = True
                me.invun = 100
    return

def menu(score,highscore,new):
    screen_image = pygame.image.load("assets/menu_screen.png")
    if new == True:new = "New highscore!"
    else:new = " "
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return MenuJob.quit
                elif event.key == pygame.K_p:
                    return MenuJob.play
                elif event.key ==pygame.K_s:
                    return MenuJob.story
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pygame.Rect(0,0,283,40).collidepoint(pos):
                    return MenuJob.story
                elif pygame.Rect(63,400,437,100).collidepoint(pos):
                    return MenuJob.quit
                elif pygame.Rect(103,49,335,49).collidepoint(pos):
                        return MenuJob.play
        #Do drawings
        screen.blit(screen_image,(0,0))
        if score > 100:
            a="Well Done"
        else:
            a = " "
        if score != False:
            message_display(screen,"Game Over! Score:{}   Highscore:{} {}  {}".format(math.floor(score),math.floor(highscore),a,new),'Scratched Letters.ttf')
        else:
            message_display(screen,"Highscore:{}".format(math.floor(highscore)),'Scratched Letters.ttf')

        pygame.display.flip()


def main():
    score = False
    new = False
    try:
        with open("highscore.txt",'rb')as f:
            [highscore] = pickle.load(f)
    except:
        highscore = 0
    while True:
        job = menu(score,highscore,new)
        if  job == MenuJob.play:
            #PLay the game
            score = game()
            if score > highscore:
                highscore = score
                new = True
                with open("highscore.txt",'wb')as f:
                    pickle.dump([highscore],f,protocol=2)
            else:new = False
        elif job == MenuJob.story:
            print("Story")
            story()
            new = False
        else:
            new = False
            return


main()
