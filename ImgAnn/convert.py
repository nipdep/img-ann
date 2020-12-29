# convert method implementation class

from .operators import *
import os
import logging

#set logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Convertor:

    def __init__(self):
        pass

    def coco2csv(self, dataset_dir: str,
                 coco_ann_dir: str,
                 save_dir: str):
        """ convert coco to csv

        :param dataset_dir: relative path current folder, or absolute path to the main folder of the image dataset
        :param coco_ann_dir: relative path current folder, or absolute path to the main folder of the annotated file
        :param save_dir: .csv file saving location
        :return:
        """
        if os.path.isfile(save_dir):
            root, file = os.path.split(save_dir)
            ext = file.split('.')[-1]
            if ext == 'csv':
                logger.error(f"given directory : <{save_dir}> must not include .csv file name.")
                return
            else:
                pass
        else:
            logger.error(f"given directory : <{save_dir}> must be a path to a .csv file")
            return

        imgdataset = ImgData.extract(dataset_dir)
        coco_obj = coco.COCO(imgdataset.dataset)
        coco_obj.extract(coco_ann_dir)
        ann, cls = coco_obj.get_annotations()

        csv_obj = csv.CSV(imgdataset)
        csv_obj.set_annotations(ann, cls)
        csv_fomatted = csv_obj.translate()
        csv_obj.archive(save_dir, csv_fomatted)

    def coco2pascalvoc(self, dataset_dir: str,
                       coco_ann_dir: str,
                       save_dir: str):
        # TODO: convert coco to pascal VOC
        imgdataset = ImgData.extract(dataset_dir)
        coco_obj = coco.COCO(imgdataset.dataset)
        coco_obj.extract(coco_ann_dir)
        ann, cls = coco_obj.get_annotations()

        voc_obj = pascalvoc.PascalVOC(imgdataset)
        voc_obj.set_annotations(ann, cls)

        pass

    def csv2coco(self, dataset_dir: str,
                 csv_ann_dir: str,
                 save_dir: str):
        # TODO: convert .csv into coco
        pass

    def csv2pascalvoc(self, dataset_dir: str,
                      csv_ann_dir: str,
                      save_dir: str):
        # TODO: convert .csv into pascal VOC
        pass

    def pascalvoc2coco(self, dataset_dir: str,
                       voc_ann_dir: str,
                       save_dir: str):
        # TODO: convert pascal VOC into coco
        pass

    def pascalvoc2csv(self, dataset_dir: str,
                      voc_ann_dir: str,
                      save_dir: str):
        # TODO: convert pascal VOC into .csv
        pass
