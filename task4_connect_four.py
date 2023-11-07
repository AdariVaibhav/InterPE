import pygame
import sys
import random

class ConnectFourGame:
    def __init__(self):
        pygame.init()
        self.row_count = 6
        self.column_count = 7
        self.board = [[0] * self.column_count for _ in range(self.row_count)]
        self.current_player = 1
        self.square_size = 100
        self.width = self.column_count * self.square_size
        self.height = (self.row_count + 1) * self.square_size
        self.radius = int(self.square_size / 2 - 5)

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Connect Four")

        self.create_board()

    def create_board(self):
        self.game_over = False
        self.myfont = pygame.font.SysFont("monospace", int(self.square_size / 3))

        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if self.current_player == 1:
                    self.player_turn(event)
                else:
                    self.computer_turn()

                self.draw_board()
                pygame.display.update()

    def player_turn(self, event):
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.width, self.square_size))
            posx = event.pos[0]
            pygame.draw.circle(self.screen, (255, 0, 0), (posx, int(self.square_size / 2)), self.radius)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, self.width, self.square_size))
            posx = event.pos[0]
            col = int(posx / self.square_size)

            if self.is_valid_location(col):
                row = self.get_next_open_row(col)
                self.drop_piece(row, col, self.current_player)

                if self.winning_move():
                    self.display_winner()
                    self.ask_for_restart()

                self.current_player = 3 - self.current_player  # Switch player

    def computer_turn(self):
        pygame.time.wait(500)  # Pause for a moment to simulate the computer's "thinking"
        col = self.get_computer_move()
        row = self.get_next_open_row(col)
        self.drop_piece(row, col, 2)

        if self.winning_move():
            self.display_winner()
            self.ask_for_restart()

        self.current_player = 3 - self.current_player  # Switch player

    def get_computer_move(self):
        valid_moves = [col for col in range(self.column_count) if self.is_valid_location(col)]
        return random.choice(valid_moves)

    def is_valid_location(self, col):
        return self.board[self.row_count - 1][col] == 0

    def get_next_open_row(self, col):
        for r in range(self.row_count):
            if self.board[r][col] == 0:
                return r

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def winning_move(self):
        # Check horizontal locations for win
        for c in range(self.column_count - 3):
            for r in range(self.row_count):
                if (
                    self.board[r][c] == self.current_player
                    and self.board[r][c + 1] == self.current_player
                    and self.board[r][c + 2] == self.current_player
                    and self.board[r][c + 3] == self.current_player
                ):
                    return True

        # Check vertical locations for win
        for c in range(self.column_count):
            for r in range(self.row_count - 3):
                if (
                    self.board[r][c] == self.current_player
                    and self.board[r + 1][c] == self.current_player
                    and self.board[r + 2][c] == self.current_player
                    and self.board[r + 3][c] == self.current_player
                ):
                    return True

        # Check positively sloped diagonals
        for c in range(self.column_count - 3):
            for r in range(self.row_count - 3):
                if (
                    self.board[r][c] == self.current_player
                    and self.board[r + 1][c + 1] == self.current_player
                    and self.board[r + 2][c + 2] == self.current_player
                    and self.board[r + 3][c + 3] == self.current_player
                ):
                    return True

        # Check negatively sloped diagonals
        for c in range(self.column_count - 3):
            for r in range(3, self.row_count):
                if (
                    self.board[r][c] == self.current_player
                    and self.board[r - 1][c + 1] == self.current_player
                    and self.board[r - 2][c + 2] == self.current_player
                    and self.board[r - 3][c + 3] == self.current_player
                ):
                    return True

        return False

    def display_winner(self):
        label = self.myfont.render(f"Player {self.current_player} wins!!", 1, (255, 0, 0) if self.current_player == 1 else (255, 255, 0))
        self.screen.blit(label, (int(self.width / 6), int(self.square_size / 2)))

        # Draw the winning combination
        for c in range(self.column_count - 3):
            for r in range(self.row_count):
                if (
                    self.board[r][c] == self.current_player
                    and self.board[r][c + 1] == self.current_player
                    and self.board[r][c + 2] == self.current_player
                    and self.board[r][c + 3] == self.current_player
                ):
                    pygame.draw.circle(self.screen, (255, 0, 0) if self.current_player == 1 else (255, 255, 0), (int((c + 1.5) * self.square_size), int(r * self.square_size + self.square_size / 2)), self.radius)

        pygame.display.update()

    def ask_for_restart(self):
        pygame.display.update()
        pygame.time.wait(2000)  # Wait for 2 seconds after game over
        self.screen.fill((0, 0, 0))  # Clear the screen
        label1 = self.myfont.render("Game Over!", 1, (255, 255, 255))
        label2 = self.myfont.render("Do you want to restart? (Y/N)", 1, (255, 255, 255))
        self.screen.blit(label1, (int(self.width / 6), int(self.height / 3)))
        self.screen.blit(label2, (int(self.width / 6), int(self.height / 2)))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        self.reset_game()
                        return
                    elif event.key == pygame.K_n:
                        sys.exit()

    def reset_game(self):
        self.board = [[0] * self.column_count for _ in range(self.row_count)]
        self.current_player = 1
        self.game_over = False

    def draw_board(self):
        for c in range(self.column_count):
            for r in range(self.row_count):
                pygame.draw.rect(self.screen, (0, 0, 255), (c * self.square_size, r * self.square_size + self.square_size, self.square_size, self.square_size))
                pygame.draw.circle(self.screen, (0, 0, 0), (int(c * self.square_size + self.square_size / 2), int(r * self.square_size + self.square_size + self.square_size / 2)), self.radius)

        for c in range(self.column_count):
            for r in range(self.row_count):
                if self.board[r][c] == 1:
                    pygame.draw.circle(self.screen, (255, 0, 0), (int(c * self.square_size + self.square_size / 2), self.height - int(r * self.square_size + self.square_size / 2)), self.radius)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(self.screen, (255, 255, 0), (int(c * self.square_size + self.square_size / 2), self.height - int(r * self.square_size + self.square_size / 2)), self.radius)

        # Draw the winning combination
        for c in range(self.column_count):
            for r in range(self.row_count - 3):
                if (
                    self.board[r][c] == self.current_player
                    and self.board[r + 1][c] == self.current_player
                    and self.board[r + 2][c] == self.current_player
                    and self.board[r + 3][c] == self.current_player
                ):
                    pygame.draw.circle(self.screen, (255, 0, 0) if self.current_player == 1 else (255, 255, 0), (int(c * self.square_size + self.square_size / 2), int((r + 2.5) * self.square_size)), self.radius)

        pygame.display.update()

if __name__ == "__main__":
    game = ConnectFourGame()
