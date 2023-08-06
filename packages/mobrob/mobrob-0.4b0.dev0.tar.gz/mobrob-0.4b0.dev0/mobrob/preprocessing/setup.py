#from distutils.core import setup
from setuptools import find_packages, setup

setup(
    name='prepocessing',
    version='0.3dev',
    author='68-6f-6c-67-69',
    author_email='68.6f.6c.67.69@gmail.com',
    url='https://github.com/68-6f-6c-67-69/mobrob',
    packages = find_packages(),
    py_modules=['preprocessing.rosbag2', 'preprocessing.dataframe'], 
    license='',
    long_description=open('README.txt').read(),
)





