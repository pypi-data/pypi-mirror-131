from setuptools import setup

VERSION = '0.0.1'
DESCRIPTION = 'Information retrieval system for pdf documents'

# Setting up
setup(
    name='irspdf',
    version=VERSION,
    author='Jibril Frej',
    description=DESCRIPTION,
    packages=['irspdf'],
    install_requires=['numpy', 'pdfplumber', 'nltk'],
    keywords=['python', 'information retrieval'],
    classifiers=[
        'Programming Language :: Python :: 3',
        ]
)
