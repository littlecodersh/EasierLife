from PIL import Image 
import sys, os

class CoordinateClient():
    def __init__(self, size = {'x':1000,'y':1000}, splitline = {'x':[100,200], 'y':[500]}
            , blank = {'x':0, 'y':0}, padding = {'x':0, 'y':0}, backgroundcolor = (255,255,255)):
        self.color = { 'black': (0,0,0), 'white':(255,255,255), 'red':(255,0,0), 'grey':(96,96,96) }
        self.size = {xy: value + 1 for xy, value in size.items()}
        self.splitline = splitline
        self.blank = blank
        self.maxlayer = 0
        self.padding = padding
        self.backgroundcolor = backgroundcolor
        self.img = self.create_img(self.size, self.blank, self.padding) # self.img = Image.open(fileName)
        self.create_splitline(splitline)
    def create_img(self, size, blank, padding):
        def fn(xy): return (2 * size[xy] - 1) * blank[xy] + (size[xy] - 1) * padding[xy] + size[xy]
        img = Image.new("RGB",(fn('x'), fn('y')), self.backgroundcolor)
        return img
    def inside_xy_change(self, x, y, blank = None, padding = None):
        if blank is None: blank = self.blank
        if padding is None: padding = self.padding
        def fn(i, xy): return (1 + 2 * blank[xy] + padding[xy]) * i
        return (fn(x, 'x'), fn(y, 'y'))
    def get_point(self, x, y, adjust = None, img = None, blank = None, padding = None):
        if img is None: img = self.img
        if adjust is None: adjust = (0,0)
        inside_xy = self.inside_xy_change(x, y, blank, padding)
        return img.getpixel((inside_xy[0] + adjust[0], inside_xy[1] + adjust[1]))
    def add_point(self, x, y, color = None):
        def is_blank(x, y, adjust = None): return self.get_point(x, y, adjust) in (self.backgroundcolor, self.color['grey'])
        def has_space(layer, x, y):
            for adjust in range(layer + 1):
            # * * *  1. first test point in xy direction
            # * * *  2. then test the rest layer in order of distance
            # * * *  3. return adjust if has space else false
                for direction in (-1, 1): # up, right, down, left
                    if is_blank(x, y, (adjust * direction, layer)): return (adjust * direction, layer)
                    if is_blank(x, y, (layer, adjust * direction)): return (layer, adjust * direction)
                    if is_blank(x, y, (adjust * direction, -layer)): return (adjust * direction, -layer)
                    if is_blank(x, y, (-layer, adjust * direction)): return (-layer, adjust * direction)
            return False
        if color is None: color = self.color['black']
        addPointAdjust = (0,0)
        if not is_blank(x, y):
            layer = 1
            currentLayer = self.blank['y'] if self.blank['y'] < self.blank['x'] else self.blank['x']
            while layer <= currentLayer:
                adjust = has_space(layer, x, y)
                if adjust: break
                layer += 1
            if currentLayer < layer:
                self.resize_img(blank = {'x': self.blank['x'] if layer < self.blank['x'] else layer,
                    'y': self.blank['y'] if layer < self.blank['y'] else layer})
                adjust = (0, layer)
            if self.maxlayer < layer: self.maxlayer = layer
            addPointAdjust = adjust
        inside_xy = self.inside_xy_change(x,y)
        self.img.putpixel((inside_xy[0] + addPointAdjust[0], inside_xy[1] + addPointAdjust[1]), color)
    def create_splitline(self, splitline = None):
        if splitline is None: splitline = self.splitline
        for x in splitline['x']:
            for y in range(self.size['y']):
                self.add_point(x, y, self.color['grey'])
        for y in splitline['y']:
            for x in range(self.size['x']):
                self.add_point(x, y, self.color['grey'])
    def resize_img(self, size = None, blank = {'x':0, 'y':0}, padding = {'x':0, 'y':0}):
        size = self.size if size is None else {xy: value + 1 for xy, value in size.items()}
        old_img = self.img
        old_size = self.size
        old_blank = self.blank
        old_padding = self.padding
        self.size = size
        self.blank = blank
        self.padding = padding
        self.img = self.create_img(size, blank, padding)
        self.create_splitline()
        for x in range(1, old_size['x']):
            for y in range(1, old_size['y']):
                # add the xy point
                pointColor = self.get_point(x, y, None, old_img, old_blank, old_padding) 
                if pointColor != self.backgroundcolor: self.add_point(x, y, pointColor)
                # add the point in blank areas
                blank_min = {'x': old_blank['x'] if old_blank['x'] < blank['x'] else blank['x'],
                    'y': old_blank['y'] if old_blank['y'] < blank['y'] else blank['y']}
                for adjust_x in range(-blank_min['x'], blank_min['x'] + 1):
                    for adjust_y in range(-blank_min['y'], blank_min['y'] + 1):
                        if self.get_point(x, y, (adjust_x, adjust_y), old_img, old_blank, old_padding) != self.backgroundcolor: 
                            if (adjust_x, adjust_y) != (0,0): self.add_point(x, y, pointColor)
    def save(self, filename = 'coordinate.png'):
        save_img = self.create_img(self.size, self.blank, self.padding)
        x_size, y_size = self.img.size 
        for x in range(x_size):
            for y in range(y_size):
                save_img.putpixel((x, y), self.img.getpixel((x, y_size - y - 1)))
        save_img.save(filename, 'PNG')

if __name__ == '__main__':
    cc = CoordinateClient(size = {'x':5, 'y':5}, splitline = {'x':range(0, 6), 'y': range(0, 6)})
    cc.save()
