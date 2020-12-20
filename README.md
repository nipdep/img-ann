![Build Status](https://travis-ci.com/nipdep/img-ann.svg?branch=main)
# img-ann
 // description
The ImgAnn is a package for a simplify operations in image annotated files.
such as, annotation type converting \[coco format, pascalVOC format, csv format], image dataset sampling], etc.


## Installation
You can install the Real Python Feed Reader from [PyPI](https://pypi.org/project/ImgAnn/):

pip install ImgAnn

The package is support Python 3.4 and above.
 
## Usage
 // summary of commands you can run.
 
 - To get N number of annotated images randomly.
    you can use coco format, pascalVOC format or csv format as annotation format.
    <annotation type> keywords can be from \['coco', 'csv', 'voc'::wq
    ]
 `
 from ImgAnn import Sample
 Sample.show_samples(<image dataset dir> : string, <annotation file dit> : string, <number of images> : int, <annotation type> : string= 'coco' ) 
 `
 
 
 
