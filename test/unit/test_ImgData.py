
import unittest
from unittest.mock import  Mock
from unittest.mock import patch
import pathlib
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from ImgAnn.operators.ImgData import ImgData



class TestImgData(unittest.TestCase):

    def setUp(self):
        self.here = str(pathlib.Path(__file__).parent.parent.parent.resolve())

    @patch('imgdata.os')
    def test_ext_folders(self, mock_os):
        mock_os.path.exists.side_effect = True


    def test_ext_files(self):
        self.assertEqual(['log_coco.txt','log_ImgData.txt'], ImgData.ext_files(self.here+'/logs/ImgAnn/operators'))
        self.assertEqual('log_coco.txt', ImgData.ext_files(self.here+'/logs/ImgAnn/operators/log_coco.txt'))


if __name__ == "__main__":
    unittest.main()
