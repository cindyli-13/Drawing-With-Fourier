from math import cos, sin, pi


class Circle():

    # frequency in Hz, phase in radians
    def __init__(self, amplitude: float, frequency: float, phase: float):
        self.amplitude = amplitude
        self.frequency = frequency
        self.start_phase = phase
        self.theta = phase

    # time in seconds
    def update(self, time: float):
        self.theta = time * self.frequency * 2 * pi + self.start_phase
        if self.theta > 2 * pi:
            self.theta -= 2 * pi


class EpicycleChain():

    # list of n circles
    def __init__(self, circle_res: int, center_x: float, center_y: float, circles: list):
        self.n = len(circles)
        self.circles = circles
        self.circumference_coords_x, self.circumference_coords_y = [0 for i in range(self.n)], [0 for i in range(self.n)]
        self.circle_res = circle_res

        # init centers of circles (n+1 elements)
        self.centers_x = [center_x for i in range(self.n+1)]
        self.centers_y = [center_y for i in range(self.n+1)]

        self.update(0)

    def update(self, time: float):

        if self.n > 0:
            x = self.centers_x[0]
            y = self.centers_y[0]

            for i, circle in enumerate(self.circles):
                circle.update(time)

                x += circle.amplitude * cos(circle.theta)
                y += circle.amplitude * sin(circle.theta)

                # circle centers
                self.centers_x[i+1] = x
                self.centers_y[i+1] = y

                # points on circumference of circle
                circumference_x, circumference_y = get_circle_coords(circle.amplitude, x, y, self.circle_res)
                self.circumference_coords_x[i] = circumference_x
                self.circumference_coords_y[i] = circumference_y


# converts frequency domain parameters to epicycle chain
def freq_to_epicycles(f_freq: list, center_x: float, center_y: float, drawing_speed: float) -> EpicycleChain:
    circles = [Circle(params[0], params[1] * drawing_speed, params[2]) for params in f_freq]
    return EpicycleChain(70, center_x, center_y, circles)


def get_circle_coords(radius: float, center_x: float, center_y: float, num_points: int) -> tuple:
    x, y = [], []
    theta = 0
    for i in range(num_points+1):
        theta += 2*pi/num_points
        x.append(radius * cos(theta) + center_x)
        y.append(radius * sin(theta) + center_y)
    return x, y
