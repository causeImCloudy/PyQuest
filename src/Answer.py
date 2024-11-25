import sys


class Answer:
    def __init__(self, viewable_text, next_question, validator=None, value=None, selected_status=False):
        self.value, self.viewable_text, self.selected, self.next_question = None, None, None, None

        self.set_viewable_text(viewable_text)
        self.set_value(value)
        self.set_selected_status(selected_status)
        self.set_next_question(next_question)

        self.validator = validator

    def __validate__(self):
        return self.validator.validate(self.value)

    def set_value(self, value) -> None:
        self.value = value

    def set_viewable_text(self, viewable_text: str) -> None:
        # Set viewable text
        if sys.getsizeof(viewable_text) > 2048:
            raise ValueError("Answer value must be less than 2024 bytes")

        if not isinstance(viewable_text, str):
            raise ValueError("Answer text must be a string")

        self.viewable_text = viewable_text

    def set_selected_status(self, status: bool) -> None:
        # Updates the selected status, true or false
        if isinstance(status, bool):
            self.selected = status
        else:
            raise ValueError("Status must be boolean")

    def get_viewable_text(self) -> str:
        return self.viewable_text

    def get_value(self):
        return self.value

    def get_selected_status(self) -> bool:
        return self.selected if self.selected is not None else False

    def set_next_question(self, next_question: int) -> None:
        self.next_question = next_question

    def get_next_question(self) -> int:
        return self.next_question
