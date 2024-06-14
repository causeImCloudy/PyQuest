import sys
import io
from contextlib import redirect_stdout


class MyClass:
    def perform_action(self):
        print("Hello, world!")
        print("This is a test.")


def capture_stdout():
    f = io.StringIO()  # Create a string buffer to capture the output
    with redirect_stdout(f):
        my_instance = MyClass()
        my_instance.perform_action()
    return f.getvalue()  # Return the content of the buffer


output = capture_stdout()
print("Captured Output:")
print(output)
