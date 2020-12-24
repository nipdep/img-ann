# Instance Object for COCO annotation format

from abc import ABC
import logging
import os
import pandas as pd

# setup logger
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from .operator import IOperator


class CSV(IOperator, ABC):

    def __init__(self, dataset):
        super().__init__(dataset)
        self._dataset = dataset
        self.attrs = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']

    def extract(self, path: str):
        """
        all the annotations in the file convert into general dataframe object.
        :param path: string, relative / absolute path
        :return: generalize pandas.DataFrame type object.
        """
        if os.path.exists(path):
            ann_df = pd.read_csv(path)
            attr_df_list = list(ann_df.columns)
            if all(x in attr_df_list for x in self.attrs):
                new_ann_df = self.__dfUpdates(ann_df)
                self.__updateDataset(new_ann_df.loc[:, ["name", "width", "height", "image_id"]])
                self.__setAnn(new_ann_df)
            else:
                assert Exception(
                    f"entered annotation file does not contains all the required attributes. \n {self.attrs}")
        else:
            assert Exception(f"entered directory {path}, does not exsist.")

    def archive(self):
        # TODO: save csv annotation file in the given location
        pass

    def translate(self):
        # TODO: translate common schema into json compatible format.
        pass

    def __dfUpdates(self, full_df):
        """add id, image width & height columns to self.dataset

        :param full_df: read .csv file from annotation file.
        :return: refine DataFrame object with column of ["name" ,"obj_id", "image_id", "class_id", "x_min", "y_min", "x_max", "y_max"]
        """
        full_df = full_df.copy()

        uni_files = list(full_df.loc[:, "filename"].unique())
        ns = len(uni_files)
        file_id_col = pd.Series(range(1, ns + 1), index=uni_files)
        full_df["image_id"] = full_df["filename"].map(file_id_col)

        cats = list(full_df.loc[:, "class"].unique())
        nc = len(cats)
        cat_id_col = pd.Series(range(1, nc + 1), cats)
        full_df["class_id"] = full_df["class"].map(cat_id_col)

        self.__defineClasses(nc, cats)
        full_df.drop("class", inplace=True, axis=1)

        full_df["obj_id"] = pd.Series(range(1, full_df.shape[0] + 1))
        full_df.rename(columns={"filename": "name", "xmin" : "x_min", "ymin" : "y_min", "xmax" : "x_max", "ymax" : "y_max"}, inplace=True)

        return full_df

    def __defineClasses(self, n_ids, classes):
        """

        :param n_ids: number of unique classes
        :param classes: class list
        :return: dictionary object of type {id : class-name}
        """
        if n_ids == len(classes):
            ids = range(1, n_ids + 1)
            self.classes = dict(zip(ids, classes))
        else:
            assert Exception(f"length of class names[{len(classes)}] and class ids[{n_ids}] are not equal.")
            self.classes = {}

    def __setAnn(self, full_df):
        """

        :param full_df: refined DataFrame object.
        :return: set generalized annotation df object as self.annotations
        """
        full_df = full_df.copy()
        col_lis = ["obj_id", "image_id", "class_id", "x_min", "y_min", "x_max", "y_max"]
        if all( y in list(full_df.columns) for y in col_lis):
            ann_df = full_df.loc[:, col_lis]
            self.annotations = ann_df
        else:
            assert Exception(f"there are missing of required columns in {full_df.columns}")
            self.annotations = pd.DataFrame()

    def __updateDataset(self, image_df):
        """

        :param image_df: image attributes DataFrame
        :return: merge current self.__dataset with image_df.
        """
        partial_df = image_df.copy()
        res_df = pd.merge(self._dataset, partial_df, on="name")
        self._dataset = res_df
