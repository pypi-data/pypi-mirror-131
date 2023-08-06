import setuptools
from pathlib import Path

setuptools.setup(
    name="garpdf",
    version=1.0,
    long_descriptoin=Path("README.md").read_text(),
    packages=setuptools.find_namespace_packages(exclude=["tests", "data"])
)
