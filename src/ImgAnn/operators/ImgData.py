# data extract from image dataset.

import os
import random
import logging
import traceback

# create a logger
logger = logging.getLogger(__name__)

# set log Level
logger.setLevel(logging.INFO)

# define fileHandler and formatter
# file_handler = logging.FileHandler('../logs/ImgAnn/operators/log_ImgData.txt')
# formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
# file_handler.setFormatter(formatter)

# add file handler to logger
# logger.addHandler(file_handler)

""":cvar
image_df attributes:
    - image_id : int
    - image_name : str
    - folder : str
    - path : str (separated by / )
    - width : int
    - height : int
    - format : class [(default) RGB, GBR, SHA ]

"""


class ImgData:

    def __init__(self, root: str, dataset: dict):
        self.dataset = dataset
        self.root = root

    @classmethod
    def extract(cls, dataset_path: str):
        """
        Extract folder names, all the files in the dataset.pip
        """
        folders = ImgData.ext_folders(dataset_path)
        files = ImgData.ext_files(dataset_path)
        dataset = {"folders": folders, "files": files}
        logger.info(' dataset dict : {}'.format(dataset))
        return cls(root=dataset_path, dataset=dataset)

    @staticmethod
    def ext_folders(path):
        """
        Output all the folder names in the given directory.
        """
        folders = []
        try:
            assert os.path.exists(path), "path does not exists"
            folders = [x[1] for x in os.walk(path) if x[1] != []]
            if folders == []:
                if [x for x in os.walk(path)] == []:
                    parent_path, file_name = os.path.split(path)
                    folders = os.path.basename(parent_path)
                else:
                    folders = [os.path.basename(path)]
            else:
                folders = folders[0]
        except Exception as error:
            logger.error(error.__traceback__)
        return folders

    @staticmethod
    def ext_files(path):
        """
        Output all the files in the given directory.
        """
        files = []
        try:
            assert os.path.exists(path), "path does not exists"
            files = [x[2] for x in os.walk(path) if x[2] != []]
            if files == []:
                if [x for x in os.walk(path)] == []:
                    parent_path, file_name = os.path.split(path)
                    files = file_name
                else:
                    files = None
                logger.error("Error : There are no files in the given directory")
        except Exception as error:
            logger.error(error.__traceback__)

        return files


    def random_img(self, num_of_imgs: int):
        tol_imgs = []
        img_cnt = [0, ]
        for imgs in self.dataset["files"]:
            img_cnt.append(img_cnt[-1] + len(imgs))
            tol_imgs.extend(imgs)
        img_cnt = img_cnt[1:]

        rnd_numbers = sorted(random.sample(range(0, len(tol_imgs)), num_of_imgs))
        folders = self.dataset["folders"]
        logger.info('folder info: {}'.format(folders))
        imgs = []
        img_paths = []

        try:
            for i in rnd_numbers:
                point = -1
                full_path = ''
                while img_cnt[point + 1] - i < 0:
                    point += 1
                else:
                    # print(point,i,img_sets[point+1])
                    fld = folders[point + 1]
                    position = i - img_cnt[point + 1]
                    fold = folders[point + 1]
                    img = self.dataset["files"][point + 1][position]
                    imgs.append(img)
                    img_paths.append(f"{self.root}/{fold}/{img}")
        except:
            logger.warning('calling index is {}, but length of folder is {}'.format(point,len(folders)))
        logger.info('imgs : {}'.format(imgs))
        logger.info('img_paths : {}'.format(img_paths))
        return imgs, img_paths
