
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')


setup(

    name='ImgAnn',

    version='0.0.1',

    description='image annotation file operation provider.',

    long_description=long_description,

    long_description_content_type='text/markdown',

    url='https://github.com/nipdep/img-ann.git',

    author='nipdep',

    author_email='nipun1deelaka@gmail.com',

    classifiers=[  # Optional

        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],


    keywords='sample, setuptools, development',

    package_dir={'': 'src'},

    py_modules = ["helloworld"],
    # packages=find_packages(where='src'),

    python_requires='>=3.5, <4',

    install_requires=['peppercorn'],

    extras_require={
        'dev': ['check-manifest',
                'pytest>=3.7'],
        'test': ['coverage'],
    },

    # package_data={  # Optional
    #     'sample': ['package_data.dat'],
    # },

    # data_files=[('my_data', ['data/data_file'])],  # Optional

    entry_points={  # Optional
        'console_scripts': [
            'hello=helloworld:main',
        ],
    },

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/nipdep/img-ann/issues',
        # 'Funding': 'https://donate.pypi.org',
        # 'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/nipdep/img-ann/',
    },
)