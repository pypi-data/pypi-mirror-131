from setuptools import setup, find_packages

setup(
    author="Mathias Schreiner",
    author_email="matschreiner@gmail.com",
    url="https://gitlab.com/matschreiner/pype",
    download_url="https://gitlab.com/matschreiner/pype/-/archive/v2.1.0/pype-v2.1.0.tar.gz",
    name="pype-ms",
    version="2.1.0",
    packages=find_packages(),
    install_requires=[
        "pyyaml",
        "pytest",
        "Click",
    ],
    entry_points={
        "console_scripts": [
            "pype = pype.cli:cli",
        ],
    },
)
