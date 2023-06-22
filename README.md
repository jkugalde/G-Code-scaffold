# 3DP scaffold

These python codes generate a gcode file for 3d printing a porous scaffold structure, such as the one shown Figure 1. It requires a variety of inputs, like nozzle diameter, line separation, etc. 

<img src="/img/scf.png" width="350">

Figure 1: Perpendicular line scaffold. a) 3D model of the desired structure. b) Printed scaffold with polycaprolactone.

The generated trajectories for the extruder with Cura and Simplify were not optimal, as the cells were getting blocked by material from the upper layer.
The custom gcode increased the porousity, as it is shown in Figure 2. 

<img src="/img/cut.png" width="350">

Figure 2: Transversal cuts from printing. a) Scaffold with a path obtained from Simplify3D. b) Scaffold made with the custom gcode.

The tests were done on a TUMAKER NX PRO Pellet 3d printer, with a 0.8 mm nozzle and using polycaprolactone (PCL).

The G_scaffold_square file generates a square matrix of perpendicular lines between each layer.

The G_scaffold_disc file generates a porous cylinder with a base. The file in this repository is not updated.

## Future work

- Implement retraction.
- Change pattern to triangles. 