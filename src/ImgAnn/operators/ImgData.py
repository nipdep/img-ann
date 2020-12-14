# data extract from image dataset.

import os
import random
import logging
import traceback
import pandas as pd

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

        folders = ImgData.ext_folders(dataset_path)
        if type(folders) == str:
            logger.error("you have entered a file directory. Enter Folder directory.")
        else:
            data_list = []
            if len(folders) == 1:
                files = ImgData.ext_files(os.path.abspath(dataset_path))
                if files:
                    data_list.extend(ImgData.list_creator(os.path.abspath(dataset_path), folders[0], files))
                else:
                    logger.error("Error: there are no files in given directory!")
            else:
                for folder in folders:
                    files = ImgData.ext_files(os.path.abspath(dataset_path)+"\\"+folder)
                    if files:
                        data_list.extend(ImgData.list_creator(os.path.abspath(dataset_path+"\\"+folder), folder, files))
                    else:
                        continue

            if data_list:
                data_df = pd.DataFrame.from_records(data_list, columns=['name', 'folder', 'path'])
            else:
                logger.error("there was some error, record tuples are empty.")
        return cls(root=dataset_path, dataset=data_df)

    @staticmethod
    def list_creator(root: str, folder: str, files: list):
        """

        :param root: absolute path for the folder
        :param folder: parent folder of a file
        :param files: all the files
        :return: [(name, folder, path), ..]
        """
        tol_list = []
        for file in files:
            tol_list.append((file, folder, root+"\\"+file))
        return tol_list

    @staticmethod
    def ext_folders(path):
        """
        Output all the folder names in the given directory.
        """
        folders = []
        try:
            assert os.path.exists(path), "path does not exists"
            folders = [x[1] for x in os.walk(path) if x[1] != []]
            if not folders:
                if not [x for x in os.walk(path)]:
                    parent_path, file_name = os.path.split(path)
                    folders = os.path.basename(parent_path)
                else:
                    folders = [os.path.basename(path)]
            else:
                folders = folders[0]
        except Exception as error:
            logger.exception("There is no folder in given directory.")
        return folders

    @staticmethod
    def ext_files(path):
        """
        Output all the files in the given directory.
        """
        format_list = ['png', 'jpg', 'jpeg']
        files = []
        try:
            assert os.path.exists(path), "path does not exists"
            # TODO: and x[2].split('.')[-1].lowercase() in format_list
            files = [x[2] for x in os.walk(path) if x[2] != []]
            if not files:
                if not [x for x in os.walk(path)]:
                    parent_path, file_name = os.path.split(path)
                    files = file_name
                else:
                    files = None
            else:
                if len(files) == 1:
                    files = files[0]
        except Exception as error:
            logger.exception("Error : There are no files in the given directory")

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
            logger.warning('calling index is {}, but length of folder is {}'.format(point, len(folders)))
        logger.info('imgs : {}'.format(imgs))
        logger.info('img_paths : {}'.format(img_paths))
        return imgs, img_paths
