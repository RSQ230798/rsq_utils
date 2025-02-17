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
        "colorama"=="0.4.6"
        "exceptiongroup"=="1.2.2"
        "iniconfig"=="2.0.0"
        "numpy"=="2.2.3"
        "packaging"=="24.2"
        "pandas"=="2.2.3"
        "pandas-stubs"=="2.2.3.241126"
        "pathlib"=="1.0.1"
        "pluggy"=="1.5.0"
        "psutil"=="7.0.0"
        "pytest"=="8.3.4"
        "python-dateutil"=="2.9.0.post0"
        "python-dotenv"=="1.0.1"
        "pytz"=="2025.1"
        "six"=="1.17.0"
        "tomli"=="2.2.1"
        "types-psutil"=="6.1.0.20241221"
        "types-pytz"=="2025.1.0.20250204"
        "types-setuptools"=="75.8.0.20250210"
        "tzdata"=="2025.1",
    ],
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
