from setuptools import find_packages
from setuptools import setup

setup(
    name="raytracer",
    version="0.0.1",
    author="Alexander Ershov",
    packages=find_packages("src"),
    package_dir={"": "src"},
)
