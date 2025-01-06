import tkinter as tk
import random
import time

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("Pratyush JOshi")
        self.master.geometry("500x600")
        self.master.resizable(False, False)
        
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.high_score = 0
        self.start_time = None
        
        self.create_start_menu()

    def create_start_menu(self):
        self.clear_screen()
        start_frame = tk.Frame(self.master, bg="lightblue")
        start_frame.pack(expand=True, fill="both")
        
        title = tk.Label(start_frame, text="Mr.Pratyush Joshi!", font=("Time New Roman", 30, "bold"), bg="lightblue")
        title.pack(pady=20)

        start_button = tk.Button(start_frame, text="Start Game", font=("Arial", 16), command=self.start_game)
        start_button.pack(pady=10)

        exit_button = tk.Button(start_frame, text="Exit", font=("Arial", 16), command=self.master.quit)
        exit_button.pack(pady=10)

    def start_game(self):
        self.clear_screen()
        self.setup_game_ui()
        self.reset_game()

    def setup_game_ui(self):
        self.top_frame = tk.Frame(self.master, bg="gray")
        self.top_frame.pack(fill="x")

        self.score_label = tk.Label(self.top_frame, text="Score: 0", font=("Arial", 14), bg="gray", fg="white")
        self.score_label.pack(side="left", padx=10)

        self.high_score_label = tk.Label(self.top_frame, text=f"High Score: {self.high_score}", font=("Arial", 14), bg="gray", fg="white")
        self.high_score_label.pack(side="right", padx=10)

        self.timer_label = tk.Label(self.top_frame, text="Time: 0s", font=("Arial", 14), bg="gray", fg="white")
        self.timer_label.pack(side="left", padx=10)

        self.grid_frame = tk.Frame(self.master, bg="azure3")
        self.grid_frame.pack(expand=True)

        self.grid_cells = []
        for i in range(4):
            row = []
            for j in range(4):
                cell = tk.Frame(
                    self.grid_frame,
                    bg="azure4",
                    width=100,
                    height=100)
                cell.grid(row=i, column=j, padx=5, pady=5)
                t = tk.Label(
                    master=cell,
                    text="",
                    bg="azure4",
                    justify=tk.CENTER,
                    font=("Arial", 22, "bold"),
                    width=4,
                    height=2)
                t.grid()
                row.append(t)
            self.grid_cells.append(row)

        self.update_board()
        
        self.master.bind("<Key>", self.key_press)
        self.start_time = time.time()
        self.update_timer()

    def reset_game(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()
        self.update_board()

    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    def update_timer(self):
        if self.start_time:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed_time}s")
        self.master.after(1000, self.update_timer)

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def update_board(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    self.grid_cells[i][j].configure(text="", bg="azure4")
                else:
                    self.grid_cells[i][j].configure(text=str(self.board[i][j]), bg="lightblue")
        self.score_label.config(text=f"Score: {self.score}")
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_label.config(text=f"High Score: {self.high_score}")
        self.master.update_idletasks()

    def key_press(self, event):
        key = event.keysym
        moved = False
        if key == 'Up':
            moved = self.move_up()
        elif key == 'Down':
            moved = self.move_down()
        elif key == 'Left':
            moved = self.move_left()
        elif key == 'Right':
            moved = self.move_right()

        if moved:
            self.add_new_tile()
            self.update_board()
            if not self.can_move():
                self.show_game_over()

    def move_up(self):
        self.board = self.transpose(self.board)
        moved = self.merge_board()
        self.board = self.transpose(self.board)
        return moved

    def move_down(self):
        self.board = self.transpose(self.board)
        self.board = self.reverse(self.board)
        moved = self.merge_board()
        self.board = self.reverse(self.board)
        self.board = self.transpose(self.board)
        return moved

    def move_left(self):
        return self.merge_board()

    def move_right(self):
        self.board = self.reverse(self.board)
        moved = self.merge_board()
        self.board = self.reverse(self.board)
        return moved

    def merge_board(self):
        moved = False
        new_board = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            previous = None
            for j in range(4):
                if self.board[i][j] != 0:
                    if previous is None:
                        previous = self.board[i][j]
                    else:
                        if previous == self.board[i][j]:
                            new_board[i][fill_position] = 2 * previous
                            self.score += 2 * previous
                            previous = None
                            moved = True
                            fill_position += 1
                        else:
                            new_board[i][fill_position] = previous
                            previous = self.board[i][j]
                            fill_position += 1
                            moved = True
            if previous is not None:
                new_board[i][fill_position] = previous
        self.board = new_board
        return moved

    def reverse(self, board):
        return [row[::-1] for row in board]

    def transpose(self, board):
        return [list(row) for row in zip(*board)]

    def can_move(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    return True
                if i > 0 and self.board[i][j] == self.board[i - 1][j]:
                    return True
                if j > 0 and self.board[i][j] == self.board[i][j - 1]:
                    return True
        return False

    def show_game_over(self):
        self.clear_screen()
        game_over_frame = tk.Frame(self.master, bg="red")
        game_over_frame.pack(expand=True, fill="both")

        game_over_label = tk.Label(game_over_frame, text="Game Over!", font=("Arial", 28, "bold"), bg="red", fg="white")
        game_over_label.pack(pady=20)

        final_score_label = tk.Label(game_over_frame, text=f"Final Score: {self.score}", font=("Arial", 18), bg="red", fg="white")
        final_score_label.pack(pady=10)

        retry_button = tk.Button(game_over_frame, text="Retry", font=("Arial", 16), command=self.start_game)
        retry_button.pack(pady=10)

        exit_button = tk.Button(game_over_frame, text="Exit", font=("Arial", 16), command=self.master.quit)
        exit_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
