from pathlib import Path
from setuptools import setup

# The directory containing this file
HERE = Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="todopyedu",
    version="1.0.0",
    description="Issue log created for educational purposes",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/kekbek/python-todo",
    author="kekbek",
    author_email="vadyusha.surin@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["todopyedu"],
    include_package_data=True,
    install_requires=["typer", "colorama","prettytable","shellingham"],
    entry_points={
        "console_scripts": [
            "todopyeud=todopyedu.__main__:main",
        ]
    },
)