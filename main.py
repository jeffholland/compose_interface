import tkinter as tk

from constants import *
from note import Note
from print import print_notes

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bg=W_BG)

        self.notes = dict()
        self.note_bindings_on = True
        self.selected_note = None
        self.entry_to_param = dict()

        self.grid()
        self.create_widgets()
        self.bind_keys()

        for widget in self.grid_slaves():
            if 'label' in str(widget) or 'entry' in str(widget):
                widget.configure(bg=W_BG, fg=TEXT_COLOR)
            if 'entry' in str(widget):
                widget.configure(width=4)

    def create_widgets(self):
        # Top row
        self.v_label = tk.Label(self, text="V")
        self.v_label.grid(row=0, column=0)

        self.v_var = tk.StringVar()
        self.v_entry = tk.Entry(self, textvariable=self.v_var)
        self.v_var.set(0)
        self.v_entry.grid(row=0, column=1, pady=10)
        self.entry_to_param[str(self.v_entry)] = 'v'

        self.f1_label = tk.Label(self, text="f1")
        self.f1_label.grid(row=0, column=3)

        self.f1_var = tk.StringVar()
        self.f1_entry = tk.Entry(self, textvariable=self.f1_var)
        self.f1_var.set(2)
        self.f1_entry.grid(row=0, column=4, pady=10)
        self.entry_to_param[str(self.f1_entry)] = 'f1'

        self.f2_label = tk.Label(self, text="f2")
        self.f2_label.grid(row=0, column=5)

        self.f2_var = tk.StringVar()
        self.f2_entry = tk.Entry(self, textvariable=self.f2_var)
        self.f2_var.set(12)
        self.f2_entry.grid(row=0, column=6, pady=10)
        self.entry_to_param[str(self.f2_entry)] = 'f2'

        self.f3_label = tk.Label(self, text="f3")
        self.f3_label.grid(row=0, column=7)

        self.f3_var = tk.StringVar()
        self.f3_entry = tk.Entry(self, textvariable=self.f3_var)
        self.f3_var.set(440)
        self.f3_entry.grid(row=0, column=8, pady=10)
        self.entry_to_param[str(self.f3_entry)] = 'f3'


        # Left side

        self.p_label = tk.Label(self, text="p")
        self.p_label.grid(row=2, column=0, padx=4)

        self.p_var = tk.StringVar()
        self.p_entry = tk.Entry(self, textvariable=self.p_var)
        self.p_var.set(48)
        self.p_entry.grid(row=2, column=1, padx=10)
        self.entry_to_param[str(self.p_entry)] = 'p'

        self.fq_label = tk.Label(self, text="f")
        self.fq_label.grid(row=3, column=0, padx=4)

        self.fq_var = tk.StringVar()
        self.fq_entry = tk.Entry(self, textvariable=self.fq_var)
        self.fq_entry.grid(row=3, column=1, padx=10)
        self.entry_to_param[str(self.fq_entry)] = 'fq'

        self.p2_label = tk.Label(self, text="p2")
        self.p2_label.grid(row=4, column=0, padx=4)

        self.p2_var = tk.StringVar()
        self.p2_entry = tk.Entry(self, textvariable=self.p2_var)
        self.p2_var.set(48)
        self.p2_entry.grid(row=4, column=1, padx=10)
        self.entry_to_param[str(self.p2_entry)] = 'p2'

        self.fq2_label = tk.Label(self, text="f2")
        self.fq2_label.grid(row=5, column=0, padx=4)

        self.fq2_var = tk.StringVar()
        self.fq2_entry = tk.Entry(self, textvariable=self.fq2_var)
        self.fq2_entry.grid(row=5, column=1, padx=10)
        self.entry_to_param[str(self.fq2_entry)] = 'fq2'
        self.set_fq_vars()


        # Canvas

        self.note_canvas = tk.Canvas(self, bg=CANVAS_BG, width=CANV_WIDTH, height=CANV_HEIGHT)
        self.note_canvas.grid(row=2, column=2, rowspan=18, columnspan=18)
        self.note_canvas.bind('<Button-1>', self.left_click_canvas)
        self.note_canvas.bind('<Button-2>', self.right_click_canvas)


        # Right side

        self.voices_label = tk.Label(self, text="Voices", width=12)
        self.voices_label.grid(row=0, column=21, columnspan=2)

        self.voices_list = tk.StringVar()
        self.voices_listbox = tk.Listbox(self, width=10, height=12, listvariable=self.voices_list, bg=NOTE_COLOR)
        self.voices_listbox.grid(row=1, column=21, rowspan=8, columnspan=2)

        self.btn_add_voice = tk.Button(self, text='+', width=1, highlightbackground=W_BG)
        self.btn_add_voice.grid(row=9, column=21)
        self.btn_rm_voice = tk.Button(self, text='-', width=1, highlightbackground=W_BG)
        self.btn_rm_voice.grid(row=9, column=22)

        self.params_label = tk.Label(self, text="Params", width=12)
        self.params_label.grid(row=10, column=21, columnspan=2)

        self.params_list = tk.StringVar()
        self.params_listbox = tk.Listbox(self, width=10, height=12, listvariable=self.params_list, bg=NOTE_COLOR)
        self.params_listbox.grid(row=11, column=21, rowspan=8, columnspan=2)

        self.btn_add_param = tk.Button(self, text='+', width=1, highlightbackground=W_BG)
        self.btn_add_param.grid(row=19, column=21)
        self.btn_rm_param = tk.Button(self, text='-', width=1, highlightbackground=W_BG)
        self.btn_rm_param.grid(row=19, column=22)

        # self.vars_label = tk.Label(self, text="Vars", width=12)
        # self.vars_label.grid(row=0, column=23, columnspan=2)

        # self.vars_list = tk.StringVar()
        # self.vars_listbox = tk.Listbox(self, width=10, height=30, listvariable=self.vars_list, bg=NOTE_COLOR)
        # self.vars_listbox.grid(row=1, column=23, rowspan=18, columnspan=2)

        # self.btn_add_var = tk.Button(self, text='+', width=1, highlightbackground=W_BG)
        # self.btn_add_var.grid(row=20, column=23)
        # self.btn_rm_var = tk.Button(self, text='-', width=1, highlightbackground=W_BG)
        # self.btn_rm_var.grid(row=20, column=24)


        # Bottom

        self.print_button = tk.Button(self, text="print", highlightbackground=W_BG, command=self.print)
        self.print_button.grid(row=20, column=0, columnspan=2)

        self.st_label = tk.Label(self, text="st")
        self.st_label.grid(row=20, column=3)

        self.st_var = tk.StringVar()
        self.st_entry = tk.Entry(self, textvariable=self.st_var)
        self.st_entry.grid(row=20, column=4, pady=10)
        self.entry_to_param[str(self.st_entry)] = 'st'

        self.en_label = tk.Label(self, text="en")
        self.en_label.grid(row=20, column=5)

        self.en_var = tk.StringVar()
        self.en_entry = tk.Entry(self, textvariable=self.en_var)
        self.en_entry.grid(row=20, column=6, pady=10)
        self.entry_to_param[str(self.en_entry)] = 'en'

        self.ln_label = tk.Label(self, text="ln")
        self.ln_label.grid(row=20, column=7)

        self.ln_var = tk.StringVar()
        self.ln_entry = tk.Entry(self, textvariable=self.ln_var)
        self.ln_entry.grid(row=20, column=8, pady=10)
        self.entry_to_param[str(self.ln_entry)] = 'ln'

        self.at_label = tk.Label(self, text='at')
        self.at_label.grid(row=20, column=9)

        self.at_var = tk.StringVar()
        self.at_entry = tk.Entry(self, textvariable=self.at_var)
        self.at_var.set(0.005)
        self.at_entry.grid(row=20, column=10, pady=10)
        self.entry_to_param[str(self.at_entry)] = 'at'

        self.pk_label = tk.Label(self, text='pk')
        self.pk_label.grid(row=20, column=11)

        self.pk_var = tk.StringVar()
        self.pk_entry = tk.Entry(self, textvariable=self.pk_var)
        self.pk_var.set(0.25)
        self.pk_entry.grid(row=20, column=12, pady=10)
        self.entry_to_param[str(self.pk_entry)] = 'pk'

        self.dc_label = tk.Label(self, text='dc')
        self.dc_label.grid(row=20, column=13)

        self.dc_var = tk.StringVar()
        self.dc_entry = tk.Entry(self, textvariable=self.dc_var)
        self.dc_var.set(0.1)
        self.dc_entry.grid(row=20, column=14)
        self.entry_to_param[str(self.dc_entry)] = 'dc'


    def set_fq_vars(self):
        pitch = float(self.p_var.get())
        pitch2 = float(self.p2_var.get())
        f1 = float(self.f1_var.get())
        f2 = float(self.f2_var.get())
        f3 = float(self.f3_var.get())

        fq1 = pow(f1, ((pitch - 69) / f2)) * f3
        fq2 = pow(f1, ((pitch2 - 69) / f2)) * f3
        self.fq_var.set(fq1)
        self.fq2_var.set(fq2)

    def left_click_canvas(self, event):
        id = self.note_canvas.create_line(
            event.x, 
            event.y, 
            event.x + NOTE_SIZE, 
            event.y, 
            width=NOTE_HEIGHT, 
            fill=NOTE_COLOR)

        self.notes[id] = Note(event.x, event.y, id)

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

        self.st_var.set(str(self.selected_note.params['st']))
        self.en_var.set(str(self.selected_note.params['en']))
        self.ln_var.set(str(self.selected_note.params['ln']))
        self.p_var.set(str(self.selected_note.params['p']))
        self.p2_var.set(str(self.selected_note.params['p2']))
        self.set_fq_vars()
        
    def right_click_canvas(self, event):
        self.focus()
        self.note_bindings_on = True
        for note in self.notes:
            if (event.x >= self.notes[note].params['x'] and event.x <= self.notes[note].params['x'] + self.notes[note].size and
                event.y >= self.notes[note].params['y'] and event.y <= self.notes[note].params['y'] + NOTE_HEIGHT):
                self.select_note(self.notes[note].id)
                return
        self.deselect_all_notes()


    def print(self, event=None):
        print_notes(self.notes)

    
    def bind_keys(self):
        self.bind_all('<Key-BackSpace>', self.backspace_pressed)
        self.bind_all('<Key-Return>', self.return_pressed)
        self.bind_all('<Left>', self.arrow_key_pressed)
        self.bind_all('<Right>', self.arrow_key_pressed)
        self.bind_all('<Up>', self.arrow_key_pressed)
        self.bind_all('<Down>', self.arrow_key_pressed)

        for obj in self.grid_slaves():
            if isinstance(obj, tk.Entry):
                obj.bind('<Button-1>', self.turn_note_bindings_off)
                obj.bind('<KeyPress>', self.turn_note_bindings_off)
                obj.bind('<Key-Return>', self.update_selected_note)

    def update_selected_note(self, event=None):
        param = self.entry_to_param[str(event.widget)]
        self.selected_note.set_param(param, float(event.widget.get()))
        self.note_canvas.coords(self.selected_note.id,
                                self.selected_note.params['x'],
                                self.selected_note.params['y'],
                                self.selected_note.params['x2'],
                                self.selected_note.params['y2'])
        self.select_note(self.selected_note.id)

    def turn_note_bindings_off(self, event=None):
        self.note_bindings_on = False

    def backspace_pressed(self, event):
        if event.state == 0 and self.selected_note and self.note_bindings_on:
            self.delete_selected_note()
        elif event.state == 1:
            self.clear_all()

    def return_pressed(self, event):
        # shift+enter to print to text
        if event.state == 1:
            self.print()

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
        if self.selected_note.params['x'] + xmove < 0:
            xmove = -(self.selected_note.params['x'])

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
                                self.selected_note.params['x'], self.selected_note.params['y'], 
                                self.selected_note.params['x2'], self.selected_note.params['y2'])
        self.select_note(self.selected_note.id)

    def tilt_selected_note(self, direction):
        if direction == 'Up':
            tilt_amount = -(MOVE_AMOUNT)
        elif direction == 'Down':
            tilt_amount = MOVE_AMOUNT
        
        self.selected_note.tilt(tilt_amount)
        self.note_canvas.coords(self.selected_note.id, self.selected_note.params['x'], 
                                self.selected_note.params['y'], self.selected_note.params['x2'], self.selected_note.params['y2'])
        self.select_note(self.selected_note.id)

app = Application()
app.master.title("Compose interface")
app.master.geometry(f"{W_WIDTH}x{W_HEIGHT}")
app.mainloop()