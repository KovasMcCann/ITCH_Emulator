import curses
import random
import time

def is_prime(num):
    """Check if a number is prime."""
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def draw_window(win, title, numbers):
    """Draw a window with a border and a scrolling feed of random numbers, highlighting primes."""
    win.clear()
    win.box()  # Add border
    win.addstr(0, 1, title)  # Title inside the border
    for i, num in enumerate(numbers[-10:]):  # Display the last 10 numbers
        if is_prime(num):
            win.addstr(i + 1, 1, f"{num}", curses.A_BOLD | curses.color_pair(1))
        else:
            win.addstr(i + 1, 1, f"{num}")
    win.refresh()

def main(stdscr):
    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    # Main loop to create and refresh windows
    numbers1 = []
    numbers2 = []
    
    try:
        while True:
            height, width = stdscr.getmaxyx()

            # Set window dimensions to fill the terminal
            win_height = height - 2  # Leave room for borders
            win_width = width // 2  # Split width for two windows

            # Create two windows, split evenly in width
            win1 = curses.newwin(win_height, win_width, 1, 1)  # Window 1
            win2 = curses.newwin(win_height, win_width, 1, win_width + 1)  # Window 2

            # Add new random number to each feed
            numbers1.append(random.randint(1, 100))
            numbers2.append(random.randint(1, 100))

            # Keep only the last 50 numbers for scrolling
            if len(numbers1) > 50:
                numbers1.pop(0)
            if len(numbers2) > 50:
                numbers2.pop(0)

            draw_window(win1, "SoupBinTCP Packets", numbers1)
            draw_window(win2, "Parsed Messages", numbers2)

            time.sleep(0.5)  # Refresh every half second
    except KeyboardInterrupt:
        pass

curses.wrapper(main)
