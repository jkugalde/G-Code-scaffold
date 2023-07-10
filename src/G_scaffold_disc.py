#ESTRUCTURA DISCO

import math

def gline(writer,line):
    s=str(line)
    writer.write(s)
    writer.write('\n')

#diseno 

#parametros de diseno

L = 20  #diámetro aproximado de cilindro en mm
lh = 0.3 #altura de capa en mm
N = 10 #numero de capas (sin contar capas de tapa)
Nt = 3 #número de capas en tapa
e = 0.4 #espacio entre lineas en mm
dn =  0.4 #diametro de boquilla en mm
Lt = 26 #diámetro aproximado de tapa 

#calculo de estructura

ln = round(L/(e+dn)) #lineas vacias por capa en cilindro
lf=ln+1 #lineas solidas por capa en cilindro
Lf = (e+dn)*ln+dn #diámetro final de cilindro
dens = e*ln/Lf #densidad aproximada del modelo

lnt =round(Lt/(dn+e)) #lineas vacias en tapa
lft = lnt+1 #líneas sólidas en la tapa
Lft = (e+dn)*lnt+dn #diámetro final de la tapa

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

def makelayerA(D,nl,theta): #con circulo perimetral



    xf=X0+(D/2)*math.cos(theta)
    yf=Y0+(D/2)*math.sin(theta)
    yi=yf
    c=1

    gline(gcode,"G1 X"+str(xf)+" Y"+str(yf)+" F"+str(feedt)) #punto inicial

    gline(gcode,"G2 X"+str(xf)+" Y"+str(yf)+" I"+str(-D/2*math.cos(theta))+" J"+str(-D/2*math.sin(theta))+" E"+str(math.pi*D*fp)+" F"+str(feedp)) #circulo perimetral

    r=(D-2*dn)/2

    xf=X0+r*math.cos(theta)
    yf=Y0+r*math.sin(theta)

    r=r-2*dn
    l=2*math.sqrt(abs(pow((D-2*dn)/2,2)-pow(r,2))) #largo de linea (Lft-2*n diametro de infill dentro de círculo perimetral)
    ang0=math.atan2(l/2,r)
    yf=Y0+((D-2*dn)/2)*math.sin(theta+ang0)
    xf=X0+((D-2*dn)/2)*math.cos(theta+ang0)
    gline(gcode,"G1 X"+str(xf)+" Y"+str(yf)+" F"+str(feedt))

    for i in range(nl): #extrusion de linea y mover a inicio de nueva linea
        
        yf=Y0+((D-2*dn)/2)*math.sin(theta-ang0*c)
        xf=X0+((D-2*dn)/2)*math.cos(theta-ang0*c)
        ang0i=ang0

        gline(gcode,"G1 X"+str(xf)+" Y"+str(yf)+" E"+str(l*fp)+" F"+str(feedp))

        if i<nl-1: #espaciado entre lineas

            r=r-dn-e
            l=2*math.sqrt(abs(pow((D-2*dn)/2,2)-pow(r,2)))
            ang0=math.atan2(l/2,r)
            xf=(D-2*dn)/2*math.cos(theta-c*ang0)+X0
            yf=(D-2*dn)/2*math.sin(theta-c*ang0)+Y0
            arc=abs((ang0i-ang0))*(D-2*dn)/2
            c=-c

            if yf>yi:

                gline(gcode,"G3 X"+str(xf)+" Y"+str(yf)+" R"+str((D-2*dn)/2)+" E"+str(arc*fp)+" F"+str(feedt))

            else:
            
                gline(gcode,"G2 X"+str(xf)+" Y"+str(yf)+" R"+str((D-2*dn)/2)+" E"+str(arc*fp)+" F"+str(feedt))

def makelayerB(D,nl,theta): #sin circulo perimetral

    xf=X0+(D/2)*math.cos(theta)
    yf=Y0+(D/2)*math.sin(theta)
    yi=yf
    c=1

    r=D/2

    gline(gcode,"G1 X"+str(xf)+" Y"+str(yf)+" F"+str(feedt)) #punto inicial

    xf=X0+r*math.cos(theta)
    yf=Y0+r*math.sin(theta)

    r=r-2*dn
    l=2*math.sqrt(abs(pow((D)/2,2)-pow(r,2))) #largo de linea (Lft-2*n diametro de infill dentro de círculo perimetral)
    ang0=math.atan2(l/2,r)
    yf=Y0+((D)/2)*math.sin(theta+ang0)
    xf=X0+((D)/2)*math.cos(theta+ang0)
    gline(gcode,"G1 X"+str(xf)+" Y"+str(yf)+" F"+str(feedt))

    for i in range(nl): #extrusion de linea y mover a inicio de nueva linea
        
        yf=Y0+((D)/2)*math.sin(theta-ang0*c)
        xf=X0+((D)/2)*math.cos(theta-ang0*c)
        ang0i=ang0

        gline(gcode,"G1 X"+str(xf)+" Y"+str(yf)+" E"+str(l*fp)+" F"+str(feedp))

        if i<nl-1: #espaciado entre lineas

            r=r-dn-e
            l=2*math.sqrt(abs(pow((D)/2,2)-pow(r,2)))
            ang0=math.atan2(l/2,r)
            xf=(D)/2*math.cos(theta-c*ang0)+X0
            yf=(D)/2*math.sin(theta-c*ang0)+Y0
            arc=abs((ang0i-ang0))*(D)/2
            c=-c

            if yf>yi:

                gline(gcode,"G3 X"+str(xf)+" Y"+str(yf)+" R"+str((D)/2)+" E"+str(arc*fp)+" F"+str(feedt))

            else:
            
                gline(gcode,"G2 X"+str(xf)+" Y"+str(yf)+" R"+str((D)/2)+" E"+str(arc*fp)+" F"+str(feedt))

with open('scaffold_disc.gcode', 'w') as gcode:

    gline(gcode,"G90")
    gline(gcode,"M83")
    gline(gcode,"M106 S255 P1")
    gline(gcode,"G28")
    xf=X0-Lf/2 #coordenadas iniciales
    yf=Y0
    xi=xf
    yi=yf
    xtf=X0-Lft/2
    lin=""
    gline(gcode,"G1 Z"+str(zf))
    gline(gcode,"G1 X" +str(X0-Lft)+" Y"+str(Y0)+" F3000")
    gline(gcode, "G2 X" +str(X0-Lft)+" Y"+str(Y0)+" I"+str(Lft)+ " J"+str(0)+ " E"+str(math.pi*Lft*2*fp)+ " F"+str(feedp)) #skirt

#tapas

    for i in range(Nt):

        if(i%2==0):
            makelayerA(Lft,lnt,math.pi*(i%3)*(1/3))

        else:
            makelayerB(Lft,lnt,math.pi*(i%3)*(1/3))

        zf=zf+lh
        gline(gcode,"G1 Z"+str(zf)) #siguiente capa
        
#cilindro

    for i in range(N):

        if(i%2==0):
            makelayerA(Lf,ln,math.pi*(i%3)*(1/3))

        else:
            makelayerB(Lf,ln,math.pi*(i%3)*(1/3))

        zf=zf+lh
        gline(gcode,"G1 Z"+str(zf)) #siguiente capa    
    
    gline(gcode,"G1 Z"+str(zf+20))
    gline(gcode,"M18 X Y")
    gline(gcode,"M104 S0")
    gline(gcode,"M140 S0")

gcode.close()

