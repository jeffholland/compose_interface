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
        self.end_time = ((self.x + self.width)/ CANV_WIDTH) * TIME_LENGTH
        self.pitch = PITCH_RANGE - ((self.y / CANV_HEIGHT) * PITCH_RANGE)