import logging

import Answer


class Question:
    def __init__(self, ID, question):
        logging.log(logging.DEBUG, "Question initialised: ID = " + str(ID))

        q = question["question"]
        a = question["answers"]

        self.question_text = q['viewable_text']
        self.question_type = q['type']
        self.answers = [
            Answer.Answer(
                viewable_text=ans['viewable_text'],
                validator=ans.get('validator'),
                value=ans.get('value')
            ) if isinstance(ans, dict)
            else Answer.Answer(
                viewable_text=ans,
                value=i
            )
            for i, ans in enumerate(a)
        ]

        self.next_question = q['next_question']
        self.previous_question = q['previous_question']

    def get_viewable_text(self) -> None:
        return self.question_text

    def get_answers(self) -> list[Answer]:
        return self.answers

    def get_answer_by_id(self, aid) -> Answer:
        return self.answers[aid]

    def get_next_question(self) -> int:
        return self.next_question

    def get_previous_question(self) -> int:
        return self.previous_question

    def get_navigation(self) -> list:
        navbar = (self.next_question, self.previous_question)
        return [item for item in navbar if item is not None]

    def get_selected_answer(self) -> Answer:
        if self.question_type == 'multiple_choice':
            for ans in self.answers:
                if ans.selected:
                    return ans

            return None
        else:
            raise NotImplementedError("Non implemented question type")
