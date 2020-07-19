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


class EpicycleSeries():

    # list of n circles
    def __init__(self, center_x: float, center_y: float, circles: list):
        self.n = len(circles)
        self.circles = circles

        # init centers of circles (n+1 elements)
        self.centers_x = [center_x]
        self.centers_y = [center_y]

        for circle in circles:
            
            center_x = circle.amplitude * cos(circle.theta) + center_x
            center_y = circle.amplitude * sin(circle.theta) + center_y

            self.centers_x.append(center_x)
            self.centers_y.append(center_y)

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


# converts frequency domain params to epicycles
def freq_to_epicycles(f_freq: list, center_x: float, center_y: float) -> EpicycleSeries:
    circles = [Circle(params[0], params[1], params[2]) for params in f_freq]
    return EpicycleSeries(center_x, center_y, circles)
