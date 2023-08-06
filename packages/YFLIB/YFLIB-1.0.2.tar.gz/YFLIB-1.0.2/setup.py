import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="YFLIB",
    version="1.0.2",
    description="Read the latest README.md",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/SharkFinRice/Python_YFLib",
    author="Dev",
    author_email="alvinhoidam1128@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["yflib","yflib/indicators","yflib/cache"],
    include_package_data=True,
    install_requires=["feedparser", "html2text"],
    entry_points={
        "console_scripts": [
            "read_dayEnd=yflib.functions:read_dayEnd",
            "read_indicator=yflib.functions:read_indicator"
        ]
    },
)
