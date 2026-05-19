
import tkinter as tk
from tkinter import messagebox
import math
from josephus_logic import JosephusGameLogic

class JosephusGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("THE JOSEPHUS PROBLEM - PREDICTION GAME")
        self.root.geometry("1000x750")
        self.root.configure(bg="#1a1a2e")
        self.root.resizable(False, False)

        self.logic = JosephusGameLogic()
        self.is_playing = False
        self.step_mode = False
        self.person_canvas_items = {}

        # Table management 
        self.table_labels = []
        self.table_rows = 0
        self.table_cols = 8
        self.empty_message = None

        self.colors = {
            'bg': '#1a1a2e', 'card_bg': '#0f0f1a', 'accent': '#e94560',
            'accent_light': '#ff6b6b', 'text': '#eeeeee', 'text_muted': '#888888',
            'success': '#4ade80', 'warning': '#ffd93d', 'error': '#ff4444',
            'eliminated': '#2a2a3a', 'circle_bg': '#0a0a15', 'gold': '#ffd700'
        }

        self.setup_ui()
        self.reset_game()

# ------------------------- UI BUILDING ---------------------
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        self.create_header(main_frame)
        self.create_controls(main_frame)

        content_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Left: circle canvas
        left_frame = tk.Frame(content_frame, bg=self.colors['card_bg'], relief=tk.RIDGE, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        tk.Label(left_frame, text="CIRCLE VISUALIZATION", font=("Arial", 11, "bold"),
                 fg=self.colors['accent'], bg=self.colors['card_bg']).pack(pady=8)
        self.canvas = tk.Canvas(left_frame, width=400, height=400,
                                bg=self.colors['circle_bg'], highlightthickness=0)
        self.canvas.pack(pady=10, padx=10)

        # Right: elimination table
        right_frame = tk.Frame(content_frame, bg=self.colors['card_bg'], relief=tk.RIDGE, bd=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        tk.Label(right_frame, text="ORDER OF ELIMINATION", font=("Arial", 11, "bold"),
                 fg=self.colors['accent'], bg=self.colors['card_bg']).pack(pady=8)

        self.table_container = tk.Frame(right_frame, bg=self.colors['card_bg'])
        self.table_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=5)
        self.table_frame = tk.Frame(self.table_container, bg=self.colors['card_bg'])
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        self.set_empty_message()

        self.survivor_label = tk.Label(right_frame, text="", font=("Arial", 11, "bold"),
                                       fg=self.colors['success'], bg=self.colors['card_bg'])
        self.survivor_label.pack(pady=8)
        self.result_label = tk.Label(right_frame, text="", font=("Arial", 10, "bold"),
                                     fg=self.colors['gold'], bg=self.colors['card_bg'])
        self.result_label.pack(pady=5)

        self.create_status_bar(main_frame)
        self.create_formula_display(main_frame)

    def create_header(self, parent):
        header_frame = tk.Frame(parent, bg=self.colors['bg'])
        header_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(header_frame, text=" THE JOSEPHUS PROBLEM ", font=("Arial", 20, "bold"),
                 fg=self.colors['accent'], bg=self.colors['bg']).pack()
        tk.Label(header_frame, text="Eliminate every k-th person | PREDICT THE SURVIVOR!",
                 font=("Arial", 9), fg=self.colors['text_muted'], bg=self.colors['bg']).pack()

    def create_controls(self, parent):
        control_frame = tk.Frame(parent, bg=self.colors['card_bg'], relief=tk.RIDGE, bd=2)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        inner = tk.Frame(control_frame, bg=self.colors['card_bg'])
        inner.pack(padx=15, pady=10, fill=tk.X)

        # n input
        n_frame = tk.Frame(inner, bg=self.colors['card_bg'])
        n_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(n_frame, text="NUMBER OF PEOPLE:", font=("Arial", 9, "bold"),
                 fg=self.colors['accent'], bg=self.colors['card_bg']).pack(anchor=tk.W)
        self.n_var = tk.StringVar(value="0")
        tk.Entry(n_frame, textvariable=self.n_var, font=("Arial", 12, "bold"), width=6,
                 bg=self.colors['bg'], fg=self.colors['text'], insertbackground=self.colors['text'],
                 relief=tk.FLAT, justify=tk.CENTER).pack(pady=3)

        # k input
        k_frame = tk.Frame(inner, bg=self.colors['card_bg'])
        k_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(k_frame, text="ELIMINATION STEP (k):", font=("Arial", 9, "bold"),
                 fg=self.colors['accent'], bg=self.colors['card_bg']).pack(anchor=tk.W)
        self.k_var = tk.StringVar(value="0")
        tk.Entry(k_frame, textvariable=self.k_var, font=("Arial", 12, "bold"), width=6,
                 bg=self.colors['bg'], fg=self.colors['text'], insertbackground=self.colors['text'],
                 relief=tk.FLAT, justify=tk.CENTER).pack(pady=3)

        # Buttons: START  and STEP
        button_frame = tk.Frame(inner, bg=self.colors['card_bg'])
        button_frame.pack(side=tk.LEFT, padx=15)
        self.start_btn = tk.Button(button_frame, text="START SIMULATION",
                                   font=("Arial", 9, "bold"), bg=self.colors['accent'],
                                   fg="white", padx=15, pady=6, relief=tk.RAISED,
                                   cursor="hand2", command=self.start_simulation)
        self.start_btn.pack(side=tk.LEFT, padx=3)

        self.step_btn = tk.Button(button_frame, text="STEP BY STEP",
                                  font=("Arial", 9, "bold"), bg="#e9a845",
                                  fg="white", padx=15, pady=6, relief=tk.RAISED,
                                  cursor="hand2", command=self.step_by_step)
        self.step_btn.pack(side=tk.LEFT, padx=3)

        # Prediction entry
        pred_frame = tk.Frame(inner, bg=self.colors['card_bg'])
        pred_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(pred_frame, text="PREDICT PERSON:", font=("Arial", 9, "bold"),
                 fg=self.colors['warning'], bg=self.colors['card_bg']).pack(side=tk.LEFT, padx=5)
        self.pred_var = tk.StringVar()
        tk.Entry(pred_frame, textvariable=self.pred_var, font=("Arial", 10, "bold"), width=5,
                 bg=self.colors['bg'], fg=self.colors['text'], insertbackground=self.colors['text'],
                 relief=tk.FLAT, justify=tk.CENTER).pack(side=tk.LEFT, padx=5)
        tk.Button(pred_frame, text="SET", font=("Arial", 8, "bold"), bg=self.colors['success'],
                  fg="white", padx=12, pady=4, relief=tk.RAISED, cursor="hand2",
                  command=self.set_prediction).pack(side=tk.LEFT, padx=5)

        self.pred_status = tk.Label(pred_frame, text=" No prediction",
                                    font=("Arial", 8, "italic"),
                                    fg=self.colors['text_muted'], bg=self.colors['card_bg'])
        self.pred_status.pack(side=tk.LEFT, padx=10)

    def create_status_bar(self, parent):
        status_frame = tk.Frame(parent, bg=self.colors['card_bg'], relief=tk.RIDGE, bd=2)
        status_frame.pack(fill=tk.X, pady=(10, 5))
        inner = tk.Frame(status_frame, bg=self.colors['card_bg'])
        inner.pack(padx=15, pady=6, fill=tk.X)

        self.status_label = tk.Label(inner, text="STATUS: Enter n and k values",
                                     font=("Arial", 9), fg=self.colors['text'], bg=self.colors['card_bg'])
        self.status_label.pack(side=tk.LEFT)

        self.remaining_label = tk.Label(inner, text="REMAINING: 0", font=("Arial", 9),
                                        fg=self.colors['text'], bg=self.colors['card_bg'])
        self.remaining_label.pack(side=tk.LEFT, padx=20)

        self.eliminating_label = tk.Label(inner, text="ELIMINATING: -", font=("Arial", 9),
                                          fg=self.colors['warning'], bg=self.colors['card_bg'])
        self.eliminating_label.pack(side=tk.LEFT)

        self.pred_display_label = tk.Label(inner, text="", font=("Arial", 9, "bold"),
                                           fg=self.colors['gold'], bg=self.colors['card_bg'])
        self.pred_display_label.pack(side=tk.LEFT, padx=30)

    def create_formula_display(self, parent):
        formula_frame = tk.Frame(parent, bg=self.colors['card_bg'], relief=tk.RIDGE, bd=2)
        formula_frame.pack(fill=tk.X, pady=(5, 0))
        inner = tk.Frame(formula_frame, bg=self.colors['card_bg'])
        inner.pack(padx=15, pady=6, fill=tk.X)
        tk.Label(inner, text=" DECREASE-AND-CONQUER: J(2k) = 2×J(k)-1 | J(2k+1) = 2×J(k)+1 | J(1)=1",
                 font=("Arial", 8), fg=self.colors['text_muted'], bg=self.colors['card_bg']).pack()

# ---------------------- PREDICTION -------------------------
    def update_prediction_display(self):
        pred = self.logic.get_prediction_status()
        if pred is not None:
            self.pred_display_label.config(text=f" PREDICTION: #{pred} ")
            self.pred_status.config(text=f" Predicting #{pred}", fg=self.colors['success'])
        else:
            self.pred_display_label.config(text="")
            self.pred_status.config(text=" No prediction", fg=self.colors['text_muted'])

    def set_prediction(self):
        try:
            pred = int(self.pred_var.get())
            if pred < 1 or pred > 100:
                messagebox.showwarning("Invalid Prediction", "Prediction must be between 1 and 100")
                self.pred_var.set("")
                return
            n = self.logic.get_n()
            if n > 0 and pred > n:
                messagebox.showwarning("Invalid Prediction", f"Prediction cannot exceed number of people ({n})")
                self.pred_var.set("")
                return
            if self.logic.set_prediction(pred):
                self.pred_var.set("")
                self.result_label.config(text="")
                self.survivor_label.config(text="")
                self.update_prediction_display()
                messagebox.showinfo("Prediction Set",
                                    f"You predicted Person #{pred} will survive!\n\nWatch the elimination to see if you are correct!")
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a valid number (1-100)")
            self.pred_var.set("")

    def show_prediction_result(self, survivor):
        result = self.logic.check_prediction(survivor)
        if result is True:
            self.result_label.config(text=" YOUR PREDICTION WAS CORRECT! YOU WIN! ", fg=self.colors['gold'])
            self.status_label.config(text=f" YOU WIN! Survivor: Person {survivor} - Your prediction was CORRECT!")
            if survivor in self.person_canvas_items:
                self.canvas.itemconfig(self.person_canvas_items[survivor]['circle'],
                                       fill=self.colors['gold'], outline="white", width=3)
                self.canvas.itemconfig(self.person_canvas_items[survivor]['text'],
                                       fill="black", font=("Arial", 10, "bold"))
        elif result is False:
            self.result_label.config(text=f" YOUR PREDICTION WAS WRONG! Survivor: Person #{survivor} ", fg=self.colors['error'])
            self.status_label.config(text=f" GAME OVER! Survivor: Person {survivor} - You predicted {self.logic.get_prediction_status()}")

#---------------------- VISUALISATION -----------------------
    def create_circle_visualization(self):
        self.canvas.delete("all")
        self.person_canvas_items.clear()
        n = self.logic.get_n()
        if n < 1:
            self.canvas.create_text(200, 200,
                                    text="Enter n > 0 and k ≥ 2\n then click START",
                                    fill=self.colors['text_muted'], font=("Arial", 12), justify="center")
            return

        people = self.logic.get_people_state()
        w, h = 400, 400
        cx, cy = w//2, h//2
        r = 165
        self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, outline=self.colors['accent'], width=2, fill=self.colors['circle_bg'])

        if n <= 20:
            csize, fsize = 16, 9
        elif n <= 30:
            csize, fsize = 13, 8
        elif n <= 50:
            csize, fsize = 10, 7
        else:
            csize, fsize = 8, 6

        for i, p in enumerate(people):
            angle = (i * 2 * math.pi / n) - math.pi/2
            x = cx + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            eliminated = p['eliminated']
            fill = self.colors['eliminated'] if eliminated else self.colors['bg']
            outline = "#555" if eliminated else self.colors['accent']
            textfill = self.colors['text_muted'] if eliminated else self.colors['text']
            circle = self.canvas.create_oval(x-csize, y-csize, x+csize, y+csize,
                                             fill=fill, outline=outline, width=1.5)
            text = self.canvas.create_text(x, y, text=str(p['id']), fill=textfill,
                                           font=("Arial", fsize, "bold"))
            self.person_canvas_items[p['id']] = {'circle': circle, 'text': text}
        self.highlight_active()

    def highlight_active(self):
        if not self.person_canvas_items:
            return
        cur_idx = self.logic.get_current_index()
        people = self.logic.get_people_state()
        if cur_idx >= len(people):
            return
        cur_id = people[cur_idx]['id'] if cur_idx < len(people) else None
        for pid, items in self.person_canvas_items.items():
            p = next((x for x in people if x['id'] == pid), None)
            if not p:
                continue
            if not p['eliminated'] and pid == cur_id:
                self.canvas.itemconfig(items['circle'], fill=self.colors['accent'], outline="white", width=2)
                self.canvas.itemconfig(items['text'], fill="white")
            elif not p['eliminated']:
                self.canvas.itemconfig(items['circle'], fill=self.colors['bg'], outline=self.colors['accent'], width=1.5)
                self.canvas.itemconfig(items['text'], fill=self.colors['text'])

# ------------------------ TABLE ----------------------------
    def set_empty_message(self):
        for w in self.table_frame.winfo_children():
            w.destroy()
        self.table_labels = []
        self.table_rows = 0
        self.empty_message = tk.Label(self.table_frame,
                                      text="Set n > 0 and k ≥ 2\n then click START SIMULATION",
                                      font=("Arial", 10), fg=self.colors['text_muted'], bg=self.colors['card_bg'])
        self.empty_message.pack(expand=True, pady=30)

    def remove_empty_message(self):
        if self.empty_message is not None:
            self.empty_message.destroy()
            self.empty_message = None

    def ensure_table_grid(self, required_rows):
        self.remove_empty_message()
        while self.table_rows < required_rows:
            row_frame = tk.Frame(self.table_frame, bg=self.colors['card_bg'])
            row_frame.pack(fill=tk.X, pady=2)
            row_labels = []
            for _ in range(self.table_cols):
                lbl = tk.Label(row_frame, text="", font=("Arial", 9, "bold"), width=5,
                               bg=self.colors['card_bg'], relief=tk.RIDGE, bd=1)
                lbl.pack(side=tk.LEFT, padx=1)
                row_labels.append(lbl)
            self.table_labels.append(row_labels)
            self.table_rows += 1

    def update_elimination_table(self):
        elim = self.logic.get_elimination_order()
        n = self.logic.get_n()
        if not elim:
            self.set_empty_message()
            alive = sum(1 for p in self.logic.get_people_state() if not p['eliminated']) if self.logic.get_people_state() else 0
            self.remaining_label.config(text=f"REMAINING: {alive}")
            return

        needed_rows = (len(elim) + self.table_cols - 1) // self.table_cols
        self.ensure_table_grid(needed_rows)

        for idx, val in enumerate(elim):
            row, col = divmod(idx, self.table_cols)
            if idx == len(elim)-1 and len(elim) < n:
                bg, fg = self.colors['accent'], "white"
            else:
                bg, fg = self.colors['bg'], self.colors['warning']
            self.table_labels[row][col].config(text=str(val), bg=bg, fg=fg)

        last_row = needed_rows - 1
        filled = len(elim) % self.table_cols
        if filled == 0 and len(elim) > 0:
            filled = self.table_cols
        for col in range(filled, self.table_cols):
            self.table_labels[last_row][col].config(text="", bg=self.colors['card_bg'])

        alive = sum(1 for p in self.logic.get_people_state() if not p['eliminated'])
        self.remaining_label.config(text=f"REMAINING: {alive}")
        self.root.update_idletasks()

    # ---------------------------- SIMULATION  ----------------------------
    def start_simulation(self):
        if self.is_playing:
            return

        try:
            n = int(self.n_var.get())
            k = int(self.k_var.get())
            if n < 1:
                messagebox.showwarning("Invalid Input", "Number of people (n) must be at least 1")
                return
            if n > 100:
                messagebox.showwarning("Invalid Input", "n cannot exceed 100")
                return
            if k < 2:
                messagebox.showwarning("Invalid Input", "Elimination step (k) must be at least 2")
                return
            if k > 10:
                messagebox.showwarning("Invalid Input", "k cannot exceed 10")
                return
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter valid numbers for n and k")
            return

        self.reset_game()
        if self.logic.setup_game(n, k):
            self.is_playing = True
            self.step_mode = False
            self.start_btn.config(state=tk.DISABLED, text="RUNNING...")
            self.status_label.config(text="STATUS: Simulating...")
            self.create_circle_visualization()
            self.update_elimination_table()
            self.run_simulation()

    def run_simulation(self):
        if not self.is_playing or self.step_mode:
            return
        if self.logic.is_game_finished():
            self.finish_game()
            return
        eliminated = self.logic.eliminate_one()
        if eliminated:
            self.update_elimination_table()
            if eliminated in self.person_canvas_items:
                self.canvas.itemconfig(self.person_canvas_items[eliminated]['circle'],
                                       fill=self.colors['eliminated'], outline="#555")
                self.canvas.itemconfig(self.person_canvas_items[eliminated]['text'],
                                       fill=self.colors['text_muted'])
            self.eliminating_label.config(text=f"ELIMINATING: Person {eliminated}")
            self.highlight_active()
            self.root.after(300, self.run_simulation)
        else:
            self.finish_game()

    def step_by_step(self):
        try:
            n = int(self.n_var.get())
            k = int(self.k_var.get())
            if n < 1 or k < 2:
                messagebox.showwarning("Invalid Input", "n ≥ 1 and k ≥ 2")
                return
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter valid numbers")
            return

        if self.is_playing:
            self.stop_simulation()

        self.step_mode = True
        if self.logic.get_n() != n or self.logic.get_k() != k or self.logic.is_game_finished():
            self.reset_game()
            self.logic.setup_game(n, k)
            self.create_circle_visualization()
            self.update_elimination_table()

        if self.logic.is_game_finished():
            self.finish_game()
            return

        eliminated = self.logic.eliminate_one()
        if eliminated:
            self.update_elimination_table()
            if eliminated in self.person_canvas_items:
                self.canvas.itemconfig(self.person_canvas_items[eliminated]['circle'],
                                       fill=self.colors['eliminated'], outline="#555")
                self.canvas.itemconfig(self.person_canvas_items[eliminated]['text'],
                                       fill=self.colors['text_muted'])
            self.eliminating_label.config(text=f"ELIMINATING: Person {eliminated}")
            self.highlight_active()
            self.status_label.config(text="STATUS: Step Mode - Click STEP to continue")
        else:
            self.finish_game()

    def stop_simulation(self):
        self.is_playing = False
        self.start_btn.config(state=tk.NORMAL, text="START SIMULATION")

    def finish_game(self):
        self.stop_simulation()
        survivor = self.logic.find_survivor()
        if survivor:
            self.survivor_label.config(text=f"SURVIVOR: Person #{survivor} ", fg=self.colors['gold'])
            self.show_prediction_result(survivor)
            self.eliminating_label.config(text=f"SURVIVOR: #{survivor}")
        self.update_elimination_table()

    def reset_game(self):
        self.stop_simulation()
        try:
            n = int(self.n_var.get())
            n = max(0, min(100, n))
        except:
            n = 0
        try:
            k = int(self.k_var.get())
            k = max(0, min(10, k))
        except:
            k = 0
        self.logic.setup_game(n, k)
        self.step_mode = False
        self.create_circle_visualization()
        self.update_elimination_table()
        self.result_label.config(text="")
        self.survivor_label.config(text="")
        self.status_label.config(text="STATUS: Ready" if n>0 and k>=2 else "STATUS: Enter n > 0 and k ≥ 2")
        self.eliminating_label.config(text="ELIMINATING: -")
        self.start_btn.config(state=tk.NORMAL, text="START SIMULATION")
        self.update_prediction_display()


def main():
    root = tk.Tk()
    app = JosephusGameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()