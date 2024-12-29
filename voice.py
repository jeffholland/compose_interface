import json

class Voice:
    def __init__(self, name, params):
        self.name = name
        self.params = params

def load_voices():
    with open("voice.json", 'r') as f:
        return json.load(f)