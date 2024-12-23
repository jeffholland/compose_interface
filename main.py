import tkinter as tk

W_WIDTH = 600
W_HEIGHT = 400
W_MARGIN = 40

W_BG = '#94BFA7'
CANVAS_BG = "#E0B7B7"

RECT_WIDTH = 10
RECT_HEIGHT = 5
RECT_COLOR = "#2F2F2F"

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master, bg=W_BG)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.note_canvas = tk.Canvas(self, bg=CANVAS_BG, width=W_WIDTH-(W_MARGIN*2), height=W_HEIGHT-(W_MARGIN*2))
        self.note_canvas.grid(padx=W_MARGIN, pady=W_MARGIN)
        self.note_canvas.bind('<Button-1>', self.left_click_canvas)
        self.note_canvas.bind('<Button-2>', self.right_click_canvas)

    def left_click_canvas(self, event):
        self.note_canvas.create_rectangle(
            event.x, 
            event.y, 
            event.x + RECT_WIDTH, 
            event.y + RECT_HEIGHT, 
            width=0, 
            fill=RECT_COLOR)
        
    def right_click_canvas(self, event):
        closest_obj_id = self.note_canvas.find_closest(event.x, event.y)
        if len(closest_obj_id) > 0:
            self.note_canvas.delete(closest_obj_id)


app = Application()
app.master.title("Compose interface")
app.master.geometry(f"{W_WIDTH}x{W_HEIGHT}")
app.mainloop()