#ESTRUCTURA CUBICA

#diseno 

#parametros de diseno

def gline(writer,line):
    s=str(line)
    writer.write(s)
    writer.write('\n')

L = 20  #longitud de linea aproximada en mm
lh = 0.4 #altura de capa en mm
N = 20 #numero de capas
e = 0.8 #espacio entre lineas en mm
dn =  0.8 #diametro de boquilla

#calculo de estructura

ln = round(L/(e+dn)) #lineas vacias por capa
lf=ln+1 #lineas solidas por capa
Lf = (e+dn)*ln+dn #Longitud final
dens = e*ln/Lf
print("Densidad de malla "+str(round(dens*100,1)))
print("Longitud de arista "+str(Lf))

#impresion

#parametros de impresion

flow_0803 = 0.1996 #pasos por mm extruido con boquilla de 0.8 mm y altura de capa 0.3mm
flow = flow_0803/(0.3*0.8) #flujo normalizado
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

with open('scaffold.gcode', 'w') as gcode:

    gline(gcode,"G90")
    gline(gcode,"M83")
    gline(gcode,"M106 S255 P1")
    gline(gcode,"G28")
    xf=X0-Lf/2+dn/2 #coordenadas iniciales
    yf=Y0-Lf/2+dn/2
    xi=xf
    yi=yf
    zf=lh+ofz
    lin=""
    gline(gcode,"G1 Z"+str(zf))
    gline(gcode,"G1 X" +str(X0-20)+" Y"+str(Y0-20)+" F3000")
    gline(gcode,"G1 X" +str(X0+20)+" Y"+str(Y0-20)+" E"+str(40*fp)+" F300")
    gline(gcode,"G1 X" +str(X0+20)+" Y"+str(Y0+20)+" E"+str(40*fp))
    gline(gcode,"G1 X" +str(X0-20)+" Y"+str(Y0+20)+" E"+str(40*fp))
    gline(gcode,"G1 X" +str(X0-20)+" Y"+str(Y0-20)+" E"+str(40*fp))
    gline(gcode,"G1 X"+str(xf)+" Y"+str(yf)+" F3000")

    for j in range(N):

        for i in range(lf): #extrusion de linea y mover a inicio de nueva linea

            xf=xf+Lff*((j)%2)*c
            yf=yf+Lff*((j+1)%2)*c
            c=-c

            gline(gcode,"G1 X"+str(xf)+" Y"+str(yf)+" E"+str(Lff*fp)+" F"+str(feedp))

            if i<lf-1: #espaciado entre lineas
                xf=xf+(e+dn)*((j+1)%2)*d
                yf=yf+(e+dn)*((j)%2)*d
                gline(gcode,"G1 X"+str(xf)+" Y"+str(yf)+" F"+str(feedt))

        zf=zf+lh
        gline(gcode,"G1 Z"+str(zf)) #siguiente capa

        if j%2==0:
            if yf!=yi:
                d=-1
        else:
            if xf!=xi:
                d=1
    
    gline(gcode,"G1 Z"+str(zf+20))
    gline(gcode,"M18 X Y")
    gline(gcode,"M104 S0")
    gline(gcode,"M140 S0")

gcode.close()