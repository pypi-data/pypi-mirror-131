from pathlib import Path
from setuptools import find_packages, setup

# Package meta-data.
NAME = 'tid-houseregression-model'
DESCRIPTION = "Example regression model package to train regression on house\
              data"
URL = "https://github.com/Nakulbajaj101/deploying-machine-learning-models"
EMAIL = "bajaj.nakul@gmail.com"
AUTHOR = "Nakul Bajaj"
REQUIRES_PYTHON = ">=3.6.0"

long_description = DESCRIPTION

about = {}

ROOT_DIR = Path(__file__).parent
REQUIREMENTS_DIR = ROOT_DIR / 'requirements'
PACKAGE_DIR = ROOT_DIR / 'houseregression_model'

with open(PACKAGE_DIR / "VERSION") as f:
    _version = f.read().strip()
    about["__version__"] = _version


def list_reqs(fname="requirements.txt"):
    with open(REQUIREMENTS_DIR / fname) as fd:
        return fd.read().splitlines()


setup(
    name=NAME,
    version=about["__version__"],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=("tests",)),
    package_data={"houseregression_model": ["VERSION"]},
    install_requires=list_reqs(),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
