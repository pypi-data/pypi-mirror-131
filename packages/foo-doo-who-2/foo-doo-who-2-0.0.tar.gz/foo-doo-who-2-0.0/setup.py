from setuptools import setup, find_packages
 
classifiers = [
  'Operating System :: Microsoft :: Windows',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='foo-doo-who-2',
  version='0.0',
  description='useless junk',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='nate',
  author_email='nbenton90@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='junk-foo', 
  packages=find_packages(),
  install_requires=[''] 
)
