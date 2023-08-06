import os, lordkelvin
from setuptools import setup
setup(name='lordkelvin', version=lordkelvin.__version__,
      description='super cool toolkit',
      long_description=open(__file__[:-8]+"README.md").read(),
      long_description_content_type='text/markdown',
      url='https://gitlab.com/circleclicklabs/lordkelvin.git',
      author='Joel Ward', author_email='jmward+python@gmail.com',
      zip_safe=True, license='MIT',
      packages=['lordkelvin'],
      entry_points=dict(console_scripts=['lordkelvin=lordkelvin.__main__:main']),
      scripts=(lambda d:[d+x for x in os.listdir(d)])('scripts/'),
      install_requires=['docopt','web3==5.24','eth_account'],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
    ])
