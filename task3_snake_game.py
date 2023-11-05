import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.canvas = tk.Canvas(master, width=400, height=400, bg="black")
        self.canvas.pack()
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = "Right"
        self.food = self.create_food()
        self.canvas.bind_all("<KeyPress>", self.on_key_press)
        self.update()

    def create_food(self):
        x = random.randint(1, 39) * 10
        y = random.randint(1, 39) * 10
        return self.canvas.create_oval(x, y, x + 10, y + 10, fill="red")

    def move_snake(self):
        head = self.snake[0]
        if self.direction == "Right":
            new_head = (head[0] + 10, head[1])
        elif self.direction == "Left":
            new_head = (head[0] - 10, head[1])
        elif self.direction == "Up":
            new_head = (head[0], head[1] - 10)
        else:
            new_head = (head[0], head[1] + 10)

        self.snake.insert(0, new_head)
        if new_head == (self.canvas.coords(self.food)[0], self.canvas.coords(self.food)[1]):
            self.canvas.delete(self.food)
            self.food = self.create_food()
        else:
            self.canvas.delete(self.snake[-1])
            self.snake.pop()

    def check_collision(self):
        head = self.snake[0]
        if (
            head in self.snake[1:]
            or head[0] < 0
            or head[0] >= 400
            or head[1] < 0
            or head[1] >= 400
        ):
            return True
        return False

    def update(self):
        if not self.check_collision():
            self.move_snake()
            self.canvas.delete("snake")
            for segment in self.snake:
                self.canvas.create_rectangle(
                    segment[0], segment[1], segment[0] + 10, segment[1] + 10, fill="green", tags="snake"
                )
            self.master.after(100, self.update)
        else:
            self.canvas.create_text(
                200, 200, text="Game Over", font=("Helvetica", 16), fill="white"
            )

    def on_key_press(self, event):
        new_dir = event.keysym
        if (new_dir == "Right" and not self.direction == "Left") or (
            new_dir == "Left" and not self.direction == "Right"
        ) or (new_dir == "Up" and not self.direction == "Down") or (
            new_dir == "Down" and not self.direction == "Up"
        ):
            self.direction = new_dir

root = tk.Tk()
game = SnakeGame(root)
root.mainloop()
