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
            if notes[note_a].params['st'] < nl[i].params['st']:
                nl.insert(i, notes[note_a])
                inserted = True
                break
        if not inserted:
            nl.append(notes[note_a])


    # Write notes to result, traversing notes using a cursor (or "playhead")

    cursor = 0

    for i in range(len(nl)):

        # Delay until start of current note
        result += f"/ {nl[i].params['st'] - cursor},\n"
        cursor = nl[i].params['st']

        # Write note attack
        result += f"{o_v} {nl[i].params['p']} {nl[i].params['p2']} {nl[i].params['ln']},\n"
        result += f"{a_v} {nl[i].params['pk']} {nl[i].params['at']},\n"

        # if next note starts before current note ends, delay only until start of next note
        # (start of next note overrides end of current note)
        if i + 1 < len(nl) and cursor + nl[i].params['ln'] > nl[i + 1].params['st']:
            result += f"/ {nl[i + 1].params['st'] - cursor},\n"
            cursor = nl[i + 1].params['st']

        # otherwise, delay until end of current note and then begin decay current note
        else:
            result += f"/ {nl[i].params['ln']},\n"
            cursor += nl[i].params['ln']

            # same logic as above, but for current note decay time
            if i + 1 < len(nl) and cursor + nl[i].params['dc'] > nl[i + 1].params['st']:
                result += f"/ {nl[i + 1].params['st'] - cursor},\n"
                cursor = nl[i + 1].params['st']
            else:
                result += f"{a_v} 0 {nl[i].params['dc']},\n"
                result += f"/ {nl[i].params['dc']},\n"
                cursor += nl[i].params['dc']

    # Write result to file
    outfilename = "./pd/read/result.txt"
    with open(outfilename, "w") as f:
        f.write(result)