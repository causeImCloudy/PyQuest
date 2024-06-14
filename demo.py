import PyQuest
from icecream import ic
import curses

i = 1


def main(stdscr):
    stdscr.addstr(15, 15, f"Hello, I am {i}")
    stdscr.getch()


if __name__ == '__main__':
    # quest1 = PyQuest.PyQuest(config="demo.json")
    # quest1.start_quest()
    #
    # answer = quest1.get_question_by_id(0).get_selected_answer()
    #
    # del quest1
    #
    # ic(answer)
    # print(answer)

    for i in range(1,10):
        curses.wrapper(main)
        print("Fuck")


    curses.wrapper(main)
    print("done")