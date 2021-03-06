'''Cloud ML Engine package configuration.'''
from setuptools import setup, find_packages

setup(name='onset_detector',
      version='1.0',
      packages=find_packages(),
      include_package_data=True,
      description='CNN onset detection keras model on Cloud ML Engine',
      author='David Haas',
      author_email='dhaas6@vt.edu',
      license='MIT',
      install_requires=[
          'keras',
          'numpy',
          'tinytag',
          'h5py'],
      zip_safe=False)
