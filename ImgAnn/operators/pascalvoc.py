# Instance Object for COCO annotation format

from abc import ABC
import xml.etree.ElementTree as ET
import pandas as pd
import os
import logging

# setup logger
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from .operator import IOperator


class PascalVOC(IOperator, ABC):

    def __init__(self, dataset):
        super().__init__(dataset)
        self._dataset = dataset

    def describe(self):
        # TODO: xml file description outputs (to - superClass )
        pass

    def extract(self, path: str):
        """ extract annotation data when input the path to .xml files

        :param path:
        :return:
        """
        files_list = self.__extractFiles(path)
        image_id = 0
        img_list = []
        tol_obj_list = []
        for file in files_list:
            
            img_data, obj_list = self.__FileReader(os.path.abspath(path) + "\\" + file)
            image_id += 1
            img_data.append(image_id)
            obj_list = [i+[image_id] for i in obj_list]
            img_list.append(img_data)
            tol_obj_list.extend(obj_list)
        if img_list:
            img_df = pd.DataFrame.from_records(img_list, columns=['name', 'width', 'height','image_id'])
            self.__updateDataset(img_df)
        else:
            logger.error("[var]: img_list is empty.")

        if obj_list and len(obj_list[0]) == 6:
            obj_df = pd.DataFrame.from_records(obj_list,
                                               columns=['x_min', 'y_min', 'x_max', 'y_max', 'class', 'image_id'])
            self.__DFRefiner(obj_df)
        else:
            logger.error(f"obj_list has not many attrs. : {len(obj_list[0])} or obj_list is empty : {len(obj_list)}")

    def archive(self):
        # TODO: save pascalVOC annotation file in the given location
        pass

    def translate(self):
        # TODO: translate common schema into json compatible format.
        pass

    def __extractFiles(self, path: str):
        """

        :param path: relative or absolute directory to the annotation folder.
        :return: return list of all .xml file names in given directory.
        """
        if os.path.exists(path):
            if not [x[1] for x in os.walk(path) if x[1] != []]:
                path_list = [y[2] for y in os.walk(path) if y[2] != []][0]
                if path_list:
                    xml_list = [n for n in path_list if n.split('.')[-1] == 'xml']
                    if xml_list:
                        return xml_list
                    else:
                        assert Exception("There are no .xml files in the given directory.")
                else:
                    assert Exception("The folder is empty.")
        else:
            assert Exception(f"The entered path <{path}> is not valid.")

    def __DFRefiner(self, ann_df):
        ann_df = ann_df.copy()

        cats = list(ann_df.loc[:, "class"].unique())
        n_cats = len(cats)
        cat_series = pd.Series(range(1, n_cats + 1), index=cats)

        ann_df["class_id"] = ann_df["class"].map(cat_series)
        ann_df["obj_id"] = range(1,ann_df.shape[0]+1)
        nw_df = ann_df.loc[:, ["obj_id", "image_id", "class_id", "x_min", "y_min", "x_max", "y_max"]]

        self.annotations = nw_df
        self.classes = dict(zip(range(1,n_cats+1),cats))

    def __FileReader(self, file_path: str):
        ann_tree = ET.parse(file_path)
        ann_root = ann_tree.getroot()
        try:
            filename = ann_root.find('filename').text
            size = ann_root.find('size')
            width = int(size.find('width').text)
            height = int(size.find('height').text)
            img_data = [filename, width, height]

            obj_list = []
            for obj in ann_root.findall('object'):
                obj_list.append(self.__get_coco_annotation_from_obj(obj))
        except Exception as error:
            logger.exception(error)
            assert error
        else:
            return img_data, obj_list

    def __get_coco_annotation_from_obj(self, obj):
        try:
            label = obj.find('name').text
            bndbox = obj.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)
            ann = [xmin, ymin, xmax, ymax, label]
            return ann
        except Exception as error:
            logger.exception(error)
            assert error

    def __updateDataset(self, image_df):
        """

        :param image_df: image attributes DataFrame
        :return: merge current self.__dataset with image_df.
        """
        partial_df = image_df.copy()
        res_df = pd.merge(self._dataset, partial_df, on="name")
        self._dataset = res_df
