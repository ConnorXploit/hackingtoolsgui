from setuptools import setup, find_packages

requirements = ''
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='hackingtools',
        version='0.7.2',
        description='All Hacking Tools in this Python with Manually Created Modules',
        url='http://github.com/ConnorXploit/hackingtools-py',
        author='Connor',
        author_email='cgehminecraft@gmail.com',
        license='MIT',
        packages=find_packages(include=['hackingtools*']),
        include_package_data = True,
        package_data = {
            'hackingtools/core': ['config.json'],
            '': ['requirements.txt']
        },
        classifiers=[
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: MIT License"
        ],
        install_requires=requirements,
        zip_safe=False)