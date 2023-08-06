import pathlib
from setuptools import find_packages, setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="CAStatus",
    version="1.0.0",
    description="status.json and log.txt for your programs",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/codingaround/CAStatus.git",
    author="codingaround",
    author_email="codingaround90s@gmail.com",
    license="GNU",
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    # packages=["CAImport"],
    packages=find_packages(exclude=("tests",)),
    install_requires=['instanceTuner'],
    # entry_points={
    #    "console_scripts": [
    #    "realpython=instanceTuner.__main__:main",
    # ]
    # },
)
