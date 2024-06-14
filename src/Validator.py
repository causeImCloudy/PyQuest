import re

# TODO
STATIC_VALIDATORS = {}

class Validator:
    def __init__(self, regex):
        self.regex = regex

    def validate(self, string):
        return re.match(self.regex, string) is not None
