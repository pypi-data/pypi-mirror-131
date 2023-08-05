from setuptools import setup
from setuptools.command.install import install

VERSION = '0.1.0'
DESCRIPTION = 'Information retrieval system for pdf documents'


def _install():
    import nltk
    nltk.download('stopwords')


class Install(install):
    def run(self):
        install.run(self)
        self.execute(_install, [], msg='Downloading nltk stopwords')


setup(
    name='irspdf',
    version=VERSION,
    author='Jibril Frej',
    author_email="<frejjibril@gmail.com>",
    description=DESCRIPTION,
    packages=['irspdf'],
    cmdclass={'install': Install},
    install_requires=['nltk', 'numpy', 'pdfplumber'],
    setup_requires=['nltk'],
    keywords=['python', 'information retrieval'],
    classifiers=[
        'Programming Language :: Python :: 3'
        ]
)
