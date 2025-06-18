#!/usr/bin/env python3

import curses
import random
import time

def main(stdscr):
    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake color
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Food color
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Score color
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Text color

    # Hide cursor and disable input echo
    curses.curs_set(0)
    curses.noecho()
    
    # Enable non-blocking input
    stdscr.nodelay(1)
    
    # Get screen dimensions
    height, width = stdscr.getmaxyx()
    
    # Set up game area constraints
    game_area_height = height - 2  # Leave room for score display
    game_area_width = width - 2    # Leave a 1-character border
    
    # Initialize game variables
    snake = [(game_area_height // 2, game_area_width // 4)]  # Start at center-left
    food = None
    direction = curses.KEY_RIGHT  # Start moving right
    score = 0
    
    # Game speed (lower = faster)
    game_speed = 0.15
    
    # Generate initial food
    def generate_food():
        while True:
            # Ensure food doesn't spawn on snake
            new_food = (random.randint(1, game_area_height), random.randint(1, game_area_width))
            if new_food not in snake:
                return new_food
    
    food = generate_food()
    
    # Main game loop
    game_over = False
    while not game_over:
        # Handle user input
        key = stdscr.getch()
        
        # Quit on 'q'
        if key == ord('q'):
            break
            
        # Change direction based on arrow keys
        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            # Prevent 180-degree turns (can't go in the opposite direction)
            if (key == curses.KEY_UP and direction != curses.KEY_DOWN) or \
               (key == curses.KEY_DOWN and direction != curses.KEY_UP) or \
               (key == curses.KEY_LEFT and direction != curses.KEY_RIGHT) or \
               (key == curses.KEY_RIGHT and direction != curses.KEY_LEFT):
                direction = key
        
        # Calculate new head position based on direction
        head_y, head_x = snake[0]
        if direction == curses.KEY_UP:
            head_y -= 1
        elif direction == curses.KEY_DOWN:
            head_y += 1
        elif direction == curses.KEY_LEFT:
            head_x -= 1
        elif direction == curses.KEY_RIGHT:
            head_x += 1
        
        new_head = (head_y, head_x)
        
        # Check for collisions with walls
        if (head_y <= 0 or head_y >= game_area_height or 
            head_x <= 0 or head_x >= game_area_width):
            game_over = True
            continue
            
        # Check for collisions with self (except tail, which will move)
        if new_head in snake[:-1]:
            game_over = True
            continue
            
        # Add new head
        snake.insert(0, new_head)
        
        # Check if snake ate food
        if new_head == food:
            # Increase score
            score += 10
            # Generate new food
            food = generate_food()
            # Speed up game slightly
            if game_speed > 0.05:  # Don't make it too fast
                game_speed *= 0.95
        else:
            # Remove tail if no food was eaten
            snake.pop()
        
        # Clear screen for redrawing
        stdscr.clear()
        
        # Draw border
        stdscr.border(0)
        
        # Draw score
        score_text = f" Score: {score} "
        stdscr.addstr(0, width // 2 - len(score_text) // 2, score_text, curses.color_pair(3))
        
        # Draw snake
        for segment in snake:
            try:
                y, x = segment
                stdscr.addch(y, x, curses.ACS_BLOCK, curses.color_pair(1))
            except curses.error:
                # Handle potential out-of-bounds errors
                pass
        
        # Draw food
        try:
            food_y, food_x = food
            stdscr.addch(food_y, food_x, '*', curses.color_pair(2))
        except curses.error:
            # Handle potential out-of-bounds errors
            pass
        
        # Refresh screen
        stdscr.refresh()
        
        # Control game speed
        time.sleep(game_speed)
    
    # Game over screen
    if game_over:
        stdscr.nodelay(0)  # Switch back to blocking mode
        stdscr.clear()
        game_over_text = "GAME OVER!"
        final_score_text = f"Final Score: {score}"
        exit_text = "Press any key to exit"
        
        # Display game over message
        stdscr.addstr(height // 2 - 1, width // 2 - len(game_over_text) // 2, 
                     game_over_text, curses.color_pair(2) | curses.A_BOLD)
        
        # Display final score
        stdscr.addstr(height // 2, width // 2 - len(final_score_text) // 2, 
                     final_score_text, curses.color_pair(3))
        
        # Display exit instructions
        stdscr.addstr(height // 2 + 2, width // 2 - len(exit_text) // 2, 
                     exit_text, curses.color_pair(4))
        
        stdscr.refresh()
        stdscr.getch()  # Wait for keypress before exiting

if __name__ == "__main__":
    try:
        # Initialize curses
        curses.wrapper(main)
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        pass
    finally:
        # Ensure terminal settings are restored
        curses.endwin()
        print("Snake Game closed. Thanks for playing!")

