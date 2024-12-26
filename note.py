from constants import *
import math

class Note:
    def __init__(self, x, y, id, size=NOTE_SIZE):
        self.x = x
        self.y = y
        self.id = id
        self.size = size
        self.x2 = x + size
        self.y2 = y
        
        self.recalc_vals()

        self.attack = 0.005
        self.peak = 0.25
        self.decay = 0.1

        self.params = dict()

    def recalc_vals(self):
        self.start_time = (self.x / CANV_WIDTH) * TIME_LENGTH
        self.end_time = ((self.x + self.size)/ CANV_WIDTH) * TIME_LENGTH
        self.length = self.end_time - self.start_time
        self.pitch = PITCH_RANGE - ((self.y / CANV_HEIGHT) * PITCH_RANGE)
        self.pitch2 = PITCH_RANGE - ((self.y2 / CANV_HEIGHT) * PITCH_RANGE)

    def set_params(self, params):
        # expects a dictionary
        if not isinstance(params, dict):
            raise TypeError("passed non-dict to set_params in note.py")
        
        for key, value in params.items():
            self.params[key] = value

    def move(self, xAmount, yAmount):
        self.x += xAmount
        self.y += yAmount
        self.recalc_vals()

    def resize(self, new_size):
        self.size = new_size
        self.x2 = self.x + self.size
        self.recalc_vals()

    def tilt(self, tilt_amount):
        self.y2 += tilt_amount
        self.recalc_vals()
