# Реализовать класс векторов Vector — выполнить перегрузку основных математических операций: сумма Vector.add, разность Vector.sub, умножение на скаляр и скалярное умножение (Vector.mul); добавить возможность вычислять длину вектора L через len(L);добавить метод int_pair для получение пары целых чисел в виде кортежа.

import pygame
from random import random
from math import sqrt

SCREEN_SIZE = (1280, 720)


class Vector:
    def __init__(self, x):
        self.x = x

    def __add__(self, previous):
        return self.x[0] + previous.x[0], self.x[1] + previous.x[1]

    def __sub__(self, previous):
        return self.x[0] - previous.x[0], self.x[1] - previous.x[1]

    def __mul__(self, previous):
        return self.x[0] * previous.x, self.x[1] * previous.x

    @staticmethod
    def __len__(L):
        return sqrt(L[0] * L[0] + L[1] * L[1])

    @staticmethod
    def speed_change(param):
        for i in range(len(speeds)):
            if speeds[i][0] + speeds[i][1]< 10:
                speeds[i] = (speeds[i][0] * param, speeds[i][1] * param)



    def int_pair(self):
        return (int(self.x[0]), int(self.x[1]))


# Реализовать класс замкнутых ломаных Line, с возможностями: добавление в ломаную точки (Vector) c её скоростью; пересчёт координат точек (set_points); отрисовка ломаной (draw_points),

class Line():
    def __init__(self, points, style="points", width=4, color=(255, 255, 255)):
        self.points = points
        self.style = style
        self.width = width
        self.color = color

    def draw_points(self):
        if self.style == "line":
            for point_number in range(-1, len(self.points) - 1):
                pygame.draw.line(gameDisplay, self.color,
                                 (int(self.points[point_number][0]), int(self.points[point_number][1])),
                                 (int(self.points[point_number + 1][0]), int(self.points[point_number + 1][1])),
                                 self.width)


        elif self.style == "points":
            for point in self.points:
                pygame.draw.circle(gameDisplay, self.color,
                                   (int(point[0]), int(point[1])), self.width)

    def set_points(self, speeds):
        for point in range(len(self.points)):
            self.points[point] = Vector(self.points[point]) + Vector(speeds[point])
            if self.points[point][0] > SCREEN_SIZE[0] or self.points[point][0] < 0:
                speeds[point] = (- speeds[point][0], speeds[point][1])
            if self.points[point][1] > SCREEN_SIZE[1] or self.points[point][1] < 0:
                speeds[point] = (speeds[point][0], -speeds[point][1])




class Joint(Line):
    def __init__(self, points, count):
        super().__init__(points)
        self.count = count

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return Vector(Vector(points[deg]) * Vector(alpha)) + Vector(Vector(self.get_point(points, alpha, deg - 1)) * Vector(1 - alpha))

    def get_points(self, base_points):
        alpha = 1 / self.count
        result = []
        for i in range(self.count):
            result.append(self.get_point(base_points, i * alpha))
        return result

    def get_joint(self):
        if len(self.points) < 3:
            return []
        result = []
        for i in range(-2, len(self.points) - 2):
            pnt = []
            ex1 = Vector(self.points[i]) + Vector(self.points[i + 1])
            pnt.append(Vector(ex1) * Vector(0.5))
            pnt.append(self.points[i + 1])
            ex2 = Vector(self.points[i + 1]) + Vector(self.points[i + 2])
            pnt.append(Vector(ex2) * Vector(0.5))

            result.extend(self.get_points(pnt))
        return result


def display_help(steps):
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("arial", 30)
    font2 = pygame.font.SysFont("serif", 30)
    data = []
    data.append(["F1", "Помощь"])
    data.append(["R", "Перезапуск"])
    data.append(["P", "Воспроизвести / Пауза"])
    data.append(["Num+", "Добавить точку"])
    data.append(["Num-", "Удалить точку"])
    data.append(["ЛКМ", "Удалить точку"])
    data.append(["→", "Ускорить"])
    data.append(["←", "Замедлить"])
    data.append(["", ""])
    data.append([str(steps), "текущих точек"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for item, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * item))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * item))


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Screen Saver")

    steps = 20
    working = True
    points = []
    speeds = []
    show_help = False
    pause = False

    color_param = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    points = []
                    speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                if event.key == pygame.K_RIGHT:
                    Vector.speed_change(2)
                if event.key == pygame.K_LEFT:
                    Vector.speed_change(0.5)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                points.append(event.pos)
                speeds.append((random() * 2, random() * 2))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and points != []:
                points.pop()
                speeds.pop()
        gameDisplay.fill((0, 0, 0))
        color_param = (color_param + 1) % 360
        color.hsla = (color_param, 100, 50, 100)
        Line(points).draw_points()
        Line(Joint(points, steps).get_joint(), "line", 4, color).draw_points()

        if not pause:
            Line(points).set_points(speeds)
        if show_help:
            display_help(steps)

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
