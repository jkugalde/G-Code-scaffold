#ESTRUCTURA RECTANGULAR CON MALLADO 60-120

import math
import numpy

def gline(writer,line):
    s=str(line)
    writer.write(s)
    writer.write('\n')

#diseno 

#parametros de diseno

A = 20  #longitud en x
B = 10 #longitud en y
lh = 0.3 #altura de capa en mm
N = 10 #numero de capas 
e = 0.4 #espacio entre lineas en mm
dn =  0.4 #diametro de boquilla en mm

#calculo de estructura

ln = round(A/(e+dn)) #lineas vacias por capa
lf=ln+1 #lineas solidas por capa
A = (e+dn)*ln+dn #longitud en x final
dens = e*ln/A #densidad aproximada del modelo

#impresion

#parametros de impresion

flow_0803 = 0.1996 #pasos por mm extruido con boquilla de 0.8 mm y altura de capa 0.3mm
flow = flow_0803/(0.3*0.8) #flujo normalizado
flowmultiplier=1.8
flow=flow*flowmultiplier
fp = flow*dn*lh #flujo de impresion
feedp = 300 #velocidad de impresion en mm/min
feedt = 300 #velocidad travel en mm/min 
X0 = 147.5 #centro del eje x
Y0 = 92.5 #centro del eje y
ofz=0.1 #offset en z
zf=lh+ofz

#algoritmo de impresion

c=1 #sentido (-1 o 1)

def makelayer(a,b,nl,theta): #con perimetro

    #perimetro

    xf = X0-a/2
    yf = Y0+b/2

    gline(gcode,"G1 X"+str(xf)+" Y"+str(yf-b)+" E"+str(b*fp)+" F"+str(feedp))
    gline(gcode,"G1 X"+str(xf+a)+" Y"+str(yf)+" E"+str(a*fp)+" F"+str(feedp)) 
    gline(gcode,"G1 X"+str(xf)+" Y"+str(yf+b)+" E"+str(b*fp)+" F"+str(feedp)) 
    gline(gcode,"G1 X"+str(xf-a)+" Y"+str(yf)+" E"+str(a*fp)+" F"+str(feedp)) 

    #punto inicial

    a=a-2*dn
    b=b-2*dn

    xf=X0-a/2
    yf=Y0+b/2

    for i in range nl:

    #ubicar cuadrante y definir direcciones 

        dirx=0
        diry=0

        if(xf>X0) and (yf>Y0):
            dirx=1
            xf=xf-e
        if(xf<X0) and (yf>Y0):
            dirx=-1
            xf=xf+e
        if(xf<X0) and (yf<Y0):
            diry=1
            xf=xf+e
        if(xf>X0) and (yf<Y0):
            diry=-1
            xf=xf-e

        gline(gcode,"G1 X"+str(xf)+" Y"+str(yf)+" F"+str(feedt)) #mover a punto inicial del patron  

        #interseccion de curvas

        #línea del patrón

        m1=math.tan(theta)
        a1=-m1
        b1=1
        c1=m1*xf-yf

        #líneas perímetro del área interna rectangular

        #linea inferior y=Y0-b/2
        a2=0
        b2=1
        c2=b/2-Y0
        #linea izquierda x=X0-a/2
        a3=1
        b3=0
        c3=a/2-X0
        #linea superior y=Y0+b/2
        a4=0
        b4=1
        c4=-b/2-Y0
        #linea derecha x=X0+a/2
        a5=1
        b5=0
        c5=-a/2-X0

        a_r = [a1,a2,a3,a4,a5]
        b_r = [b1,b2,b3,b4,b5]
        c_r = [c1,c2,c3,c4,c5]

        inter = numpy.empty((2,4))
        #par de líneas a intersectar, el criterio es minimizar la distancia entre puntos para encontrar el par

        for i in range(1,5):

            num1=(b_r[0]*c_r[i]-b_r[i]*c_r[0])
            num2=(a_r[i]*c_r[0]-a_r[0]*c_r[i])
            den=(a_r[0]*b_r[i]-a_r[i]*b_r[0])
            if den==0:
                den=0.0001
            inter[0,i-1]=num1/den
            inter[1,i-1]=num2/den

        minval=1000000
        min_index = [0,0]

        dists=numpy.empty((4,4))
        for i in range(4):
            for j in range(4):
                dists[i,j]=math.sqrt(math.pow(inter[0][j]-inter[0][i],2)+math.pow(inter[1][j]-inter[1][i],2))
                if dists[i,j]==0:
                    dists[i,j]=1000000
                if dists[i,j]<minval:
                    minval=dists[i,j]
                    min_index[0]=i
                    min_index[1]=j

        print(dists)
        print(dists.min())
        print(min_index[0],min_index[1])

        xi=inter[0][min_index[0]]
        yi=inter[1][min_index[0]]
        xf=inter[0][min_index[1]]
        yf=inter[1][min_index[1]]

        print(xi,yi)
        print(xf,yf)

        L=0
        gline(gcode,"G1 X"+str(xf)+" Y"+str(yf)+" E"+str(L*fp)+" F"+str(feedp))
  

with open('scaffold_box.gcode', 'w') as gcode:

    gline(gcode,"G90")
    gline(gcode,"M83")
    gline(gcode,"M106 S255 P1")
    gline(gcode,"G28")

    #skirt

    skrt_dis = 20 #skirt distance
    xf=X0-A-skrt_dis
    yf=Y0+B+skrt_dis
    c=1

    gline(gcode,"G1 X"+str(xf)+" Y"+str(yf)+" F"+str(feedt)) #mover a punto inicial de skirt

    #skirt

    gline(gcode,"G1 X"+str(xf)+" Y"+str(yf-B-skrt_dis)+" E"+str((A+skrt_dis)*fp)+" F"+str(feedp))
    gline(gcode,"G1 X"+str(xf+A+skrt_dis)+" Y"+str(yf)+" E"+str((A+skrt_dis)*fp)+" F"+str(feedp)) 
    gline(gcode,"G1 X"+str(xf)+" Y"+str(yf+B+skrt_dis)+" E"+str((A+skrt_dis)*fp)+" F"+str(feedp)) 
    gline(gcode,"G1 X"+str(xf-A-skrt_dis)+" Y"+str(yf)+" E"+str((A+skrt_dis)*fp)+" F"+str(feedp)) 

    gline(gcode,"G1 X"+str(xf+skrt_dis)+" Y"+str(yf-skrt_dis)+" F"+str(feedt))
        
#estructura

    for i in range(N):

        makelayer(A,B,ln,math.pi*(i%3)*(1/3))
        zf=zf+lh
        gline(gcode,"G1 Z"+str(zf)) #siguiente capa    
    
    gline(gcode,"G1 Z"+str(zf+20))
    gline(gcode,"M18 X Y")
    gline(gcode,"M104 S0")
    gline(gcode,"M140 S0")

gcode.close()

