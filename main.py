import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random
import itertools


class Circle(object):
    def __init__(self, radius, cx, cy):
        self.radius = radius
        self.cx = cx
        self.cy = cy
        self.epsilon = 0.05

    def contains(self, px, py):
        dx = self.cx - px
        dy = self.cy - py
        return dx ** 2 + dy ** 2 <= self.radius ** 2 + self.epsilon

    def __contains__(self, point):
        return self.contains(point[0], point[1])

    def contains_all(self, points):
        for point in points:
            if point not in self:
                return False
        return True

    def area(self):
        return self.radius ** 2 * np.pi


def three_points_to_circle(p1, p2, p3):
    x, y, z = p1[0] + 1j * p1[1], p2[0] + 1j * p2[1], p3[0] + 1j * p3[1]
    w = z - x
    w /= y - x
    c = (x - y) * (w - abs(w) ** 2) / 2j / w.imag - x
    print '(x%+.3f)^2+(y%+.3f)^2 = %.3f^2' % (c.real, c.imag, abs(c + x))
    cx, cy, radius = -c.real, -c.imag, abs(c + x)
    return Circle(
        cx=cx,
        cy=cy,
        radius=radius
    )


def two_points_to_circle(p1, p2):
    cx, cy, radius = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) / 2
    return Circle(
        cx=cx,
        cy=cy,
        radius=radius
    )


def naive(p):
    best = None
    for pair in itertools.combinations(p, 2):
        circle = two_points_to_circle(*pair)
        if (best is None or circle.area() < best.area()) and circle.contains_all(p):
            best = circle
    for triple in itertools.combinations(p, 3):
        circle = three_points_to_circle(*triple)
        if (best is None or circle.area() < best.area()) and circle.contains_all(p):
            best = circle
    return best


def welzl(p, r):
    if len(p) == 0 or len(r) >= 3:
        if len(r) == 3:
            return three_points_to_circle(*r)
        elif len(r) > 3:
            print r
            return three_points_to_circle(r[0], r[1], r[2])
        else:
            return None

    random_p = random.choice(tuple(p))
    circle = welzl(p - {random_p}, r)
    if circle is not None and random_p in circle:
        return circle
    else:
        return welzl(p - {random_p}, r | {random_p})


def main():
    fig, ax = plt.subplots()
    pts = 10 * np.random.randn(30, 2)

    welzl_circle = welzl(set(tuple(point) for point in pts), set())
    naive_circle = naive(pts)

    ax.set_title('Smallest circle enclosing points')
    ax.plot(pts.T[0], pts.T[1], 'o')
    welzl_circle_artist = plt.Circle((welzl_circle.cx, welzl_circle.cy), welzl_circle.radius, alpha=0.2)
    naive_circle_artist = plt.Circle((naive_circle.cx, naive_circle.cy), naive_circle.radius, alpha=0.2, color='r')
    ax.add_artist(welzl_circle_artist)
    ax.add_artist(naive_circle_artist)
    plt.axis('equal')
    plt.xlim((welzl_circle.cx - welzl_circle.radius*2.00, welzl_circle.cx + welzl_circle.radius*2.00))
    plt.ylim((welzl_circle.cy - welzl_circle.radius*2.00, welzl_circle.cy + welzl_circle.radius*2.00))
    plt.show()


if __name__ == "__main__":
    three_points_to_circle([1, 1], [0, 0], [-1, 0])
    main()
