import tkinter
from math import *
import time
import keyboard as kb


class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return None

    def dist(self, vector2):
        return ((vector2.x - self.x)**2 + (vector2.y - self.y)**2)**0.5


class Point:
    def __init__(self, name, coords, canvas):
        self.fill = 'red'
        self.outline = 'black'
        self.coords = coords
        self.coords_plane = Vector2(coords.x, plane.pry(coords.y))
        self.name = name
        self.canvas = canvas
        self.cl = Vector2()
        self.id = self.canvas.create_oval(self.coords.x-4, self.coords.y-4,
                                          self.coords.x+4, self.coords.y+4,
                                          fill=self.fill, outline=self.outline,
                                          tag=self.name)
        self.canvas.tag_bind(self.name, '<B1-Motion>', self.drag)
        self.canvas.tag_bind(self.name, '<Button-1>', self.click)

    def drag(self, event):
        self.canvas.move(self.id, event.x - (self.coords.x + self.cl.x), event.y - (self.coords.y + self.cl.y))
        self.coords.x = event.x - self.cl.x
        self.coords.y = event.y - self.cl.y
        self.coords_plane.x = self.coords.x
        self.coords_plane.y = plane.pry(self.coords.y)

    def click(self, event):
        self.cl.x = event.x - self.coords.x
        self.cl.y = event.y - self.coords.y


class Line:
    def __init__(self, name, canvas):
        self.name = name
        self.color = 'red'
        self.canvas = canvas
        self.v1 = Point(f'{self.name}_v1', Vector2(10, 100), self.canvas)
        self.v2 = Point(f'{self.name}_v2', Vector2(50, 100), self.canvas)
        self.a = None
        self.b = None
        self.c = None
        self.pos_dir = True
        self.calc_line()

    def calc_line(self):
        with self.v1.coords_plane as v1, self.v2.coords_plane as v2:
            self.a = v2.y-v1.y
            self.b = v1.x-v2.x
            self.c = v2.x*v1.y-v1.x*v2.y
            if self.b != 0:
                if v2.x > v1.x:
                    self.pos_dir = True
                else:
                    self.pos_dir = False
            else:
                if v2.y > v1.y:
                    self.pos_dir = True
                else:
                    self.pos_dir = False

    def draw(self, dbg=False):
        self.calc_line()
        self.canvas.create_line(self.v1.coords.x, self.v1.coords.y,
                                self.v2.coords.x, self.v2.coords.y,
                                fill=self.color, tag=self.name)
        if dbg:
            self.canvas.create_text(self.v1.coords.x, self.v1.coords.y-10,
                                    text=(f'Name: {self.v1.name}\n'
                                          f'x: {self.v1.coords_plane.x}\n'
                                          f'y: {self.v1.coords_plane.y}'),
                                    tag=self.name,
                                    fill=self.color, font=('consolas', '8'), anchor=tkinter.SW
                                    )
            self.canvas.create_text(self.v2.coords.x, self.v2.coords.y-10,
                                    text=(f'Name: {self.v2.name}\n'
                                          f'x: {self.v2.coords_plane.x}\n'
                                          f'y: {self.v2.coords_plane.y}\n'
                                          f'Pos dir: {self.pos_dir}\n'
                                          f'a: {self.a}\n'
                                          f'b: {self.b}\n'
                                          f'c: {self.c}'),
                                    tag=self.name,
                                    fill=self.color, font=('consolas', '8'), anchor=tkinter.SW
                                    )

class Polygon:
    def __init__(self, base, name, length, width, angle_l=pi/2, angle_r=pi/2, abs_refr_indx=1.65):
        self.dbg_colors = ['blue', 'red', 'green', 'purple']
        self.color = 'black'
        self.name = name
        self.abs_refr_indx = abs_refr_indx
        self.angle_l = angle_l
        self.angle_r = angle_r
        self.width = width
        if self.angle_r + self.angle_l == pi:
            self.length_t = self.length_b = length
        elif self.angle_l + self.angle_r < pi:  # короткая сверху
            self.length_t = length
            self.length_b = length + self.width/tan(angle_l) + self.width/tan(angle_r)
        else:                                   # короткая снизу
            self.length_t = length + self.width*tan(angle_l-pi/2) + self.width*tan(angle_r-pi/2)
            self.length_b = length
        self.coords = []
        self.coords.append(base)
        self.coords.append(Vector2(base.x+self.length_t, base.y))

        if self.angle_r == pi/2:
            self.coords.append(Vector2(self.coords[1].x, self.coords[1].y-self.width))
        else:
            self.coords.append(Vector2(self.width/tan(self.angle_r)+self.coords[1].x, -self.width+self.coords[1].y))
        self.coords.append(Vector2(self.coords[2].x-self.length_b, self.coords[2].y))

    def draw(self, canvas, y_mod, dbg=False):
        if dbg:
            col_l = self.dbg_colors[0]
            col_r = self.dbg_colors[1]
            col_t = self.dbg_colors[2]
            col_b = self.dbg_colors[3]
            canvas.create_text(self.coords[0].x, y_mod - self.coords[0].y,
                               text=(f'Name: {self.name}\n'
                                     f'V1: {self.coords[0]}\n'
                                     f'V2: {self.coords[1]}\n'
                                     f'V3: {self.coords[2]}\n'
                                     f'V4: {self.coords[3]}\n'
                                     f'Width:  {self.width}\n'
                                     f'Length top: {self.length_t}\n'
                                     f'Lenght bot: {self.length_b}\n'
                                     f'Angle Left:  {self.angle_l.__round__(2)} rad {degrees(self.angle_l).__round__(2)} deg\n'
                                     f'Angle Right: {self.angle_r.__round__(2)} rad {degrees(self.angle_r).__round__(2)} deg'),
                               fill=self.color, font=('consolas', '8'), anchor=tkinter.SW, tag='dbg'
                               )
        else:
            col_l = col_r = col_t = col_b = self.color
        canvas.delete(self.name)
        canvas.create_line(self.coords[0].x, y_mod-self.coords[0].y,
                           self.coords[1].x, y_mod-self.coords[1].y,
                           tag=self.name,
                           fill=col_t)
        canvas.create_line(self.coords[1].x, y_mod-self.coords[1].y,
                           self.coords[2].x, y_mod-self.coords[2].y,
                           tag=self.name,
                           fill=col_r)
        canvas.create_line(self.coords[2].x, y_mod-self.coords[2].y,
                           self.coords[3].x, y_mod-self.coords[3].y,
                           tag=self.name,
                           fill=col_b)
        canvas.create_line(self.coords[3].x, y_mod-self.coords[3].y,
                           self.coords[0].x, y_mod-self.coords[0].y,
                           tag=self.name,
                           fill=col_l)

    def intersections(self, a, b, c):
        result = []
        # top
        v1, v2 = self.coords[0], self.coords[1]
        intr = calc_intersection(a, b, c, v2.y-v1.y, v1.x-v2.x, v2.x*v1.y-v1.x*v2.y)
        if intr is not None:
            if v1.x < intr[0].x < v2.x:
                result.append(intr+[self.abs_refr_indx])

        # right
        v1, v2 = self.coords[1], self.coords[2]
        intr = calc_intersection(a, b, c, v2.y - v1.y, v1.x - v2.x, v2.x * v1.y - v1.x * v2.y)
        if intr is not None:
            if self.angle_r == pi/2:
                if v2.y <= intr[0].y <= v1.y:
                    result.append(intr+[self.abs_refr_indx])
            elif self.angle_r > pi/2:
                if v2.x <= intr[0].x <= v1.x:
                    result.append(intr+[self.abs_refr_indx])
            else:
                if v1.x <= intr[0].x <= v2.x:
                    result.append(intr+[self.abs_refr_indx])

        # down
        v1, v2 = self.coords[3], self.coords[2]
        intr = calc_intersection(a, b, c, v2.y - v1.y, v1.x - v2.x, v2.x * v1.y - v1.x * v2.y)
        if intr is not None:
            if v1.x < intr[0].x < v2.x:
                result.append(intr+[self.abs_refr_indx])

        # left
        v1, v2 = self.coords[3], self.coords[0]
        intr = calc_intersection(a, b, c, v2.y - v1.y, v1.x - v2.x, v2.x * v1.y - v1.x * v2.y)
        if intr is not None:
            if self.angle_l == pi/2:
                if v1.y <= intr[0].y <= v2.y:
                    result.append(intr+[self.abs_refr_indx])
            elif self.angle_l > pi / 2:
                if v2.x <= intr[0].x <= v1.x:
                    result.append(intr+[self.abs_refr_indx])
            else:
                if v1.x <= intr[0].x <= v2.x:
                    result.append(intr+[self.abs_refr_indx])

        return result


class Lens:
    def __init__(self, base, name, length, width, rad_l, rad_r, abs_refr_indx=1.65):
        self.dbg_colors = ['blue', 'red', 'green', 'purple']
        self.color = 'black'
        self.name = name
        self.abs_refr_indx = abs_refr_indx
        self.length = length
        self.width = width
        self.convex_l = True if (rad_l >= 0) else False
        self.convex_r = True if (rad_r >= 0) else False
        self.base_l = base
        self.base_r = Vector2(base.x+length, base.y)
        self.rad_l = abs(rad_l)
        self.rad_r = abs(rad_r)
        self.alpha_l = asin(width/(2*self.rad_l))
        self.alpha_r = asin(width/(2*self.rad_r))
        if self.convex_l:
            self.centre_l = Vector2(self.base_l.x+self.rad_l*cos(self.alpha_l), self.base_l.y-width/2)
        else:
            self.centre_l = Vector2(self.base_l.x-self.rad_l*cos(self.alpha_l), self.base_l.y-width/2)
        if self.convex_r:
            self.centre_r = Vector2(self.base_r.x-self.rad_r*cos(self.alpha_r), self.base_r.y-width/2)
        else:
            self.centre_r = Vector2(self.base_r.x+self.rad_r*cos(self.alpha_r), self.base_r.y-width/2)

    def draw(self, canvas, y_mod, dbg=False):
        if dbg:
            col_l = self.dbg_colors[0]
            col_r = self.dbg_colors[1]
            col_u = self.dbg_colors[2]
            col_d = self.dbg_colors[3]
            canvas.create_oval(self.centre_l.x - 2, y_mod - self.centre_l.y + 2,
                               self.centre_l.x + 2, y_mod - self.centre_l.y - 2,
                               fill=col_l, outline=col_l, tag='dbg')
            canvas.create_oval(self.centre_r.x - 2, y_mod - self.centre_r.y + 2,
                               self.centre_r.x + 2, y_mod - self.centre_r.y - 2,
                               fill=col_r, outline=col_r, tag='dbg')
            canvas.create_text(self.base_l.x, y_mod-self.base_l.y,
                               text=(f'Name: {self.name}\n'
                                     f'Base: {self.base_l}\n'
                                     f'Width:  {self.width}\n'
                                     f'Length: {self.length}\n'
                                     f'R left:  {self.rad_l}\n'
                                     f'R right: {self.rad_l}'),
                               fill=self.color, font=('consolas', '8'), anchor=tkinter.SW, tag='dbg'
                               )
        else:
            col_l = col_r = col_u = col_d = self.color
        canvas.delete(self.name)
        start = degrees(pi-self.alpha_l) if self.convex_l else degrees(-self.alpha_l)
        canvas.create_arc(self.centre_l.x-self.rad_l, y_mod-(self.centre_l.y+self.rad_l),
                          self.centre_l.x+self.rad_l, y_mod-(self.centre_l.y-self.rad_l),
                          start=start, extent=degrees(self.alpha_l*2),
                          style=tkinter.ARC, tag=self.name,
                          outline=col_l)
        start = degrees(-self.alpha_r) if self.convex_r else degrees(pi-self.alpha_r)
        canvas.create_arc(self.centre_r.x - self.rad_r, y_mod - (self.centre_r.y + self.rad_r),
                          self.centre_r.x + self.rad_r, y_mod - (self.centre_r.y - self.rad_r),
                          start=start, extent=degrees(self.alpha_r*2),
                          style=tkinter.ARC, tag=self.name,
                          outline=col_r)
        canvas.create_line(self.base_l.x, y_mod-self.base_l.y,
                           self.base_r.x, y_mod-self.base_r.y,
                           tag=self.name,
                           fill=col_u)
        canvas.create_line(self.base_l.x, y_mod - (self.base_l.y-self.width),
                           self.base_r.x, y_mod - (self.base_r.y-self.width),
                           tag=self.name,
                           fill=col_d)

    def intersections(self, a, b, c):
        result = []

        # top
        intr = calc_intersection(a, b, c, 0, 1, -self.base_l.y)
        if intr is not None:
            if self.base_l.x <= intr[0].x <= self.base_r.x:
                result.append(intr+[self.abs_refr_indx])

        # right
        intr = calc_intersection_circle(a, b, c, self.centre_r.x, self.centre_r.y, self.rad_r)
        for i in intr:
            if self.centre_r.y-self.width/2 <= i[0].y <= self.centre_r.y+self.width/2:
                if self.convex_r:
                    if i[0].x >= self.centre_r.x:
                        result.append(i+[self.abs_refr_indx])
                else:
                    if i[0].x <= self.centre_r.x:
                        result.append(i+[self.abs_refr_indx])

        # bottom
        intr = calc_intersection(a, b, c, 0, 1, -(self.base_l.y-self.width))
        if intr is not None:
            if self.base_l.x <= intr[0].x <= self.base_r.x:
                result.append(intr+[self.abs_refr_indx])

        # left
        intr = calc_intersection_circle(a, b, c, self.centre_l.x, self.centre_l.y, self.rad_l)
        for i in intr:
            if self.centre_l.y - self.width/2 <= i[0].y <= self.centre_l.y+self.width/2:
                if self.convex_l:
                    if i[0].x <= self.centre_l.x:
                        result.append(i+[self.abs_refr_indx])
                else:
                    if i[0].x >= self.centre_l.x:
                        result.append(i+[self.abs_refr_indx])

        return result


class Plane:
    def __init__(self, tk_root, resolution=(1280, 720)):
        self.bg_color = 'white'
        self.res_x = resolution[0]
        self.res_y = resolution[1]
        self.main_axis_y = self.res_y//2
        self.canvas = tkinter.Canvas(tk_root, width=self.res_x, height=self.res_y, bg=self.bg_color)
        self.canvas.pack()
        self.max_recursion_depth = 5
        self.abs_refr_indx = 1.0
        self.obj_list = [Polygon(Vector2(200, 50), 'Polygon_test', 100, 100, radians(60), radians(60)),
                         Lens(Vector2(600, 70), 'Lens_test', 50, 140, 70, 70)]

    def add_obj(self, obj):
        pass

    def pry(self, coord_y):
        return self.main_axis_y - coord_y

    def intersections(self, a, b, c):
        result = []
        # top
        intr = calc_intersection(a, b, c, 0, 1, -self.pry(0))
        if intr is not None:
            if 0 < intr[0].x < self.res_x:
                result.append(intr)
        # right
        intr = calc_intersection(a, b, c, 1, 0, -self.res_x)
        if intr is not None:
            if self.pry(self.res_y) <= intr[0].y <= self.pry(0):
                result.append(intr)
        # bot
        intr = calc_intersection(a, b, c, 0, 1, -self.pry(self.res_y))
        if intr is not None:
            if 0 < intr[0].x < self.res_x:
                result.append(intr)
        # left
        intr = calc_intersection(a, b, c, 1, 0, 0)
        if intr is not None:
            if self.pry(self.res_y) <= intr[0].y <= self.pry(0):
                result.append(intr)
        return result

    def cast_ray(self, origin, a, b, c, positive_dir, refr_indx, recursion_depth=0):
        if recursion_depth > self.max_recursion_depth:
            print('Recursion gone too deep')
            return None
        eps = 0.001
        collision = None
        min_dist = inf
        for obj in self.obj_list:
            for intr in obj.intersections(a, b, c):
                if positive_dir:
                    if b == 0:  # if vertical line
                        if intr[0].y < origin.y + eps:
                            continue
                    else:
                        if intr[0].x < origin.x + eps:
                            continue
                else:
                    if b == 0:  # if vertical line
                        if intr[0].y > origin.y - eps:
                            continue
                    else:
                        if intr[0].x > origin.x - eps:
                            continue
                distance = origin.dist(intr[0])
                if distance < min_dist:
                    min_dist = distance
                    collision = intr

        if collision is not None:
            reflection = calc_crossing_line(collision[0], a, b, c, collision[1]*2)
            if reflection is not None:
                a2, b2, c2 = reflection
                refl_pos_dir = calc_direction(origin, collision[0], a2, b2, c2, collision[2][0], collision[2][1],
                                              collision[2][2], get_trough=False)

                # --- dbg section start
                ddd = self.intersections(collision[2][0], collision[2][1], collision[2][2])
                if len(ddd) > 1:
                    self.canvas.create_line(ddd[0][0].x, self.pry(ddd[0][0].y), ddd[1][0].x, self.pry(ddd[1][0].y),
                                            dash=(4, 2), tag='dbg')
                # --- dbg section end

                # self.cast_ray(collision[0], a2, b2, c2, refl_pos_dir, refr_indx=refr_indx, recursion_depth=recursion_depth+1)

            n1 = refr_indx
            if collision[3] == n1:
                n2 = self.abs_refr_indx
            else:
                n2 = collision[3]

            angle = collision[1]
            alpha = angle/fabs(angle) * (pi/2 - fabs(angle))
            beta = asin((sin(alpha)*n1)/n2)
            angle = -alpha+beta

            refraction = calc_crossing_line(collision[0], a, b, c, angle)    # угол??
            if refraction is not None:
                a2, b2, c2 = refraction
                refr_pos_dir = calc_direction(origin, collision[0], a2, b2, c2, collision[2][0], collision[2][1],
                                              collision[2][2], get_trough=True)
                self.cast_ray(collision[0], a2, b2, c2, refr_pos_dir, refr_indx=n2, recursion_depth=recursion_depth+1)
        else:
            point = None
            for intr in self.intersections(a, b, c):
                if positive_dir:
                    if b == 0:  # if vertical line
                        if intr[0].y < origin.y:
                            continue
                    else:
                        if intr[0].x < origin.x:
                            continue
                else:
                    if b == 0:  # if vertical line
                        if intr[0].y > origin.y:
                            continue
                    else:
                        if intr[0].x > origin.x:
                            continue
                point = intr[0]
            if point is not None:
                self.canvas.create_line(origin.x, self.pry(origin.y), point.x, self.pry(point.y),
                                        fill='blue', tag='ray')
        if collision is not None and True:
            self.canvas.create_line(origin.x, self.main_axis_y-origin.y, collision[0].x, self.main_axis_y-collision[0].y,
                                    fill='red', tag='ray')

            self.canvas.create_oval(collision[0].x-2, self.main_axis_y-collision[0].y+2,
                                    collision[0].x+2, self.main_axis_y-collision[0].y-2,
                                    fill='red', outline='red', tag='ray')

            self.canvas.create_text(collision[0].x, self.main_axis_y-collision[0].y-10,
                                    text=f'{degrees(collision[1]).__round__(1)}',
                                    fill='red', font=('consolas', '8'), tag='ray')

    def draw(self, dbg=False):
        for i in self.obj_list:
            i.draw(self.canvas, self.main_axis_y, dbg=dbg)


def calc_intersection(a1, b1, c1, a2, b2, c2):
    D = a1*b2-b1*a2
    if D == 0:
        return None
    Dx = -c1*b2+b1*c2
    Dy = -a1*c2+c1*a2
    if b1 != 0:
        if b2 != 0:
            k1 = -a1/b1
            k2 = -a2/b2
            if k1*k2 == -1:
                angle = pi/2
            else:
                angle = atan((k1 - k2) / (1 + k1 * k2))
        else:           # b2 == 0
            angle = (pi/2 - atan(-a1/b1))
    else:
        if b2 != 0:     # b1 == 0
            angle = -(pi/2 - atan(-a2/b2))
        else:
            return None
    return [Vector2(Dx/D, Dy/D), angle, (a2, b2, c2)]


def calc_intersection_circle(a, b, c, x0, y0, R):
    if a != 0 and b != 0:
        D = 4*(a*c+a*b*y0-b**2*x0)**2 - 4*(a**2+b**2)*(b**2*(x0**2+y0**2-R**2)+c**2+2*b*c*y0)
        if D > 0:
            x1 = (-2*(a*c+a*b*y0-b**2*x0)+D**0.5) / (2*(a**2+b**2))
            x2 = (-2*(a*c+a*b*y0-b**2*x0)-D**0.5) / (2*(a**2+b**2))
            y1 = (-a*x1-c)/b
            y2 = (-a*x2-c)/b
            intrs = [Vector2(x1, y1), Vector2(x2, y2)]
        elif D == 0:
            x = (-2*(a*c+a*b*y0-b**2*x0)) / (2*(a**2+b**2))
            y = (-a*x-c)/b
            intrs = [Vector2(x, y)]
        else:
            intrs = []
    elif a == 0 and b != 0:
        y = -c/b
        und_sqrt = R**2 - (y-y0)**2
        if und_sqrt >= 0:
            x1 = und_sqrt**0.5 + x0
            x2 = -und_sqrt**0.5 + x0
            if x1 != x2:
                intrs = [Vector2(x2, y), Vector2(x1, y)]
            else:
                intrs = [Vector2(x2, y)]
        else:
            intrs = []
    elif a != 0 and b == 0:
        x = -c/a
        und_sqrt = R**2 - (x-x0)**2
        if und_sqrt >= 0:
            y1 = und_sqrt**0.5 + y0
            y2 = -und_sqrt**0.5 + y0
            if y1 != y2:
                intrs = [Vector2(x, y2), Vector2(x, y1)]
            else:
                intrs = [Vector2(x, y2)]
        else:
            intrs = []
    else:
        intrs = []
    result = []
    for i in intrs:
        a2 = i.x - x0
        b2 = i.y - y0
        c2 = x0**2 - x0*i.x + y0**2 - y0*i.y - R**2
        calc = calc_intersection(a, b, c, a2, b2, c2)
        if calc is not None:
            angle = calc[1]
            result.append([i, angle, (a2, b2, c2)])
    return result


def calc_crossing_line(point, a, b, c, angle):
    if angle == 0 or angle == pi:
        return a, b, c
    if angle != pi/2:   # angle != pi/2
        if b != 0:      # b1 != 0
            tan_ang = tan(angle)
            if (a/b)*tan_ang != 1:   # b2 != 0
                k2 = (tan_ang+a/b) / ((a/b)*tan_ang-1)
                a2 = -k2
                b2 = 1
                c2 = k2*point.x - point.y
            else:                       # b2 == 0
                a2 = 1
                b2 = 0
                c2 = point.x
        else:           # b1 == 0
            tan_ang = tan(angle)
            k2 = -tan_ang
            a2 = 1
            b2 = -k2
            c2 = k2*point.y - point.x
    else:               # angle == pi/2
        if a != 0 and b != 0:                       # эта часть не была протестирована!
            print('pi/2,  a!=0,  b!=0  Может работать некорректно!')
            b2 = -c/(-b/a*point.x+point.y)
            a2 = -b*b2/a
            c2 = c
        elif a == 0:                                # ok
            a2 = 1
            b2 = 0
            c2 = -point.x
        else:                                       # ok
            a2 = 0
            b2 = 1
            c2 = -point.y
    return a2, b2, c2


def calc_direction(point_from, point_intr, a, b, c, surf_a, surf_b, surf_c, get_trough):
    positive_direction = True
    if b != 0:
        point_chck = Vector2(point_intr.x+1, (-a/b)*(point_intr.x+1)-c/b)
    else:
        point_chck = Vector2((-b/a)*(point_intr.y+1)-c/a, point_intr.y+1)

    if surf_b != 0:
        if point_from.y > (-surf_a/surf_b) * point_from.x - surf_c/surf_b:
            if point_chck.y > (-surf_a/surf_b)*point_chck.x - surf_c/surf_b:
                same_side = True
            else:
                same_side = False
        else:
            if point_chck.y > (-surf_a / surf_b) * point_chck.x - surf_c / surf_b:
                same_side = False
            else:
                same_side = True
    else:
        if point_from.x > point_intr.x:
            if point_chck.x > point_intr.x:
                same_side = True
            else:
                same_side = False
        else:
            if point_chck.x > point_intr.x:
                same_side = False
            else:
                same_side = True

    if not same_side:
        positive_direction = not positive_direction

    if get_trough:
        positive_direction = not positive_direction

    return positive_direction


def pause(*args):
    global ppp
    ppp = not ppp


def rr(*args):
    global k
    k -= 1


def ll(*args):
    global k
    k += 1


"""
##########################
##########################
##########################
"""
if __name__ == '__main__':
    ppp = False
    kb.on_press_key('p', pause)
    kb.on_press_key('d', rr)
    kb.on_press_key('a', ll)

    root = tkinter.Tk()
    plane = Plane(root, (1280, 720))  # (640, 360))

    k = 0.0

    line_r = Line('TestLine', plane.canvas)

    repeat = True
    while repeat:
        while ppp:
            pass

        t = time.time()

        # k -= 1

        plane.canvas.delete('ray', 'Polygon_test', 'Lens_test', 'dbg', 'TestLine')
        plane.draw(dbg=True)
        plane.canvas.create_line(0, plane.main_axis_y, plane.res_x, plane.main_axis_y, fill='black', dash=(3, 9),
                                 tag='dbg')
        line_r.draw(dbg=True)

        a90 = 0
        a66 = 0
        a45 = 0
        a0 = 0
        line = 1
        ray = 1
        ray_from_line = 1
        intersections = 0

        if line:
            if a45:
                plane.canvas.create_line(-300-k, plane.pry(-300), 300-k, plane.pry(300), fill='grey', tag='dbg')
            if a90:
                plane.canvas.create_line(-k, plane.pry(-300), -k, plane.pry(300), fill='grey', tag='dbg')
            if a66:
                plane.canvas.create_line(-150-k, plane.pry(-300), 150-k, plane.pry(300), fill='grey', tag='dbg')
            if a0:
                plane.canvas.create_line(0, plane.pry(k), plane.res_x, plane.pry(k), fill='grey', tag='dbg')

        if ray:
            if a45:
                plane.cast_ray(Vector2(-300-k, -300), -1, 1, -k, positive_dir=True, refr_indx=1.0)
            if a90:
                plane.cast_ray(Vector2(-k, -300), -1, 0, -k, positive_dir=True, refr_indx=1.0)
            if a66:
                plane.cast_ray(Vector2(-150-k, -300), -2, 1, -2*k, positive_dir=True, refr_indx=1.0)
            if a0:
                plane.cast_ray(Vector2(10, k), 0, 1, -k, positive_dir=True, refr_indx=1.0)
            if ray_from_line:
                plane.cast_ray(line_r.v2.coords_plane, line_r.a, line_r.b, line_r.c, line_r.pos_dir, refr_indx=1.0)

        if intersections:
            for o in plane.obj_list:
                if a45:
                    for ii in o.intersections(-1, 1, -k):
                        plane.canvas.create_oval(ii[0].x-2, plane.pry(ii[0].y-2), ii[0].x+2, plane.pry(ii[0].y+2),
                                                 tag='dbg')
                        plane.canvas.create_text(ii[0].x, plane.pry(ii[0].y+10),
                                                 text=f'{degrees(fabs(ii[1])).__round__(1)}',
                                                 fill='black', font=('consolas', '8'), tag='dbg')
                        a2, b2, c2 = ii[2]
                        if b2 != 0:
                            _y1 = -c2 / b2
                            _y2 = (-a2 / b2) * plane.res_x - c2 / b2
                            plane.canvas.create_line(0, plane.pry(_y1), plane.res_x, plane.pry(_y2), tag='dbg')
                if a90:
                    for ii in o.intersections(-1, 0, -k):
                        plane.canvas.create_oval(ii[0].x-2, plane.pry(ii[0].y-2), ii[0].x+2, plane.pry(ii[0].y+2),
                                                 tag='dbg')
                        plane.canvas.create_text(ii[0].x, plane.pry(ii[0].y+10),
                                                 text=f'{degrees(fabs(ii[1])).__round__(1)}',
                                                 fill='black', font=('consolas', '8'), tag='dbg')
                        a2, b2, c2 = ii[2]
                        if b2 != 0:
                            _y1 = -c2 / b2
                            _y2 = (-a2 / b2) * plane.res_x - c2 / b2
                            plane.canvas.create_line(0, plane.pry(_y1), plane.res_x, plane.pry(_y2), tag='dbg')
                if a66:
                    for ii in o.intersections(-2, 1, -2*k):
                        plane.canvas.create_oval(ii[0].x-2, plane.pry(ii[0].y-2), ii[0].x+2, plane.pry(ii[0].y+2),
                                                 tag='dbg')
                        plane.canvas.create_text(ii[0].x, plane.pry(ii[0].y+10),
                                                 text=f'{degrees(fabs(ii[1])).__round__(1)}',
                                                 fill='black', font=('consolas', '8'), tag='dbg')
                        a2, b2, c2 = ii[2]
                        if b2 != 0:
                            _y1 = -c2 / b2
                            _y2 = (-a2 / b2) * plane.res_x - c2 / b2
                            plane.canvas.create_line(0, plane.pry(_y1), plane.res_x, plane.pry(_y2), tag='dbg')
                if a0:
                    for ii in o.intersections(0, 1, -k):
                        plane.canvas.create_oval(ii[0].x-2, plane.pry(ii[0].y-2), ii[0].x+2, plane.pry(ii[0].y+2),
                                                 tag='dbg')
                        plane.canvas.create_text(ii[0].x, plane.pry(ii[0].y+10),
                                                 text=f'{degrees(fabs(ii[1])).__round__(1)}',
                                                 fill='black', font=('consolas', '8'), tag='dbg')
                        a2, b2, c2 = ii[2]
                        if b2 != 0:
                            _y1 = -c2 / b2
                            _y2 = (-a2 / b2) * plane.res_x - c2 / b2
                            plane.canvas.create_line(0, plane.pry(_y1), plane.res_x, plane.pry(_y2), tag='dbg')

        t = time.time() - t

        plane.canvas.create_text(3, 3, text=f'{int(1/t) if t>=0.0005 else "inf"} FPS\n{int(t*1000)} ms',
                                 font=('consolas', '8'), anchor=tkinter.NW, tag='dbg')

        plane.canvas.tag_raise(line_r.v1.name, line_r.v2.name)

        root.update_idletasks()
        root.update()
        # time.sleep(0.1)
        repeat = True

    root.mainloop()
