# Operator Abstract class

from abc import ABCMeta, abstractmethod


class IOperator:

    def __init__(self):
        pass

    @abstractmethod
    def describe(self): raise NotImplementedError

    @abstractmethod
    def sample(self): raise NotImplementedError

    @abstractmethod
    def extract(self): raise NotImplementedError

    @abstractmethod
    def translator(self): raise NotImplementedError

    @abstractmethod
    def archive(self): raise NotImplementedError

    def descFormat(self):
        # TODO: make nice format to show descibe result.
        pass

    def render(self):
        # TODO: show annotated image
        pass
