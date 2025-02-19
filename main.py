import tkinter as tk
import tkinter.messagebox as tk_msg

from json import load as jsload

def load_voices():
    with open(VOICES_PATH, 'r') as f:
        return jsload(f)
    
from constants import *
from note import *
from print import print_notes
from convert import p_to_f


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bg=W_BG)

        self.notes = []
        self.default_note_size = NOTE_SIZE
        self.note_bindings_on = True
        self.selected_note = None
        self.entry_to_param = dict()

        self.voices = load_voices()

        self.grid()
        self.create_widgets()
        self.bind_keys()


    def create_widgets(self):
        # Top row

        self.xsnap_toggle_var = tk.IntVar(self)
        self.xsnap_toggle = tk.Checkbutton(self, text='x', variable=self.xsnap_toggle_var, 
                                        fg=TEXT_COLOR, bg=W_BG)
        self.xsnap_toggle.grid(row=0, column=0)

        self.xsnap_entry_var = tk.StringVar(self)
        self.xsnap_entry = tk.Entry(self, textvariable=self.xsnap_entry_var)
        self.xsnap_entry.grid(row=0, column=1)
        self.xsnap_entry_var.set(0.25)

        self.ysnap_toggle_var = tk.IntVar(self)
        self.ysnap_toggle = tk.Checkbutton(self, text='y', variable=self.ysnap_toggle_var, 
                                        fg=TEXT_COLOR, bg=W_BG)
        self.ysnap_toggle.grid(row=0, column=2)

        self.ysnap_entry_var = tk.StringVar(self)
        self.ysnap_entry = tk.Entry(self, textvariable=self.ysnap_entry_var)
        self.ysnap_entry.grid(row=0, column=3)
        self.ysnap_entry_var.set(1.0)

        self.f1_label = tk.Label(self, text="f1")
        self.f1_label.grid(row=0, column=4)

        self.f1_var = tk.StringVar()
        self.f1_entry = tk.Entry(self, textvariable=self.f1_var)
        self.f1_var.set(2)
        self.f1_entry.grid(row=0, column=5, pady=10)
        self.entry_to_param[str(self.f1_entry)] = 'f1'

        self.f2_label = tk.Label(self, text="f2")
        self.f2_label.grid(row=0, column=6)

        self.f2_var = tk.StringVar()
        self.f2_entry = tk.Entry(self, textvariable=self.f2_var)
        self.f2_var.set(12)
        self.f2_entry.grid(row=0, column=7, pady=10)
        self.entry_to_param[str(self.f2_entry)] = 'f2'

        self.f3_label = tk.Label(self, text="f3")
        self.f3_label.grid(row=0, column=8)

        self.f3_var = tk.StringVar()
        self.f3_entry = tk.Entry(self, textvariable=self.f3_var)
        self.f3_var.set(440)
        self.f3_entry.grid(row=0, column=9, pady=10)
        self.entry_to_param[str(self.f3_entry)] = 'f3'


        # Left side

        self.dependent_vars = [] # variables dependent on x and y axis

        self.p_label = tk.Label(self, text="p")
        self.p_label.grid(row=2, column=0, padx=4)

        self.p_var = tk.StringVar()
        self.dependent_vars.append(self.p_var)
        self.p_entry = tk.Entry(self, textvariable=self.p_var)
        self.p_entry.grid(row=2, column=1, padx=10)
        self.entry_to_param[str(self.p_entry)] = 'p'

        self.fq_label = tk.Label(self, text="f")
        self.fq_label.grid(row=3, column=0, padx=4)

        self.fq_var = tk.StringVar()
        self.dependent_vars.append(self.fq_var)
        self.fq_entry = tk.Entry(self, textvariable=self.fq_var)
        self.fq_entry.grid(row=3, column=1, padx=10)
        self.entry_to_param[str(self.fq_entry)] = 'fq'

        self.p2_label = tk.Label(self, text="p2")
        self.p2_label.grid(row=4, column=0, padx=4)

        self.p2_var = tk.StringVar()
        self.dependent_vars.append(self.p2_var)
        self.p2_entry = tk.Entry(self, textvariable=self.p2_var)
        self.p2_entry.grid(row=4, column=1, padx=10)
        self.entry_to_param[str(self.p2_entry)] = 'p2'

        self.fq2_label = tk.Label(self, text="f2")
        self.fq2_label.grid(row=5, column=0, padx=4)

        self.fq2_var = tk.StringVar()
        self.dependent_vars.append(self.fq2_var)
        self.fq2_entry = tk.Entry(self, textvariable=self.fq2_var)
        self.fq2_entry.grid(row=5, column=1, padx=10)
        self.entry_to_param[str(self.fq2_entry)] = 'fq2'


        # Canvas

        self.note_canvas = tk.Canvas(self, bg=CANVAS_BG, width=CANV_WIDTH, height=CANV_HEIGHT)
        self.note_canvas.grid(row=2, column=2, rowspan=18, columnspan=18)
        self.note_canvas.bind('<Button-1>', self.left_click_canvas)
        self.note_canvas.bind('<Button-2>', self.right_click_canvas)


        # Bottom

        self.print_button = tk.Button(self, text="print", command=self.print)
        self.print_button.grid(row=20, column=0, columnspan=2)

        self.st_label = tk.Label(self, text="st")
        self.st_label.grid(row=20, column=3)

        self.st_var = tk.StringVar()
        self.dependent_vars.append(self.st_var)
        self.st_entry = tk.Entry(self, textvariable=self.st_var)
        self.st_entry.grid(row=20, column=4, pady=10)
        self.entry_to_param[str(self.st_entry)] = 'st'

        self.en_label = tk.Label(self, text="en")
        self.en_label.grid(row=20, column=5)

        self.en_var = tk.StringVar()
        self.dependent_vars.append(self.en_var)
        self.en_entry = tk.Entry(self, textvariable=self.en_var)
        self.en_entry.grid(row=20, column=6, pady=10)
        self.entry_to_param[str(self.en_entry)] = 'en'

        self.ln_label = tk.Label(self, text="ln")
        self.ln_label.grid(row=20, column=7)

        self.ln_var = tk.StringVar()
        self.dependent_vars.append(self.ln_var)
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


        # Right side - top half: voices

        self.voice_entries = []

        self.voices_label = tk.Label(self, text="Voices", width=12)
        self.voices_label.grid(row=0, column=21, columnspan=2)

        self.voices_list = tk.StringVar()
        self.voices_listbox = tk.Listbox(self, width=10, height=12, listvariable=self.voices_list, bg=NOTE_COLOR, selectmode='browse')
        self.voices_listbox.grid(row=1, column=21, rowspan=8, columnspan=2)

        voice_str = ""
        for voice in self.voices:
            voice_str += voice['name'] + ' '
        self.voices_list.set(voice_str)
        self.voices_listbox.selection_set(0)
        for voice in self.voices:
            if voice['name'] == self.voices_listbox.get(0):
                self.selected_voice = voice
        self.voices_listbox.bind('<<ListboxSelect>>', self.listbox_selected)

        self.btn_add_voice = tk.Button(self, text='+', width=1)
        self.btn_add_voice.grid(row=9, column=21)
        self.btn_rm_voice = tk.Button(self, text='-', width=1)
        self.btn_rm_voice.grid(row=9, column=22)

        self.voice_name_label = tk.Label(self, text='name')
        self.voice_name_label.grid(row=2, column=23)

        self.voice_name_var = tk.StringVar()
        self.voice_name_entry = tk.Entry(self, textvariable=self.voice_name_var)
        self.voice_name_entry.grid(row=2, column=24, padx=10)
        self.voice_name_var.set(self.selected_voice['name'])
        self.voice_entries.append(self.voice_name_entry)

        self.o_v_label = tk.Label(self, text='o_v')
        self.o_v_label.grid(row=3, column=23)
        
        self.o_v_var = tk.StringVar()
        self.o_v_entry = tk.Entry(self, textvariable=self.o_v_var)
        self.o_v_entry.grid(row=3, column=24, padx=10)
        self.o_v_var.set(self.selected_voice['o_v'])
        self.voice_entries.append(self.o_v_entry)

        self.a_v_label = tk.Label(self, text='a_v')
        self.a_v_label.grid(row=4, column=23)
        
        self.a_v_var = tk.StringVar()
        self.a_v_entry = tk.Entry(self, textvariable=self.a_v_var)
        self.a_v_entry.grid(row=4, column=24, padx=10)
        self.a_v_var.set(self.selected_voice['a_v'])
        self.voice_entries.append(self.a_v_entry)


        # Right side - bottom half: parameters

        self.param_entries = []

        self.params_label = tk.Label(self, text="Params", width=12)
        self.params_label.grid(row=10, column=21, columnspan=2)

        self.params_list = tk.StringVar()
        self.params_listbox = tk.Listbox(self, width=10, height=12, listvariable=self.params_list, bg=NOTE_COLOR, selectmode='browse')
        self.params_listbox.grid(row=11, column=21, rowspan=8, columnspan=2)
        self.params_listbox.bind('<<ListboxSelect>>', self.listbox_selected)
        self.selected_param = None

        self.btn_add_param = tk.Button(self, text='+', width=1)
        self.btn_add_param.grid(row=19, column=21)
        self.btn_rm_param = tk.Button(self, text='-', width=1)
        self.btn_rm_param.grid(row=19, column=22)

        self.pm_name_label = tk.Label(self, text='name')
        self.pm_name_label.grid(row=11, column=23)
        
        self.pm_name_var = tk.StringVar()
        self.pm_name_entry = tk.Entry(self, textvariable=self.pm_name_var)
        self.pm_name_entry.grid(row=11, column=24, padx=10)
        self.voice_entries.append(self.pm_name_entry)

        self.pm_v1_label = tk.Label(self, text='v1')
        self.pm_v1_label.grid(row=12, column=23)
        
        self.pm_v1_var = tk.StringVar()
        self.pm_v1_entry = tk.Entry(self, textvariable=self.pm_v1_var)
        self.pm_v1_entry.grid(row=12, column=24, padx=10)

        self.pm_v2_label = tk.Label(self, text='v2')
        self.pm_v2_label.grid(row=13, column=23)
        
        self.pm_v2_var = tk.StringVar()
        self.pm_v2_entry = tk.Entry(self, textvariable=self.pm_v2_var)
        self.pm_v2_entry.grid(row=13, column=24, padx=10)

        self.select_voice()


        # Mass-config widgets
        for widget in self.grid_slaves():
            if 'label' in str(widget) or 'entry' in str(widget):
                widget.configure(bg=W_BG, fg=TEXT_COLOR)
            if 'entry' in str(widget):
                widget.configure(width=4)
                self.validate_command = self.register(self.validate_input)
                widget.configure(validate='key', validatecommand=(self.validate_command, '%S'))
            if 'button' in str(widget):
                widget.configure(highlightbackground=W_BG)


    def listbox_selected(self, event):
        # ListboxSelect is a global event called anytime any listbox is touched, thought about, or breathed on.
        # So we have to check which widget is selected and that a selection was actually made.
        
        voice_selected = self.voices_listbox.curselection()
        if event.widget == self.voices_listbox and len(voice_selected) > 0:
            self.select_voice()
        
        param_selected = self.params_listbox.curselection()
        if event.widget == self.params_listbox and len(param_selected) > 0:
            self.select_param()


    def left_click_canvas(self, event):
        note = Note(self.selected_voice['name'], event.x, event.y, size=self.default_note_size)

        # no selected note? then set note params to specified
        if self.selected_note == None:
            for obj in self.grid_slaves():
                if isinstance(obj, tk.Entry):
                    if str(obj) in self.entry_to_param:
                        if len(obj.get()) > 0:
                            key = self.entry_to_param[str(obj)]
                            note.set_param(key, float(obj.get()), pitch_dependent=False)

        id = self.note_canvas.create_line(note.params['x'], note.params['y'], note.params['x2'], note.params['y2'], 
            width=NOTE_HEIGHT, fill=NOTE_COLOR, tag=note.voice)
        note.id = id

        if self.xsnap_toggle_var.get() != 0:
            round_amt = float(self.xsnap_entry_var.get())
            note.xsnap(round_amt)
            self.note_canvas.coords(note.id, note.params['x'], note.params['y'], note.params['x2'], note.params['y2'])
        if self.ysnap_toggle_var.get() != 0:
            round_amt = float(self.ysnap_entry_var.get())
            note.ysnap(round_amt)
            self.note_canvas.coords(note.id, note.params['x'], note.params['y'], note.params['x2'], note.params['y2'])

        self.notes.append(note)

        self.select_note(id)

        for key, val in self.selected_voice['param_defaults'].items():
            self.selected_note.set_param(key+'_1', val)

        self.focus() # remove focus from any entry widgets
        self.note_bindings_on = True


    def select_voice(self):
        for note in self.notes:
            if note.voice == self.selected_voice['name']:
                note.hidden = True
        self.note_canvas.delete(self.selected_voice['name'])

        for voice in self.voices:
            if voice['name'] == self.voices_listbox.get(self.voices_listbox.curselection()[0]):
                self.selected_voice = voice

        for note in self.notes:
            if note.voice == self.selected_voice['name']:
                note.hidden = False
                note.id = self.note_canvas.create_line(
                    note.params['x'], 
                    note.params['y'], 
                    note.params['x2'], 
                    note.params['y2'], 
                    width=NOTE_HEIGHT, 
                    fill=NOTE_COLOR,
                    tag=self.selected_voice['name'])

        params_str = ""
        for param in self.selected_voice['params']:
            params_str += param + ' '
        self.params_list.set(params_str)

        self.voice_name_var.set(self.selected_voice['name'])
        self.o_v_var.set(self.selected_voice['o_v'])
        self.a_v_var.set(self.selected_voice['a_v'])

        self.params_listbox.selection_set(0)


    def select_param(self):
        self.selected_param = self.params_listbox.get(self.params_listbox.curselection()[0])
        self.pm_name_var.set(self.selected_param)

        self.entry_to_param[str(self.pm_v1_entry)] = self.selected_param + '_1'
        self.entry_to_param[str(self.pm_v2_entry)] = self.selected_param + '_2'

        try:
            pm1 = self.selected_note.params[self.selected_param + '_1']
            self.pm_v1_var.set(pm1)
        except (KeyError, AttributeError) as e:
            self.pm_v1_var.set('')

        try:
            pm2 = self.selected_note.params[self.selected_param + '_2']
            self.pm_v2_var.set(pm2)
        except (KeyError, AttributeError) as e:
            self.pm_v2_var.set('')


    def deselect_all_notes(self, event=None):
        self.selected_note = None

        for var in self.dependent_vars:
            var.set('')

        all_notes = self.note_canvas.find_all()
        for note in all_notes:
            self.note_canvas.itemconfig(note, fill=NOTE_COLOR)

    def select_note(self, id):
        self.deselect_all_notes()
        for note in self.notes:
            if note.id == id:
                self.selected_note = note
        self.note_canvas.itemconfig(id, fill='white')

        self.st_var.set(str(round(self.selected_note.params['st'], ROUND_DIGITS)))
        self.en_var.set(str(round(self.selected_note.params['en'], ROUND_DIGITS)))
        self.ln_var.set(str(round(self.selected_note.params['ln'], ROUND_DIGITS)))
        self.p_var.set(str(round(self.selected_note.params['p'], ROUND_DIGITS)))
        self.p2_var.set(str(round(self.selected_note.params['p2'], ROUND_DIGITS)))

        self.set_fq_vars()

        self.at_var.set(str(round(self.selected_note.params['at'], ROUND_DIGITS)))
        self.pk_var.set(str(round(self.selected_note.params['pk'], ROUND_DIGITS)))
        self.dc_var.set(str(round(self.selected_note.params['dc'], ROUND_DIGITS)))

        try:
            pm1 = self.selected_note.params[self.selected_param + '_1']
            self.pm_v1_var.set(pm1)
        except (KeyError, AttributeError, TypeError) as e:
            self.pm_v1_var.set('')
        try:
            pm2 = self.selected_note.params[self.selected_param + '_2']
            self.pm_v2_var.set(pm2)
        except (KeyError, AttributeError, TypeError) as e:
            self.pm_v2_var.set('')
        
    def right_click_canvas(self, event):
        self.focus()
        self.note_bindings_on = True
        for note in self.notes:
            if note.in_bounds(event.x, event.y):
                self.select_note(note.id)
                return
        self.deselect_all_notes()


    def print(self, event=None):
        print_notes(self.notes, self.voices)

    
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
                obj.bind('<KeyPress>', self.entry_keypress)
                obj.bind('<FocusIn>', self.entry_widget_focus)
                if obj in self.voice_entries:
                    obj.bind('<Key-Return>', self.update_selected_voice)
                else:
                    obj.bind('<Key-Return>', self.update_selected_note)

    def update_selected_note(self, event=None):
        if self.selected_note != None and str(event.widget) in self.entry_to_param:
            param = self.entry_to_param[str(event.widget)]
            self.selected_note.set_param(param, float(event.widget.get()))
            self.note_canvas.coords(self.selected_note.id,
                                    self.selected_note.params['x'],
                                    self.selected_note.params['y'],
                                    self.selected_note.params['x2'],
                                    self.selected_note.params['y2'])
            self.select_note(self.selected_note.id)

    def update_selected_voice(self, event=None):
        if event.widget == self.voice_name_entry:
            self.selected_voice['name'] = self.voice_name_var.get()

            new_voice_list = ""
            for voice in self.voices:
                new_voice_list += voice['name'] + ' '
            self.voices_list.set(new_voice_list)

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

    def entry_keypress(self, event):
        self.turn_note_bindings_off()

        if event.widget == self.ln_entry:
            try:
                print(event.widget.selection_get())
                self.default_note_size = length_to_size(float(event.char))
            except:
                self.default_note_size = length_to_size(float(event.widget.get() + event.char))

    def validate_input(self, text):
        try:
            float(text)
            return True
        except:
            if text == '.':
                return True
            else:
                return False

    def delete_selected_note(self):
        self.note_canvas.delete(self.selected_note.id)
        self.notes.remove(self.selected_note)
        self.deselect_all_notes()

    def clear_all(self):
        for note in self.notes:
            self.note_canvas.delete(note.id)
        self.notes.clear()
        self.deselect_all_notes()

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

    def set_fq_vars(self):
        pitch = float(self.p_var.get())
        pitch2 = float(self.p2_var.get())
        f1 = float(self.f1_var.get())
        f2 = float(self.f2_var.get())
        f3 = float(self.f3_var.get())

        fq1 = p_to_f(pitch, f1, f2, f3)
        fq2 = p_to_f(pitch2, f1, f2, f3)
        self.fq_var.set(round(fq1, ROUND_DIGITS))
        self.fq2_var.set(round(fq2, ROUND_DIGITS))

    def entry_widget_focus(self, event):
        event.widget.select_range(0, tk.END)

app = Application()
app.master.title("Compose interface")
app.master.geometry(f"{W_WIDTH}x{W_HEIGHT}")
app.mainloop()