from setuptools import setup, find_packages
import re


def get_ptdc_version():
    VERSION_FILE = "ptdc/__init__.py"
    ver_file = open(VERSION_FILE, "rt").read()
    VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, ver_file, re.M)
    if mo:
        return mo.group(1)
    else:
        raise RuntimeError("Unable to find version string in {}.".format(VERSION_FILE,))

def get_requirements():
    with open("requirements.txt") as req_file:
        return [line for line in req_file]


setup(
    name='ptdc',
    version=get_ptdc_version(),
    description='Twitter data collection library',
    keywords="twitter api tweepy collection data streaming",
    author='Andrea Lamparelli',
    author_email='lampa9559@gmail.com',
    url='https://github.com/lampajr/PTDC/',
    license="MIT License",
    zip_safe=False,

    packages=find_packages(exclude=['tests', 'samples', 'dataset']),
    install_requires=get_requirements(),

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    # use the module docs as the long description:
    long_description=open('README.md', 'r').read()
)
