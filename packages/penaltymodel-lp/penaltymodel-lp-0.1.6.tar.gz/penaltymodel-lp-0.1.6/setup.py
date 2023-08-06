from __future__ import absolute_import

import sys
from setuptools import setup

exec(open("./penaltymodel/lp/package_info.py").read())

FACTORY_ENTRYPOINT = 'penaltymodel_factory'

install_requires = ['dimod>=0.8.0,<0.11.0',
                    'penaltymodel>=0.16.0,<0.17.0',
                    'scipy>=1.5.2,<2.0.0',
                    'numpy>=1.19.1,<2.0.0',
                    ]

packages = ['penaltymodel',
            'penaltymodel.lp',
            ]

classifiers = [
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    ]

python_requires = '>=3.6'

setup(
    name="penaltymodel-lp",
    version=__version__,
    author=__author__,
    author_email=__authoremail__,
    description=__description__,
    long_description=open('README.rst').read(),
    url='https://github.com/dwavesystems/penaltymodel',
    license='Apache 2.0',
    packages=packages,
    classifiers=classifiers,
    python_requires=python_requires,
    install_requires=install_requires,
    entry_points={FACTORY_ENTRYPOINT: ['lp = penaltymodel.lp:get_penalty_model']},
    zip_safe=False
)
