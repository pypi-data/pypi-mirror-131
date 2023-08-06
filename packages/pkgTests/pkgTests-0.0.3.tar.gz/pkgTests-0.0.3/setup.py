from setuptools import setup, find_packages
from os import path as OSPath
import io
here = OSPath.abspath(OSPath.dirname(__file__))

VERSION = '0.0.3'
DESCRIPTION = 'My first Python Hello world library'
#LONG_DESCRIPTION = 'A basic hello world package.'

with open("README.md", 'r') as f:
    long_description = f.read()

# get the dependencies and installs
with io.open(OSPath.join(here, 'requirements.txt'), encoding='utf-8') as f:
    #all_reqs = f.read().split('\n')
    all_reqs = f.read().split('\n')
    
install_requires = [x.strip() for x in all_reqs if 'git+' not in x]



# Setting up
setup(
    name="pkgTests",
    version=VERSION,
    author='ChenChih.Lee',
    author_email="jacklee26@gmail.com",
    url='https://github.com/chenchih/PackageTest',
    license='MIT',
    description=DESCRIPTION,   
    long_description_content_type="text/markdown",
    long_description=long_description,
    #adding packagedata for bdistr
    include_package_data=True,
    package_data={'pkgTest': ['test_use/*.txt']},
    packages=find_packages(),
    #packages=find_packages(exclude=['*_files']),
    #requirement will automatic install it
    #install_requires=['opencv-python', 'pyautogui', 'pyaudio'],
    #install_requires=['selenium==3.141.0']
    install_requires=install_requires,   
    #keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    entry_points={
    'console_scripts': [
        'helloworld-cli = pkgTest.helloworld:hellotest',
    ],
},

    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
