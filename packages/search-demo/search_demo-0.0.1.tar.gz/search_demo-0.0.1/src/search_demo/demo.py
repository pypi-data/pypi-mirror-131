import curses
import time


class SearchDemo:
    """
        Make a terminal text input that runs a function every time you enter
        a new character

        Function should return an iterable
    """
    def __init__(self, function):
        self.function = function
        curses.wrapper(self.main)

    def main(self, stdscr):
        search_string = ""
        while True:
            char = stdscr.getkey()

            if char == "\n":
                search_string = ""
            elif char == "KEY_BACKSPACE":
                search_string = search_string[:-1]
            elif char == "q":
                break
            else:
                search_string += char

            ts = time.perf_counter()
            res = self.function(search_string)
            te = time.perf_counter()
            t = str(te - ts)

            stdscr.clear()
            stdscr.addstr(search_string, curses.A_BOLD)
            for r in res:
                stdscr.addstr("\n")
                stdscr.addstr(r)
            stdscr.addstr("\n")
            stdscr.addstr(f"Query took: {t}")
            stdscr.refresh()
