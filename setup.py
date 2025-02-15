"""Setup configuration for rsq-utils package."""
from setuptools import setup, find_packages

setup(
    name="rsq-utils",
    version="1.0.0",
    description="Utility functions for all projects",
    author="Ryan Quigley",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "python-dotenv",
        "requests",
        "psutil",
        "pandas",
        "types-setuptools",
    ],
    extras_require={
        "dev": [
            "coverage>=7.0.0",
            "types-psutil",
            "pandas-stubs",
            "types-setuptools",
            "mypy>=1.0.0",
            "pylint>=2.17.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
