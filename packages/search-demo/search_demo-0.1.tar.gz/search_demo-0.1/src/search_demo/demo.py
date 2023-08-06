"""
    Super simple curses fzf-like demo to demo a function that
    returns an iterable

    Run a function on a string input with every character pressed,
    enter breaks and returns the results
"""
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

    def run_demo(self):
        """ Run the demo """
        return curses.wrapper(self.main)

    def main(self, stdscr):
        """
            Main curses loop
        """
        search_string = ""
        results = []
        while True:
            char = stdscr.getkey()

            if char == "\n":
                return results

            if char == "KEY_BACKSPACE":
                search_string = search_string[:-1]
            else:
                search_string += char

            t_s = time.perf_counter()
            results = self.function(search_string)
            t_e = time.perf_counter()
            total_time = str(t_e - t_s)

            stdscr.clear()
            stdscr.addstr(search_string, curses.A_BOLD)
            try:
                for result in results:
                    stdscr.addstr("\n")
                    stdscr.addstr(result)
            except TypeError:
                stdscr.addstr("\n")
                stdscr.addstr("""ERROR: ensure tht your function returns
                              an iterable""")
            stdscr.addstr("\n")
            stdscr.addstr(f"Function took: {total_time}", curses.A_ITALIC)
            stdscr.refresh()
