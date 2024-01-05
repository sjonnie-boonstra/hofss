from setuptools import find_packages, setup

# parse version number: __version__
__version__ = None  # in case hofss/_version.py does not define __version__
with open("hofss/_version.py") as fh:
    exec(fh.read())

# parse long description
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="hofss",
    version=__version__,
    description="Simulation of human and organizational factors in structural design.",
    url="https://gitlab.tudelft.nl/xinren/hofss",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Xin Ren",
    author_email="x.ren@tudelft.nl",
    packages=find_packages(exclude=["tests", ".github", "example_scripts"]),
    install_requires=["dataclass-csv>=1.4.0"],
    extras_require={
        "test": ["pytest>=7.4"]
    },
)
