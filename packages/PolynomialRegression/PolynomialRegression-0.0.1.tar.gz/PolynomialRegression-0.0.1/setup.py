from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
 #setup.py- tool that publishes the package to pypi uses

setup(
  name='PolynomialRegression',
  version='0.0.1',
  description='A library for polynomial regression',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  long_description_content_type="text/markdown",
  url='',  
  author='Sabrina Marshal and Sharon Immanuel',
  author_email='sharonimmanuel01@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='polynomial regression, best hypothesis', 
  packages=find_packages(),
  install_requires=['numpy','pandas','sklearn']  
  )