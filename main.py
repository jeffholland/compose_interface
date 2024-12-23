import tkinter as tk
from constants import *
from note import Note

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bg=W_BG)
        self.grid()
        self.create_widgets()

        self.notes = dict()

    def create_widgets(self):
        # Top row
        self.v_label = tk.Label(self, text="V", bg=W_BG)
        self.v_label.grid(row=0, column=0)

        self.v_entry = tk.Entry(self, width=2, bg=W_BG)
        self.v_entry.grid(row=0, column=1, pady=10)

        self.f1_label = tk.Label(self, text="f1", bg=W_BG)
        self.f1_label.grid(row=0, column=3)

        self.f1_entry = tk.Entry(self, width=2, bg=W_BG)
        self.f1_entry.grid(row=0, column=4, pady=10)

        self.f2_label = tk.Label(self, text="f2", bg=W_BG)
        self.f2_label.grid(row=0, column=5)

        self.f2_entry = tk.Entry(self, width=2, bg=W_BG)
        self.f2_entry.grid(row=0, column=6, pady=10)

        self.f2_label = tk.Label(self, text="f3", bg=W_BG)
        self.f2_label.grid(row=0, column=7)

        self.f3_entry = tk.Entry(self, width=2, bg=W_BG)
        self.f3_entry.grid(row=0, column=8, pady=10)


        # Left side

        self.p_label = tk.Label(self, text="p", bg=W_BG)
        self.p_label.grid(row=4, column=0, padx=10)

        self.p_entry = tk.Entry(self, width=2, bg=W_BG)
        self.p_entry.grid(row=4, column=1, padx=10)

        self.th_label = tk.Label(self, text="θ", bg=W_BG)
        self.th_label.grid(row=5, column=0, padx=10)

        self.th_entry = tk.Entry(self, width=2, bg=W_BG)
        self.th_entry.grid(row=5, column=1, padx=10)


        # Right side

        self.vars_label = tk.Label(self, text="Vars", bg=W_BG, width=12)
        self.vars_label.grid(row=0, column=27, columnspan=2)

        self.vars_list = tk.StringVar()
        self.vars_listbox = tk.Listbox(self, width=10, height=30, listvariable=self.vars_list, bg=W_BG)
        self.vars_list.set('a b c')
        self.vars_listbox.grid(row=1, column=27, rowspan=7, columnspan=2)


        # Bottom

        self.st_label = tk.Label(self, text="st", bg=W_BG)
        self.st_label.grid(row=9, column=3)

        self.st_var = tk.StringVar()
        self.st_entry = tk.Entry(self, width=2, bg=W_BG, textvariable=self.st_var)
        self.st_entry.grid(row=9, column=4, pady=10)

        self.en_label = tk.Label(self, text="en", bg=W_BG)
        self.en_label.grid(row=9, column=5)

        self.en_var = tk.StringVar()
        self.en_entry = tk.Entry(self, width=2, bg=W_BG, textvariable=self.en_var)
        self.en_entry.grid(row=9, column=6, pady=10)

        self.ln_label = tk.Label(self, text="ln", bg=W_BG)
        self.ln_label.grid(row=9, column=7)

        self.ln_var = tk.StringVar()
        self.ln_entry = tk.Entry(self, width=2, bg=W_BG, textvariable=self.ln_var)
        self.ln_entry.grid(row=9, column=8, pady=10)




        # Canvas

        self.note_canvas = tk.Canvas(self, bg=CANVAS_BG, width=CANV_WIDTH, height=CANV_HEIGHT)
        self.note_canvas.grid(row=2, column=2, rowspan=7, columnspan=24)
        self.note_canvas.bind('<Button-1>', self.left_click_canvas)
        self.note_canvas.bind('<Button-2>', self.right_click_canvas)

    def left_click_canvas(self, event):
        id = self.note_canvas.create_line(
            event.x, 
            event.y, 
            event.x + NOTE_WIDTH, 
            event.y, 
            width=NOTE_HEIGHT, 
            fill=NOTE_COLOR)

        self.notes[id] = Note(event.x, event.y, id)
        self.select_note(id)


    def deselect_all_notes(self):
        self.selected_note = None

        all_notes = self.note_canvas.find_all()
        for note in all_notes:
            self.note_canvas.itemconfig(note, fill=NOTE_COLOR)

    def select_note(self, id):
        self.deselect_all_notes()
        self.selected_note = self.notes[id]
        self.note_canvas.itemconfig(id, fill='white')

        self.st_var.set(str(self.selected_note.start_time))
        self.en_var.set(str(self.selected_note.end_time))
        self.ln_var.set(str(self.selected_note.length))


        
    def right_click_canvas(self, event):
        for note in self.notes:
            if (event.x >= self.notes[note].x and event.x <= self.notes[note].x + self.notes[note].width and
                event.y >= self.notes[note].y and event.y <= self.notes[note].y + NOTE_HEIGHT):
                self.select_note(self.notes[note].id)
                return
        self.deselect_all_notes()


app = Application()
app.master.title("Compose interface")
app.master.geometry(f"{W_WIDTH}x{W_HEIGHT}")
app.mainloop()