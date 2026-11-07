import tkinter as tk
from tkinter import ttk
import random
class GameOfLife:
   def __init__(self, root, rows=30, cols=40):
       self.root = root
       self.root.title("Conway's Game of Life")
       self.rows = rows
       self.cols = cols
       self.cell_size = 20
       self.is_running = False
       self.speed = 200
       self.birth_rules = {3}
       self.survive_rules = {2, 3}
       self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
       self.setup_ui()
   def setup_ui(self):
       control_frame = ttk.LabelFrame(self.root, text=" Kontroller & Kurallar ", padding=10)
       control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
       self.btn_start = ttk.Button(control_frame, text="Başlat", command=self.toggle_simulation)
       self.btn_start.pack(fill=tk.X, pady=5)
       btn_step = ttk.Button(control_frame, text="Tek Adım İlerle", command=self.step)
       btn_step.pack(fill=tk.X, pady=5)
       btn_random = ttk.Button(control_frame, text="Rastgele Doldur", command=self.randomize_grid)
       btn_random.pack(fill=tk.X, pady=5)
       btn_clear = ttk.Button(control_frame, text="Temizle", command=self.clear_grid)
       btn_clear.pack(fill=tk.X, pady=5)
       ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, pady=10)
       ttk.Label(control_frame, text="Doğum Kuralları (Ölü -> Canlı)", font=('Helvetica', 10, 'bold')).pack(anchor=tk.W)
       ttk.Label(control_frame, text="Gereken komşu sayısı:").pack(anchor=tk.W, pady=2)
       self.birth_vars = {}
       for i in range(9):
           self.birth_vars[i] = tk.BooleanVar(value=(i in self.birth_rules))
           cb = ttk.Checkbutton(control_frame, text=str(i), variable=self.birth_vars[i], command=self.update_rules)
           cb.pack(anchor=tk.W, padx=10)
       ttk.Separator(control_frame, orient='horizontal').pack(fill=tk.X, pady=10)
       ttk.Label(control_frame, text="Hayatta Kalma Kuralları (Canlı -> Canlı)", font=('Helvetica', 10, 'bold')).pack(anchor=tk.W)
       ttk.Label(control_frame, text="Gereken komşu sayısı:").pack(anchor=tk.W, pady=2)
       self.survive_vars = {}
       for i in range(9):
           self.survive_vars[i] = tk.BooleanVar(value=(i in self.survive_rules))
           cb = ttk.Checkbutton(control_frame, text=str(i), variable=self.survive_vars[i], command=self.update_rules)
           cb.pack(anchor=tk.W, padx=10)
       canvas_frame = ttk.Frame(self.root)
       canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
       self.canvas = tk.Canvas(canvas_frame, width=self.cols*self.cell_size, height=self.rows*self.cell_size, bg="white")
       self.canvas.pack()
       self.canvas.bind("<Button-1>", self.on_canvas_click)
       self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
       self.draw_grid()
   def update_rules(self):
       self.birth_rules = {i for i, var in self.birth_vars.items() if var.get()}
       self.survive_rules = {i for i, var in self.survive_vars.items() if var.get()}
   def draw_grid(self):
       self.canvas.delete("all")
       for r in range(self.rows):
           for c in range(self.cols):
               x1 = c * self.cell_size
               y1 = r * self.cell_size
               x2 = x1 + self.cell_size
               y2 = y1 + self.cell_size
               color = "black" if self.grid[r][c] == 1 else "white"
               self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#e0e0e0")
   def toggle_simulation(self):
       if self.is_running:
           self.is_running = False
           self.btn_start.config(text="Başlat")
       else:
           self.is_running = True
           self.btn_start.config(text="Durdur")
           self.run_simulation()
   def run_simulation(self):
       if self.is_running:
           self.step()
           self.root.after(self.speed, self.run_simulation)
   def count_neighbors(self, r, c):
       count = 0
       for dr in [-1, 0, 1]:
           for dc in [-1, 0, 1]:
               if dr == 0 and dc == 0:
                   continue
               nr = (r + dr) % self.rows
               nc = (c + dc) % self.cols
               count += self.grid[nr][nc]
       return count
   def step(self):
       new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
       for r in range(self.rows):
           for c in range(self.cols):
               neighbors = self.count_neighbors(r, c)
               if self.grid[r][c] == 1:
                   if neighbors in self.survive_rules:
                       new_grid[r][c] = 1
                   else:
                       new_grid[r][c] = 0
               else:
                   if neighbors in self.birth_rules:
                       new_grid[r][c] = 1
                   else:
                       new_grid[r][c] = 0
       self.grid = new_grid
       self.draw_grid()
   def handle_pixel_click(self, event):
       c = event.x // self.cell_size
       r = event.y // self.cell_size
       if 0 <= r < self.rows and 0 <= c < self.cols:
           return r, c
       return None
   def on_canvas_click(self, event):
       pos = self.handle_pixel_click(event)
       if pos:
           r, c = pos
           self.grid[r][c] = 1 if self.grid[r][c] == 0 else 0
           self.draw_grid()
   def on_canvas_drag(self, event):
       pos = self.handle_pixel_click(event)
       if pos:
           r, c = pos
           self.grid[r][c] = 1
           self.draw_grid()
   def randomize_grid(self):
       self.grid = [[random.choice([0, 1]) for _ in range(self.cols)] for _ in range(self.rows)]
       self.draw_grid()
   def clear_grid(self):
       self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
       self.draw_grid()
if __name__ == "__main__":
   root = tk.Tk()
   app = GameOfLife(root)
   root.mainloop()