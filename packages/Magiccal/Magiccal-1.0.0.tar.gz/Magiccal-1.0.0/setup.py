from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Magiccal',
  version='1.0.0',
  description='Calculate 11 different complex calculations like Data, BMI, GST, Discount, Date, Age, Time, Decimal, Temperature, Speed, Pressure',
  long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='http://ashishjaiswal.great-site.net/',
  project_urls={
        "Source Code": "https://github.com/itsashishjaiswal/PythonLibraries/tree/main/MagiccalLibrary",
    },
  author='Ashish Jaiswal',
  author_email='a.j250897@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['python', 'education', 'calculations', 'conversions', 'magiccal', 'data'], 
  packages=find_packages(),
  install_requires=[''] 
)