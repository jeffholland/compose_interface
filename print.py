from sys import argv

def print_notes(notes, voices):
    if not isinstance(notes, list):
        raise TypeError("passed non-list to print_notes in print.py")

    result = ""

    # Sort notes by start time
    
    notes = sorted(notes, key=lambda note: note.params['st'])

    # Write notes to result, traversing notes using a cursor (or "playhead")
    # Track "unfinished" notes in a list to make sure all notes get finished

    cursor = 0
    unfinished = []

    for i in range(len(notes)):

        # Voice parameters
        for voice in voices:
            if notes[i].voice == voice['name']:
                o_v = voice['o_v']
                a_v = voice['a_v']

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
        if st > cursor:
            result += f"/ {st - cursor},\n"
            cursor = st

        # Write note attack
        result += f"{o_v} {p} {p2} {ln},\n"
        result += f"{a_v} {pk} {at},\n"

        # Write additional note parameters
        for key, v1 in notes[i].params.items():
            # add'l parameters have suffix _1 and _2 appended
            if key[-2:] == '_1':
                pm = key[:-2]

                if pm + '_2' in notes[i].params:
                    v2 = notes[i].params[pm + '_2']
                    result += f"{pm} {v1} {v2} {ln},\n"
                else:
                    result += f"{pm} {v1},\n"

        # if next note starts before current note ends, delay until start of next note
        # (start of next note overrides end of current note)
        if next_st and cursor + ln > next_st:
            result += f"/ {next_st - cursor},\n"
            cursor = next_st

            unfinished.append(notes[i])
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

        # finish unfinished notes
        for u_note in unfinished:
            u_en = u_note.params['en']
            u_dc = u_note.params['dc']
            u_a_v = next((voice['a_v'] for voice in voices if voice['name'] == u_note.voice), None)

            if not next_st or next_st > u_en:
                result += f"/ {u_en - cursor},\n"
                cursor = u_en
                result += f"{u_a_v} 0 {u_dc},\n"

                if not next_st:
                    result += f"/ {u_dc},\n"
                
                unfinished.remove(u_note)


    # Write result to file
    outfilename = "./pd/read/result.txt"
    with open(outfilename, "w") as f:
        f.write(result)