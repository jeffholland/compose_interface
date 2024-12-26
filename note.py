from constants import *
import math

class Note:
    def __init__(self, x, y, id, size=NOTE_SIZE):
        self.x = x
        self.y = y
        self.id = id
        self.size = size

        # rotation
        self.theta = 0
        self.x2 = self.x + self.size
        self.y2 = self.y

        self.start_time = (x / CANV_WIDTH) * TIME_LENGTH
        self.end_time = ((x + self.size)/ CANV_WIDTH) * TIME_LENGTH
        self.length = self.end_time - self.start_time
        self.pitch = PITCH_RANGE - ((y / CANV_HEIGHT) * PITCH_RANGE)

        self.attack = 0.005
        self.peak = 0.25
        self.decay = 0.1

        self.params = dict()

    def set_params(self, params):
        # expects a dictionary
        if not isinstance(params, dict):
            raise TypeError("passed non-dict to set_params in note.py")
        
        for key, value in params.items():
            self.params[key] = value

    def move(self, xAmount, yAmount):
        self.x += xAmount
        self.y += yAmount

        self.start_time = (self.x / CANV_WIDTH) * TIME_LENGTH
        self.end_time = ((self.x + self.size)/ CANV_WIDTH) * TIME_LENGTH
        self.pitch = PITCH_RANGE - ((self.y / CANV_HEIGHT) * PITCH_RANGE)

    def resize(self, new_size):
        self.size = new_size
        self.x2 = self.x + self.size
        self.end_time = ((self.x + self.size)/ CANV_WIDTH) * TIME_LENGTH
        self.length = self.end_time - self.start_time

    def tilt(self, new_angle):
        self.theta = new_angle % 360
        print(f"rotating to {self.theta}")
        angle_radians = math.radians(self.theta)
        self.x2, self.y2 = self.rotate_point(self.x, self.y, self.x2, self.y2, angle_radians)

    def rotate_point(self, x1, y1, x2, y2, angle_radians):
        dx, dy = x2 - x1, y2 - y1
        new_x = x1 + (dx * math.cos(angle_radians) - dy * math.sin(angle_radians))
        new_y = y1 + (dx * math.sin(angle_radians) + dy * math.cos(angle_radians))
        return new_x, new_y