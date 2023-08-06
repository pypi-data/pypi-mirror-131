from distutils.core import setup
from setuptools import find_packages

with open("README.rst","r",encoding='gb18030',errors='ignore') as f:
    long_description = f.read()

setup(name='xlwang_package', #包名
      version='2.0.2',
      description='A small simple package',
      long_description = long_description,
      author= 'xlwang',
      author_email='172783266@qq.com',
      url='https://github.com/cassiewang123',
      install_requires=[],
      license='BSD License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
                  'Intended Audience :: Developers',
                  'Operating System :: OS Independent',
                  'Natural Language :: Chinese (Simplified)',
                  'Programming Language :: Python',
                  'Programming Language :: Python :: 2',
                  'Programming Language :: Python :: 2.5',
                  'Programming Language :: Python :: 2.6',
                  'Programming Language :: Python :: 2.7',
                  'Programming Language :: Python :: 3',
                  'Programming Language :: Python :: 3.5',
                  'Programming Language :: Python :: 3.6',
                  'Programming Language :: Python :: 3.7',
                  'Programming Language :: Python :: 3.8',
                  'Topic :: Software Development :: Libraries'
            ],
      )