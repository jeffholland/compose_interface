class Event:
    def __init__(self, type, note, voice):
        self.type = type
        self.note = note
        self.voice = voice

        o_v = self.voice['o_v']
        a_v = self.voice['a_v']

        self.line = ""

        if self.type == "start":
            self.time = self.note.params['st']

            p = self.note.params['p']
            p2 = self.note.params['p2']
            ln = self.note.params['ln']
            pk = self.note.params['pk']
            at = self.note.params['at']
            self.line += f"{o_v} {p} {p2} {ln},\n"
            self.line += f"{a_v} {pk} {at},\n"

            for key, v1 in self.note.params.items():
                # add'l parameters have suffix _1 and _2 appended
                if key[-2:] == '_1':
                    pm = key[:-2]

                    if pm + '_2' in self.note.params:
                        v2 = self.note.params[pm + '_2']
                        self.line += f"{pm} {v1} {v2} {ln},\n"
                    else:
                        self.line += f"{pm} {v1},\n"
        else:
            self.time = self.note.params['en']
            dc = self.note.params['dc']

            self.time = self.note.params['en']
            self.line += f"{a_v} 0 {dc},\n"


def print_notes(notes, voices):
    events = []

    for note in notes:
        # Create start events
        for voice in voices:
            if voice['name'] == note.voice:
                events.append(Event("start", note, voice))
                events.append(Event("end", note, voice))
                break

    # Sort by event time
    events = sorted(events, key=lambda event: event.time)

    # Traverse events, adding gaps in between notes
    result = ""
    cursor = 0
    voice_current_note_id = dict()

    for event in events:
        # Track current note id of each voice
        if event.type == "start":
            voice_current_note_id[event.voice["name"]] = event.note.id
        else:
            # skip end event if not current note (so old notes don't cut off new notes)
            if voice_current_note_id[event.voice["name"]] != event.note.id:
                continue

        # Delay event if necessary
        if event.time > cursor:
            delay = event.time - cursor
            result += f"/ {delay},\n"
            cursor = event.time
        
        # Write line
        result += event.line

    # Leave time to decay last note
    result += f"/ {events[-1].note.params['dc']},\n"

    outfilename = "./pd/read/result.txt"
    with open(outfilename, "w") as f:
        f.write(result)