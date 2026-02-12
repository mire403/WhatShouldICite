"""
Setup script for WhatShouldICite
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="whatshouldicite",
    version="0.1.0",
    author="WhatShouldICite Team",
    description="Suggest citations for selected text in your editor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/whatshouldicite",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        # 当前版本无外部依赖
    ],
)
