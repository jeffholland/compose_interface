def print_notes(notes):
    result = ""
    notes_sorted_list = []

    o_v = 'o1'
    a_v = 'a1'

    # Sort notes by start time
    
    for note_a in notes:
        inserted = False
        for i in range(len(notes_sorted_list)):
            if notes[note_a].start_time < notes_sorted_list[i].start_time:
                notes_sorted_list.insert(i, notes[note_a])
                inserted = True
                break
        if not inserted:
            notes_sorted_list.append(notes[note_a])

    # Write notes to result string

    cursor = notes_sorted_list[0].start_time
    result += f"/ {cursor},\n"
    for i in range(len(notes_sorted_list)):
        # Write note attack
        result += f"{o_v} {notes_sorted_list[i].pitch},\n"
        result += f"{a_v} {notes_sorted_list[i].peak} {notes_sorted_list[i].attack},\n"

        # Advance cursor
        cursor += notes_sorted_list[i].length
        result += f"/ {notes_sorted_list[i].length},\n"
        result += f"{a_v} 0 {notes_sorted_list[i].decay},\n"
        result += f"/ {notes_sorted_list[i].decay},\n"

        if i + 1 < len(notes_sorted_list):
            result += f"/ {notes_sorted_list[i + 1].start_time - cursor},\n"
            cursor = notes_sorted_list[i + 1].start_time


    # Write to file

    with open("/Users/jeffholland/Documents/Pd/compose/read/result.txt", "w") as f:
        f.write(result)