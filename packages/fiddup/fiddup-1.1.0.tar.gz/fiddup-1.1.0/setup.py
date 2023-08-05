import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="fiddup",
    version="1.1.0",
    description="Find files with similar names.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jarviscodes/fiddup",
    author="Jarvis Codes",
    author_email="jarvis@jayradz.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    packages=["fiddup"],
    include_package_data=True,
    install_requires=["click", "colorama"],
    entry_points={
        "console_scripts": [
            "fiddup=fiddup.__main__:fiddup"
        ]
    }
)