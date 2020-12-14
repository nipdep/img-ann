
import unittest
import pathlib
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from src.ImgAnn.operators.ImgData import ImgData



class TestImgData(unittest.TestCase):

    def setUp(self):
        self.here = str(pathlib.Path(__file__).parent.parent.parent.resolve())

    def test_ext_folders(self):
        self.assertEqual(['operators'], ImgData.ext_folders(self.here+'/logs/ImgAnn/'))
        self.assertEqual(['operators'], ImgData.ext_folders(self.here+'/logs/ImgAnn/operators'))
        self.assertEqual('operators', ImgData.ext_folders(self.here+'/logs/ImgAnn/operators/log_coco.txt'))
        # self.assert(AssertionError, self.obj.ext_folders(self.here+'/logs/ImgAnn/operator'))

    def test_ext_files(self):
        self.assertEqual(['log_coco.txt','log_ImgData.txt'], ImgData.ext_files(self.here+'/logs/ImgAnn/operators'))
        self.assertEqual('log_coco.txt', ImgData.ext_files(self.here+'/logs/ImgAnn/operators/log_coco.txt'))


if __name__ == "__main__":
    unittest.main()
