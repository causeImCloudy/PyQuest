import curses


def myfunc(stdscr):
    stdscr.getch()
    val = "math.sucks"
    a,b = val.split('.')
    return a, b


a, b = curses.wrapper(myfunc)

print(a, b)