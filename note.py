from constants import *

class Note:
    def __init__(self, x, y, id, width=NOTE_WIDTH):
        self.x = x
        self.y = y
        self.id = id
        self.width = width

        self.start_time = (x / CANV_WIDTH) * TIME_LENGTH
        self.end_time = ((x + self.width)/ CANV_WIDTH) * TIME_LENGTH
        self.length = self.end_time - self.start_time
        self.pitch = PITCH_RANGE - ((y / CANV_HEIGHT) * PITCH_RANGE)

        self.attack = 0.005
        self.peak = 0.25
        self.decay = 0.1

        self.params = dict()