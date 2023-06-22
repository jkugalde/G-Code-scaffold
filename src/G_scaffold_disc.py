#ESTRUCTURA DISCO

import math

def gline(writer,line):
    s=str(line)
    writer.write(s)
    writer.write('\n')

#diseno 

#parametros de diseno

L = 20  #diámetro aproximado en mm
lh = 0.4 #altura de capa en mm
N = 10 #numero de capas (hacia arriba)
e = 0.8 #espacio entre lineas en mm
dn =  0.8 #diametro de boquilla
Lt = 22 #diámetro aproximado de tapa

#calculo de estructura

ln = round(L/(e+dn)) #lineas vacias por capa
lf=ln+1 #lineas solidas por capa
Lf = (e+dn)*ln+dn #Longitud final
dens = e*ln/Lf
nt = round(Lt/dn) #numero de lineas de la tapa
lft = nt*dn #diámetro final de tapa
print("Densidad de malla "+str(round(dens*100,1)))
print("Longitud de arista "+str(Lf))

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
Lff = Lf-dn #longitud de impresion de linea
ofz=0.1 #offset en z
c=1 #sentido (-1 o 1)
d=1

#algoritmo de impresion

with open('scaffold_disc.gcode', 'w') as gcode:

    gline(gcode,"G90")
    gline(gcode,"M83")
    gline(gcode,"M106 S255 P1")
    gline(gcode,"G28")
    xf=X0-Lff/2 #coordenadas iniciales
    yf=Y0
    xi=xf
    xtf=X0-lft/2
    yi=yf
    zf=lh+ofz
    lin=""
    gline(gcode,"G1 Z"+str(zf))
    gline(gcode,"G1 X" +str(X0-L)+" Y"+str(Y0)+" F3000")
    gline(gcode, "G2 X" +str(X0-L)+" Y"+str(Y0)+" I"+str(L)+ " J"+str(0)+ " E"+str(math.pi*L*2)+ " F"+str(feedp)) #skirt

    #tapa

    gline(gcode,"G1 X"+str(xtf)+" Y"+str(yf)+" F"+str(feedt))

    for i in range(nt): #extrusion de linea y mover a inicio de nueva linea

        l=2*math.sqrt(abs(pow(lft/2,2)-pow(X0-xtf,2)))*c
        yf=yf+l
        c=-c

        gline(gcode,"G1 X"+str(xtf)+" Y"+str(yf)+" E"+str(abs(l)*fp)+" F"+str(feedp))

        if i<nt-1: #espaciado entre lineas

            xfi=xtf
            xtf=xtf+dn
            yf=yf-(math.sqrt(abs(pow(lft/2,2)-pow(xtf-X0,2)))*c-math.sqrt(abs(pow(lft/2,2)-pow(xfi-X0,2)))*c)


        gline(gcode,"G1 X"+str(xtf)+" Y"+str(yf)+" F"+str(feedt))

    zf=zf+lh
    gline(gcode,"G1 Z"+str(zf)) #siguiente capa

    xf=xi
    yf=yi
    c=1

    gline(gcode,"G1 X"+str(xf)+" Y"+str(yf)+" F3000") #punto inicial de impresión

    #scaffold

    for j in range(N):

        for i in range(lf): #extrusion de linea y mover a inicio de nueva linea

            if j%2==1:

                 l=2*math.sqrt(abs(pow(Lff/2,2)-pow(Y0-yf,2)))*c
                 xf=xf+l
                
            else:

                 l=2*math.sqrt(abs(pow(Lff/2,2)-pow(X0-xf,2)))*c
                 yf=yf+l

            c=-c

            gline(gcode,"G1 X"+str(xf)+" Y"+str(yf)+" E"+str(abs(l)*fp)+" F"+str(feedp))

            if i<lf-1: #espaciado entre lineas

                if(j%2==0):

                    xfi=xf
                    xf=xf+(e+dn)*d
                    yf=yf-(math.sqrt(abs(pow(Lff/2,2)-pow(xf-X0,2)))*c-math.sqrt(abs(pow(Lff/2,2)-pow(xfi-X0,2)))*c)

                else:
                    
                    yfi=yf
                    yf=yf+(e+dn)*d
                    xf=xf-(math.sqrt(abs(pow(Lff/2,2)-pow(yf-Y0,2)))*c-math.sqrt(abs(pow(Lff/2,2)-pow(yfi-Y0,2)))*c)

                gline(gcode,"G1 X"+str(xf)+" Y"+str(yf)+" F"+str(feedt))

        zf=zf+lh

        gline(gcode,"G1 Z"+str(zf)) #siguiente capa


        if j%2==0:

            d=-1
            yf=Y0+Lff/2
            xf=X0
            gline(gcode,"G1 Y"+str(yf)+" F"+str(feedt))
            gline(gcode,"G1 X"+str(xf)+" F"+str(feedt))

        else:

            d=1
            xf=X0-Lff/2
            yf=Y0
            gline(gcode,"G1 X"+str(xf)+" F"+str(feedt))
            gline(gcode,"G1 Y"+str(yf)+" F"+str(feedt))
    
    gline(gcode,"G1 Z"+str(zf+20))
    gline(gcode,"M18 X Y")
    gline(gcode,"M104 S0")
    gline(gcode,"M140 S0")

gcode.close()