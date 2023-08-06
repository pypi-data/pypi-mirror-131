from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 1 - Planning',
  'Intended Audience :: Education',
  'Operating System :: MacOS :: MacOS X',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='paul_smiley_prediction',
  version='0.0.1',
  description='Smiley face predictior',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='Paul Fentress',
  author_email='fentresspaul@berkeley.edu',
  license='MIT',
  classifiers=classifiers,
  keywords='Smiley Face',
  packages=find_packages(),
  install_requires=(['opencv-python-headless',
  'matplotlib==3.5.0',
  'numpy==1.18.1',
  'opencv_python==4.5.4.58',
  'pandas==0.24.2',
  'streamlit==1.2.0',
  'streamlit_drawable_canvas==0.8.0',
  'tensorflow==2.3.1',
  'Keras==2.4.3'])
)
