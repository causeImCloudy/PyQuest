def build() -> None:
    import PyQuest
    import Answer
    import Question

    settings_config = {
        "first_question": 0,
        "timed": False,
        "scored": False,
        "printer": "screen",
        "0": {
            "question": {
                "viewable_text": "What is the title of your quest?",
                "next_question": None,
                "previous_question": None,
                "type": "free_form"
            },
            "answers": [
                {
                    "viewable_text": "",
                    "next_question": 1,
                }

            ]
        },
        "1": {
            "question": {
                "viewable_text": "Is your quest scored?",
                "next_question": None,
                "previous_question": 0,
                "type": "multiple_choice"
            },
            "answers": [
                {
                    "viewable_text": "Yes",
                    "value": True,
                    "next_question": 2,
                },
                {
                    "viewable_text": "No",
                    "value": False,
                    "next_question": 2,
                }
            ]
        },
        "2": {
            "question": {
                "viewable_text": "Is your quest timed?",
                "next_question": None,
                "previous_question": 1,
                "type": "multiple_choice"
            },
            "answers": [
                {
                    "viewable_text": "Yes",
                    "value": True,
                    "next_question": 3,
                },
                {
                    "viewable_text": "No",
                    "value": False,
                    "next_question": 3,
                }
            ]
        },
        "3": {
            "question": {
                "viewable_text": "What screen type would you like?",
                "next_question": None,
                "previous_question": 2,
                "type": "multiple_choice"
            },
            "answers": [
                {
                    "viewable_text": "Terminal Screen",
                    "value": "screen"
                },
                {
                    "viewable_text": "Default Terminal I/O",
                    "value": "terminal"
                }
            ]
        }
    }

    question_loop_config = {
        "first_question": 0,
        "timed": False,
        "scored": False,
        "printer": "screen",
        "0": {
            "question": {
                "viewable_text": "Do you want to add a question?",
                "next_question": None,
                "previous_question": 1,
                "type": "multiple_choice"
            },
            "answers": [
                {
                    "viewable_text": "Yes",
                    "value": True,
                    "next_question": 1,
                },
                {
                    "viewable_text": "No",
                    "value": False
                }
            ]
        },
        "1": {
            "question": {
                "viewable_text": "What is the text of your question?",
                "next_question": None,
                "previous_question": 0,
                "type": "free_form"
            },
            "answers": [
                {
                    "viewable_text": "",
                    "next_question": 2,
                }

            ]
        },
        "2": {
            "question": {
                "viewable_text": "What is the previous question?",
                "next_question": None,
                "previous_question": 1,
                "type": "free_form"
            },
            "answers": [
                {
                    "viewable_text": "",
                    "next_question": 3,
                }
            ]
        },
        "3": {
            "question": {
                "viewable_text": "What type of question is this?",
                "next_question": None,
                "previous_question": 2,
                "type": "multiple_choice"
            },
            "answers": [
                {
                    "viewable_text": "Multiple Choice",
                    "value": "multiple_choice"
                },
                {
                    "viewable_text": "Freeform",
                    "value": "free_form"
                }
            ]
        }
    }

    answer_loop_config = {
        "first_question": 0,
        "timed": False,
        "scored": False,
        "printer": "screen",
        "0": {
            "question": {
                "viewable_text": "Do you want to add a answer to the question?",
                "next_question": None,
                "previous_question": None,
                "type": "multiple_choice"
            },
            "answers": [
                {
                    "viewable_text": "Yes",
                    "value": True,
                    "next_question": 1,
                },
                {
                    "viewable_text": "No",
                    "value": False,
                    "next_question": None
                }
            ]
        },
        "1": {
            "question": {
                "viewable_text": "What is the text of your answer?",
                "next_question": None,
                "previous_question": 0,
                "type": "free_form"
            },
            "answers": [
                {
                    "viewable_text": "",
                    "next_question": 2,
                }

            ]
        },
        "2": {
            "question": {
                "viewable_text": "What is the value of your answer?",
                "next_question": None,
                "previous_question": 0,
                "type": "free_form"
            },
            "answers": [
                {
                    "viewable_text": "",
                    "next_question": 3,
                }

            ]
        },
        "3": {
            "question": {
                "viewable_text": "What question does this answer go to?",
                "next_question": None,
                "previous_question": 0,
                "type": "free_form"  # TODO Add a better way to do this
            },
            "answers": [
                {
                    "viewable_text": ""
                }
            ]
        }
    }

    answer_loop_free_form_config = {
        "first_question": 0,
        "timed": False,
        "scored": False,
        "printer": "screen",
        "0": {
            "question": {
                "viewable_text": "Do you want to add a default text to the question?",
                "next_question": None,
                "previous_question": None,
                "type": "free_form"
            },
            "answers": [
                {
                    "viewable_text": "",
                    "next_question": 1,
                }
            ]
        },
        "1": {
            "question": {
                "viewable_text": "What question does this answer go to?",
                "next_question": None,
                "previous_question": 0,
                "type": "free_form"  # TODO Add a better way to do this
            },
            "answers": [
                {
                    "viewable_text": "",
                }
            ]
        }
    }

    # Initialize the 3 PyQuest variables with the above config
    # Create an output PyQuest instance to then save to file later.
    settings = PyQuest.PyQuest(settings_config)
    question_quest = PyQuest.PyQuest(question_loop_config)
    output = PyQuest.PyQuest(None)

    # Run through the opening to determine the settings for the quest
    # Then assign to the output PyQuest
    settings.start()

    # Pass the settings from the answered quest into
    output.set_scored(
        settings.get_question_by_id(1).get_selected_answer().get_value()
    )
    output.set_timed(
        settings.get_question_by_id(2).get_selected_answer().get_value()
    )
    output.set_printer(
        settings.get_question_by_id(3).get_selected_answer().get_value()
    )

    index = 0

    # Continually loop through the Question PyQuest to grab all the questions you want
    # Additionally add internal loop to add all the answers
    while True:
        # Start the question PyQuest
        question_quest.start()

        # Grab the first question (Do you want to make a question) and break if the answer is No
        continue_question = question_quest.get_question_by_id(0).get_answer_by_id(0).get_selected_status()
        if not continue_question:
            break

        # Assign the question values to temporary variables to later add to the output Quest
        viewable_text = question_quest.get_question_by_id(1).get_selected_answer().get_value()
        prev_question = question_quest.get_question_by_id(2).get_selected_answer().get_value()
        question_type = question_quest.get_question_by_id(3).get_selected_answer().get_value()

        question = Question.Question({
            "question": {
                "viewable_text": viewable_text,
                "prev_question": prev_question,
                "type": question_type
            }
        })

        if question_type == "multiple_choice":
            answer_quest = PyQuest.PyQuest(answer_loop_config)
            while True:
                # Start Answer PyQuestion
                answer_quest.start()

                # Break if you don't want to add any answers
                continue_answer = answer_quest.get_question_by_id(0).get_selected_answer().get_value()
                if not continue_answer:
                    break

                # Create an answer with the respective associated answer, assign to question, then reset question
                ans_viewable_text = answer_quest.get_question_by_id(1).get_selected_answer().get_value()
                value = answer_quest.get_question_by_id(2).get_selected_answer().get_value()
                next_question = answer_quest.get_question_by_id(3).get_selected_answer().get_value()

                answer = Answer.Answer(
                    viewable_text=ans_viewable_text,
                    value=value,
                    next_question=int(next_question) if len(next_question) > 0 else None,
                )
                question.add_answer(answer)
                answer_quest.reset()

        elif question_type == "free_form":
            # Run through the free form question then creat the answer, and add it to question
            answer_quest = PyQuest.PyQuest(answer_loop_free_form_config)
            answer_quest.start()

            ans_viewable_text = answer_quest.get_question_by_id(0).get_selected_answer().get_value()
            next_question = answer_quest.get_question_by_id(1).get_selected_answer().get_value()

            answer = Answer.Answer(
                viewable_text=ans_viewable_text,
                value=None,
                next_question=int(next_question) if next_question is not None and len(next_question) > 0 else None
            )
            question.add_answer(answer)

        output.add_question(question, index)
        question_quest.reset()

        # Increment the index of the question
        index += 1

    filename = settings.get_question_by_id(0).get_selected_answer().get_value()
    output.save_quest(filename)


if __name__ == '__main__':
    import PyQuest
    import logging

    logging.basicConfig(level=logging.DEBUG, filename="log.txt")

    build()
