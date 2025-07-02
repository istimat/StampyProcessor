# Stampy processor
## What?
This is a tool that converts dxf files to gcode for dot peen marking machines:
![image](https://github.com/user-attachments/assets/ca1b9956-8078-4f73-9164-6acafa3a64ef)

By inputting a dxf file and specifying a resolution and dot duplication tolerance, you can go from this:
![image](https://github.com/user-attachments/assets/d768ec2e-a313-470c-9721-41366875eb40)

To this:
![image](https://github.com/user-attachments/assets/d89598c3-379d-41c0-acbf-89bf3a986b1b)
![image](https://github.com/user-attachments/assets/b616f03b-f70b-49e1-88f4-ec305292eb57)

With corresponding g-code:
```
G90 G17
G00 X0.0 Y0.03557299999999941
M3 S100
G04 P0.001
S0
G01 X0.0 Y0.23557299999999942 F10000
M3 S100
G04 P0.001
S0
G01 X0.0 Y0.43557299999999943 F10000
M3 S100
G04 P0.001
S0
G01 X0.0 Y0.6355729999999995 F10000
M3 S100
G04 P0.001
S0
G01 X0.0 Y0.8355729999999995 F10000
M3 S100
G04 P0.001
S0
G01 X0.0 Y1.0355729999999994 F10000
M3 S100
G04 P0.001
S0
G01 X0.0 Y1.2355729999999994 F10000
M3 S100
G04 P0.001
S0
G01 X0.0 Y1.4355729999999993 F10000
M3 S100
G04 P0.001
........
```
