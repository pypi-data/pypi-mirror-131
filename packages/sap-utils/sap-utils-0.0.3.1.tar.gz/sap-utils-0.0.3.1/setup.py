#!/usr/bin/env python
# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


install_requires = [
    "numpy",
    "pandas",
    "matplotlib",
    "tqdm",
    "joblib",
]

with open(file='README.md', mode='r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name="sap-utils",
    version="0.0.3.1",
    description="Random utility code.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Satyarth Praveen",
    author_email="satyarth934@gmail.com",
    url="https://github.com/satyarth934/sap-utils",
    packages=find_packages(
        where="src",
    ),
    package_dir={"": "src"},
    # include_package_data=True,
    python_requires=">=3.6",
    install_requires=install_requires,
    # zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/satyarth934/sap-utils/issues",
        # 'Documentation': None,
        "Source": "https://github.com/satyarth934/sap-utils",
    },
)