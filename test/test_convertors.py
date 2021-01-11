from ImgAnn import convert

cnv = convert.Convertor()

# cnv.coco2csv('F:\JetBrain Project Files\Pycharm\security-point-object-detecton-Torch\data\data',
#                     'F:\JetBrain Project Files\Pycharm\security-point-object-detecton-Torch\data\COCO\dataset.json','../data/data.csv')

cnv.coco2voc('F:\JetBrain Project Files\Pycharm\security-point-object-detecton-Torch\data\data',
             'F:\JetBrain Project Files\Pycharm\security-point-object-detecton-Torch\data\COCO\dataset.json',
             '../data/voc')
