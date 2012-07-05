from setuptools import setup,find_packages
import os

PATH = os.path.dirname(os.path.abspath(__file__))
templates_dir= os.path.join(PATH, "libgravatar")
templates_files = [os.path.join(templates_dir, file) for file in os.listdir(templates_dir)]

setup(name='pyGravatar',
    version='0.1',
    description='Simple API for Gravatar service',
    author='Ernesto Bossi',
    author_email='bossi.ernestog@gmail.com',
    license='GPL v3',
    keywords='gravatar api ',
    packages=find_packages(exclude=["test"]),
    data_files=[
        (templates_dir, templates_files)
    ],
    install_requires=['lxml']
)


