# Instance Object for COCO annotation format

from abc import ABC
import json
import logging

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

    # def __init__(self, annotations):
    #     self.annotations = annotations
    #     pass

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
        # TODO: output:: all the annotations in the file
        with open(path) as fp:
            ann_data = json.load(fp)
        return ann_data

    def archive(self):
        # TODO: save coco annotation file in the given location
        pass

    def translate(self):
        # TODO: translate common schema into json compatible format.
        pass

    def __normalized2KITTI(self,box):
        o_x, o_y, o_width, o_height = box
        xmin = int(o_x - o_width / 2)
        ymin = int(o_y - o_height / 2)
        xmax = int(o_x + o_width / 2)
        ymax = int(o_y + o_height / 2)
        return [(xmin, ymin), (xmax, ymax)]
