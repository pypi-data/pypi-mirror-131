from setuptools import setup

VERSION = '0.0.2'
DESCRIPTION = 'Information retrieval system for pdf documents'

# Setting up
setup(
    name='irspdf',
    version=VERSION,
    author='Jibril Frej',
    description=DESCRIPTION,
    packages=['irspdf'],
    install_requires=['nltk==3.6.5', 'numpy==1.21.4', 'pdfplumber==0.5.28'],
    keywords=['python', 'information retrieval'],
    classifiers=[
        'Programming Language :: Python :: 3',
        ]
)
