import pygame
import keyboard

pygame.init()

class Collor:
    def __init__(self):
        pass


    def SET_COL(self,collor=[]):
        return collor
    
    def COL_BOT(self,collor1=[],collor2=[]):
        collor=[]
        collor.append((collor1[0]+collor2[0])/2);collor.append((collor1[1]+collor2[1])/2);collor.append((collor1[2]+collor2[2])/2)
        return collor
class MOuse:
    def __init__(self):
        pass
    def GetPos(self):
        pos = pygame.mouse.get_pos()
        return pos
    def GET_PRESS_s(self,but=""):
        pr = pygame.mouse.get_pressed()
        if but == "l":
            return pr[0]
        elif but == "r":
            return pr[2]
        elif but == "m":
            print(pr)
            return pr[1]
class KB0rd:
    def __init__(self):
        pass
    def On_kee_press(self,key=""):
        on = keyboard.is_pressed(key)
        return on
class GRP:
    def __init__(self,win_w,win_h):
        global screen
        self.win_w = win_w
        self.win_h = win_h
        pygame.init()
        pygame.mixer.init()
        pygame.display.init()
        self.clock = pygame.time.Clock()
        screen = pygame.display.set_mode((win_w,win_h))
        self.screen = screen

    def set_fps(self,fps):
        self.clock.tick(fps)

    def close(self,running=True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        return running 
    
    def update(self,col = (0,0,0)):
        pygame.display.flip()
        self.screen.fill(col)


    class draw:
        def __init__(self,):
            pass

        def dravrect(col=(),x=0,y=0,width=0,height=0):
                pygame.draw.rect   (screen, 
                                        col, 
                                        (x,y,width,height))

        def dravcircle(col=(),x=0,y=0,rad=0,sh=0):
                pygame.draw.circle (screen,
                                        col,
                                        (x,y),
                                        rad,
                                        sh)
                                
        def dravellips(col=(),x=0,y=0,width=0,height=0):
                pygame.draw.ellipse(screen,
                                        col,
                                        (x,y,width,height))

        def dravtringl(col=(),pos1=[],pos2=[],pos3=[],sh=0):
                pygame.draw.polygon(screen,
                                        col,
                                        [(pos1[0],pos1[1]),(pos2[0],pos2[1]),(pos3[0],pos3[1])],
                                        sh)

        def dravline(col=(),start_pos=[],end_pos=[],sh=0):
                pygame.draw.line(   screen,
                                        col,
                                        (start_pos[0],start_pos[1]),
                                        (end_pos[0],end_pos[1]),
                                        sh)
        def dravliness(col=(),points=(),ZAMKNT=False,sh=0):
                pygame.draw.lines(  screen,
                                        col,
                                        ZAMKNT,
                                        points,
                                        sh)