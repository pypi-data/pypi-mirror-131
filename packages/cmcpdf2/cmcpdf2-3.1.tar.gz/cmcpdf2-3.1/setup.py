import setuptools
from pathlib import Path

setuptools.setup(
    name="cmcpdf2",
    version=3.1,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
