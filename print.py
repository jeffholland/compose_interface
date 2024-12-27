from sys import argv

def print_notes(notes):
    # expects a dict of {id, note obj}
    if not isinstance(notes, dict):
        raise TypeError("passed non-dict to print_notes in print.py")

    result = ""
    nl = []         # notes list, sorted by start time (objects only)

    o_v = 'o1'      # oscillator voice (fixed to 1 for now)
    a_v = 'a1'      # amplifier voice



    # Sort notes by start time
    
    for note_a in notes:
        inserted = False
        for i in range(len(nl)):
            if notes[note_a].start_time < nl[i].start_time:
                nl.insert(i, notes[note_a])
                inserted = True
                break
        if not inserted:
            nl.append(notes[note_a])


    # Write notes to result, traversing notes using a cursor (or "playhead")

    cursor = 0

    for i in range(len(nl)):

        # Delay until start of current note
        result += f"/ {nl[i].start_time - cursor},\n"
        cursor = nl[i].start_time

        if '--debug' in argv:
            result += f"--start of note {i} at {cursor},\n"

        # Write note attack
        result += f"{o_v} {nl[i].pitch} {nl[i].pitch2} {nl[i].length},\n"
        result += f"{a_v} {nl[i].peak} {nl[i].attack},\n"

        # if next note starts before current note ends, delay only until start of next note
        # (start of next note overrides end of current note)
        if i + 1 < len(nl) and cursor + nl[i].length > nl[i + 1].start_time:
            result += f"/ {nl[i + 1].start_time - cursor},\n"
            cursor = nl[i + 1].start_time

            if '--debug' in argv:
                result += f"--cursor to {cursor} for jumping from note {i} to note {i + 1},\n"

        # otherwise, delay until end of current note and then begin decay current note
        else:
            result += f"/ {nl[i].length},\n"
            cursor += nl[i].length

            if '--debug' in argv:
                result += f"--cursor to {cursor} for full length of note {i},\n"

            # same logic as above, but for current note decay time
            if i + 1 < len(nl) and cursor + nl[i].decay > nl[i + 1].start_time:
                result += f"/ {nl[i + 1].start_time - cursor},\n"
                cursor = nl[i + 1].start_time

                if '--debug' in argv:
                    result += f"--cursor to {cursor} for jump from decay of note {i} to note {i + 1},\n"
            else:
                result += f"{a_v} 0 {nl[i].decay},\n"
                result += f"/ {nl[i].decay},\n"
                cursor += nl[i].decay

                if '--debug' in argv:
                    result += f"--cursor to {cursor} for full decay of note {i},\n"

    # Write result to file
    outfilename = "result.txt"

    with open(outfilename, "w") as f:
        f.write(result)

    outfilename = "/Users/jeffholland/Documents/Pd/compose/read/" + outfilename
    with open(outfilename, "w") as f:
        f.write(result)