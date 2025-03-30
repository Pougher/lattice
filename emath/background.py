import pygame
import random
import math

class Background:
    def __init__(self, points, width, height):
        """
        Sebastian lague inspired background. Im guessing his one was made up
        of a bunch of points and lines (kind of like a voronoi diagram)
        """
        self.n_tris = points
        self.width = width
        self.height = height

        self.colors = [
            [ 70, 70, 255 ],
            [ 240, 190, 90 ],
            [ 170, 170, 255 ],
            [ 250, 120, 60 ],
            [ 100, 230, 90 ],
            [ 190, 240, 90 ],
            [ 250, 150, 160 ],
            [ 100, 100, 255 ],
            [ 90, 180, 255 ],
            [ 185, 100, 255 ]
        ]

        self.base_color = random.choice(self.colors)
        self.point_color = [
            min(self.base_color[0] + 80, 255),
            min(self.base_color[1] + 80, 255),
            min(self.base_color[2] + 80, 255),
        ]
        self.min_color_sub = int(min(self.base_color) / 5)

        self.tris = []
        self.tri_colors = []

        self.centers = []
        self.rotation_factors = []

        previous1 = [20, 20]
        previous2 = [50, 50]
        for i in range(self.n_tris):
            new_tri = self.gen_triangle(self.tris, previous1, previous2)
            previous1 = previous2
            previous2 = new_tri[2]
            self.tris.append(new_tri)
            self.tri_colors.append([
                min(self.base_color[0] +\
                    random.randint(-self.min_color_sub, 30), 255),
                min(self.base_color[1] +\
                    random.randint(-self.min_color_sub, 30), 255),
                min(self.base_color[2] +\
                    random.randint(-self.min_color_sub, 30), 255),
            ])

        for i in self.tris:
            for k in i:
                self.centers.append([
                    k[0] + random.randint(-300, 300),
                    k[1] + random.randint(-300, 300),
                ])
                self.rotation_factors.append(random.uniform(0.0001, 0.02) / 10)

    def within_triangle(self, points, k):
        """
        Using the cross product, we can test if a point k exists within a given
        triangle (defined of course by a list of points)
        """
        c1 = (points[1][0] - points[0][0]) * (k[1]- points[0][1]) - \
                (points[1][1] - points[0][1]) * (k[0] - points[0][0])
        c2 = (points[2][0] - points[1][0]) * (k[1]- points[1][1]) - \
                (points[2][1] - points[1][1]) * (k[0] - points[1][0])
        c3 = (points[0][0] - points[2][0]) * (k[1]- points[2][1]) - \
                (points[0][1] - points[2][1]) * (k[0] - points[2][0])
        return (c1 > 0 and c2 > 0 and c3 > 0) or (c1 < 0 and c2 < 0 and c3 < 0)

    def in_generated_triangles(self, triangles, point):
        """
        This literally checks every triangle in our currently generated
        triangle list and test whether or not the point is within any of them
        """
        for tri in self.tris:
            if self.within_triangle(tri, point):
                return True
        return False

    def new_point_in_bounds(self, previous1, previous2, point):
        """
        Check to see if the point we have generated sits within the bounds
        we have decided for each point
        """
        d1 = math.sqrt(
            (point[0] - previous1[0]) ** 2 + (point[1] - previous1[1])**2)
        d2 = math.sqrt(
            (point[0] - previous2[0]) ** 2 + (point[1] - previous2[1])**2)

        return (d1 <= 500 and d1 >= 200) and (d2 <= 500 and d2 >= 200)

    def new_point_on_screen(self, point):
        """
        Checks if the new point is visible in the viewable window area
        """
        return (point[0] < self.width and point[0] >= 0) and \
            (point[1] >= 0 and point[1] < self.height)

    def gen_triangle(self, generated, previous1, previous2):
        """
        Okay so I have noticed all of the points seem to like to form triangles,
        so lets generate a bunch of random triangles that all connect.

        Treating the previous two points like so:
            p2

        p1      k
        we want K to be at least 10 units away from p1 and p2 and at most 200
        units, and not lie in the areas of any other triangles
        """
        new_point = [
            previous1[0] + random.randint(-500, 500),
            previous1[1] + random.randint(-500, 500)]
        while (self.in_generated_triangles(generated, new_point)) or \
            not self.new_point_in_bounds(previous1, previous2, new_point) or \
            not self.new_point_on_screen(new_point):
            new_point = [
                previous1[0] + random.randint(-500, 500),
                previous1[1] + random.randint(-500, 500)]
        return [previous1, previous2, new_point]

    def render(self, screen):
        screen.fill(self.base_color)
        for i in range(self.n_tris):
            pygame.draw.polygon(screen, self.tri_colors[i], self.tris[i])
            pygame.draw.circle(screen, self.point_color, self.tris[i][0], 5)
            pygame.draw.circle(screen, self.point_color, self.tris[i][1], 5)
            pygame.draw.circle(screen, self.point_color, self.tris[i][2], 5)

    def update(self, events, delta):
        """
        Each point exists on the circumference of a sphere with a randomized
        centre. This code rotates the point around the sphere at a fixed
        speed.
        """
        p_index = 0
        for tri in range(len(self.tris)):
            for p in self.tris[tri]:
                # lets rotate that point
                r = self.rotation_factors[p_index]
                x = p[0] - self.centers[p_index][0]
                y = p[1] - self.centers[p_index][1]
                x1 = (x * math.cos(r) - y * math.sin(r)) + \
                    self.centers[p_index][0]
                y1 = (x * math.sin(r) + y * math.cos(r)) + \
                    self.centers[p_index][1]
                p[0] = x1
                p[1] = y1
                p_index += 1
