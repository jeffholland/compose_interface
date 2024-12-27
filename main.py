import tkinter as tk

from constants import *
from note import Note
from print import print_notes

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bg=W_BG)

        self.notes = dict()
        self.note_bindings_on = True

        self.grid()
        self.create_widgets()
        self.bind_keys()

    def create_widgets(self):
        # Top row
        self.v_label = tk.Label(self, text="V", bg=W_BG)
        self.v_label.grid(row=0, column=0)

        self.v_var = tk.StringVar()
        self.v_entry = tk.Entry(self, width=2, bg=W_BG, textvariable=self.v_var)
        self.v_var.set(0)
        self.v_entry.grid(row=0, column=1, pady=10)

        self.f1_label = tk.Label(self, text="f1", bg=W_BG)
        self.f1_label.grid(row=0, column=3)

        self.f1_var = tk.StringVar()
        self.f1_entry = tk.Entry(self, width=3, bg=W_BG, textvariable=self.f1_var)
        self.f1_var.set(2)
        self.f1_entry.grid(row=0, column=4, pady=10)

        self.f2_label = tk.Label(self, text="f2", bg=W_BG)
        self.f2_label.grid(row=0, column=5)

        self.f2_var = tk.StringVar()
        self.f2_entry = tk.Entry(self, width=3, bg=W_BG, textvariable=self.f2_var)
        self.f2_var.set(12)
        self.f2_entry.grid(row=0, column=6, pady=10)

        self.f3_label = tk.Label(self, text="f3", bg=W_BG)
        self.f3_label.grid(row=0, column=7)

        self.f3_var = tk.StringVar()
        self.f3_entry = tk.Entry(self, width=3, bg=W_BG, textvariable=self.f3_var)
        self.f3_var.set(440)
        self.f3_entry.grid(row=0, column=8, pady=10)


        # Left side

        self.p_label = tk.Label(self, text="p", bg=W_BG)
        self.p_label.grid(row=2, column=0, padx=10)

        self.p_var = tk.StringVar()
        self.p_entry = tk.Entry(self, width=3, bg=W_BG, textvariable=self.p_var)
        self.p_var.set(48)
        self.p_entry.grid(row=2, column=1, padx=10)

        self.fq_label = tk.Label(self, text="f", bg=W_BG)
        self.fq_label.grid(row=3, column=0, padx=10)

        self.fq_var = tk.StringVar()
        self.fq_entry = tk.Entry(self, width=3, bg=W_BG, textvariable=self.fq_var)
        self.set_fq_var()
        self.fq_entry.grid(row=3, column=1, padx=10)

        self.p2_label = tk.Label(self, text="p2", bg=W_BG)
        self.p2_label.grid(row=4, column=0, padx=10)

        self.p2_var = tk.StringVar()
        self.p2_entry = tk.Entry(self, width=3, bg=W_BG, textvariable=self.p2_var)
        self.p2_var.set(0)
        self.p2_entry.grid(row=4, column=1, padx=10)


        # Canvas

        self.note_canvas = tk.Canvas(self, bg=CANVAS_BG, width=CANV_WIDTH, height=CANV_HEIGHT)
        self.note_canvas.grid(row=2, column=2, rowspan=18, columnspan=18)
        self.note_canvas.bind('<Button-1>', self.left_click_canvas)
        self.note_canvas.bind('<Button-2>', self.right_click_canvas)


        # Right side

        self.voices_label = tk.Label(self, text="Voices", bg=W_BG, width=12)
        self.voices_label.grid(row=0, column=21, columnspan=2)

        self.voices_list = tk.StringVar()
        self.voices_listbox = tk.Listbox(self, width=10, height=30, listvariable=self.voices_list, bg=NOTE_COLOR)
        self.voices_listbox.grid(row=1, column=21, rowspan=18, columnspan=2)

        self.btn_add_voice = tk.Button(self, text='+', width=1, highlightbackground=W_BG)
        self.btn_add_voice.grid(row=20, column=21)
        self.btn_rm_voice = tk.Button(self, text='-', width=1, highlightbackground=W_BG)
        self.btn_rm_voice.grid(row=20, column=22)

        self.vars_label = tk.Label(self, text="Vars", bg=W_BG, width=12)
        self.vars_label.grid(row=0, column=23, columnspan=2)

        self.vars_list = tk.StringVar()
        self.vars_listbox = tk.Listbox(self, width=10, height=30, listvariable=self.vars_list, bg=NOTE_COLOR)
        self.vars_listbox.grid(row=1, column=23, rowspan=18, columnspan=2)

        self.btn_add_var = tk.Button(self, text='+', width=1, highlightbackground=W_BG)
        self.btn_add_var.grid(row=20, column=23)
        self.btn_rm_var = tk.Button(self, text='-', width=1, highlightbackground=W_BG)
        self.btn_rm_var.grid(row=20, column=24)


        # Bottom

        self.print_button = tk.Button(self, text="print", highlightbackground=W_BG, command=self.print)
        self.print_button.grid(row=20, column=0, columnspan=2)

        self.st_label = tk.Label(self, text="st", bg=W_BG)
        self.st_label.grid(row=20, column=3)

        self.st_var = tk.StringVar()
        self.st_entry = tk.Entry(self, width=4, bg=W_BG, textvariable=self.st_var)
        self.st_entry.grid(row=20, column=4, pady=10)

        self.en_label = tk.Label(self, text="en", bg=W_BG)
        self.en_label.grid(row=20, column=5)

        self.en_var = tk.StringVar()
        self.en_entry = tk.Entry(self, width=4, bg=W_BG, textvariable=self.en_var)
        self.en_entry.grid(row=20, column=6, pady=10)

        self.ln_label = tk.Label(self, text="ln", bg=W_BG)
        self.ln_label.grid(row=20, column=7)

        self.ln_var = tk.StringVar()
        self.ln_entry = tk.Entry(self, width=4, bg=W_BG, textvariable=self.ln_var)
        self.ln_entry.grid(row=20, column=8, pady=10)

        self.at_label = tk.Label(self, text='at', bg=W_BG)
        self.at_label.grid(row=20, column=9)

        self.at_var = tk.StringVar()
        self.at_entry = tk.Entry(self, width=4, bg=W_BG, textvariable=self.at_var)
        self.at_var.set(0.005)
        self.at_entry.grid(row=20, column=10, pady=10)

        self.pk_label = tk.Label(self, text='pk', bg=W_BG)
        self.pk_label.grid(row=20, column=11)

        self.pk_var = tk.StringVar()
        self.pk_entry = tk.Entry(self, width=4, bg=W_BG, textvariable=self.pk_var)
        self.pk_var.set(0.25)
        self.pk_entry.grid(row=20, column=12, pady=10)

        self.dc_label = tk.Label(self, text='dc', bg=W_BG)
        self.dc_label.grid(row=20, column=13)

        self.dc_var = tk.StringVar()
        self.dc_entry = tk.Entry(self, width=4, bg=W_BG, textvariable=self.dc_var)
        self.dc_var.set(0.1)
        self.dc_entry.grid(row=20, column=14)


    def set_fq_var(self):
        pitch = float(self.p_var.get())
        f1 = float(self.f1_var.get())
        f2 = float(self.f2_var.get())
        f3 = float(self.f3_var.get())

        frequency = pow(f1, ((pitch - 69) / f2)) * f3
        self.fq_var.set(frequency)

    def left_click_canvas(self, event):
        id = self.note_canvas.create_line(
            event.x, 
            event.y, 
            event.x + NOTE_SIZE, 
            event.y, 
            width=NOTE_HEIGHT, 
            fill=NOTE_COLOR)

        self.notes[id] = Note(event.x, event.y, id)

        self.notes[id].set_params(
            {
                'v': self.v_var.get(),
                'f1': self.f1_var.get(),
                'f2': self.f2_var.get(),
                'f3': self.f3_var.get(),
                'p2': self.p2_var.get(),
                'at': self.at_var.get(),
                'pk': self.pk_var.get(),
                'dc': self.dc_var.get()
            }
        )

        self.select_note(id)
        self.focus() # remove focus from any entry widgets
        self.note_bindings_on = True


    def deselect_all_notes(self, event=None):
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
        self.p_var.set(str(self.selected_note.pitch))
        self.p2_var.set(str(self.selected_note.pitch2))
        self.set_fq_var()
        
    def right_click_canvas(self, event):
        for note in self.notes:
            if (event.x >= self.notes[note].x and event.x <= self.notes[note].x + self.notes[note].size and
                event.y >= self.notes[note].y and event.y <= self.notes[note].y + NOTE_HEIGHT):
                self.select_note(self.notes[note].id)
                self.note_bindings_on = True
                return
        self.deselect_all_notes()

    def print(self, event=None):
        print_notes(self.notes)

    
    def bind_keys(self):
        self.bind_all('<Key-BackSpace>', self.backspace_pressed)
        self.bind_all('<Key-Return>', self.print)
        self.bind_all('<Left>', self.arrow_key_pressed)
        self.bind_all('<Right>', self.arrow_key_pressed)
        self.bind_all('<Up>', self.arrow_key_pressed)
        self.bind_all('<Down>', self.arrow_key_pressed)

        for obj in self.grid_slaves():
            if isinstance(obj, tk.Entry):
                obj.bind('<Button-1>', self.turn_note_bindings_off)
                obj.bind('<KeyPress>', self.turn_note_bindings_off)

    def turn_note_bindings_off(self, event=None):
        self.note_bindings_on = False

    def backspace_pressed(self, event):
        if event.state == 0 and self.selected_note and self.note_bindings_on:
            self.delete_selected_note()
        elif event.state == 1:
            self.clear_all()

    def arrow_key_pressed(self, event):
        if self.selected_note and self.note_bindings_on:
            # no modifier keys - move selected note
            if event.state == 96:
                self.move_selected_note(event.keysym)

            # shift key held with left/right - resize selected note
            elif event.state == 97 and (event.keysym == 'Left' or event.keysym == 'Right'):
                self.resize_selected_note(event.keysym)

            # shift key held with up/down - tilt selected note
            elif event.state == 97 and (event.keysym == 'Up' or event.keysym == 'Down'):
                self.tilt_selected_note(event.keysym)

    def delete_selected_note(self):
        self.note_canvas.delete(self.selected_note.id)
        self.notes.pop(self.selected_note.id)
        self.selected_note = None

    def clear_all(self):
        for note in self.notes:
            self.note_canvas.delete(note)
        self.notes.clear()
        self.selected_note = None

    def move_selected_note(self, direction):
        xmove = 0
        ymove = 0
        if direction == 'Left':
            xmove = -(MOVE_AMOUNT)
        elif direction == 'Right':
            xmove = MOVE_AMOUNT
        elif direction == 'Up':
            ymove = -(MOVE_AMOUNT)
        elif direction == 'Down':
            ymove = MOVE_AMOUNT

        # hard left boundary at 0
        if self.selected_note.x + xmove < 0:
            xmove = -(self.selected_note.x)

        self.note_canvas.move(self.selected_note.id, xmove, ymove)
        self.selected_note.move(xmove, ymove)
        self.select_note(self.selected_note.id)

    def resize_selected_note(self, direction):
        new_size = self.selected_note.size

        if direction == 'Left':
            if self.selected_note.size < RESIZE_AMOUNT:
                new_size = self.selected_note.size / 2
            else:
                new_size = self.selected_note.size - RESIZE_AMOUNT
        elif direction == 'Right':
            new_size = self.selected_note.size + RESIZE_AMOUNT
        else:
            return

        self.selected_note.resize(new_size)
        self.note_canvas.coords(self.selected_note.id, 
                                self.selected_note.x, self.selected_note.y, 
                                self.selected_note.x2, self.selected_note.y2)
        self.select_note(self.selected_note.id)

    def tilt_selected_note(self, direction):
        if direction == 'Up':
            tilt_amount = -(MOVE_AMOUNT)
        elif direction == 'Down':
            tilt_amount = MOVE_AMOUNT
        
        self.selected_note.tilt(tilt_amount)
        self.note_canvas.coords(self.selected_note.id, self.selected_note.x, self.selected_note.y, self.selected_note.x2, self.selected_note.y2)
        self.select_note(self.selected_note.id)

app = Application()
app.master.title("Compose interface")
app.master.geometry(f"{W_WIDTH}x{W_HEIGHT}")
app.mainloop()