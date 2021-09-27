from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='sidfunc',
  version='0.0.3',
  description='siddharth functions',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Siddharth Singh',
  author_email='siddharthsingh5010@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='basicfunctions', 
  packages=find_packages(),
  install_requires=[''] 
)