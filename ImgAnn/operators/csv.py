# Instance Object for COCO annotation format

from abc import ABC

from .operator import IOperator


class CSV(IOperator, ABC):

    def __init__(self):
        pass

    def describe(self):
        # TODO: csv file description outputs (to - superClass )
        pass

    def sample(self):
        # TODO: output:: list of annotation results from annotation file
        pass

    def extract(self):
        # TODO: output:: all the annotations in the file
        pass

    def archive(self):
        # TODO: save csv annotation file in the given location
        pass

    def translate(self):
        # TODO: translate common schema into json compatible format.
        pass
