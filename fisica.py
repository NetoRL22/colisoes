import commentjson
import sys
import ga
import random

## global mudar
tps=60 #ticks por segundo
nBolas=None
threeD=None
w=None
h=None
l=None
pos=None 
v=None
dt=None  
g=None 
m=None 
r=None 
cor=None
cr=None
camD=None
k=None
u=None
e=None


def setup(filename):
    global nBolas,threeD,w,h,l,pos,v,dt,g,m,r,cor,cr,camD
    with open(filename, 'r', encoding='utf-8') as file:
        data=commentjson.load(file)
        if(data["nBolas"] > 0):
            nBolas = data["nBolas"]
        else:
            sys.exit()
        if(data["3d"]):
            threeD=data["3d"]
        else:
            threeD=False
        w = data["width"]
        h = data["height"]
        l = data["length"]
        if(data["dt"]=="default"):
            dt=1/tps
        else:
            dt=data["dt"]
        g = data["g"]
        if(data["massas"][0]=="random"):
            m = []
            mAleat(data["massas"][1],data["massas"][2])
        else:
            m=data["massas"]
        if(data["raios"][0]=="random"):
            r = []
            rAleat(data["raios"][1],data["raios"][2])
        else:
            r=data["raios"]
        if(data["cores"][0]=="random"):
            cor = []
            corAleat(data["cores"][1],data["cores"][2])
        else:
            cor=data["cores"]
        cr = data["cr"]
        camD = data["camDist"]
        if(data["initV"][0]=="random"):
            vAleat(data["initV"][1],data["initV"][2])
        else:
            v=data["initV"]
        if(data["initPos"]=="random"):
            posAleat(nBolas)
        else:
            pos=data["initPos"]
        


def posAleat(n):
    global nBolas,threeD,w,h,l,pos,v,dt,g,m,r,cor,cr
    pos=[]
    for i in range(nBolas):
        if(threeD):
            pos.append([random.random()*w,random.random()*h,random.random()*l])
        else:
            pos.append([random.random()*w,random.random()*h])

def vAleat(base,disp):
    global nBolas,threeD,w,h,l,pos,v,dt,g,m,r,cor,cr
    v=[]
    for i in range(nBolas):
        v.append([random.randrange(-1,1,2)*base[0]+(random.random()*2-1)*(disp),random.randrange(-1,1,2)*base[1]+(random.random()*2-1)*(disp)])
    if(threeD):
        for i in range(nBolas):
            v[i].append(random.randrange(-1,1,2)*base[2]+((random.random()*2-1)*(disp)))

def mAleat(base,disp):
    global nBolas,threeD,w,h,l,pos,v,dt,g,m,r,cor,cr
    for i in range(nBolas):
        m.append(base+(disp/100)*(random.random()*2-1)*(base-1))

def rAleat(base,disp):
    global nBolas,threeD,w,h,l,pos,v,dt,g,m,r,cor,cr
    for i in range(nBolas):
        r.append(base+(disp/100)*(random.random()*2-1)*(base-1))

def corAleat(base,disp):
    global nBolas,threeD,w,h,l,pos,v,dt,g,m,r,cor,cr
    for i in range(nBolas):
        cor.append([base[0]-base[0]*random.random()*(disp/100)+(255-base[0])*random.random()*(disp/100),base[1]-base[1]*random.random()*(disp/100)+(255-base[1])*random.random()*(disp/100),base[2]-base[2]*random.random()*(disp/100)+(255-base[2])*random.random()*(disp/100)]) # to do rand disp

def parEstaColidindo(a,b):
    global nBolas,threeD,w,h,l,pos,v,dt,g,m,r,cor,cr
    if(ga.norma(ga.diferenca(pos[a],pos[b]))-r[a]-r[b]<=0):
        colidirPar(a,b)

def colidirBolas():
    global nBolas,threeD,w,h,l,pos,v,dt,g,m,r,cor,cr
    for i in range(nBolas):
        colidirBorda(i)
        for j in range(i+1,nBolas):
            parEstaColidindo(i,j)

def colidirPar(a,b):
    global nBolas,threeD,w,h,l,pos,v,dt,g,m,r,cor,cr
    eixoCol=ga.diferenca(pos[a],pos[b])
    vaCol=ga.projecao(v[a],eixoCol)
    vbCol=ga.projecao(v[b],eixoCol)
    vaConst=ga.diferenca(v[a],vaCol)
    vbConst=ga.diferenca(v[b],vbCol)
    vcm=ga.produto_escalar(1/(m[a]+m[b]),ga.soma(ga.produto_escalar(m[a],vaCol),ga.produto_escalar(m[b],vbCol)))
    vaFinCol=ga.diferenca(ga.produto_escalar(1+cr,vcm),ga.produto_escalar(cr,vaCol))
    vbFinCol=ga.diferenca(ga.produto_escalar(1+cr,vcm),ga.produto_escalar(cr,vbCol))
    v[a]=ga.soma(vaConst,vaFinCol)
    v[b]=ga.soma(vbConst,vbFinCol)
    pos[a]=ga.soma(pos[b],ga.produto_escalar((r[a]+r[b]+1),ga.produto_escalar(1/ga.norma(eixoCol),eixoCol)))
    

def colidirBorda(a):
    global nBolas,threeD,w,h,l,pos,v,dt,g,m,r,cor,cr
    # Paredes Verticais
    if(pos[a][0]<=r[a]):
        pos[a][0]=r[a]+1
        v[a][0]=(-1)*cr*v[a][0]
    elif(pos[a][0]>=w-r[a]):
        pos[a][0]=w-r[a]-1
        v[a][0]=(-1)*cr*v[a][0]
    # Chao e Teto
    if(pos[a][1]<=r[a]):
        pos[a][1]=r[a]+1
        v[a][1]=(-1)*cr*v[a][1]
    elif(pos[a][1]>=h-r[a]):
        pos[a][1]=h-r[a]-1
        v[a][1]=(-1)*cr*v[a][1]
    if(threeD):
        if(pos[a][2]<=r[a]):
            pos[a][2]=r[a]+1
            v[a][2]=(-1)*cr*v[a][2]
        elif(pos[a][2]>=l-r[a]):
          pos[a][2]=l-r[a]-1
          v[a][2]=(-1)*cr*v[a][2]

def atualizaPos():
    global nBolas,threeD,w,h,l,pos,v,dt,g,m,r,cor,cr
    for i in range(nBolas):
        pos[i]=ga.soma(pos[i],ga.produto_escalar(dt,v[i]))

def atualizaV():
    global nBolas,threeD,w,h,l,pos,v,dt,g,m,r,cor,cr
    for i in range(nBolas):
        v[i]=ga.soma(v[i],(ga.produto_escalar((g*dt),ga.e2)))

def calculaStats():
    global nBolas,threeD,w,h,l,pos,v,dt,g,m,r,cor,cr,k,u,e
    k=0
    u=0
    for i in range(nBolas):
        k+=(m[i]/2)*ga.norma(v[i])*ga.norma(v[i])
        u+=m[i]*g*(h-pos[i][1])
    e=k+u
        

    