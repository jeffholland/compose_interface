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


    # Write notes to result

    cursor = nl[0].start_time
    result += f"/ {cursor},\n"
    for i in range(len(nl)):
        # Write note attack
        result += f"{o_v} {nl[i].pitch} {nl[i].pitch2} {nl[i].length},\n"
        result += f"{a_v} {nl[i].peak} {nl[i].attack},\n"

        # Advance cursor
        cursor += nl[i].length
        result += f"/ {nl[i].length},\n"
        result += f"{a_v} 0 {nl[i].decay},\n"
        result += f"/ {nl[i].decay},\n"

        if i + 1 < len(nl) and nl[i + 1].start_time > cursor:
            result += f"/ {nl[i + 1].start_time - cursor},\n"
            cursor = nl[i + 1].start_time


    # Write result to file
    outfilename = "result.txt"
    if '--mv' in argv:
        outfilename = "/Users/jeffholland/Documents/Pd/compose/read/" + outfilename

    with open(outfilename, "w") as f:
        f.write(result)