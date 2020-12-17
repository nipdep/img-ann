# Instance Object for COCO annotation format

from abc import ABC
import json
import os
import logging
import pandas as pd

# setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# set fileHandler and formatter
# file_handler = logging.FileHandler('../logs/ImgAnn/operators/log_coco.txt')
# formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
# file_handler.setFormatter(formatter)

# add file handler to logger
# logger.addHandler(file_handler)

from .operator import IOperator


class COCO(IOperator, ABC):

    def __init__(self, dataset):
        super().__init__(dataset)
        self._dataset = dataset


    def describe(self):
        # TODO: coco file description outputs (to - superClass )

        pass

    def sample(self, ann_data, names: list):
        # TODO: output:: list of annotation results from annotation file
        ann_filt_data = {}
        images_name = [elem['file_name'] for elem in ann_data["images"] if (elem['file_name'] in names)]
        image_id = [elem['id'] for elem in ann_data["images"] if (elem['file_name'] in names)]
        objects = ann_data["annotations"]
        for obj in objects:
            obj_id = obj['image_id']
            if obj_id in image_id:
                if obj_id not in ann_data:
                    ann_filt_data[obj_id] = {"name": images_name[image_id.index(obj_id)],
                                             "box": [self.__normalized2KITTI(obj['bbox'])],
                                             "category_id": [obj["category_id"]]}
                else:
                    ann_filt_data[obj_id]["box"].append(self.__normalized2KITTI(obj['bbox']))
                    ann_filt_data[obj_id]["category_id"].append(obj["category_id"])
                # ann_filt_data.append(obj)
        categ = ann_data["categories"]
        cat_dict = {}
        for cat in categ:
            cat_dict[cat["id"]] = cat["name"]

        reodered_ann_data = [ann_filt_data[i] for i in image_id]

        orderd = sorted(ann_filt_data.values(), key=lambda x: names.index(x['name']))
        logger.info('just extra data : {}, {}'.format(reodered_ann_data, names))

        return orderd, cat_dict

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

        return ann_data

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
        ann_id = []
        img_width = []
        img_height = []
        for obj in images:
            if obj["file_name"] in dataset_imgs:
                try:
                    ann_imgs.append(obj["file_name"])
                    ann_id.append(obj["id"])
                    img_width.append(obj["width"])
                    img_height.append(obj["height"])
                except Exception as error:
                    logger.exception("ERROR: annotation file doesn't in accept the format.")
        id_series = pd.Series(ann_id, index=ann_imgs)
        width_series = pd.Series(img_width, index=ann_imgs)
        height_series = pd.Series(img_height, index=ann_imgs)

        self._dataset["image_id"] = id_series
        self._dataset["width"] = width_series
        self._dataset["height"] = height_series
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
                ann_df = pd.DataFrame.from_records(ann_list, columns=['obj_id', 'image_id', 'class_id', 'x_min', 'y_min', 'x_max', 'y_max'])
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
