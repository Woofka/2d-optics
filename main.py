import tkinter
from math import inf, pi, fabs, sin, cos, tan, asin, acos, atan, degrees, radians
import time
# import keyboard as kb   # pip install keyboard


class CustomError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return str(self.message)
        else:
            return 'CustomError has been raised'


class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x+other.x, self.y+other.y)

    def __sub__(self, other):
        return Vector2(self.x-other.x, self.y-other.y)

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return None

    def dist(self, vector2):
        return ((vector2.x - self.x)**2 + (vector2.y - self.y)**2)**0.5


class Line:
    """
    a*x + b*y + c = 0
    """
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def is_vertical(self):
        """
        a*x + b*y + c = 0
        b = 0
        <=>
        x = -c/a
        """
        if self.b == 0:
            return True
        else:
            return False

    def is_horizontal(self):
        """
        a*x + b*y + c = 0
        a = 0
        <=>
        y = -c/b
        """
        if self.a == 0:
            return True
        else:
            return False

    def k(self):
        """
        a*x + b*y + c = 0
        y = k*x + l
        k = -a/b
        """
        if self.is_vertical():
            return None
        else:
            return -self.a/self.b

    def angle(self):
        """
        y = kx + l
        k = tan(alpha)
        alpha = atan(k)
        """
        if self.is_vertical():
            return pi/2
        else:
            return atan(self.k())

    def intersection_line(self, line):
        """
        { a1*x + b1*y + c1 = 0
        { a2*x + b2*y + c2 = 0

        d = |a1 b1| = a1*b2 - b1*a2
            |a2 b2|

        dx = |-c1 b1| = -c1*b2 + b1*c2
             |-c2 b2|

        dy = |a1 -c1| = -a1*c2 + c1*a2
             |a2 -c2|

        x = dx / d
        y = dy / d
        """
        d = self.a * line.b - self.b * line.a
        if d == 0:      # no intersections
            return None
        else:
            dx = -self.c * line.b + self.b * line.c
            dy = -self.a * line.c + self.c * line.a
            return Vector2(dx/d, dy/d)

    def intersection_circle(self, center, r):
        """
        { a*x + b*y + c = 0
        { (x-x0)^2 + (y-y0)^2 = R^2

        x^2*(a^2+b^2) + x*(2(ac+aby0-2b^2*x0)) + (b^2*(x0^2+y0^2-r^2)+c^2+2bcy0) = 0

        D = 4(ac+aby0-b^2*x0)^2 - 4(a^2+b^2)*(b^2*(x0^2+y0^2-r^2)+c^2+2bcy0)

        x1,2 = (-2(ac+aby0-2b^2*x0) +- sqrt(D)) / (2*(a^2+b^2))
        y1,2 = (-a * x1,2 - c) / b
        """
        x0, y0 = center.x, center.y
        if not self.is_vertical():      # not vertical line
            d = 4*(self.a*self.c + self.a*self.b*y0 - self.b**2 * x0)**2 - 4*(self.a**2 + self.b**2) *\
                (self.b**2 * (x0**2 + y0**2 - r**2) + self.c**2 + 2*self.b*self.c*y0)
            if d > 0:       # two intersections
                x1 = (-2*(self.a*self.c + self.a*self.b*y0 - self.b**2 * x0) + d**0.5) / (2*(self.a**2 + self.b**2))
                x2 = (-2*(self.a*self.c + self.a*self.b*y0 - self.b**2 * x0) - d**0.5) / (2*(self.a**2 + self.b**2))
                y1 = (-self.a*x1 - self.c) / self.b
                y2 = (-self.a*x2 - self.c) / self.b
                return [Vector2(x1, y1), Vector2(x2, y2)]
            elif d == 0:    # one intersection
                x = (-2*(self.a*self.c + self.a*self.b*y0 - self.b**2 * x0)) / (2*(self.a**2 + self.b**2))
                y = (-self.a*x - self.c) / self.b
                return [Vector2(x, y)]
            else:           # no intersections
                return []
        else:                           # vertical line
            x = -self.c / self.a
            und_sqrt = r**2 - (x - x0)**2
            if und_sqrt >= 0:
                y1 = und_sqrt**0.5 + y0
                y2 = -und_sqrt**0.5 + y0
                if y1 != y2:    # two intersections
                    return [Vector2(x, y2), Vector2(x, y1)]
                else:           # one intersection
                    return [Vector2(x, y2)]
            else:               # no intersections
                return []

    def intersection_angle(self, line):
        """
        y = k1*x + l1
        y = k2*x + l2
        tan(O) = (k2 - k1) / (1 + k1*k2)
        return angle from self to line
        """
        k1 = self.k()
        k2 = line.k()
        if (k1 is not None) and (k2 is not None):   # both lines are not vertical
            if k1*k2 == -1:     # perpendicular lines (atan(inf) = pi/2)
                if k1 > k2:
                    return -pi/2
                else:
                    return pi/2
            else:               # not perpendicular lines
                return atan((k2 - k1) / (1 + k1*k2))
        elif (k1 is None) and (k2 is not None):     # first line is vertical
            return -pi/2 + atan(k2)
        elif (k1 is not None) and (k2 is None):     # second line is vertical
            return pi/2 - atan(k1)
        else:                                       # both lines are vertical
            return 0

    def rotate(self, point, angle):
        """
        y = k1*x + l1
        y = k2*x + l2
        k1 = tan(alpha1)
        k2 = tan(alpha2)
        alpha2 = alpha1 + angle
        """
        return Line.line_through_1p_angle(point, self.angle()+angle)

    def direction(self, point_from, point_surf, surface, get_through):
        """
        Positive direction is a direction of increasing X. Or Y if line is vertical
        """
        positive_direction = True
        if self.is_vertical():
            point_chck = Vector2((-self.b/self.a) * (point_surf.y+1) - self.c/self.a, point_surf.y+1)
        else:
            point_chck = Vector2(point_surf.x+1, (-self.a/self.b) * (point_surf.x+1) - self.c/self.b)

        if not surface.is_vertical():
            if point_from.y > (-surface.a/surface.b) * point_from.x - surface.c/surface.b:
                if point_chck.y > (-surface.a/surface.b) * point_chck.x - surface.c/surface.b:
                    same_side = True
                else:
                    same_side = False
            else:
                if point_chck.y > (-surface.a/surface.b) * point_chck.x - surface.c/surface.b:
                    same_side = False
                else:
                    same_side = True
        else:
            if point_from.x > point_surf.x:
                if point_chck.x > point_surf.x:
                    same_side = True
                else:
                    same_side = False
            else:
                if point_chck.x > point_surf.x:
                    same_side = False
                else:
                    same_side = True

        if not same_side:
            positive_direction = not positive_direction

        if get_through:
            positive_direction = not positive_direction

        return positive_direction

    @staticmethod
    def line_through_2p(p1, p2):
        """
        (x-x1)/(x2-x1) = (y-y1)/(y2-y1)
        <=>
        (y2-y1)x + (x1-x2)y - (x1*y2-x2*y1) = 0
        """
        if p1.x != p2.x or p1.y != p2.y:
            return Line(p2.y-p1.y, p1.x-p2.x, p2.x*p1.y-p1.x*p2.y)
        else:
            raise CustomError('Points should not be the same')

    @staticmethod
    def line_through_1p_k(p, k):
        """
        y = k(x-x0) + y0
        <=>
        -kx + y + (k*x0-y0) = 0
        """
        if k == inf or k == -inf or k is None:   # vertical line
            return Line(1, 0, -p.x)
        else:                       # not vertical line
            return Line(-k, 1, k*p.x-p.y)

    @staticmethod
    def line_through_1p_angle(p, angle):
        """
        y = kx + l
        k = tan(alpha)
        """
        try:
            k = tan(angle)
        except:     # tan(pi/2) = inf
            k = None
        return Line.line_through_1p_k(p, k)

    @staticmethod
    def line_k_l(k, l):
        """
        y = kx + l
        <=>
        -kx + y - l = 0
        """
        if k == inf or k == -inf or k is None:  # vertical line
            return Line(1, 0, -l)
        else:                                   # not vertical line
            return Line(-k, 1, -l)

    @staticmethod
    def line_tangent_to_circle(p, center, r):
        """
        (x1–х0)*(х–х0) + (у1–у0)*(у–у0) = R^2
        (x1-x0)*x + (y1-y0)*y + (x0^2 - x0*x1 + y0^2 - y0*y1 - R^2) = 0
        """
        x0, y0 = center.x, center.y
        return Line(p.x-x0, p.y-y0, x0**2-x0*p.x+y0**2-y0*p.y-r**2)


class Ruler:
    def __init__(self, plane, v1, v2, name, color='grey', dbg=False):
        self.plane = plane
        self.name = name
        self.color = color
        self.dbg = dbg
        self.name_dbg = f'{name}Dbg'
        self.name_v1 = f'{name}v1'
        self.name_v2 = f'{name}v2'
        self.v1 = v1
        self.v2 = v2
        self.move_offset = Vector2()
        self.move_offset_pix = Vector2()
        self.line = Line.line_through_2p(v1, v2)

    def draw_dbg(self):
        plane = self.plane
        plane.canvas.delete(self.name_dbg)
        x = self.v1.x + (self.v2.x - self.v1.x) / 2
        y = self.v1.y + (self.v2.y - self.v1.y) / 2
        if self.line.angle() >= 0:
            anchor = tkinter.SE
        else:
            anchor = tkinter.SW
        if self.dbg:
            text = (f'Name:  {self.name}\n'
                    f'v1:    {self.v1}\n'
                    f'v2:    {self.v2}\n'
                    f'Distance: {self.v1.dist(self.v2)}')
        else:
            text = f'{self.v1.dist(self.v2).__round__(2)}'
        plane.canvas.create_text(plane.x2pix(x), plane.y2pix(y+5),
                                 text=text,
                                 fill=plane.color_ol, font=plane.font, anchor=anchor,
                                 tag=self.name_dbg)

    def draw(self):
        self.draw_dbg()
        self.draw_line()
        plane = self.plane
        plane.canvas.create_oval(plane.x2pix(self.v1.x-3), plane.y2pix(self.v1.y+3),
                                 plane.x2pix(self.v1.x+3), plane.y2pix(self.v1.y-3),
                                 fill=self.color, outline=self.color,
                                 tag=self.name_v1)
        plane.canvas.create_oval(plane.x2pix(self.v2.x-3), plane.y2pix(self.v2.y+3),
                                 plane.x2pix(self.v2.x+3), plane.y2pix(self.v2.y-3),
                                 fill=self.color, outline=self.color,
                                 tag=self.name_v2)

        plane.canvas.tag_bind(self.name_v1, '<Button-1>', self.click_v1)
        plane.canvas.tag_bind(self.name_v2, '<Button-1>', self.click_v2)
        plane.canvas.tag_bind(self.name_v1, '<B1-Motion>', self.drag_v1)
        plane.canvas.tag_bind(self.name_v2, '<B1-Motion>', self.drag_v2)

    def draw_line(self):
        plane = self.plane
        plane.canvas.delete(self.name)
        plane.canvas.create_line(plane.x2pix(self.v1.x), plane.y2pix(self.v1.y),
                                 plane.x2pix(self.v2.x), plane.y2pix(self.v2.y),
                                 fill=self.color, width=2, dash=(4, 2),
                                 tag=self.name)

        plane.canvas.tag_raise(self.name_v1)
        plane.canvas.tag_raise(self.name_v2)
        plane.canvas.tag_bind(self.name, '<Button-1>', self.click_v1)
        plane.canvas.tag_bind(self.name, '<B1-Motion>', self.drag_line)

    def recalculate_line(self):
        self.line = Line.line_through_2p(self.v1, self.v2)

    def drag_v1(self, event):
        move = Vector2(self.plane.pix2x(event.x) - self.v1.x - self.move_offset.x,
                       self.plane.pix2y(event.y) - self.v1.y - self.move_offset.y)
        move_pix = Vector2(event.x - self.plane.x2pix(self.v1.x) - self.move_offset_pix.x,
                           event.y - self.plane.y2pix(self.v1.y) - self.move_offset_pix.y)
        self.plane.canvas.move(self.name_v1, move_pix.x, move_pix.y)
        self.v1 += move
        self.recalculate_line()
        self.draw_dbg()
        self.draw_line()
        self.plane.update()

    def drag_v2(self, event):
        move = Vector2(self.plane.pix2x(event.x) - self.v2.x - self.move_offset.x,
                       self.plane.pix2y(event.y) - self.v2.y - self.move_offset.y)
        move_pix = Vector2(event.x - self.plane.x2pix(self.v2.x) - self.move_offset_pix.x,
                           event.y - self.plane.y2pix(self.v2.y) - self.move_offset_pix.y)
        self.plane.canvas.move(self.name_v2, move_pix.x, move_pix.y)
        self.v2 += move
        self.recalculate_line()
        self.draw_dbg()
        self.draw_line()
        self.plane.update()

    def drag_line(self, event):
        move = Vector2(self.plane.pix2x(event.x) - self.v1.x - self.move_offset.x,
                       self.plane.pix2y(event.y) - self.v1.y - self.move_offset.y)
        move_pix = Vector2(event.x - self.plane.x2pix(self.v1.x) - self.move_offset_pix.x,
                           event.y - self.plane.y2pix(self.v1.y) - self.move_offset_pix.y)
        self.plane.canvas.move(self.name, move_pix.x, move_pix.y)
        self.plane.canvas.move(self.name_v1, move_pix.x, move_pix.y)
        self.plane.canvas.move(self.name_v2, move_pix.x, move_pix.y)
        self.v1 += move
        self.v2 += move
        self.recalculate_line()
        self.draw_dbg()
        self.plane.update()

    def click_v1(self, event):
        self.move_offset = Vector2(self.plane.pix2x(event.x)-self.v1.x,
                                   self.plane.pix2y(event.y)-self.v1.y)
        self.move_offset_pix = Vector2(event.x-self.plane.x2pix(self.v1.x),
                                       event.y-self.plane.y2pix(self.v1.y))

    def click_v2(self, event):
        self.move_offset = Vector2(self.plane.pix2x(event.x)-self.v2.x,
                                   self.plane.pix2y(event.y)-self.v2.y)
        self.move_offset_pix = Vector2(event.x-self.plane.x2pix(self.v2.x),
                                       event.y-self.plane.y2pix(self.v2.y))


class RayCaster:
    def __init__(self, plane, v1, v2, name, color='grey', ray_color='red', dbg=False):
        self.plane = plane
        self.dbg = dbg
        self.color = color
        self.ray_color = ray_color
        self.name = name
        self.name_dbg = f'{name}Dbg'
        self.name_v1 = f'{name}v1'
        self.name_v2 = f'{name}v2'
        self.v1 = v1
        self.v2 = v2
        self.move_offset = Vector2()
        self.move_offset_pix = Vector2()
        self.line = Line.line_through_2p(v1, v2)

    def draw_dbg(self):
        if self.dbg:
            plane = self.plane
            plane.canvas.delete(self.name_dbg)
            x = self.v1.x + (self.v2.x - self.v1.x) / 2
            y = self.v1.y + (self.v2.y - self.v1.y) / 2
            if self.line.angle() >= 0:
                anchor = tkinter.SE
            else:
                anchor = tkinter.SW
            plane.canvas.create_text(plane.x2pix(x), plane.y2pix(y+5),
                                     text=(f'Name:  {self.name}\n'
                                           f'v1:    {self.v1}\n'
                                           f'v2:    {self.v2}\n'
                                           f'Alpha: {degrees(self.line.angle()).__round__(2)}'),
                                     fill=plane.color_ol, font=plane.font, anchor=anchor,
                                     tag=self.name_dbg)

    def draw(self):
        self.draw_dbg()
        self.draw_line()
        plane = self.plane
        plane.canvas.create_oval(plane.x2pix(self.v1.x-5), plane.y2pix(self.v1.y+5),
                                 plane.x2pix(self.v1.x+5), plane.y2pix(self.v1.y-5),
                                 fill=self.color, outline=self.color,
                                 tag=self.name_v1)
        plane.canvas.create_oval(plane.x2pix(self.v2.x-5), plane.y2pix(self.v2.y+5),
                                 plane.x2pix(self.v2.x+5), plane.y2pix(self.v2.y-5),
                                 fill=self.color, outline=self.color,
                                 tag=self.name_v2)

        plane.canvas.tag_bind(self.name_v1, '<Button-1>', self.click_v1)
        plane.canvas.tag_bind(self.name_v2, '<Button-1>', self.click_v2)
        plane.canvas.tag_bind(self.name_v1, '<B1-Motion>', self.drag_v1)
        plane.canvas.tag_bind(self.name_v2, '<B1-Motion>', self.drag_v2)

    def draw_line(self):
        plane = self.plane
        plane.canvas.delete(self.name)
        plane.canvas.create_line(plane.x2pix(self.v1.x), plane.y2pix(self.v1.y),
                                 plane.x2pix(self.v2.x), plane.y2pix(self.v2.y),
                                 fill=self.color, width=3,
                                 tag=self.name)

        plane.canvas.tag_raise(self.name_v1)
        plane.canvas.tag_raise(self.name_v2)
        plane.canvas.tag_bind(self.name, '<Button-1>', self.click_v1)
        plane.canvas.tag_bind(self.name, '<B1-Motion>', self.drag_line)

    def recalculate_line(self):
        self.line = Line.line_through_2p(self.v1, self.v2)

    def drag_v1(self, event):
        move = Vector2(self.plane.pix2x(event.x) - self.v1.x - self.move_offset.x,
                       self.plane.pix2y(event.y) - self.v1.y - self.move_offset.y)
        move_pix = Vector2(event.x - self.plane.x2pix(self.v1.x) - self.move_offset_pix.x,
                           event.y - self.plane.y2pix(self.v1.y) - self.move_offset_pix.y)
        self.plane.canvas.move(self.name_v1, move_pix.x, move_pix.y)
        self.v1 += move
        self.recalculate_line()
        self.draw_dbg()
        self.draw_line()
        self.plane.update()

    def drag_v2(self, event):
        move = Vector2(self.plane.pix2x(event.x) - self.v2.x - self.move_offset.x,
                       self.plane.pix2y(event.y) - self.v2.y - self.move_offset.y)
        move_pix = Vector2(event.x - self.plane.x2pix(self.v2.x) - self.move_offset_pix.x,
                           event.y - self.plane.y2pix(self.v2.y) - self.move_offset_pix.y)
        self.plane.canvas.move(self.name_v2, move_pix.x, move_pix.y)
        self.v2 += move
        self.recalculate_line()
        self.draw_dbg()
        self.draw_line()
        self.plane.update()

    def drag_line(self, event):
        move = Vector2(self.plane.pix2x(event.x) - self.v1.x - self.move_offset.x,
                       self.plane.pix2y(event.y) - self.v1.y - self.move_offset.y)
        move_pix = Vector2(event.x - self.plane.x2pix(self.v1.x) - self.move_offset_pix.x,
                           event.y - self.plane.y2pix(self.v1.y) - self.move_offset_pix.y)
        self.plane.canvas.move(self.name, move_pix.x, move_pix.y)
        self.plane.canvas.move(self.name_v1, move_pix.x, move_pix.y)
        self.plane.canvas.move(self.name_v2, move_pix.x, move_pix.y)
        self.v1 += move
        self.v2 += move
        self.recalculate_line()
        self.draw_dbg()
        self.plane.update()

    def click_v1(self, event):
        self.move_offset = Vector2(self.plane.pix2x(event.x)-self.v1.x,
                                   self.plane.pix2y(event.y)-self.v1.y)
        self.move_offset_pix = Vector2(event.x-self.plane.x2pix(self.v1.x),
                                       event.y-self.plane.y2pix(self.v1.y))

    def click_v2(self, event):
        self.move_offset = Vector2(self.plane.pix2x(event.x)-self.v2.x,
                                   self.plane.pix2y(event.y)-self.v2.y)
        self.move_offset_pix = Vector2(event.x-self.plane.x2pix(self.v2.x),
                                       event.y-self.plane.y2pix(self.v2.y))


class Polygon:
    def __init__(self, plane, v1, name, length, width, angle_l=pi/2, angle_r=pi/2, abs_refr_indx=1.65, dbg=False):
        self.plane = plane
        self.dbg = dbg
        self.name = name
        self.name_mask = f'{name}Mask'
        self.name_dbg = f'{name}Dbg'
        self.abs_refr_indx = abs_refr_indx
        self.angle_l = angle_l
        self.angle_r = angle_r
        self.move_offset = Vector2()
        self.move_offset_pix = Vector2()
        self.width = width
        if self.angle_r + self.angle_l == pi:
            self.length_t = self.length_b = length
        elif self.angle_l + self.angle_r < pi:  # top is shorter
            self.length_t = length
            self.length_b = length + self.width/tan(angle_l) + self.width/tan(angle_r)
        else:                                   # bottom is shorter
            self.length_t = length + self.width*tan(angle_l-pi/2) + self.width*tan(angle_r-pi/2)
            self.length_b = length

        self.v1 = v1
        self.v2 = Vector2(self.v1.x+self.length_t, self.v1.y)
        if self.angle_r == pi/2:
            self.v3 = Vector2(self.v2.x, self.v2.y-self.width)
        else:
            self.v3 = Vector2(self.width/tan(self.angle_r)+self.v2.x, -self.width+self.v2.y)
        self.v4 = Vector2(self.v3.x-self.length_b, self.v3.y)

        self.line12 = Line(0, 0, 0)
        self.line23 = Line(0, 0, 0)
        self.line34 = Line(0, 0, 0)
        self.line41 = Line(0, 0, 0)
        self.recalculate_lines()

    def draw_dbg(self):
        if self.dbg:
            plane = self.plane
            plane.canvas.delete(self.name_dbg)
            plane.canvas.create_text(plane.x2pix(self.v1.x), plane.y2pix(self.v1.y),
                                     text=(f'Name: {self.name}\n'
                                           f'v1:   {self.v1}\n'
                                           f'v2:   {self.v2}\n'
                                           f'v3:   {self.v3}\n'
                                           f'v4:   {self.v4}\n'
                                           f'AbsRefrIndx: {self.abs_refr_indx}\n'
                                           f'Width:       {self.width}\n'
                                           f'Length top:  {self.length_t}\n'
                                           f'Lenght bot:  {self.length_b}\n'
                                           f'Angle Left:  {degrees(self.angle_l).__round__(2)} deg\n'
                                           f'Angle Right: {degrees(self.angle_r).__round__(2)} deg'),
                                     fill=plane.color_ol, font=plane.font, anchor=tkinter.SW,
                                     tag=self.name_dbg)

    def draw(self):
        self.draw_dbg()
        plane = self.plane
        plane.canvas.create_polygon(plane.x2pix(self.v1.x), plane.y2pix(self.v1.y),
                                    plane.x2pix(self.v2.x), plane.y2pix(self.v2.y),
                                    plane.x2pix(self.v3.x), plane.y2pix(self.v3.y),
                                    plane.x2pix(self.v4.x), plane.y2pix(self.v4.y),
                                    fill=plane.color_fl, outline=plane.color_bg,
                                    tag=self.name_mask)
        plane.canvas.create_line(plane.x2pix(self.v1.x), plane.y2pix(self.v1.y),
                                 plane.x2pix(self.v2.x), plane.y2pix(self.v2.y),
                                 fill=plane.color_ol,
                                 tag=self.name)
        plane.canvas.create_line(plane.x2pix(self.v2.x), plane.y2pix(self.v2.y),
                                 plane.x2pix(self.v3.x), plane.y2pix(self.v3.y),
                                 fill=plane.color_ol,
                                 tag=self.name)
        plane.canvas.create_line(plane.x2pix(self.v3.x), plane.y2pix(self.v3.y),
                                 plane.x2pix(self.v4.x), plane.y2pix(self.v4.y),
                                 fill=plane.color_ol,
                                 tag=self.name)
        plane.canvas.create_line(plane.x2pix(self.v4.x), plane.y2pix(self.v4.y),
                                 plane.x2pix(self.v1.x), plane.y2pix(self.v1.y),
                                 fill=plane.color_ol,
                                 tag=self.name)
        plane.canvas.tag_bind(self.name_mask, '<Button-1>', self.click)
        plane.canvas.tag_bind(self.name_mask, '<B1-Motion>', self.drag)

    def intersections(self, line):
        result = []
        # top
        intr_point = self.line12.intersection_line(line)
        if intr_point is not None:
            if self.v1.x < intr_point.x < self.v2.x:
                result.append([intr_point, self.line12.intersection_angle(line), self.line12, self.abs_refr_indx])

        # right
        intr_point = self.line23.intersection_line(line)
        if intr_point is not None:
            if self.angle_r == pi/2:
                if self.v3.y <= intr_point.y <= self.v2.y:
                    result.append([intr_point, self.line23.intersection_angle(line), self.line23, self.abs_refr_indx])
            elif self.angle_r > pi/2:
                if self.v3.x <= intr_point.x <= self.v2.x:
                    result.append([intr_point, self.line23.intersection_angle(line), self.line23, self.abs_refr_indx])
            else:
                if self.v2.x <= intr_point.x <= self.v3.x:
                    result.append([intr_point, self.line23.intersection_angle(line), self.line23, self.abs_refr_indx])

        # down
        intr_point = self.line34.intersection_line(line)
        if intr_point is not None:
            if self.v4.x < intr_point.x < self.v3.x:
                result.append([intr_point, self.line34.intersection_angle(line), self.line34, self.abs_refr_indx])

        # left
        intr_point = self.line41.intersection_line(line)
        if intr_point is not None:
            if self.angle_l == pi/2:
                if self.v4.y <= intr_point.y <= self.v1.y:
                    result.append([intr_point, self.line41.intersection_angle(line), self.line41, self.abs_refr_indx])
            elif self.angle_l > pi/2:
                if self.v1.x <= intr_point.x <= self.v4.x:
                    result.append([intr_point, self.line41.intersection_angle(line), self.line41, self.abs_refr_indx])
            else:
                if self.v4.x <= intr_point.x <= self.v1.x:
                    result.append([intr_point, self.line41.intersection_angle(line), self.line41, self.abs_refr_indx])

        return result

    def recalculate_lines(self):
        self.line12 = Line.line_through_2p(self.v1, self.v2)
        self.line23 = Line.line_through_2p(self.v2, self.v3)
        self.line34 = Line.line_through_2p(self.v3, self.v4)
        self.line41 = Line.line_through_2p(self.v4, self.v1)

    def drag(self, event):
        move = Vector2(self.plane.pix2x(event.x) - self.v1.x - self.move_offset.x,
                       self.plane.pix2y(event.y) - self.v1.y - self.move_offset.y)
        move_pix = Vector2(event.x - self.plane.x2pix(self.v1.x) - self.move_offset_pix.x,
                           event.y - self.plane.y2pix(self.v1.y) - self.move_offset_pix.y)
        self.plane.canvas.move(self.name, move_pix.x, move_pix.y)
        self.plane.canvas.move(self.name_mask, move_pix.x, move_pix.y)
        self.v1 += move
        self.v2 += move
        self.v3 += move
        self.v4 += move
        self.recalculate_lines()
        self.draw_dbg()
        self.plane.update()

    def click(self, event):
        self.move_offset = Vector2(self.plane.pix2x(event.x)-self.v1.x,
                                   self.plane.pix2y(event.y)-self.v1.y)
        self.move_offset_pix = Vector2(event.x-self.plane.x2pix(self.v1.x),
                                       event.y-self.plane.y2pix(self.v1.y))


class Lens:
    def __init__(self, plane, v1, name, length, width, rad_l, rad_r, abs_refr_indx=1.65, dbg=False):
        self.dbg = dbg
        self.name = name
        self.plane = plane
        self.name_mask = f'{name}Mask'
        self.name_dbg = f'{name}Dbg'
        self.abs_refr_indx = abs_refr_indx
        self.length = length
        self.width = width
        self.convex_l = True if (rad_l >= 0) else False
        self.convex_r = True if (rad_r >= 0) else False
        self.v1 = v1
        self.v2 = Vector2(v1.x + length, v1.y)
        self.v3 = Vector2(self.v2.x, self.v2.y-width)
        self.v4 = Vector2(v1.x, v1.y-width)
        self.line12 = Line.line_through_2p(self.v1, self.v2)
        self.line34 = Line.line_through_2p(self.v3, self.v4)
        self.move_offset = Vector2()
        self.move_offset_pix = Vector2()
        self.rad_l = abs(rad_l)
        self.rad_r = abs(rad_r)
        self.alpha_l = asin(width/(2*self.rad_l))
        self.alpha_r = asin(width/(2*self.rad_r))
        if self.convex_l:
            self.center_l = Vector2(self.v1.x + self.rad_l * cos(self.alpha_l), self.v1.y - width / 2)
        else:
            self.center_l = Vector2(self.v1.x - self.rad_l * cos(self.alpha_l), self.v1.y - width / 2)
        if self.convex_r:
            self.center_r = Vector2(self.v2.x - self.rad_r * cos(self.alpha_r), self.v2.y - width / 2)
        else:
            self.center_r = Vector2(self.v2.x + self.rad_r * cos(self.alpha_r), self.v2.y - width / 2)

    def draw_dbg(self):
        if self.dbg:
            plane = self.plane
            plane.canvas.delete(self.name_dbg)
            # plane.canvas.create_oval(plane.x2pix(self.center_l.x - 2), plane.y2pix(self.center_l.y + 2),
            #                          plane.x2pix(self.center_l.x + 2), plane.y2pix(self.center_l.y - 2),
            #                          fill=plane.color_ol, outline=plane.color_ol,
            #                          tag=self.name_dbg)
            # plane.canvas.create_oval(plane.x2pix(self.center_r.x - 2), plane.y2pix(self.center_r.y + 2),
            #                          plane.x2pix(self.center_r.x + 2), plane.y2pix(self.center_r.y - 2),
            #                          fill=plane.color_ol, outline=plane.color_ol,
            #                          tag=self.name_dbg)
            plane.canvas.create_text(plane.x2pix(self.v1.x), plane.y2pix(self.v1.y),
                                     text=(f'Name: {self.name}\n'
                                           f'v1:   {self.v1}\n'
                                           f'v2:   {self.v2}\n'
                                           f'v3:   {self.v3}\n'
                                           f'v4:   {self.v4}\n'
                                           f'AbsRefrIndx: {self.abs_refr_indx}\n'
                                           f'Width:    {self.width}\n'
                                           f'Length:   {self.length}\n'
                                           f'Center l: {self.center_l}\n'
                                           f'Center r: {self.center_r}\n'
                                           f'R left:   {self.rad_l}\n'
                                           f'R right:  {self.rad_r}'),
                                     fill=plane.color_ol, font=plane.font, anchor=tkinter.SW,
                                     tag=self.name_dbg)

    def draw(self):
        self.draw_dbg()
        plane = self.plane

        start_l = degrees(pi-self.alpha_l) if self.convex_l else degrees(-self.alpha_l)
        start_r = degrees(-self.alpha_r) if self.convex_r else degrees(pi - self.alpha_r)

        plane.canvas.create_arc(plane.x2pix(self.center_l.x - self.rad_l), plane.y2pix(self.center_l.y + self.rad_l),
                                plane.x2pix(self.center_l.x + self.rad_l), plane.y2pix(self.center_l.y - self.rad_l),
                                start=start_l, extent=degrees(self.alpha_l*2),
                                fill=plane.color_fl, outline=plane.color_bg,
                                style=tkinter.CHORD, tag=self.name_mask)
        plane.canvas.create_arc(plane.x2pix(self.center_r.x - self.rad_r), plane.y2pix(self.center_r.y + self.rad_r),
                                plane.x2pix(self.center_r.x + self.rad_r), plane.y2pix(self.center_r.y - self.rad_r),
                                start=start_r, extent=degrees(self.alpha_r*2),
                                fill=plane.color_fl, outline=plane.color_bg,
                                style=tkinter.CHORD, tag=self.name_mask)
        plane.canvas.create_polygon(plane.x2pix(self.v1.x), plane.y2pix(self.v1.y),
                                    plane.x2pix(self.v2.x), plane.y2pix(self.v2.y),
                                    plane.x2pix(self.v3.x), plane.y2pix(self.v3.y),
                                    plane.x2pix(self.v4.x), plane.y2pix(self.v4.y),
                                    fill=plane.color_fl, outline=plane.color_bg,
                                    tag=self.name_mask)
        plane.canvas.create_arc(plane.x2pix(self.center_l.x - self.rad_l), plane.y2pix(self.center_l.y + self.rad_l),
                                plane.x2pix(self.center_l.x + self.rad_l), plane.y2pix(self.center_l.y - self.rad_l),
                                start=start_l, extent=degrees(self.alpha_l*2),
                                outline=plane.color_ol,
                                style=tkinter.ARC, tag=self.name)
        plane.canvas.create_arc(plane.x2pix(self.center_r.x - self.rad_r), plane.y2pix(self.center_r.y + self.rad_r),
                                plane.x2pix(self.center_r.x + self.rad_r), plane.y2pix(self.center_r.y - self.rad_r),
                                start=start_r, extent=degrees(self.alpha_r*2),
                                outline=plane.color_ol,
                                style=tkinter.ARC, tag=self.name)
        plane.canvas.create_line(plane.x2pix(self.v1.x), plane.y2pix(self.v1.y),
                                 plane.x2pix(self.v2.x), plane.y2pix(self.v2.y),
                                 tag=self.name,
                                 fill=plane.color_ol)
        plane.canvas.create_line(plane.x2pix(self.v3.x), plane.y2pix(self.v3.y),
                                 plane.x2pix(self.v4.x), plane.y2pix(self.v4.y),
                                 tag=self.name,
                                 fill=plane.color_ol)
        plane.canvas.tag_bind(self.name_mask, '<Button-1>', self.click)
        plane.canvas.tag_bind(self.name_mask, '<B1-Motion>', self.drag)

    def intersections(self, line):
        result = []

        # top
        intr_point = self.line12.intersection_line(line)
        if intr_point is not None:
            if self.v1.x <= intr_point.x <= self.v2.x:
                result.append([intr_point, self.line12.intersection_angle(line), self.line12, self.abs_refr_indx])

        # right
        intr_points = line.intersection_circle(self.center_r, self.rad_r)
        for intr_point in intr_points:
            if self.center_r.y-self.width/2 <= intr_point.y <= self.center_r.y+self.width/2:
                tangent = Line.line_tangent_to_circle(intr_point, self.center_r, self.rad_r)
                if self.convex_r:
                    if intr_point.x >= self.center_r.x:
                        result.append([intr_point, tangent.intersection_angle(line), tangent, self.abs_refr_indx])
                else:
                    if intr_point.x <= self.center_r.x:
                        result.append([intr_point, tangent.intersection_angle(line), tangent, self.abs_refr_indx])

        # bottom
        intr_point = self.line34.intersection_line(line)
        if intr_point is not None:
            if self.v4.x <= intr_point.x <= self.v3.x:
                result.append([intr_point, self.line34.intersection_angle(line), self.line34, self.abs_refr_indx])

        # left
        intr_points = line.intersection_circle(self.center_l, self.rad_l)
        for intr_point in intr_points:
            if self.center_l.y-self.width/2 <= intr_point.y <= self.center_l.y+self.width/2:
                tangent = Line.line_tangent_to_circle(intr_point, self.center_l, self.rad_l)
                if self.convex_l:
                    if intr_point.x <= self.center_l.x:
                        result.append([intr_point, tangent.intersection_angle(line), tangent, self.abs_refr_indx])
                else:
                    if intr_point.x >= self.center_l.x:
                        result.append([intr_point, tangent.intersection_angle(line), tangent, self.abs_refr_indx])

        return result

    def recalculate_lines(self):
        self.line12 = Line.line_through_2p(self.v1, self.v2)
        self.line34 = Line.line_through_2p(self.v3, self.v4)

    def drag(self, event):
        move = Vector2(self.plane.pix2x(event.x) - self.v1.x - self.move_offset.x,
                       self.plane.pix2y(event.y) - self.v1.y - self.move_offset.y)
        move_pix = Vector2(event.x - self.plane.x2pix(self.v1.x) - self.move_offset_pix.x,
                           event.y - self.plane.y2pix(self.v1.y) - self.move_offset_pix.y)
        self.plane.canvas.move(self.name, move_pix.x, move_pix.y)
        self.plane.canvas.move(self.name_mask, move_pix.x, move_pix.y)
        self.v1 += move
        self.v2 += move
        self.v3 += move
        self.v4 += move
        self.center_l += move
        self.center_r += move
        self.recalculate_lines()
        self.draw_dbg()
        self.plane.update()

    def click(self, event):
        self.move_offset = Vector2(self.plane.pix2x(event.x)-self.v1.x,
                                   self.plane.pix2y(event.y)-self.v1.y)
        self.move_offset_pix = Vector2(event.x-self.plane.x2pix(self.v1.x),
                                       event.y-self.plane.y2pix(self.v1.y))


class Plane:
    def __init__(self, tk_root, resolution=(1280, 720), dbg=False):
        self.root = tk_root
        self.dbg = dbg
        self.color_bg = 'white'
        self.color_ol = 'black'
        self.color_fl = 'white'
        self.font = ('consolas', '8')
        self.name_dbg = 'dbg'
        self.name_ray = 'ray'
        self.res_x = resolution[0]
        self.res_y = resolution[1]
        self.pix_x0 = self.res_x//2
        self.pix_y0 = self.res_y//2
        self.move_offset = Vector2()
        self.move_offset_pix = Vector2()
        self.canvas = tkinter.Canvas(tk_root, width=self.res_x, height=self.res_y, bg=self.color_bg)
        self.canvas.pack()
        self.max_recursion_depth = 25
        self.abs_refr_indx = 1.0
        self.s = 4
        self.tools_list = [
            Ruler(self, Vector2(0, 0), Vector2(100, 0), 'Ruler', dbg=False),
            RayCaster(self, Vector2(-500, 15*self.s), Vector2(-475, 15*self.s), 'RayCaster1', ray_color='red', dbg=True),
            RayCaster(self, Vector2(-500, 7.5*self.s), Vector2(-475, 7.5*self.s), 'RayCaster2', ray_color='green', dbg=True),
            RayCaster(self, Vector2(-500, -7.5*self.s), Vector2(-475, -7.5*self.s), 'RayCaster3', ray_color='blue', dbg=True),
            RayCaster(self, Vector2(-500, -15*self.s), Vector2(-475, -15*self.s), 'RayCaster4', ray_color='purple', dbg=True)
        ]

        self.obj_list = [
            Polygon(self, Vector2(200, 0), 'PolygonTest', length=80, width=150, angle_l=radians(60), angle_r=radians(60), dbg=True),
            # Lens(self, Vector2(-200, 0), 'LensTest', length=20, width=140, rad_l=140, rad_r=140, dbg=True)
            # Lens(self, Vector2(-10, 259), 'Lens1', length=10, width=518, rad_l=297.14, rad_r=-975.8, abs_refr_indx=1.475, dbg=True),
            # Lens(self, Vector2(-15, 347.5), 'Lens2', length=15, width=695, rad_l=529.45, rad_r=2096.50, abs_refr_indx=1.475, dbg=True),
            # Lens(self, Vector2(-20, 570), 'Lens3', length=20, width=1140, rad_l=848.41, rad_r=1000000000.0, abs_refr_indx=1.4575, dbg=True),
            # Lens(self, Vector2(-140, 447.5), 'Lens4', length=140, width=895, rad_l=2921.96, rad_r=2921.96, abs_refr_indx=1.4575, dbg=True),
            # Lens(self, Vector2(-140, 447.5), 'None', length=140, width=895, rad_l=2921.96, rad_r=2921.96, abs_refr_indx=1.4575, dbg=True),

            Lens(self, Vector2(-1.0*self.s, 25.9*self.s), 'Lens1', length=1.0*self.s, width=51.8*self.s, rad_l=29.*self.s, rad_r=-97.58*self.s, abs_refr_indx=1.475, dbg=True),
            Lens(self, Vector2(-1.0*self.s, 25.9*self.s), 'Lens1R', length=1.0*self.s, width=51.8*self.s, rad_l=-97.58*self.s, rad_r=29.714*self.s, abs_refr_indx=1.475, dbg=True),
            Lens(self, Vector2(-1.5*self.s, 34.75*self.s), 'Lens2', length=1.5*self.s, width=69.5*self.s, rad_l=52.945*self.s, rad_r=209.650*self.s, abs_refr_indx=1.475, dbg=True),
            Lens(self, Vector2(-1.5*self.s, 34.75*self.s), 'Lens2R', length=1.5*self.s, width=69.5*self.s, rad_l=209.650*self.s, rad_r=52.945*self.s, abs_refr_indx=1.475, dbg=True),
            #Lens(self, Vector2(-2.0*self.s, 57.0*self.s), 'Lens3', length=2.0*self.s, width=114.0*self.s, rad_l=84.841*self.s, rad_r=1000000000.0, abs_refr_indx=1.4575, dbg=True),
            #Lens(self, Vector2(-2.0*self.s, 57.0*self.s), 'Lens3R', length=2.0*self.s, width=114.0*self.s, rad_l=1000000000.0, rad_r=84.841*self.s, abs_refr_indx=1.4575, dbg=True),
            Lens(self, Vector2(-14.0*self.s, 44.75*self.s), 'Lens4', length=14.0*self.s, width=89.5*self.s, rad_l=292.196*self.s, rad_r=292.196*self.s, abs_refr_indx=1.4575, dbg=True),
            Lens(self, Vector2(-0.5 * self.s, 5.5 * self.s), 'Lens5', length=0.5 * self.s, width=11 * self.s, rad_l=11.25 * self.s, rad_r=11.25 * self.s, abs_refr_indx=1.4575, dbg=True),
        ]

        self.canvas.bind('<Button-3>', self.click)
        self.canvas.bind('<B3-Motion>', self.drag)

    def update(self):
        t = time.time()
        self.canvas.delete(self.name_ray, self.name_dbg)



        for tool in self.tools_list:
            if isinstance(tool, RayCaster):
                if tool.v2.x > tool.v1.x:
                    pos_dir = True
                elif tool.v2.x < tool.v1.x:
                    pos_dir = False
                else:
                    if tool.v2.y >= tool.v1.y:
                        pos_dir = True
                    else:
                        pos_dir = False
                self.cast_ray(tool.v2, tool.line, pos_dir, self.abs_refr_indx, color=tool.ray_color)

        self.canvas.tag_lower(self.name_dbg)

        t = time.time() - t
        self.canvas.create_text(3, 3, text=f'{int(1 / t) if t >= 0.0005 else "inf"} FPS\n{int(t * 1000)} ms',
                                font=self.font, anchor=tkinter.NW, tag=self.name_dbg)

        line_x = Line(0, 1, 0)
        line_y = Line(1, 0, 0)
        self.draw_line(line_x, 'grey', self.name_dbg)
        self.draw_line(line_y, 'grey', self.name_dbg)

    def x2pix(self, x):
        return self.pix_x0 + x

    def y2pix(self, y):
        return self.pix_y0 - y

    def pix2x(self, pix_x):
        return pix_x - self.pix_x0

    def pix2y(self, pix_y):
        return self.pix_y0 - pix_y

    def add_obj(self, obj):
        pass

    def intersections(self, line):
        result = []
        ext = 100000
        # top
        intr_point = Line(0, 1, -self.pix2y(0-ext)).intersection_line(line)
        if intr_point is not None:
            if self.pix2x(0-ext) < intr_point.x < self.pix2x(self.res_x+ext):
                result.append(intr_point)
        # right
        intr_point = Line(1, 0, -self.pix2x(self.res_x+ext)).intersection_line(line)
        if intr_point is not None:
            if self.pix2y(self.res_y+ext) <= intr_point.y <= self.pix2y(0-ext):
                result.append(intr_point)
        # bot
        intr_point = Line(0, 1, -self.pix2y(self.res_y+ext)).intersection_line(line)
        if intr_point is not None:
            if self.pix2x(0-ext) < intr_point.x < self.pix2x(self.res_x+ext):
                result.append(intr_point)
        # left
        intr_point = Line(1, 0, -self.pix2x(0-ext)).intersection_line(line)
        if intr_point is not None:
            if self.pix2y(self.res_y+ext) <= intr_point.y <= self.pix2y(0-ext):
                result.append(intr_point)
        return result

    def cast_ray(self, origin, line, positive_dir, refr_indx, color='red', recursion_depth=0):
        if recursion_depth > self.max_recursion_depth:
            if self.dbg:
                print('Recursion gone too deep')
            return None
        eps = 0.001
        collision = None
        min_dist = inf
        for obj in self.obj_list:
            for intr_info in obj.intersections(line):
                if positive_dir:
                    if line.is_vertical():
                        if intr_info[0].y < origin.y + eps:
                            continue
                    else:
                        if intr_info[0].x < origin.x + eps:
                            continue
                else:
                    if line.is_vertical():
                        if intr_info[0].y > origin.y - eps:
                            continue
                    else:
                        if intr_info[0].x > origin.x - eps:
                            continue
                distance = origin.dist(intr_info[0])
                if distance < min_dist:
                    min_dist = distance
                    collision = intr_info

        if collision is not None:
            if self.dbg:
                self.draw_line(collision[2], color='grey', tag=self.name_dbg, dash=(4, 2))

            n1 = refr_indx
            if collision[3] == n1:
                n2 = self.abs_refr_indx
            else:
                n2 = collision[3]
            angle = collision[1]

            if angle != 0:
                alpha = angle/fabs(angle) * (pi/2 - fabs(angle))
            else:
                alpha = pi/2

            beta_tmp = sin(alpha)*n1/n2
            if -1 <= beta_tmp <= 1:
                beta = asin(beta_tmp)
                angle = alpha - beta
                refr_line = line.rotate(collision[0], angle)
                refr_pos_dir = refr_line.direction(origin, collision[0], collision[2], get_through=True)

                self.cast_ray(collision[0], refr_line, refr_pos_dir, refr_indx=n2, color=color, recursion_depth=recursion_depth+1)
            else:
                refl_line = line.rotate(collision[0], -collision[1] * 2)
                refl_pos_dir = refl_line.direction(origin, collision[0], collision[2], get_through=False)

                self.cast_ray(collision[0], refl_line, refl_pos_dir, refr_indx=refr_indx, color=color,
                              recursion_depth=recursion_depth + 1)

            self.canvas.create_line(self.x2pix(origin.x), self.y2pix(origin.y),
                                    self.x2pix(collision[0].x), self.y2pix(collision[0].y),
                                    fill=color, tag=self.name_ray)
            if self.dbg:
                self.canvas.create_oval(self.x2pix(collision[0].x - 2), self.y2pix(collision[0].y + 2),
                                        self.x2pix(collision[0].x + 2), self.y2pix(collision[0].y - 2),
                                        fill=color, outline=color, tag=self.name_dbg)

                self.canvas.create_text(self.x2pix(collision[0].x), self.y2pix(collision[0].y + 10),
                                        text=f'{degrees(collision[1]).__round__(1)}',
                                        fill=color, font=self.font, tag=self.name_dbg)
        else:
            point = None
            for intr_point in self.intersections(line):
                if positive_dir:
                    if line.is_vertical():
                        if intr_point.y < origin.y:
                            continue
                    else:
                        if intr_point.x < origin.x:
                            continue
                else:
                    if line.is_vertical():
                        if intr_point.y > origin.y:
                            continue
                    else:
                        if intr_point.x > origin.x:
                            continue
                point = intr_point
            if point is not None:
                self.canvas.create_line(self.x2pix(origin.x), self.y2pix(origin.y),
                                        self.x2pix(point.x), self.y2pix(point.y),
                                        fill=color, tag=self.name_ray)

    def draw(self):
        for i in self.obj_list:
            i.draw()
        for i in self.tools_list:
            i.draw()

    def draw_line(self, line, color='black', tag=None, dash=None):
        intr = self.intersections(line)
        if len(intr) > 1:
            self.canvas.create_line(self.x2pix(intr[0].x), self.y2pix(intr[0].y),
                                    self.x2pix(intr[1].x), self.y2pix(intr[1].y),
                                    fill=color, tag=tag, dash=dash)

    def drag(self, event):
        move = Vector2(self.pix2x(event.x) - self.pix2x(self.pix_x0) - self.move_offset.x,
                       self.pix2y(event.y) - self.pix2y(self.pix_y0) - self.move_offset.y)
        move_pix = Vector2(event.x - self.pix_x0 - self.move_offset_pix.x,
                           event.y - self.pix_y0 - self.move_offset_pix.y)
        self.canvas.move('all', move_pix.x, move_pix.y)
        self.pix_x0 += move_pix.x
        self.pix_y0 += move_pix.y
        self.update()

    def click(self, event):
        self.move_offset = Vector2(self.pix2x(event.x)-self.pix2x(self.pix_x0),
                                   self.pix2y(event.y)-self.pix2y(self.pix_y0))
        self.move_offset_pix = Vector2(event.x-self.pix_x0,
                                       event.y-self.pix_y0)


if __name__ == '__main__':
    root = tkinter.Tk()
    pl = Plane(root, (1280, 720))
    pl.draw()
    pl.update()
    root.mainloop()
