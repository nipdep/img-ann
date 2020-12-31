#!/usr/bin/python
# -*- coding: utf-8 -*-

from .operators.ImgData import ImgData
from .operators import *
import logging

# set logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Convertor:

    """ convert method implementation class """

    @staticmethod
    def coco2csv(dataset_dir: str,
                 coco_ann_dir: str,
                 save_dir: str):
        """ convert coco to csv

        :param dataset_dir: relative path current folder, or absolute path to the main folder of the image dataset
        :param coco_ann_dir: relative path current folder, or absolute path to the main folder of the annotated file
        :param save_dir: .csv file saving location
        :return: None
        """
        imgdataset = ImgData.extract(dataset_dir)
        coco_obj = coco.COCO(imgdataset.dataset)
        coco_obj.extract(coco_ann_dir)
        ann, cls = coco_obj.get_annotations()

        csv_obj = csv.CSV(imgdataset)
        csv_obj.set_annotations(ann, cls)
        csv_fomatted = csv_obj.translate()
        csv_obj.archive(save_dir, csv_fomatted)

    @staticmethod
    def coco2voc(dataset_dir: str,
                 coco_ann_dir: str,
                 save_dir: str):
        """ convert coco to pascal VOC

        :param dataset_dir: relative path current folder, or absolute path to the main folder of the image dataset
        :param coco_ann_dir: relative path current folder, or absolute path to the main folder of the annotated file
        :param save_dir: .csv file saving location
        :return: None
        """
        imgdataset = ImgData.extract(dataset_dir)
        coco_obj = coco.COCO(imgdataset.dataset)
        coco_obj.extract(coco_ann_dir)
        ann, cls = coco_obj.get_annotations()

        voc_obj = pascalvoc.PascalVOC(imgdataset)
        voc_obj.set_annotations(ann, cls)
        for xml, name in voc_obj.translate():
            file_dir = save_dir + '/' + name
            voc_obj.archive(file_dir, xml)

    @staticmethod
    def csv2coco(dataset_dir: str,
                 csv_ann_dir: str,
                 save_dir: str):
        """ convert .csv into coco

        :param dataset_dir: relative path current folder, or absolute path to the main folder of the image dataset
        :param csv_ann_dir: relative path current folder, or absolute path to the main folder of the annotated file
        :param save_dir: .csv file saving location
        :return: None
        """
        imagedataset = ImgData.extract(dataset_dir)
        csv_obj = csv.CSV(imagedataset)
        csv_obj.extract(csv_ann_dir)
        ann, cls = csv_obj.get_annotations()

        coco_obj = coco.COCO(imagedataset)
        coco_obj.set_annotations(ann, cls)
        data = coco_obj.translate()
        coco_obj.archive(save_dir, data)

    @staticmethod
    def csv2voc(dataset_dir: str,
                csv_ann_dir: str,
                save_dir: str):
        """ convert .csv into pascal VOC

        :param dataset_dir: relative path current folder, or absolute path to the main folder of the image dataset
        :param csv_ann_dir: relative path current folder, or absolute path to the main folder of the annotated file
        :param save_dir: .csv file saving location
        :return: None
        """
        imagedataset = ImgData.extract(dataset_dir)
        csv_obj = csv.CSV(imagedataset)
        csv_obj.extract(csv_ann_dir)
        ann, cls = csv_obj.get_annotations()

        voc_obj = pascalvoc.PascalVOC(imagedataset)
        voc_obj.set_annotations(ann, cls)
        for xml, name in voc_obj.translate():
            file_dir = save_dir + '/' + name
            voc_obj.archive(file_dir, xml)

    @staticmethod
    def voc2coco(dataset_dir: str,
                 voc_ann_dir: str,
                 save_dir: str):
        """ convert pascal VOC into coco

        :param dataset_dir: relative path current folder, or absolute path to the main folder of the image dataset
        :param voc_ann_dir: relative path current folder, or absolute path to the main folder of the annotated file
        :param save_dir: .csv file saving location
        :return: None
        """
        imagedataset = ImgData.extract(dataset_dir)
        voc_obj = pascalvoc.PascalVOC(imagedataset)
        voc_obj.extract(voc_ann_dir)
        ann, cls = voc_obj.get_annotations()

        coco_obj = coco.COCO(imagedataset)
        coco_obj.set_annotations(ann, cls)
        data = coco_obj.translate()
        coco_obj.archive(save_dir, data)

    @staticmethod
    def voc2csv(dataset_dir: str,
                voc_ann_dir: str,
                save_dir: str):
        """ convert pascal VOC into .csv

        :param dataset_dir: relative path current folder, or absolute path to the main folder of the image dataset
        :param voc_ann_dir: relative path current folder, or absolute path to the main folder of the annotated file
        :param save_dir: .csv file saving location
        :return: None
        """
        imagedataset = ImgData.extract(dataset_dir)
        voc_obj = pascalvoc.PascalVOC(imagedataset)
        voc_obj.extract(voc_ann_dir)
        ann, cls = voc_obj.get_annotations()

        csv_obj = csv.CSV(imagedataset)
        csv_obj.set_annotations(ann, cls)
        csv_fomatted = csv_obj.translate()
        csv_obj.archive(save_dir, csv_fomatted)
