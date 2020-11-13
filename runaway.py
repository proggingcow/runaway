#! /bin/python3
import pygame,math,pickle
from random import randrange
pygame.font.init()
#r,g,b

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

    def draw(self,screen):
        pygame.draw.rect(screen,self.col,self.r)

    def time_step(self, world):
        self.move(self.speedx,self.speedy)
        if self.r.right > world.width: self.speedx = self.speedx * -1
        if self.r.left < 0: self.speedx = self.speedx * -1
        if self.r.bottom > world.width: self.speedy = self.speedy * -1
        if self.r.top < 0: self.speedy =  self.speedy * -1

    def move(self,x,y):
        self.r = self.r.move(x,y)

class Person(MyOb):
    def __init__(self,x,y):
        super().__init__(x,y,3,3)
        self.r = pic_cow_run.get_rect()
        self.r = self.r.move(100,400)
        self.col = (155,0,0)
        self.invun = 0


    def draw(self,screen):
        if self.invun > 0:
            screen.blit(pic_cow_hurt,self.r)
        else:
            screen.blit(pic_cow_run,self.r)

class Butcher(MyOb):
    def __init__(self,x,y,speedx,speedy):
        super().__init__(x,y,speedx,speedy)
        self.r = pic_butcher.get_rect().move(x,y)


    def draw(self,screen):
        screen.blit(pic_butcher,self.r)






class World:
    def __init__(self,width,hight):
        self.width = width
        self.hight = hight
    def draw(self,screen):
        screen.blit(background,(0,0))


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
                    if event.type == pygame.QUIT: # Checks if the red button in the corner of the window is clicked
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        swichinue = not swichinue

def game():
    wor = World(500,500)
    obs = [Butcher(30,30,1,3), Butcher(0,100,2,2),Butcher(300,0,3,2)]
    me = Person(400,400)
    pause = False
    score = 0
    HP = 3
    invun = 0
    tbne = 100
    run = True
    while run:
        pygame.time.delay(50)


        if not pause:
            score += 0.05
            tbne -= 0.5
        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Checks if the red button in the corner of the window is clicked
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_q:
                    pygame.quit()
                if event.key == pygame.K_SPACE:
                    pause = not pause
                    if pause:
                        continue
            if event.type == pygame.KEYDOWN:
                dx,dy = 0,0
                if event.key == pygame.K_q:
                    return 0
                elif event.key == pygame.K_DOWN:
                    dy = 6
                elif event.key == pygame.K_UP:
                    dy = -6
                elif event.key == pygame.K_LEFT:
                    dx = -6
                elif event.key == pygame.K_RIGHT:
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
        if tbne <= 0:
            obs = obs + [Butcher(randrange(1,30),randrange(1,30),randrange(1,3),randrange(1,3))]
            tbne = 100
        # timestep

        for ob in obs:
            ob.time_step(wor)

        me.time_step(wor)

        # draw stuff
        wor.draw(screen)
        for ob in obs:
            ob.draw(screen)
        me.draw(screen)
        message_display(screen,"score = {}  HP = {}".format(math.floor(score),HP),'unbatimato')


        pygame.display.flip()
        if me.invun >0:
            me.invun -=1
            continue


        #kill
        for ob in obs:
            kill = overlap(me.r,ob.r)
            if kill:
                HP = HP -1
                me.invun = 100
            if HP == 0:
                return score

def menu(score,highscore):
    screen_image = pygame.image.load("assets/menu_screen.png")
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
        #Do drawings
        screen.blit(screen_image,(0,0))
        if score > 100:
            a="Well Done"
        else:
            a = " "
        if score > 0:
            message_display(screen,"Game Over! Score:{}   Highscore:{}   {}".format(math.floor(score),math.floor(highscore),a),'Scratched Letters.ttf')
        elif highscore > 0:
            message_display(screen,"Highscore:{}".format(math.floor(highscore)),'Scratched Letters.ttf')

        pygame.display.flip()


def main():
    score = 0
    highscore = 0
    try:
        with open("highscore.txt",'rb')as f:
            [highscore] = pickle.load(f)
    except:
        pass
    while True:
        job = menu(score,highscore)
        if  job == MenuJob.play:
            #PLay the game
            score = game()
            if score > highscore:
                highscore = score
                with open("highscore.txt",'wb')as f:
                    pickle.dump([highscore],f,protocol=2)
        elif job == MenuJob.story:
            print("Story")
            story()
        else:
            return


main()
