import logging

import Answer


class Question:
    def __init__(self, question):

        q = question.get("question")
        a = question.get("answers")

        self.answers = []

        if q is not None:
            self.question_text = q.get('viewable_text')
            self.question_type = q.get('type')
            self.next_question = q.get('next_question')
            self.previous_question = q.get('previous_question')

        if a is not None:
            self.answers = [
                Answer.Answer(
                    viewable_text=ans['viewable_text'],
                    next_question=ans.get('next_question'),
                    validator=ans.get('validator'),
                    value=ans.get('value')
                )
                for i, ans in enumerate(a)
            ]

    def reset(self) -> None:
        """
        Resets the answers attached to the question to initial state.
        :return:
        """

        # Reset the answer holder for free form questions then return
        if self.question_type == 'free_form':
            self.answers[0].set_viewable_text("")
            return

        # Reset each answer in the question back to false.
        for answer in self.answers:
            answer.set_selected_status(False)

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
                    logging.debug(f"Answer Set to {ans}")
                    return ans
            return None
        elif self.question_type == 'free_form':
            logging.debug(f"Answer Set to {self.answers[0]}")
            return self.answers[0]
        else:
            raise NotImplementedError(f"Non implemented question type {self.question_type}")

    def get_question_type(self):
        return self.question_type

    def add_answer(self, answer: Answer) -> None:
        self.answers.append(answer)
