from constants import *

class Note:
    def __init__(self, voice, x, y, id=None, size=NOTE_SIZE):
        self.id = id
        self.size = size

        self.voice = voice
        self.hidden = False 
        # a note is hidden if another voice is selected - 
        # this is always false when the note is created

        self.params = {
            'x': x,
            'y': y,
            'x2': x + size,
            'y2': y,
            'at': 0.005,
            'pk': 0.25,
            'dc': 0.1
        }
        
        self.recalc_vals_from_coords()

    def recalc_vals_from_coords(self):
        self.size = self.params['x2'] - self.params['x']
        self.params['st'] = (self.params['x'] / CANV_WIDTH) * TIME_LENGTH
        self.params['en'] = ((self.params['x'] + self.size)/ CANV_WIDTH) * TIME_LENGTH
        self.params['ln'] = self.params['en'] - self.params['st']
        self.params['p'] = PITCH_RANGE - ((self.params['y'] / CANV_HEIGHT) * PITCH_RANGE)
        self.params['p2'] = PITCH_RANGE - ((self.params['y2'] / CANV_HEIGHT) * PITCH_RANGE)

    def recalc_coords_from_vals(self):
        self.params['x'] = (self.params['st'] / TIME_LENGTH) * CANV_WIDTH
        self.params['x2'] = (self.params['en'] / TIME_LENGTH) * CANV_WIDTH
        self.size = self.params['x2'] - self.params['x']
        self.params['ln'] = self.params['en'] - self.params['st']
        self.params['y'] = CANV_HEIGHT - ((self.params['p'] / PITCH_RANGE) * CANV_HEIGHT)
        self.params['y2'] = CANV_HEIGHT - ((self.params['p2'] / PITCH_RANGE) * CANV_HEIGHT)

    def xsnap(self, amt):
        self.params['st'] = round(self.params['st'] / amt) * amt
        self.params['en'] = self.params['st'] + self.params['ln']
        self.recalc_coords_from_vals()

    def ysnap(self, amt):
        self.params['p'] = round(self.params['p'] / amt) * amt
        self.params['p2'] = self.params['p']
        self.recalc_coords_from_vals()

    def set_param(self, key, val, pitch_dependent=True):
        # params depend on other params
        if key in ['p', 'p2', 'st', 'en', 'ln']:
            diff = val - self.params[key]

            if key == 'st':
                self.params['en'] += diff
            if key == 'en':
                self.params['ln'] += diff
            if key == 'ln':
                self.params['en'] += diff
            if key == 'p' and pitch_dependent:
                self.params['p2'] += diff

        self.params[key] = val
        self.recalc_coords_from_vals()

    def set_params(self, params):
        # expects a dictionary
        if not isinstance(params, dict):
            raise TypeError("passed non-dict to set_params in note.py")
        
        for key, value in params.items():
            self.params[key] = value

    def move(self, xAmount, yAmount):
        self.params['x'] += xAmount
        self.params['y'] += yAmount
        self.params['x2'] += xAmount
        self.params['y2'] += yAmount
        self.recalc_vals_from_coords()

    def resize(self, new_size):
        self.size = new_size
        self.params['x2'] = self.params['x'] + self.size
        self.recalc_vals_from_coords()

    def tilt(self, tilt_amount):
        self.params['y2'] += tilt_amount
        self.recalc_vals_from_coords()

    def in_bounds(self, x, y):
        min_x, max_x = min(self.params['x'], self.params['x2']), max(self.params['x'], self.params['x2'])
        min_y, max_y = min(self.params['y'], self.params['y2'] + NOTE_HEIGHT), max(self.params['y'], self.params['y2'] + NOTE_HEIGHT)
        
        return min_x <= x <= max_x and min_y <= y <= max_y
    
def length_to_size(length):
    return (length / TIME_LENGTH) * CANV_WIDTH