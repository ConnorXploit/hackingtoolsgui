from setuptools import setup, find_packages
import os
import sys
import subprocess
try:
    from pip import main as pipmain
except ImportError:
    from pip._internal import main as pipmain

requirements = ''
try:
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
except:
    print('You should install on Python 3.7+')


def checkPackages():
    # If Linux
    extra_packages = {
        "linux-apt": ['build-essential', 'cmake', 'libopenblas-dev', 'liblapack-dev', 'libx11-dev', 'libgtk-3-dev'],
        "linux": ['dlib'],
    }
    for system in extra_packages:
        if os.name in system:
            if '-apt' in system:
                for package in extra_packages[system]:
                    if not package in sys.modules:
                        subprocess.run('apt install {p}'.format(p=package))
            else:
                for package in extra_packages[system]:
                    if not package in sys.modules:
                        pipmain(['install', package])


checkPackages()

setup(name='hackingtools',
      version='3.2.2',
      description='All Hacking Tools in this Python with Manually Created Modules',
      url='http://github.com/ConnorXploit/hackingtools-py',
      author='Connor',
      author_email='cgehminecraft@gmail.com',
      license='MIT',
      packages=find_packages(include=['hackingtools*']),
      include_package_data=True,
      package_data={
          'hackingtools/core': ['config.json'],
          '': ['requirements.txt']
      },
      classifiers=[
          "Programming Language :: Python :: 3.7",
          "License :: OSI Approved :: MIT License"
      ],
      install_requires=requirements,
      zip_safe=False)
