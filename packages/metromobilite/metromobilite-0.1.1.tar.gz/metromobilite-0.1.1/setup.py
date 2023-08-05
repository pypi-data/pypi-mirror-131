from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="metromobilite",
    version="0.1.1",
    description="Python library for metromobilite API",
    long_description=long_description,
    long_description_content_type="text/markdown",  
    author="PierreBerger",
    license="MIT",
    url="https://github.com/PierreBerger/metromobilite",
    packages=find_packages(),
    test_suite="tests",
)