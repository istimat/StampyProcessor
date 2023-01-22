import sys
from pprint import pprint
import ezdxf
import matplotlib.pyplot as plt
import time
import math

dwg = ezdxf.readfile("test.dxf")

msp = dwg.modelspace()
 
def get_interpolation(x0, y0, x1, y1, resolution):
    seg_x = []
    seg_y = []
    length = math.dist([x0, y0], [x1, y1])
    segmented_length = 0
    while segmented_length < length:
        remaining = length - segmented_length
        if remaining < resolution * 0.9:
            seg_x.append(x1)
            seg_y.append(y1)
            break
        seg_x.append(x0 + (segmented_length/length) * (x1 - x0))
        seg_y.append(y0 + (segmented_length/length) * (y1 - y0))
        segmented_length += resolution
    
    return seg_x, seg_y
    
class Line:
    def __init__(self, xpoints, ypoints) -> None:
        self.xpoints = xpoints
        self.ypoints = ypoints
        self.seg_x = None
        self.seg_y = None
        
    

lines = []
for e in msp:
    xpoints = []
    ypoints = []
    print(e.dxftype())
    for index, point in enumerate(e):
        xpoints.append(point[0])
        ypoints.append(point[1])

    lines.append(Line(xpoints, ypoints))
    #break

#print(lines)
def get_min(lines):
    x_min = 1000
    y_min = 1000
    for line in lines:
        if x_min > min(line.xpoints):
            x_min = min(line.xpoints)
        if y_min > min(line.ypoints):
            y_min = min(line.ypoints)
    return x_min, y_min

def translate_to_origin(lines, x_min, y_min):
    for line in lines:
        for i in range(len(line.xpoints)):
            line.xpoints[i] -=  x_min
            line.ypoints[i] -=  y_min


x_min, y_min = get_min(lines)
translate_to_origin(lines, x_min, y_min)

for line in lines:
    for index , point in enumerate(line.xpoints):
        if index > 0:
            seg_x, seg_y = get_interpolation(line.xpoints[index-1], line.ypoints[index-1],
                                             line.xpoints[index], line.ypoints[index],
                                             1)
            line.seg_x = seg_x
            line.seg_y = seg_y
            plt.scatter(seg_x, seg_y, color="red")
    plt.plot(line.xpoints, line.ypoints)
    plt.axis('scaled')

print(lines[0].seg_x)

plt.show()