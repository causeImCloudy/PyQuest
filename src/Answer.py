import sys


class Answer:
    def __init__(self, viewable_text, validator=None, value=None, selected_status=False):
        self.value, self.viewable_text, self.selected = None, None, None

        self.set_viewable_text(viewable_text)
        self.set_value(value)
        self.set_selected_status(selected_status)

        self.validator = validator

    def __validate__(self):
        return self.validator.validate(self.value)

    def set_value(self, value) -> None:

        if sys.getsizeof(value) > 1024 * 1024:
            raise ValueError("Answer value must be less than 1024 bytes")
        elif value is None:
            pass
        self.value = value

    def set_viewable_text(self, viewable_text) -> None:
        # Set viewable text
        if sys.getsizeof(viewable_text) > 1024 * 1024:
            raise ValueError("Answer value must be less than 1024 bytes")
        elif not isinstance(viewable_text, str):
            raise ValueError("Answer text must be a string")

        self.viewable_text = viewable_text

    def set_selected_status(self, status) -> None:
        # Updates the selected status, true or false
        if isinstance(status, bool):
            self.selected = status
        else:
            raise ValueError("Status must be boolean")

    def get_viewable_text(self) -> str:
        return self.viewable_text

    def get_value(self):
        return self.value
