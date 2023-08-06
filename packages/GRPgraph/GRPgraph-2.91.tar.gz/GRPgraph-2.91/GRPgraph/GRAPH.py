import pygame
import keyboard
import math
import time

pygame.init()
class TimeGR:
    def __init__(self):
        pass
    def DELY(self,MLsec):
        time.sleep(MLsec)
class FonT:
    def __init__(self):
        pass
    def GETFONTS():
        return pygame.font.get_fonts()

    def PRINText(self,text='',glass=False,col=(),font='arial',pix=0,x=0,y=0):
        textt = pygame.font.SysFont(font,pix)
        texttt = textt.render(text,glass,col)
        screen.blit(texttt,(x,y))
class GPMath:
    def __init__(self):
        pass
    def COS(self,ugl):
        return math.cos(ugl)
    def SIN(self,ugl):
        return math.sin(ugl)
    
    def RAST(self,pos1=[],pos2=[]):
        if pos1[0]>pos2[0]:w = pos1[0]-pos2[0]
        else:              w = pos2[0]-pos1[0]
        if pos1[1]>pos2[1]:h = pos1[1]-pos2[1]
        else:              h = pos2[1]-pos1[1]
        dl = math.sqrt(w*w+h*h)
        return dl

    def RAST_CENT(self,rect1 = [],rect2 = []):
        if rect1[4][0]>rect2[4][0]:w = rect1[4][0]-rect2[4][0]
        else:              w = rect2[4][0]-rect1[4][0]
        if rect1[4][1]>rect2[4][1]:h = rect1[4][1]-rect2[4][1]
        else:              h = rect2[4][1]-rect1[4][1]
        dl = math.sqrt(w*w+h*h)
        return dl      
class Collor:
    def __init__(self):
        pass
    class GetCOL:
        def GET_CL_RED(collor=[]):return collor[0]

        def GET_CL_GRN(collor=[]):return collor[1]

        def GET_CL_BLU(collor=[]):return collor[2]

        def GET_CL_RGB(collor=[]):
            if collor[0]<127 and collor[1]<127 and collor[2]>127:
                col = "blue"
            elif collor[0]>127 and collor[1]<127 and collor[2]<127:
                col = "red"
            elif collor[0]<127 and collor[1]>127 and collor[2]<127:
                col = "green"
            elif collor[0]==0 and collor[1]==0 and collor[2]==0:
                col = "black"
            elif collor[0]==255 and collor[1]==255 and collor[2]==255:
                col = "white"  
            return col

    def SET_COL(self,collor=[]):return collor
    
    def COL_BOT(self,collor1=[],collor2=[]):
        collor=[]
        collor.append((collor1[0]+collor2[0])/2);collor.append((collor1[1]+collor2[1])/2);collor.append((collor1[2]+collor2[2])/2)
        return collor
class MOuse:
    def __init__(self):
        pass
    def GET_Pos(self):
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
    def SET_VIz(self,viz):
        pygame.mouse.set_visible(viz)
    def GET_VIz(self):
        viz = pygame.mouse.get_visible()
        return viz
    def SET_pos(self,pos=[]):
        pygame.mouse.set_pos([pos[0],pos[1]])
class KB0rd:
    def __init__(self):
        pass
    def On_kee_press(self,key=""):
        on = keyboard.is_pressed(key)
        return on
class WinHOW:


    def __init__(self,win_w,win_h):
        global screen,clock
        self.win_w = win_w
        self.win_h = win_h
        pygame.init()
        pygame.mixer.init()
        pygame.display.init()
        pygame.font.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((win_w,win_h))
        self.screen = screen
        self.clock = clock



    def get_color(self,x,y):
        col = screen.get_at([x,y])
        col1 = [col[0],col[1],col[2]]
        return col1

    def get_center(self):
        xc = self.win_w/2
        yc = self.win_h/2
        return xc , yc

    def set_fps(self,fps):
        if fps == "MAX":
            fps = 1000
        if fps == "MIN":
            fps = 30
        self.clock.tick(fps)

    def get_fps(self):return int(self.clock.get_fps())

    def close(self,running=True):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        return running 
    
    def update(self,col = (0,0,0)):
        pygame.display.flip()
        self.screen.fill(col)




    class draw2D:
        def __init__(self,):
            pass
        def dravrect(col=(),x=0,y=0,width=0,height=0,sh=0):
                rect = pygame.Rect(x,y,width,height)
                pygame.draw.rect   (screen, 
                                        col, 
                                        rect,
                                        sh)
                center =  [x + width/2,y+height/2]
                rectt = [x,y,width,height,center,col,sh]
                return rectt

        def dravcircle(col=(),x=0,y=0,rad=0,sh=0):
                pygame.draw.circle (screen,
                                        col,
                                        (x,y),
                                        rad,
                                        sh)
                center = [x,y]
                rectt = [x,y,rad,col,center,sh]
                return rectt
                         
        def dravellips(col=(),x=0,y=0,width=0,height=0,sh=0):
                rect = pygame.Rect(x,y,width,height)
                pygame.draw.ellipse(screen,
                                        col,
                                        rect,
                                        sh)
                center =  [x + width/2,y+height/2]
                rectt = [x,y,width,height,center,col,sh]
                return rectt

        def dravtringl(col=(),pos1=[],pos2=[],pos3=[],sh=0):
                pygame.draw.polygon(screen,
                                        col,
                                        [(pos1[0],pos1[1]),(pos2[0],pos2[1]),(pos3[0],pos3[1])],
                                        sh)
                rectt = [pos1,pos2,pos3,col,sh]
                return rectt

        def dravline(col=(),start_pos=[],end_pos=[],sh=1):
                pygame.draw.line(   screen,
                                        col,
                                        (start_pos[0],start_pos[1]),
                                        (end_pos[0],end_pos[1]),
                                        sh)
                xcnt = start_pos[0]+(end_pos[0]-start_pos[0])/2
                ycnt = start_pos[1]+(end_pos[1]-start_pos[1])/2
                center = [xcnt,ycnt]
                rectt = [start_pos,end_pos,col,sh,center]
                return rectt

        def dravliness(col=(),points=(),ZAMKNT=False,sh=1):
                pygame.draw.lines(  screen,
                                        col,
                                        ZAMKNT,
                                        points,
                                        sh)
                rectt = [points,col,ZAMKNT,sh]
                return rectt

        def dravpixel(col=(),pos=[],sh=1):
                pygame.draw.line(   screen,
                                        col,
                                        (pos[0],pos[1]),
                                        (pos[0],pos[1]),
                                        sh)
class IMG:
    def __init__(self):
        pass
    def loadIMG(file=''):
        imgg = pygame.image.load(file)
        return imgg

    def DrawIMG(pos=[],iimmgg=0):
        
        rect = iimmgg.get_rect(bottomright=(pos[0]+iimmgg.get_width(),
                                            pos[1]+iimmgg.get_height())) 
        screen.blit(iimmgg,rect)
        return rect

    def IMGScale(pov,width,height):
        tid = pygame.transform.scale(pov,(width,height))
        return tid