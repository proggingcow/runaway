import pygame,math
pygame.font.init()


from enum import Enum

cow_img = pygame.image.load("assets/cowontherun.png")


class MenuJob(Enum):
    quit = 0
    play = 1


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
    def __init__(self,x,y,col,speedx,speedy):
        self.r = pygame.Rect(x,y,100,100)
        self.col = col
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
        super().__init__(x,y,(0,0,0),3,3)
        self.r = cow_img.get_rect()
        self.r = self.r.move(100,400)



    def time_step(self, world):
        self.move(self.speedx,self.speedy)
        if self.r.right > world.width: self.speedx = self.speedx * -1
        if self.r.left < 0: self.speedx = self.speedx * -1
        if self.r.bottom > world.width: self.speedy = self.speedy * -1
        if self.r.top < 0: self.speedy =  self.speedy * -1

    def draw(self,screen):

        screen.blit(cow_img,self.r)



class World:
    def __init__(self,width,hight):
        self.width = width
        self.hight = hight


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




def game():
    wor = World(500,500)
    obs = [MyOb(30,30,(0,0,0),1,3), MyOb(0,100,(155,255,0),2,2),MyOb(300,0,(255,0,0),3,2)]
    me = Person(400,400)
    pause = False
    score = 0
    HP = 3
    invun = 0

    run = True
    while run:
        pygame.time.delay(50)
        if not pause:
            score += 0.05
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

        # timestep

        for ob in obs:
            ob.time_step(wor)

        me.time_step(wor)

        # draw stuff
        screen.fill((132,245,56))
        for ob in obs:
            ob.draw(screen)
        me.draw(screen)
        message_display(screen,"score = {}  HP = {}".format(math.floor(score),HP),'unbatimato')


        pygame.display.flip()
        if invun >0:
            invun -=1
            continue


        #kill
        for ob in obs:
            kill = overlap(me.r,ob.r)
            if kill:
                HP = HP -1
                me.speedx *= -1
                me.speedy *= -1
                invun = 100
            if HP == 0:
                return score

def menu(score,highscore):
    screen_image = pygame.image.load("assets/menu_screen.png")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Checks if the red button in the corner of the window is clicked
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return MenuJob.quit
                elif event.key == pygame.K_p:
                    return MenuJob.play
        #Do drawings
        screen.blit(screen_image,(0,0))
        if score > 100:
            a="You win!"
        else:
            a = " "
        if not score == 0:
            message_display(screen,"Game Over! Score:{}    {}".format(math.floor(score),a),'Scratched Letters.ttf')
            message_display(screen,"                                         Hiscore:{}".format(math.floor(highscore)),'unbatimato')
        pygame.display.flip()


def main():
    score = 0
    highscore = 0
    while True:
        if menu(score,highscore) == MenuJob.play:
            #PLay the game
            score = game()
            if score > highscore:
                highscore = score
        else:
            return


main()
