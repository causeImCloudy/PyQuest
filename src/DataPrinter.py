import curses
import logging
import os

import Answer


def cursesWrapped(func):

    def wrapper(*args, **kwargs):
        self = args[0]

        try:
            stdscr = curses.initscr()

            # Turn off echoing of keys, and enter cbreak mode,
            # where no buffering is performed on keyboard input
            curses.noecho()
            curses.cbreak()

            # In keypad mode, escape sequences for special keys
            # (like the cursor keys) will be interpreted and
            # a special value like curses.KEY_LEFT will be returned
            stdscr.keypad(1)
            curses.curs_set(0)

            # This wrapper should only be used within the printer class.
            # Self will pick up when places over a method of the class.
            self.stdscr = stdscr

            # Assign to result in order to return outside the try finally block
            result = func(*args, **kwargs)
        finally:
            """
            This content is copied from curses.wrapper function. 
            """
            curses.nocbreak()
            curses.echo()
            curses.endwin()

            # Clear after use in order to not use after free
            self.stdscr = None

        return result

    return wrapper


class Printer:
    def __init__(self,
                 question_color='\033[31m',
                 answer_color='\033[32m',
                 primary_color='\033[37m',
                 secondary_color='\033[34m',
                 font_size=12,
                 color=True
                 ):
        """
        Assign the passed values to the instance
        Defaults:
            question_color      red
            answer_color        green
            primary_color       white
            secondary_color     blue
        """
        if color:
            self.question_color = question_color
            self.answer_color = answer_color
            self.primary_color = primary_color
            self.secondary_color = secondary_color
            self.font_size = font_size

            self.question_prefix = f"{self.primary_color}[{self.secondary_color}Q{self.primary_color}]"
            self.answer_prefix = f"{self.primary_color}[{self.secondary_color}A{self.primary_color}]"
            self.info_prefix = f"{self.primary_color}[{self.secondary_color}Info{self.primary_color}]"
            self.warning_prefix = f"{self.primary_color}[33m!{self.primary_color}]"
        else:
            self.question_prefix = "[Q]"
            self.answer_prefix = "-\t"
            self.info_prefix = "[Info]"
            self.warning_prefix = "[!]"


class Terminal(Printer):

    def print_question(self, question):
        """Prints the question to the standard out utilizing the color structure"""
        print(f"{self.primary_color}[{self.secondary_color}Q{self.primary_color}]{self.question_color}{question}")

    def print_answers(self, answers):
        """Prints the answers to the standard out utilizing the color structure"""
        for i, answer in enumerate(answers):
            print(f"{self.primary_color}[{self.secondary_color}{i}{self.primary_color}]{self.answer_color}{answer}")

    def print_information(self, message):
        """Prints informational message to the standard out utilizing the color structure"""
        print(f"{self.primary_color}[{self.secondary_color}Info{self.primary_color}]{self.primary_color}{message}")

    def print_warning(self, message):
        """Prints a warning message to the standard out utilizing the color structure"""
        print(f"{self.primary_color}[\033[33m!{self.primary_color}]{self.primary_color}{message}")

    @staticmethod
    def clear_screen():
        """Clears the screen"""
        os.system('cls' if os.name == 'nt' else 'clear')


class ScreenPrinter(Printer):
    # TODO Add a duplicate screen on top that can print static and information
    def __init__(self):
        super().__init__(color=False)

        self.max_ans = 0
        self.min_ans = 0

        # Hold the current x and y position of the cursor on the terminal.
        # PosY starts at 1 to be passed the question line and properly show the first answer as highlighted
        # PosX starts at 5 to be a middle ground
        self.posx = 5
        self.posy = 1

        self.navigation_offset = 8
        self.highlight_format = curses.A_BOLD | curses.A_UNDERLINE
        self.navigation_array = ["< Prev", "Done", "Next >"]

        self.stdscr = None

    @cursesWrapped
    def ask_question(self, question, questionType="multiple_choice") -> (int, Answer):
        """
        Asks a question to terminal utilizing python curses. This handles different question types and returns the int
        to the answer list.

        :param question:
        :param questionType:
        :return: int
        """

        # TODO Add prefix option

        logging.debug(f"Asking question {question} with question type {questionType}")
        if questionType == "multiple_choice":
            return self.__multiple_choice__(question)
        else:
            # TODO Selected ALL, Free Text, Math
            raise NotImplementedError(f"Question type {questionType} not implemented")

    def __multiple_choice__(self, question) -> (int, Answer):

        # Reset x and y
        self.posx, self.posy = 0, 1

        # Set Min,Max Answers
        self.min_ans, self.max_ans = 1, len(question.get_answers())

        navigation = question.get_navigation()
        previous_question = question.get_previous_question()
        next_question = question.get_next_question()

        max_posx = max(0, (len(navigation) - 1) * self.navigation_offset)

        # Add 1 max row if navigation is available
        if previous_question is not None:
            self.max_ans += 1

        # Set first frame to screen
        self.stdscr.clear()

        self.__print_question__(question)
        self.__print_answers__(question.get_answers())

        if len(navigation) > 0:
            self.__navigation__(navigation)

        self.stdscr.refresh()

        while True:

            key = self.stdscr.getch()

            if os.name == "posix":  # If this is OSX

                if key == 259:  # Down
                    self.posy -= 1

                elif key == 258:  # Up
                    self.posy += 1

                elif key == 260:  # Left
                    if self.posy == self.max_ans:  # Only Update L/R on navigation row
                        self.posx -= self.navigation_offset

                elif key == 261:  # Right
                    if self.posy == self.max_ans:
                        self.posx += self.navigation_offset

                elif key == 10:  # Enter

                    if self.posy == self.max_ans and (len(navigation) > 0):
                        logging.debug("Prev nav")    # Return prev for navigation
                        index = int(self.posx / self.navigation_offset)
                        return navigation[index], None

                    else:  # Return Answered ID
                        answer = question.get_answer_by_id(self.posy - 1)
                        logging.debug(f"Answered {answer.get_value()}")
                        return answer.get_value(), answer
            else:
                raise NotImplementedError

            # Limit Y
            if self.posy < self.min_ans:
                self.posy = self.min_ans
            elif self.posy > self.max_ans:
                self.posy = self.max_ans

            # Limit X
            if self.posx < 0:
                self.posx = 0
            elif self.posx > max_posx:
                self.posx = max_posx

            # Clear screen at paste question with its answers
            self.stdscr.clear()
            self.__print_question__(question)
            self.__print_answers__(question.get_answers())

            # Determine if the na
            if len(navigation) > 0:
                self.__navigation__(navigation)

            self.stdscr.move(self.posy, self.posx, )
            self.stdscr.refresh()

    def __print_question__(self, question):
        fmt_str = self.question_prefix + question.get_viewable_text()
        self.stdscr.addstr(0, 0, fmt_str)

    def __print_answers__(self, answers):
        for i, answer in enumerate(answers):
            index = i + 1
            if index == self.posy:
                self.__print_highlighted_answer__(i + 1, answer)
            else:
                self.__print_answer__(i + 1, answer)

    def __print_highlighted_answer__(self, row, answer) -> None:
        fmt_str = self.answer_prefix + answer.get_viewable_text()
        self.stdscr.addstr(row, 5, fmt_str, curses.A_BOLD | curses.A_UNDERLINE)

    def __print_answer__(self, row, answer) -> None:
        fmt_str = self.answer_prefix + answer.get_viewable_text()
        self.stdscr.addstr(row, 5, fmt_str)

    def __navigation__(self, navigation):
        highlighted = self.posx / self.navigation_offset
        # Prints elements left to right with an offset inbetween, then handles highlighting based on x position
        for i, element in enumerate(navigation):
            self.stdscr.addstr(self.max_ans,
                               i * self.navigation_offset,
                               str(self.navigation_array[i]),
                               self.highlight_format
                               if (i == highlighted and self.posy == self.max_ans)
                               else curses.A_NORMAL
                               )
