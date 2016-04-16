"""
This example module shows various types of documentation available for use
with pydoc.  To generate HTML documentation for this module issue the
command:

    pydoc -w foo

"""


class Foo(object):
    """
    Foo encapsulates a name and an age.
    """
    def __init__(self, name, age):
        """
        When printing output to the console, pydoc attempts to paginate the
        output for easier reading. If the PAGER environment variable is set,
        pydoc will use its value as a pagination program.

        Params:
            name > string: The name of foo
            age  > integer: The age of foo

        Returns:
            nothing
        """
        self.name = name
        self.age


def bar(baz):
    """
    Prints baz to the display.
    """
    print(baz)

if __name__ == '__main__':
    f = Foo('John Doe', 42)
    bar("hello world")
