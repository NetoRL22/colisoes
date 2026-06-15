import fisica
import pygame
import ga

projPos = []
projR = []
ordem = None
clock = None
screen = None
scCenter = None
font = None

def setup():
    global projPos,projR,ordem,clock,screen,scCenter,font
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((fisica.w, fisica.h)) ## NO FILL ???
    pygame.display.set_caption("Pygame Game Loop")
    scCenter = [fisica.w/2,fisica.h/2,0]
    font=pygame.font.SysFont("Arial",20)

def projetaPosicoes():
    global projPos,projR,ordem,clock,screen,scCenter
    if(fisica.threeD):
        projPos=[]
        for i in range(fisica.nBolas):
            projPos.append(projetaNaTela(fisica.pos[i]))
    else:
        projPos = fisica.pos

def projetaRaios():
    global projPos,projR,ordem,clock,screen,scCenter
    if(fisica.threeD):
        projR=[]
        for i in range(fisica.nBolas):
            projR.append(fisica.r[i]*(fisica.camD/(fisica.camD+fisica.pos[i][2])))
    else:
        projR = fisica.r

def projetaNaTela(vetor):
    global projPos,projR,ordem,clock,screen,scCenter
    r=ga.diferenca(vetor,ga.soma(scCenter,[0,0,vetor[2]]))
    r=ga.produto_escalar(fisica.camD/(fisica.camD+vetor[2]),r)
    r=ga.soma(r,scCenter)
    del r[-1]
    return r

def ordenaRend():
    global projPos,projR,ordem,clock,screen
    ordem=[]
    if(fisica.threeD):
        for i in range(fisica.nBolas):
            maior=0
            aux=-1
            for j in range(fisica.nBolas):
                if(fisica.pos[j][2]>maior and j not in ordem):
                    aux=j
                    maior=fisica.pos[j][2]
                ordem.append(aux)

    else:
        for i in range(fisica.nBolas):
            ordem.append(i)

def desenhaQuinas():
    global projPos,projR,ordem,clock,screen
    a = projetaNaTela([0,0,fisica.l])
    b = projetaNaTela([fisica.w,0,fisica.l])
    c = projetaNaTela([0,fisica.h,fisica.l])
    d = projetaNaTela([fisica.w,fisica.h,fisica.l])
    pygame.draw.line(screen,(50,50,50),(0,0),a,5)
    pygame.draw.line(screen,(50,50,50),(fisica.w,0),b,5)
    pygame.draw.line(screen,(50,50,50),(0,fisica.h),c,5)
    pygame.draw.line(screen,(50,50,50),(fisica.w,fisica.h),d,5)
    pygame.draw.line(screen,(50,50,50),a,b,5)
    pygame.draw.line(screen,(50,50,50),a,c,5)
    pygame.draw.line(screen,(50,50,50),b,d,5)
    pygame.draw.line(screen,(50,50,50),c,d,5)


def desenhaBolas():
    global projPos,projR,ordem,clock,screen,scCenter
    for i in ordem:
        if(fisica.threeD):
            pygame.draw.line(screen,(25,70,25),(projPos[i][0],projPos[i][1]),projetaNaTela([fisica.pos[i][0],fisica.pos[i][1],fisica.l]),3)
            if(fisica.pos[i][0]<scCenter[0]):
                x=0
            else:
                x=fisica.w
            if(fisica.pos[i][1]<scCenter[1]):
                y=0
            else:
                y=fisica.h
            pygame.draw.line(screen,(70,25,25),(projPos[i][0],projPos[i][1]),projetaNaTela([x,fisica.pos[i][1],fisica.pos[i][2]]),3)
            pygame.draw.line(screen,(25,25,70),(projPos[i][0],projPos[i][1]),projetaNaTela([fisica.pos[i][0],y,fisica.pos[i][2]]),3)
    
        pygame.draw.circle(screen,(fisica.cor[i][0],fisica.cor[i][1],fisica.cor[i][2]),(projPos[i][0],projPos[i][1]),projR[i])
        pygame.draw.circle(screen,(255,255,255),(projPos[i][0],projPos[i][1]),projR[i],2)

        if(fisica.threeD):
            pygame.draw.line(screen,(25,70,25),projetaNaTela([fisica.pos[i][0],fisica.pos[i][1],fisica.pos[i][2]-fisica.r[i]]),projetaNaTela([fisica.pos[i][0],fisica.pos[i][1],0]),3)
            if(fisica.pos[i][0]<scCenter[0]):
                dirXr=1
            else:
                dirXr=-1
            if(fisica.pos[i][1]<scCenter[1]):
                dirYr=1
            else:
                dirYr=-1
            pygame.draw.line(screen,(70,25,25),projetaNaTela([fisica.pos[i][0]+(dirXr*fisica.r[i]),fisica.pos[i][1],fisica.pos[i][2]]),projetaNaTela([fisica.w-x,fisica.pos[i][1],fisica.pos[i][2]]),3)
            pygame.draw.line(screen,(25,25,70),projetaNaTela([fisica.pos[i][0],fisica.pos[i][1]+(dirYr*fisica.r[i]),fisica.pos[i][2]]),projetaNaTela([fisica.pos[i][0],fisica.h-y,fisica.pos[i][2]]),3)

       #     pygame.draw.ellipse(screen,(fisica.cor[i][0],fisica.cor[i][1],fisica.cor[i][2]),???,2)
       #     pygame.draw.circle(screen,(fisica.cor[i][0]/1.2,fisica.cor[i][1]/1.2,fisica.cor[i][2]/1.2),(projPos[i][0],projPos[i][1]),projR[i]*2/3,2)

def printaStats():
    global projPos,projR,ordem,clock,screen,scCenter,font
    surface = font.render("Olá, Pygame!", True, (255, 255, 255))
    surface = font.render("Cinética Total = " + str(round(fisica.k,1)),True,(255,255,180))
    screen.blit(surface,(10,10))
    surface = font.render("Potencial Gravitacional Total = " + str(round(fisica.u,1)),True,(255,255,180))
    screen.blit(surface,(10,35))
    surface = font.render("Energia Mecanica Total = " + str(round(fisica.e,1)),True,(255,255,180))
    screen.blit(surface,(10,60))