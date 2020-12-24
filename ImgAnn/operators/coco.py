# Instance Object for COCO annotation format

from abc import ABC
import json
import os
import logging
import pandas as pd
import random

# setup logger
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


from .operator import IOperator


class COCO(IOperator, ABC):

    def __init__(self, dataset):
        super().__init__(dataset)
        self._dataset = dataset

    def get_dataset(self):
        return self._dataset

    def describe(self):
        # TODO: coco file description outputs (to - superClass )

        pass

    def extract(self, path: str):
        """
        all the annotations in the file convert into general dataframe object.
        :param path: string, relative / absolute path
        :return: generalize pandas.DataFrame type object.
        """
        if os.path.exists(path):
            with open(path) as fp:
                ann_data = json.load(fp)
            self.__updateDataset(ann_data["images"])
            self.__extractAnnotation(ann_data["annotations"])
            self.__extractClasses(ann_data["categories"])
        else:
            logger.error(f"Error: entered path <{path}> is invalid.")
        return

    def archive(self):
        # TODO: save coco annotation file in the given location
        pass

    def translate(self):
        # TODO: translate common schema into json compatible format.
        pass

    def __normalized2KITTI(self, box):
        """

        :param box: [X, Y, width, highest]
        :return: [(xmin, ymin), (xmax, ymax)]
        """
        o_x, o_y, o_width, o_height = box
        xmin = int(o_x - o_width / 2)
        ymin = int(o_y - o_height / 2)
        xmax = int(o_x + o_width / 2)
        ymax = int(o_y + o_height / 2)
        return [(xmin, ymin), (xmax, ymax)]

    def __updateDataset(self, images):
        """

        :param images: image attributes in the .json file
        :return: add id, image width & height columns to self.dataset
        """
        dataset_imgs = list(self._dataset.iloc[:, 0].values)
        ann_imgs = []
        ann_id = {}
        img_width = {}
        img_height = {}
        for obj in images:
            if obj["file_name"] in dataset_imgs:
                try:
                    ann_imgs.append(obj["file_name"])
                    ann_id[obj["file_name"]] = obj["id"]
                    img_width[obj["file_name"]] = obj["width"]
                    img_height[obj["file_name"]] = obj["height"]
                except Exception as error:
                    logger.exception("ERROR: annotation file doesn't in accept the format.")
        if len(dataset_imgs) > len(ann_imgs):
            self._dataset = self._dataset.loc[self._dataset.loc[:, "name"].isin(ann_imgs), :]
            logger.warning("WARNING: all the images had not annotated!")
        self._dataset = self._dataset.copy()
        self._dataset["image_id"] = self._dataset["name"].map(ann_id)
        self._dataset.loc[:, "width"] = self._dataset.loc[:, "name"].map(img_width)
        self._dataset.loc[:, "height"] = self._dataset.loc[:, "name"].map(img_height)
        return

    def __extractAnnotation(self, anns):
        """

        :param anns: annotation attribute in the .json file
        :return: None , add self.annotations attr.
        """
        ann_list = []
        for obj in anns:
            try:
                obj_id = obj["id"]
                img_id = obj["image_id"]
                cls_id = obj["category_id"]
                min_tup, max_tup = self.__normalized2KITTI(obj["bbox"])
            except Exception as error:
                logger.exception("ERROR: annotation file doesn't in accept the format.")
            else:
                ann_list.append((obj_id, img_id, cls_id, min_tup[0], min_tup[1], max_tup[0], max_tup[1]))
        else:
            if ann_list:
                ann_df = pd.DataFrame.from_records(ann_list,
                                                   columns=['obj_id', 'image_id', 'class_id', 'x_min', 'y_min', 'x_max',
                                                            'y_max'])
                self.annotations = ann_df
            else:
                self.annotations = pd.DataFrame()

    def __extractClasses(self, cats):
        """

        :param cats: categories attribute in the .json file
        :return: dictionary object of type {id : class-name}
        """
        if len(cats) > 0:
            class_dict = {}
            for obj in cats:
                try:
                    class_dict[obj["id"]] = obj["name"]
                except Exception as error:
                    logger.exception("ERROR: annotation file doesn't in accept the format.")
            else:
                self.classes = class_dict
        else:
            logger.error("There are no distinctive class definition in the annotation.")
            self.classes = {}

