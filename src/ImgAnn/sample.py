# image dataset sampling method implementation class

from .operators.ImgData import ImgData



class Sample:

    @classmethod
    def show_samples(cls, data_path: str,
                     ann_path: str,
                     snn_type: str = 'coco',
                     num_of_samples: int = 5):
        imgdataset = ImgData.extract(data_path)
        sample_img, sample_paths = imgdataset.random_img(num_of_samples)
        pass
