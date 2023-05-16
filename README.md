# G-Code-scaffold

This python file generates a gcode for 3d printing a scaffold structure of perpendicular lines between each layer, such as the one shown Figure 1. It requires a variety of inputs, like nozzle diameter, line separation, etc. 

<img src="/imgs/scf.png" width="350">

Figure 1: Perpendicular line scaffold. a) 3D model of the desired structure. b) Printed scaffold with polycaprolactone.

I had to produce a porous structure with a pellet feeded FDM printer. The generated trajectories for the extruder with Cura and Simplify were not optimal, as the cells were getting blocked by material from the upper layer.

The custom gcode increased the porousity, as it is shown in Figure 2. 

<img src="/imgs/cut.png" width="350">

Figure 2: Transversal cuts from printing. a) Scaffold with a path obtained from Simplify3D. b) Scaffold made with the custom gcode.