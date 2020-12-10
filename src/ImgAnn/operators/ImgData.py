# data extract from image dataset.

import os
import random

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

    @classmethod
    def extract(cls, dataset_path: str):
        folders = [x[1] for x in os.walk(dataset_path) if x[1] != []]
        files = [x[2] for x in os.walk(dataset_path) if x[2] != []]
        dataset = {"folders": folders, "files": files}
        return cls(root=dataset_path, dataset=dataset)

    def random_img(self, num_of_imgs: int):
        tol_imgs = []
        img_cnt = [0, ]
        for imgs in self.dataset["files"]:
            img_cnt.append(img_cnt[-1] + len(imgs))
            tol_imgs.extend(imgs)

        rnd_numbers = sorted(random.sample(range(0, len(tol_imgs)), num_of_imgs))
        folders = self.dataset["folders"]

        imgs = []
        img_paths = []

        pos = 1
        for ind in rnd_numbers:
            while ind > img_cnt[pos]:
                pos += 1
            position = ind - img_cnt[pos - 1]
            fold = folders[pos]
            img = self.dataset["files"][pos][position]
            imgs.append(img)
            img_paths.append(f"{self.root}/{fold}/{img}")

        return imgs, img_paths
