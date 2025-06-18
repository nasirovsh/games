#!/usr/bin/env python3
import random
import time
import os
import sys

class TetrisGame:
    def __init__(self):
        self.width = 10
        self.height = 20
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = 1.0
        self.game_over = False
        
        # Tetromino shapes with all rotations
        self.tetrominoes = [
            # I piece
            [['....',
              '####',
              '....',
              '....'],
             ['..#.',
              '..#.',
              '..#.',
              '..#.']],
            
            # O piece  
            [['##',
              '##']],
            
            # T piece
            [['###',
              '.#.',
              '...'],
             ['.#.',
              '##.',
              '.#.'],
             ['...',
              '.#.',
              '###'],
             ['.#.',
              '.##',
              '.#.']],
            
            # S piece
            [['.##',
              '##.',
              '...'],
             ['#..',
              '##.',
              '.#.']],
            
            # Z piece
            [['##.',
              '.##',
              '...'],
             ['.#.',
              '##.',
              '#..']],
            
            # J piece
            [['#..',
              '###',
              '...'],
             ['##.',
              '#..',
              '#..'],
             ['...',
              '###',
              '..#'],
             ['.#.',
              '.#.',
              '##.']],
            
            # L piece
            [['..#',
              '###',
              '...'],
             ['#..',
              '#..',
              '##.'],
             ['...',
              '###',
              '#..'],
             ['.##',
              '.#.',
              '.#.']]
        ]
        
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
        
    def get_new_piece(self):
        shapes = random.choice(self.tetrominoes)
        return {
            'shapes': shapes,  # All rotations
            'rotation': 0,     # Current rotation index
            'x': self.width // 2 - 2,
            'y': 0,
            'color': random.randint(1, 7)
        }
    
    def get_current_shape(self, piece):
        return piece['shapes'][piece['rotation'] % len(piece['shapes'])]
    
    def valid_position(self, piece, dx=0, dy=0, rotation=None):
        if rotation is None:
            shape = self.get_current_shape(piece)
        else:
            shape = piece['shapes'][rotation % len(piece['shapes'])]
        
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell == '#':
                    new_x = piece['x'] + x + dx
                    new_y = piece['y'] + y + dy
                    
                    if (new_x < 0 or new_x >= self.width or 
                        new_y >= self.height or
                        (new_y >= 0 and self.board[new_y][new_x] != 0)):
                        return False
        return True
    
    def place_piece(self, piece):
        shape = self.get_current_shape(piece)
        
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell == '#':
                    board_x = piece['x'] + x
                    board_y = piece['y'] + y
                    if board_y >= 0:
                        self.board[board_y][board_x] = piece['color']
    
    def clear_lines(self):
        lines_to_clear = []
        for y in range(self.height):
            if all(cell != 0 for cell in self.board[y]):
                lines_to_clear.append(y)
        
        for y in reversed(lines_to_clear):
            del self.board[y]
            self.board.insert(0, [0 for _ in range(self.width)])
        
        lines_cleared = len(lines_to_clear)
        self.lines_cleared += lines_cleared
        self.score += lines_cleared * 100 * self.level
        
        # Level up every 10 lines
        self.level = self.lines_cleared // 10 + 1
        self.fall_time = max(0.2, 1.0 - (self.level - 1) * 0.1)
    
    def move_piece(self, dx, dy):
        if self.valid_position(self.current_piece, dx, dy):
            self.current_piece['x'] += dx
            self.current_piece['y'] += dy
            return True
        return False
    
    def rotate_piece(self):
        new_rotation = (self.current_piece['rotation'] + 1) % len(self.current_piece['shapes'])
        if self.valid_position(self.current_piece, rotation=new_rotation):
            self.current_piece['rotation'] = new_rotation
            return True
        return False
    
    def drop_piece(self):
        if not self.move_piece(0, 1):
            self.place_piece(self.current_piece)
            self.clear_lines()
            self.current_piece = self.next_piece
            self.next_piece = self.get_new_piece()
            
            if not self.valid_position(self.current_piece):
                self.game_over = True
    
    def draw_board(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Create display board
        display = [row[:] for row in self.board]
        
        # Add current piece to display
        if not self.game_over:
            shape = self.get_current_shape(self.current_piece)
            for y, row in enumerate(shape):
                for x, cell in enumerate(row):
                    if cell == '#':
                        board_x = self.current_piece['x'] + x
                        board_y = self.current_piece['y'] + y
                        if 0 <= board_x < self.width and 0 <= board_y < self.height:
                            display[board_y][board_x] = self.current_piece['color']
        
        # Draw the board
        print("┌" + "─" * (self.width * 2) + "┐")
        for row in display:
            print("│", end="")
            for cell in row:
                if cell == 0:
                    print("  ", end="")
                else:
                    print("██", end="")
            print("│")
        print("└" + "─" * (self.width * 2) + "┘")
        
        # Draw stats
        print(f"Score: {self.score}")
        print(f"Level: {self.level}")
        print(f"Lines: {self.lines_cleared}")
        
        print("\nControls:")
        print("← or A = Move left")
        print("→ or D = Move right")
        print("↓ or S = Drop faster")
        print("↑ or W = Rotate")
        print("Q = Quit")
        print("Press ENTER after each key!")
        
        if self.game_over:
            print("\n*** GAME OVER ***")

def main():
    game = TetrisGame()
    last_fall = time.time()
    
    print("Welcome to Simple Tetris!")
    print("Controls:")
    print("← or A = Move left")
    print("→ or D = Move right")
    print("↓ or S = Drop faster")
    print("↑ or W = Rotate")
    print("Q = Quit")
    print("Type command and press ENTER (or just ENTER to continue)")
    input("Press ENTER to start...")
    
    try:
        while not game.game_over:
            current_time = time.time()
            
            # Automatic falling
            if current_time - last_fall > game.fall_time:
                game.drop_piece()
                last_fall = current_time
            
            game.draw_board()
            
            # Get input
            try:
                key = input("Command (←→↓↑/ADSWQ or ENTER): ").strip()
                
                # Handle arrow keys and regular keys
                if key.lower() == 'q':
                    break
                elif key.lower() == 'a' or key == '←':
                    game.move_piece(-1, 0)
                elif key.lower() == 'd' or key == '→':
                    game.move_piece(1, 0)
                elif key.lower() == 's' or key == '↓':
                    game.drop_piece()
                    last_fall = current_time  # Reset fall timer
                elif key.lower() == 'w' or key == '↑':
                    game.rotate_piece()
                # If just ENTER pressed (empty string), continue game
            except:
                break
        
        # Game over
        game.draw_board()
        print("Game Over! Final Score:", game.score)
    
    except KeyboardInterrupt:
        print("\nGame interrupted!")

if __name__ == "__main__":
    main()

