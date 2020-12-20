# Operator Abstract class

from abc import ABCMeta, abstractmethod
import matplotlib.pyplot as plt
import cv2
import pandas as pd
import logging

#set logger
logger = logging.getLogger(__name__)
# set logger level
logger.setLevel(logging.INFO)

""":param
ann_df attributes:
    - obj_id : int
    - image_id : int
    - class_id : int
    - x_min : int
    - y_min : int
    - x_max : int
    - y_max : int
"""
""":param
render format
    - image path
    - box : [[(x_min, y_min), (x_max, y_max)], ...]
    - classes : [str, ...]
"""


class IOperator:
    # def __init__(self,dataset):
    #     self.dataset = dataset
    #     pass

    __dataset = pd.DataFrame()

    def __init__(self, dataset):
        self.__dataset = dataset

    def set_dataset(self, df):
        """
        :param df: pandas.DataFrame type object with attr. defined in the ImgData.py file

        save new dataset into the objects' private variable.
        """
        if type(df) is pd.DataFrame:
            self.__dataset = df
        else :
            logger.error(f"Data type of df : {type(df)} not compatible with database object.")

    def get_dataset(self):
        """
        :return pandas.DataFrame
        """
        return self.__dataset


    @abstractmethod
    def describe(self):
        raise NotImplementedError

    @abstractmethod
    def sample(self, ann_data, names: list):
        raise NotImplementedError

    @abstractmethod
    def extract(self, path: str):
        raise NotImplementedError

    @abstractmethod
    def translator(self):
        raise NotImplementedError

    @abstractmethod
    def archive(self):
        raise NotImplementedError

    def descFormat(self):
        # TODO: make nice format to show descibe result.
        pass

    def render(self, path: str, boxes: list, cls: list, rect_th=2, text_size=0.5, text_th=1):
        # TODO: show annotated image
        img = cv2.imread(path)
        # img = cv2.cvtColor(img)

        for i in range(len(boxes)):
            # print(boxes[i][0], boxes[i][1])
            cv2.rectangle(img, boxes[i][0], boxes[i][1], color=(0, 255, 0), thickness=rect_th)
            cv2.putText(img, cls[i],
                        boxes[i][0], cv2.FONT_HERSHEY_COMPLEX,
                        text_size, color=(0, 255, 0), thickness=text_th)
        plt.figure(figsize=(30, 30))
        plt.imshow(img)
        plt.xticks([])
        plt.yticks([])
        plt.show()
        return

    @classmethod
    def datasetReader(cls, data_path: str):

        return cls(object)

    @classmethod
    def randomizer(cls, num_of_samples: int):
        pass
