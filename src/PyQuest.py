import logging
import os

import Answer
import DataPrinter
import DataReader
import Question
from DataPrinter import ScreenPrinter

DEFAULT_AES = "ThisShouldBeChangedForYouIfYouWantToChangeIt"
DEFAULT_IV = "THISISANIV"


class PyQuest:
    def __init__(self, config, first_question=None, auto_start=False) -> None:
        """

        :param config:  This is a reference - make a copy if you intend to edit the passed config variable otherwise info will be deleted
        :param first_question:
        :param auto_start:
        """
        # Initialize variables for use later, and assign passed variables.
        # Some variables depend on being internalised to default None
        self.timed, self.scored, self.printer = None, None, None
        self.questions = {}

        self.current_question = 0 if first_question is None else first_question
        self.first_question = self.current_question  # Assigns the first value of current_question to record and track

        # Differentiate between passed config and a file containing the config.
        # Utilize Data reader object to read from file or dict (YAML/JSON)
        if isinstance(config, str):
            if not os.path.exists(config):  # Ensure the file path exists
                raise FileNotFoundError

            data = DataReader.data_from_file(config)

        elif isinstance(config, dict):
            data = config
        elif config is None:
            return
        else:
            raise ValueError("Invalid config variable")

        # Take in initial config variable and assign them to the instance
        # utilizing the built-in functions to limit each variable correctly
        self.set_current_question(data["first_question"])
        self.set_scored(data["scored"])
        self.set_timed(data["timed"])
        self.set_printer(data["printer"])
        self.title = data.get("title", None)

        # !!! This variable is referenced not a copy. !!!
        # Delete excess variables from the config dict
        # This is needed in order to loop and initialize each question correctly
        del data["first_question"]
        del data["scored"]
        del data["timed"]
        del data["printer"]

        # Create the questions from a dict then assign back to the instance
        self.set_questions(DataReader.data_from_dict(data))

        # Start the quest immediately if initialized from the commandline
        if auto_start:
            self.start()

    def reset(self) -> None:
        """
        Resets the PyQuest. This only resets the timer, score, and selected answers.
        Any dynamically created answers should be updated again.
        :return:
        """

        for question in self.questions:
            self.questions[question].reset()

    def add_question(self, question: Question.Question, index: int) -> None:
        # Verify that no question already has that id
        if self.questions.get(index) is not None:
            raise IndexError(f'Question already has an question with index {index}.')

        self.questions[index] = question

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

        if answer.get_next_question():
            path = answer.get_next_question()  # Update path if answer obj has a custom path

        logging.debug(f"Questing has pathed to {path}")

        # Return next question by ID of Path
        return path

    def start(self, questionId=None) -> None:
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

        cur_id = cur_ans.get_next_question()

        # Ensure the current answer has a value
        if cur_id is None:
            return cur_ans

        rtrnable = self.get_furthest_answer(cur_id)

        if rtrnable is None:
            return cur_ans

        return rtrnable

    def get_printer(self):
        return self.printer

    def set_printer(self, printer):
        if printer == "screen":
            self.printer = DataPrinter.ScreenPrinter()
        elif printer == "terminal":
            self.printer = DataPrinter.Terminal()

    def quick_save_quest(self, filename, save_path=None) -> None:
        """
        Quick save the quest to custom pquest file format given a save path and file name
        :param filename:
        :param save_path:
        :return:
        """
        import pickle
        import Crypto.Cipher.AES as AES
        from os.path import join, curdir

        # Todo update this to scored to grab from server
        pckl_obj = pickle.dumps(self)
        encrypter = AES.new(DEFAULT_AES, AES.MODE_CBC, DEFAULT_IV)
        cipher_text = encrypter.encrypt(pckl_obj)

        filename = filename.split(".")[0]
        filename = filename + ".pquest"

        if save_path is None:
            save_path = curdir

        full_path = join(save_path, filename)

        with open(full_path, "wb") as file:
            file.write(cipher_text)

    def save_quest(self, filename, save_path=None) -> None:
        from os.path import join, curdir
        from json import dump

        # Create Dict to Save and add first layer PyQuest items
        output_dict = {
            "first_question": self.first_question,
            "timed": self.timed,
            "scored": self.scored,
            "printer": "screen" if type(self.printer) is ScreenPrinter else "terminal",
        }

        # Loop through Questions and add to output dict
        for (id, question) in self.questions.items():
            question_dict = {
                "question": {
                    "viewable_text": question.get_viewable_text(),
                    "next_question": question.get_next_question(),
                    "previous_question": question.get_previous_question(),
                    "type": question.get_question_type()
                },
                "answers": [
                    {
                        "viewable_text": answer.get_viewable_text(),
                        "next_question": answer.get_next_question(),
                        "value": answer.get_value()
                    } for answer in question.get_answers()
                ]
            }

            output_dict[str(id)] = question_dict

        # Do validation on passed save path and format a full path.
        filename = filename.split(".")[0]
        filename = filename + ".json"

        if save_path is None:
            save_path = curdir

        full_path = join(save_path, filename)

        # Save dict to file in json format
        # Todo add support for YAML
        with open(full_path, "w") as file:
            dump(output_dict, file, indent=4)  # JSON.dump(_)


def quick_load_quest(self, file_path) -> PyQuest:
    import pickle
    import Crypto.Cipher.AES as AES

    # Todo update this to scored to grab from server
    encrypter = AES.new(DEFAULT_AES, AES.MODE_CBC, DEFAULT_IV)
    with open(file_path, "rb") as file:
        cipher_text = file.read()
        plain_text = encrypter.decrypt(cipher_text)

    return pickle.loads(plain_text)


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
    parser.add_argument("-b", "--build", action="store_true",
                        help="Opens the building application to build a config file.")
    parser.add_argument("-d", "-dev", action="store_true",
                        help="Enabled a dev mode where you can chose to save the state of a quest")
    args = parser.parse_args()

    logging.basicConfig(
        filename="log.txt",
        filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.DEBUG if args.debug else logging.INFO, )

    logging.log(level=args.level, msg="Starting PyQuest with Debug Logging")

    if args.build:
        import Builder

        Builder.build()
    else:
        quest = PyQuest(config=args.config, first_question=args.questions)
        try:
            quest.start()
        except KeyboardInterrupt as err:
            if args.dev:
                save_config = {
                    "first_question": 0,
                    "timed": False,
                    "scored": False,
                    "printer": "screen",
                    "0": {
                        "question": {
                            "viewable_text": "Do you want to save the current state of the quest?",
                            "next_question": None,
                            "previous_question": None,
                            "type": "multiple_choice"
                        },
                        "answers": [
                            {
                                "viewable_text": "Yes",
                                "value": 1,
                                "next_question": 1,
                            },
                            {
                                "viewable_text": "No",
                                "value": 0,
                            }
                        ]
                    },
                    "1": {
                        "question": {
                            "viewable_text": "Please enter the file name to save the current state of the quest.",
                            "next_question": None,
                            "previous_question": 0,
                            "type": "free_form"
                        },
                        "answers": [
                            {
                                "viewable_text": ""
                            }
                        ]
                    }
                }
                save = PyQuest(save_config)

                save.start()
                if save.get_question_by_id(0).get_selected_answer().get_value() == 1:
                    file_name = save.get_question_by_id(0).get_selected_answer().get_value()
                    quest.quick_save_quest(file_name)
            else:
                raise KeyboardInterrupt(err)
