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

def makelayer(a,b,theta): #con perimetro

    #perimetro

    xf = X0-a/2
    yf = Y0+b/2
    L=a

    gline(gcode,"G1 X"+str(xf)+" Y"+str(yf-b)+" E"+str(b*fp)+" F"+str(feedp))
    gline(gcode,"G1 X"+str(xf+a)+" Y"+str(yf)+" E"+str(a*fp)+" F"+str(feedp)) 
    gline(gcode,"G1 X"+str(xf)+" Y"+str(yf+b)+" E"+str(b*fp)+" F"+str(feedp)) 
    gline(gcode,"G1 X"+str(xf-a)+" Y"+str(yf)+" E"+str(a*fp)+" F"+str(feedp)) 

    #punto inicial

    a=a-2*dn
    b=b-2*dn

    xf=X0-a/2
    yf=Y0+b/2

    print(xf)
    print(yf)

    gline(gcode,"G1 X"+str(xf)+" Y"+str(yf)+" F"+str(feedt)) #mover a punto inicial del patron  

    while(True):

        #interseccion de curvas

        #línea del patrón

        m1=math.tan(theta+math.pi/2)
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

        #par de líneas a intersectar, el criterio es encontrar las líneas que intersectan en el perímetro cuadrado

        for i in range(1,5):

            num1=(b_r[0]*c_r[i]-b_r[i]*c_r[0])
            num2=(a_r[i]*c_r[0]-a_r[0]*c_r[i])
            den=(a_r[0]*b_r[i]-a_r[i]*b_r[0])
            if den==0:
                den=-1
            inter[0,i-1]=num1/den
            inter[1,i-1]=num2/den

        point = numpy.empty((2,2))

        print(inter)
        v=0

        for i in range(4):

            if (inter[0,i]>=X0-a/2 and inter[0,i]<=X0+a/2) and (inter[1,i]<=Y0+b/2 and inter[1,i]>=Y0-b/2) and (inter[1,i]>0):

                point[0,v] = inter[0,i]
                point[1,v] = inter[1,i]
                v=v+1      
                if(v==2):
                    break        

        if(v==0):
            break

        L=math.sqrt(math.pow(point[0,0]-point[0,1],2)+math.pow(point[1,0]-point[1,1],2))
        ##gline(gcode,"G1 X"+str(point[1,0])+" Y"+str(point[1,1])+" E"+str(L*fp)+" F"+str(feedp))
        xf=xf+e
        ##gline(gcode,"G1 X"+str(xf)+" Y"+str(yf)+" E"+str(L*fp)+" F"+str(feedt))
  

with open('scaffold_box.gcode','w') as gcode:

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

    for i in range(1):

        makelayer(A,B,math.pi*(i%3)*(1/3))
        zf=zf+lh
        gline(gcode,"G1 Z"+str(zf)) #siguiente capa    
    
    gline(gcode,"G1 Z"+str(zf+20))
    gline(gcode,"M18 X Y")
    gline(gcode,"M104 S0")
    gline(gcode,"M140 S0")

gcode.close()

