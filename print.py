

def print_notes(notes, voices):
    if not isinstance(notes, list):
        raise TypeError("passed non-list to print_notes in print.py")

    result = ""

    # Sort notes by start time
    
    notes = sorted(notes, key=lambda note: note.params['st'])

    # Write notes to result, traversing notes using a cursor (or "playhead")

    cursor = 0

    for i in range(len(notes)):

        # Voice parameters
        o_v = voices[notes[i].voice]['o_v']
        a_v = voices[notes[i].voice]['a_v']

        # Note parameters
        st = notes[i].params['st']
        if i+1 < len(notes):
            next_st = notes[i+1].params['st']
        else:
            next_st = None
        ln = notes[i].params['ln']
        p = notes[i].params['p']
        p2 = notes[i].params['p2']

        # Envelope parameters
        at = notes[i].params['at']
        pk = notes[i].params['pk']
        dc = notes[i].params['dc']

        # Delay until start of current note
        result += f"/ {st - cursor},\n"
        cursor = st

        # Write note attack
        result += f"{o_v} {p} {p2} {ln},\n"
        result += f"{a_v} {pk} {at},\n"

        # if next note starts before current note ends, delay onotesy until start of next note
        # (start of next note overrides end of current note)
        if next_st and cursor + ln > next_st:
            result += f"/ {next_st - cursor},\n"
            cursor = next_st
        else:
            result += f"/ {ln},\n"
            cursor += ln

            # same logic as above, but for current note decay time
            if next_st and cursor + dc > next_st:
                result += f"/ {next_st - cursor},\n"
                cursor = next_st
            else:
                result += f"{a_v} 0 {dc},\n"
                result += f"/ {dc},\n"
                cursor += dc

    # Write result to file
    outfilename = "./pd/read/result.txt"
    with open(outfilename, "w") as f:
        f.write(result)



    # for i in range(len(notes)):

    #     # Delay until start of current note
    #     result += f"/ {notes[i].params['st'] - cursor},\n"
    #     cursor = notes[i].params['st']

    #     # Write note attack
    #     result += f"{o_v} {notes[i].params['p']} {notes[i].params['p2']} {notes[i].params['ln']},\n"
    #     result += f"{a_v} {notes[i].params['pk']} {notes[i].params['at']},\n"

    #     # if next note starts before current note ends, delay onotesy until start of next note
    #     # (start of next note overrides end of current note)
    #     if i + 1 < len(notes) and cursor + notes[i].params['ln'] > notes[i + 1].params['st']:
    #         result += f"/ {notes[i + 1].params['st'] - cursor},\n"
    #         cursor = notes[i + 1].params['st']

    #     # otherwise, delay until end of current note and then begin decay current note
    #     else:
    #         result += f"/ {notes[i].params['ln']},\n"
    #         cursor += notes[i].params['ln']

    #         # same logic as above, but for current note decay time
    #         if i + 1 < len(notes) and cursor + notes[i].params['dc'] > notes[i + 1].params['st']:
    #             result += f"/ {notes[i + 1].params['st'] - cursor},\n"
    #             cursor = notes[i + 1].params['st']
    #         else:
    #             result += f"{a_v} 0 {notes[i].params['dc']},\n"
    #             result += f"/ {notes[i].params['dc']},\n"
    #             cursor += notes[i].params['dc']

    # # Write result to file
    # outfilename = "./pd/read/result.txt"
    # with open(outfilename, "w") as f:
    #     f.write(result)