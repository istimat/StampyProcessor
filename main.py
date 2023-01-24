import ezdxf
import matplotlib.pyplot as plt
import math


class Line:
    def __init__(self, xpoints, ypoints) -> None:
        self.xpoints = xpoints
        self.ypoints = ypoints
        self.seg_x = []
        self.seg_y = []

def read_dxf(input_filename):
    dwg = ezdxf.readfile(input_filename)
    msp = dwg.modelspace()
    
    return msp 


def extract_lines(modelspace):
    lines = []
    for e in modelspace:
        xpoints = []
        ypoints = []
        print(e.dxftype())
        for index, point in enumerate(e):
            xpoints.append(point[0])
            ypoints.append(point[1])

        lines.append(Line(xpoints, ypoints))
    
    return lines

def get_min(lines):
    x_min = 1000
    y_min = 1000
    for line in lines:
        if x_min > min(line.xpoints):
            x_min = min(line.xpoints)
        if y_min > min(line.ypoints):
            y_min = min(line.ypoints)
    return x_min, y_min


def get_interpolation(x0, y0, x1, y1, resolution):
    seg_x = []
    seg_y = []
    length = math.dist([x0, y0], [x1, y1])
    segmented_length = 0
    while segmented_length < length:
        remaining = length - segmented_length
        if remaining < resolution * 0.5:
            seg_x.append(x1)
            seg_y.append(y1)
            break
        seg_x.append(x0 + (segmented_length/length) * (x1 - x0))
        seg_y.append(y0 + (segmented_length/length) * (y1 - y0))
        segmented_length += resolution
    
    return seg_x, seg_y
    

def translate_to_origin(lines, x_min, y_min):
    for line in lines:
        for i in range(len(line.xpoints)):
            line.xpoints[i] -=  x_min
            line.ypoints[i] -=  y_min


def interpolate_points(resolution):
    for line in lines:
        for index , point in enumerate(line.xpoints):
            if index > 0:
                seg_x, seg_y = get_interpolation(line.xpoints[index-1], line.ypoints[index-1],
                                                 line.xpoints[index], line.ypoints[index],
                                                 resolution)
                line.seg_x += seg_x
                line.seg_y += seg_y
                plt.scatter(seg_x, seg_y, color="red")
        plt.plot(line.xpoints, line.ypoints)
        plt.axis('scaled')
    plt.show()

def generate_gcode(filename, lines,feedrate, power, dwell):
    with open(filename, 'w') as nc:
        nc.write('G90 G17\n')
        for line in lines:
            for index, point in enumerate(line.seg_x):
                if index == 0:
                    nc.write(f'G00 X{line.seg_x[index]} Y{line.seg_y[index]}\n')
                    nc.write(f'M3 S{power}\n')
                    nc.write(f'G04 P{dwell}\n')
                    nc.write(f'S0\n')
                else:
                    nc.write(f'G01 X{line.seg_x[index]} Y{line.seg_y[index]}\n')
                    nc.write(f'M3 S{power}\n')
                    nc.write(f'G04 P{dwell}\n')
                    nc.write(f'S0\n')
            
            
            
                            

if __name__ == "__main__":
    
    input_file = "data/test_small.dxf"
    output_file = "data/output.nc"
    
    modelspace = read_dxf(input_file)
    lines = extract_lines(modelspace)
    
    x_min, y_min = get_min(lines)
    translate_to_origin(lines, x_min, y_min)
    
    interpolate_points(resolution = 0.2)
    
    generate_gcode(output_file, lines, 100, 100, 100)