import tkinter as tk
import math

class RotatingLineApp:
    def __init__(self, root):
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        # Initial line coordinates (x1, y1, x2, y2)
        self.x1, self.y1, self.x2, self.y2 = 50, 150, 200, 150
        self.line = self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, width=2)

        # Center of rotation (can be the center of the canvas, the center of the line, or a specific point)
        self.center_x, self.center_y = 50, 150  # Pivot point (center of canvas)

        # Add a button to trigger the rotation
        self.rotate_button = tk.Button(root, text="Rotate Line", command=self.rotate_line)
        self.rotate_button.pack()

    def rotate_line(self):
        # Angle to rotate in degrees (can be dynamic)
        angle_degrees = 15
        angle_radians = math.radians(angle_degrees)

        # Calculate new coordinates after rotation
        self.x1, self.y1 = self.rotate_point(self.x1, self.y1, angle_radians)
        self.x2, self.y2 = self.rotate_point(self.x2, self.y2, angle_radians)

        # Redraw the line with new coordinates
        self.canvas.coords(self.line, self.x1, self.y1, self.x2, self.y2)

    def rotate_point(self, x, y, angle_radians):
        # Rotate a point (x, y) around (center_x, center_y)
        dx, dy = x - self.center_x, y - self.center_y
        new_x = self.center_x + (dx * math.cos(angle_radians) - dy * math.sin(angle_radians))
        new_y = self.center_y + (dx * math.sin(angle_radians) + dy * math.cos(angle_radians))
        return new_x, new_y

if __name__ == "__main__":
    root = tk.Tk()
    app = RotatingLineApp(root)
    root.mainloop()
