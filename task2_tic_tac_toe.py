import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.board = [" " for _ in range(9)] 
        self.current_player = "X"
        self.buttons = [tk.Button(master, text=" ", font=('normal', 20), width=5, height=2, command=lambda i=i: self.on_button_click(i)) for i in range(9)]
        for i, button in enumerate(self.buttons):
            row, col = divmod(i, 3)
            button.grid(row=row, column=col)

    def on_button_click(self, index):
        if self.board[index] == " ":
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player, state=tk.DISABLED)
            if self.check_winner():
                messagebox.showinfo("Tic Tac Toe", f"Player {self.current_player} wins!")
                self.reset_game()
            elif " " not in self.board:
                messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                self.reset_game()
            else:
                self.switch_player()
                self.computer_move()

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def computer_move(self):
        empty_indices = [i for i in range(9) if self.board[i] == " "]
        if empty_indices:
            index = self.get_best_move()
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player, state=tk.DISABLED)
            if self.check_winner():
                messagebox.showinfo("Tic Tac Toe", f"Player {self.current_player} wins!")
                self.reset_game()
            elif " " not in self.board:
                messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                self.reset_game()
            else:
                self.switch_player()

    def get_best_move(self):
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "O"
                if self.check_winner() and self.current_player == "O":
                    self.board[i] = " "
                    return i
                self.board[i] = " "
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "X"
                if self.check_winner() and self.current_player == "X":
                    self.board[i] = " "
                    return i
                self.board[i] = " "
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = "X"
                for j in range(9):
                    if self.board[j] == " ":
                        self.board[j] = "O"
                        if self.check_winner() and self.current_player == "O":
                            self.board[j] = " "
                            return i
                        self.board[j] = " "
                self.board[i] = " "
        if self.board[4] == " ":
            return 4
        return random.choice([i for i in range(9) if self.board[i] == " "])


    def check_winner(self):
        for i in range(3):
            if self.board[i * 3] == self.board[i * 3 + 1] == self.board[i * 3 + 2] != " ":
                return True
            if self.board[i] == self.board[i + 3] == self.board[i + 6] != " ":
                return True
        if self.board[0] == self.board[4] == self.board[8] != " ":
            return True
        if self.board[2] == self.board[4] == self.board[6] != " ":
            return True
        return False

    def reset_game(self):
        self.board = [" " for _ in range(9)]
        for button in self.buttons:
            button.config(text=" ", state=tk.NORMAL)
        self.current_player = "X"
        if self.current_player == "O":
            self.computer_move()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
