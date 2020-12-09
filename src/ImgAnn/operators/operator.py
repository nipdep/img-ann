# Operator Abstract class

from abc import ABCMeta, abstractmethod


class IOperator:

    def __init__(self,dataset):
        self.dataset = dataset
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

    @classmethod
    def datasetReader(cls, data_path: str):

        return cls(object)

    @classmethod
    def randomizer(cls,num_of_samples: int):
        pass
