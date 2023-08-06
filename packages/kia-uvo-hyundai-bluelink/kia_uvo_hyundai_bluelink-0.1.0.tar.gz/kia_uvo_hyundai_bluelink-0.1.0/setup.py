#!/usr/bin/env python
from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as file:
    long_description = file.read()

with open("requirements.txt", encoding="utf-8") as file:
    install_requires = list(val.strip() for val in file.readlines())

with open("requirements-test.txt", encoding="utf-8") as file:
    tests_require = list(val.strip() for val in file.readlines())

setup(
    name="kia_uvo_hyundai_bluelink",
    version="0.1.0",
    author="Fuat Akgun",
    author_email="fuatakgun@gmail.com",
    description="Python wrapper for getting vehicle data from Kia and Hyundai servers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    url="https://github.com/fuatakgun/KiaUvoHyundaiBluelinkAPI",
    license="Apache-2.0 License",
    packages=find_packages(exclude=["tests"]),
    install_requires=install_requires,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    setup_requires=("pytest-runner"),
    tests_require=tests_require,
)