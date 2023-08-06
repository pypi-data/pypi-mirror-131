from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='liop',
  version='0.0.1',
  description='To Do Operation With Every Elements Of Lists',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='HARI PRASANTH S',
  author_email='hariprasanth581@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['List Calculator','List','Operator'], 
  packages=find_packages(),
  install_requires=[''] 
)