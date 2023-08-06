import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="vidsnap",
    version="0.0.2",
    description="Vidsnap is a fast multithreaded tool to split videos into images.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jarviscodes/vidsnap",
    author="Jarvis Codes",
    author_email="jarvis@jayradz.com",
    license="MIT",
    classifiers=["Programming Language :: Python :: 3"],
    packages=["vidsnap"],
    include_package_data=True,
    install_requires=["click", "colorama", "opencv-python"],
    entry_points={"console_scripts": ["vidsnap=vidsnap.__main__:main"]},
)
