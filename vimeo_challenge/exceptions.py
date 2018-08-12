""" Exceptions docstring here #TODO """


class ClipNotFoundException(RuntimeError):
    """ Clip not found in ES index. """

    def __init__(self, args):
        self.args = args
