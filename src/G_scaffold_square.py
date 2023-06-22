#square structure

def gline(writer,line): #creates writer
    s=str(line)
    writer.write(s)
    writer.write('\n')

#design

#design parameters are in milimiters

L = 30  #square side length
lh = 0.4 #layer height 
N = 4 #number of layers
e = 0.8 #distance between lines
dn =  0.8 #nozzle diameter

#structure attributes

ln = round(L/(e+dn)) #number of spaces per layer
lf=ln+1 #number of lines per layer
Lf = (e+dn)*ln+dn #final side length
dens = (dn*lf*Lf)/(Lf*Lf) #mean layer density (printed area/total square area)
print("Layer density "+str(round(dens*100,1))+"%")
print("Side length "+str(round(Lf,1)) +"mm")

#printing

#printing parameters for TUMAKER NX PRO PELLET PRINTER

flow_0803 = 0.1996 #measured E distance for a line of 1 mm length using Simplify 3D, with a height of 0.3 mm and a nozzle of 0.8 mm. The E steps/mm was around 400.
flow = flow_0803/(0.3*0.8) #normalized flow per mm
flow_multiplier = 1.8 #flow multiplier
fp = flow*dn*lh*flow_multiplier #flow per mm with a nozzle of dn diameter and lh layer height.
feedp = 300 #printing speed mm/min
feedt = 300 #travel speed mm/min
X0 = 147.5 #midpoint in the x axis of the printer
Y0 = 92.5 #midpoint in the y axis of the printer
Lff = Lf-dn #actual printing distance of the square side
ofz=0.1 #z offset from the bed

#printing algorithm

with open('scaffold_square.gcode', 'w') as gcode:

    gline(gcode,"G90")
    gline(gcode,"M83")
    gline(gcode,"M106 S255 P1")
    gline(gcode,"G28")

    xf=X0-Lf/2+dn/2 #initial printing coordinates point of the structure
    yf=Y0-Lf/2+dn/2
    xi=xf
    yi=yf
    zf=lh+ofz
    lin=""

    #square skirt

    gline(gcode,"G1 Z"+str(zf))
    gline(gcode,"G1 X" +str(X0-(L))+" Y"+str(Y0-(L))+" F3000")
    gline(gcode,"G1 X" +str(X0+(L))+" Y"+str(Y0-(L))+" E"+str(2*L*fp)+" F300")
    gline(gcode,"G1 X" +str(X0+(L))+" Y"+str(Y0+(L))+" E"+str(2*L*fp))
    gline(gcode,"G1 X" +str(X0-(L))+" Y"+str(Y0+(L))+" E"+str(2*L*fp))
    gline(gcode,"G1 X" +str(X0-(L))+" Y"+str(Y0-(L))+" E"+str(2*L*fp))
    gline(gcode,"G1 X"+str(xf)+" Y"+str(yf)+" F3000")

    c=1 #direction alternator for consecutive lines
    d=1 #direction of overall printing in each layer

    for j in range(N):

        for i in range(lf): #make line

            xf=xf+Lff*((j)%2)*c
            yf=yf+Lff*((j+1)%2)*c
            c=-c

            gline(gcode,"G1 X"+str(xf)+" Y"+str(yf)+" E"+str(Lff*fp)+" F"+str(feedp))

            if i<lf-1: #make space between lines
                xf=xf+(e+dn)*((j+1)%2)*d
                yf=yf+(e+dn)*((j)%2)*d
                gline(gcode,"G1 X"+str(xf)+" Y"+str(yf)+" F"+str(feedt))


        zf=zf+lh #layer change

        gline(gcode,"G1 Z"+str(zf)) 

        if j%2==0: #choosing starting direction of new line and overall direction of printing
            if yf>Y0:
                d=-1
            else:
                d=1
            if xf>X0:
                c=-1
            else:
                c=1

        else:
            if xf>X0:
                d=-1
            else:
                d=1
            if yf>Y0:
                c=-1
            else:
                c=1
    
    #moves the bed down, beneath the cooling fan, and turns off the heaters.
    
    gline(gcode,"G1 Z"+str(zf+20))
    gline(gcode,"M18 X Y")
    gline(gcode,"M104 S0")
    gline(gcode,"M140 S0")

gcode.close()