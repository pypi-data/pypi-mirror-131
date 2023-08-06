from setuptools import setup
 
classifiers = []
 
setup(
  name='pypresence-stats',
  version='2',
  description='Presence-stats but you can make python script and launch it.',
  long_description=open("README.md").read(),
  long_description_content_type='text/markdown',
  url='https://redirect.rukchadisa.live/7SoIfy9ZMa',  
  author='Rukchad Wongprayoon',
  author_email='contact@biomooping.tk',
  license='MIT', 
  classifiers=classifiers,
  keywords='Tools', 
  py_modules=["presencestats"],
  install_requires=["pypresence","psutil"],
  entry_points={
    'console_scripts': ['pypresence=presencestats:launcharg']
  }
)
