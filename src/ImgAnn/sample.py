# image dataset sampling method implementation class

import logging

# setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# set fileHandler and formatter
# file_handler = logging.FileHandler('../logs/ImgAnn/log_sample.txt')
# formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
# file_handler.setFormatter(formatter)
#
# add file handler to logger
# logger.addHandler(file_handler)

from .operators.ImgData import ImgData
from .operators import coco, csv, pascalvoc


class Sample:

    @classmethod
    def show_samples(cls, data_path: str,
                     ann_path: str,
                     ann_type: str = 'coco',
                     num_of_samples: int = 5):
        imgdataset = ImgData.extract(data_path)
        # logger.info('folder attr. : {}'.format(imgdataset.dataset['folders']))
        samples_df = imgdataset.sample_dataset(num_of_samples)
        sample_img = list(samples_df.iloc[:, 0].values)
        paths = list(samples_df.iloc[:, 2].values)
        if ann_type == 'coco':
            obj = coco.COCO()
        elif ann_type == 'voc':
            obj = pascalvoc.PascalVOC()
        elif ann_type == 'csv':
            obj = csv.CSV()
        elif ann_type == 'yolo':
            obj = csv.IOperator()

        ann_data = obj.extract(ann_path)
        obj_list, cat_dict = obj.sample(ann_data, sample_img)

        for i in range(len(paths)):
            path = paths[i]
            obj_data = obj_list[i]
            # print(cat_dict, obj_data["category_id"])
            cat_name = [cat_dict[j] for j in obj_data["category_id"]]
            print(path, obj_data['name'])
            obj.render(path, obj_data["box"], cat_name)
        return
