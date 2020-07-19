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
        self.circumference_coords_x, self.circumference_coords_y = [], []

        # init centers of circles (n+1 elements)
        self.centers_x = [center_x]
        self.centers_y = [center_y]

        for circle in circles:
            
            # circle centers
            center_x += circle.amplitude * cos(circle.theta)
            center_y += circle.amplitude * sin(circle.theta)

            self.centers_x.append(center_x)
            self.centers_y.append(center_y)

            # points on circumference of circle
            x, y = get_circle_coords(circle.amplitude, center_x, center_y, circle_res)
            self.circumference_coords_x.append(x)
            self.circumference_coords_y.append(y)

    def update(self, time: float):

        if self.n > 0:
            x = self.centers_x[0]
            y = self.centers_y[0]

            for i, circle in enumerate(self.circles):
                circle.update(time)

                x += circle.amplitude * cos(circle.theta)
                y += circle.amplitude * sin(circle.theta)

                self.centers_x[i+1] = x
                self.centers_y[i+1] = y

                # points on circumference of circle
                circumference_x, circumference_y = get_circle_coords(circle.amplitude, x, y, 100)
                self.circumference_coords_x[i] = circumference_x
                self.circumference_coords_y[i] = circumference_y


# converts frequency domain params to epicycle chain
def freq_to_epicycles(f_freq: list, center_x: float, center_y: float) -> EpicycleChain:
    circles = [Circle(params[0], params[1], params[2]) for params in f_freq]
    return EpicycleChain(100, center_x, center_y, circles)


def get_circle_coords(radius: float, center_x: float, center_y: float, num_points: int) -> tuple:
    x, y = [], []
    theta = 0
    for i in range(num_points+1):
        theta += 2*pi/num_points
        x.append(radius * cos(theta) + center_x)
        y.append(radius * sin(theta) + center_y)
    return x, y
