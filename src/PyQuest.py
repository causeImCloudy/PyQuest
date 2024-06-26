import logging
import os

import Answer
import DataPrinter
import DataReader
import Question


class PyQuest:
    def __init__(self, config, first_question=None, auto_start=False) -> None:

        self.questions = None
        self.timed = None
        self.scored = None
        self.current_question = 0 if first_question is None else first_question
        self.first_question = self.current_question  # Assigns the first value of current_question to record and track

        # Differentiate between passed config and a file containing the config. Then handle errors
        if isinstance(config, str) and os.path.exists(config):
            data = DataReader.data_from_file(config)
        elif isinstance(config, dict):
            data = DataReader.data_from_dict(config)
        elif not os.path.exists(config):
            raise FileNotFoundError
        else:
            raise ValueError("Invalid config variable")

        # Take in initial config variable and assign them to the instance
        # Set variables
        self.set_current_question(data["first_question"])
        self.set_scored(data["scored"])
        self.set_timed(data["timed"])
        # TODO Add support for custom colors
        self.printer = DataPrinter.ScreenPrinter() if data["printer"] == "screen" else DataPrinter.Terminal()
        global PRINTER_TYPE
        PRINTER_TYPE = data["printer"]

        # Delete these in order to loop through the questions
        del data["first_question"]
        del data["scored"]
        del data["timed"]
        del data["printer"]

        self.set_questions(DataReader.data_from_dict(data))  # Create the questions then assign back to

        if auto_start:
            self.start_quest()

    def set_questions(self, questions) -> None:
        if not isinstance(questions, dict):
            raise ValueError("Invalid config variable")

        self.questions = questions

    def set_timed(self, timed) -> None:
        if not isinstance(timed, bool):
            raise ValueError("Timed variable must be bool.")

        self.timed = timed

    def set_scored(self, scored) -> None:
        if not isinstance(scored, bool):
            raise ValueError("Scored variable must be bool.")

        self.scored = scored

    def set_current_question(self, current_question) -> None:
        if not isinstance(current_question, int):
            raise ValueError("Current Question must be int.")

        self.current_question = current_question

    def questing(self, questionID):
        """
        Go out battle the demons and loot the winches.
        Handles the quest flow.
        For the next question -1 is a reserved value which ends the quest.

        :param questionID:
        :return:
        """

        logging.info(f"Questing {type(questionID)}{questionID}")

        current_question = self.get_question_by_id(questionID)

        #  Return from the selected path and mark that answer as selected.
        next_question, answer = self.printer.ask_question(current_question)

        if answer is None:
            return next_question

        answer.set_selected_status(True)
        logging.debug(f"Answer {answer.get_viewable_text()} has been selected")

        # Set default path.
        path = current_question.get_next_question()
        if answer.get_value():
            path = answer.get_value()  # Update path if answer obj has a custom path

        logging.debug(f"Questing has pathed to {path}")

        if path == -1:
            return None

        # Return next question by ID of Path
        return path

    def start_quest(self, questionId=None) -> None:
        """
        Start the quest from the default first_question parameter
        """
        questionId = questionId if questionId is not None else self.current_question
        while True:
            questionId = self.questing(questionId)

            if questionId is None:
                break

    def get_question_by_id(self, questionID) -> Question:
        try:
            question = self.questions[str(questionID)]
            return question
        except KeyError:
            raise KeyError(f"Invalid question ID: {questionID}")

    def get_furthest_answer(self, question=None) -> Answer:
        """
        returns the final answer by following the answer tree till there is no further answer to search.
        :return Answer
        :return None
        """
        cur_id = self.first_question if question is None else question

        # Get the answer of current question
        cur_ans = self.get_question_by_id(cur_id).get_selected_answer()

        # Check if there is a selected answer
        if cur_ans is None:
            return None

        cur_id = cur_ans.get_value()

        # Ensure the current answer has a value
        if cur_id is None:
            return cur_ans

        rtrnable = self.get_furthest_answer(cur_id)

        if rtrnable is None:
            return cur_ans

        return rtrnable


if __name__ == "__main__":
    import argparse

    # Set commandline options

    parser = argparse.ArgumentParser()
    parser.add_argument("-q", "--question", type=str,
                        help="Question to ask first")
    parser.add_argument("-D", "--debug", action="store_true",
                        help="Enable debug logging of the command line")
    parser.add_argument("-i", "--config", type=str, required=True,
                        help="Path to the configuration file.")
    parser.add_argument("-t", "--timed", action="store_true",  # TODO
                        help="WIP!!! Force timed completion of the quest.")
    parser.add_argument("-p", "--scored", action="store_true",  # TODO
                        help="WIP!!! Scored completion of the quest.")
    args = parser.parse_args()

    logging.basicConfig(
        filename="log.txt",
        filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.DEBUG if args.debug else logging.INFO, )

    logging.log(level=logging.DEBUG, msg="Starting PyQuest with Debug Logging")

    quest = PyQuest(config=args.config, first_question=args.questions, auto_start=True)
