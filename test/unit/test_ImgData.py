
import unittest

from src.ImgAnn.operators.ImgData import ImgData

class TestImgData(unittest.TestCase):

    def setUp(self):
        self.obj = ImgData("","")

    def test_ext_folders(self):
        self.assertEqual(['operators'], ImgData.ext_folders('./logs/ImgAnn/'))
        self.assertEqual(['operators'], ImgData.ext_folders('./logs/ImgAnn/operators'))
        self.assertEqual('operators', ImgData.ext_folders('./logs/ImgAnn/operators/log_coco.txt'))
        # self.assert(AssertionError, self.obj.ext_folders('./logs/ImgAnn/operator'))

    def test_ext_files(self):
        self.assertEqual([['log_coco.txt','log_ImgData.txt']], ImgData.ext_files('./logs/ImgAnn/operators'))
        self.assertEqual('log_coco.txt', ImgData.ext_files('./logs/ImgAnn/operators/log_coco.txt'))


if __name__ == "__main__":
    unittest.main()
