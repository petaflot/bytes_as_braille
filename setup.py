from pathlib import Path

from setuptools import find_packages
from setuptools import setup

setup(
    name="bytes_as_braille",
    packages=find_packages(exclude=["tests"]),
    url="https://github.com/petaflot/bytes_as_braille",
    license="MIT",
    author="JCZD",
    author_email="jczd@engrenage.ch",
    description=(
        "Display/Input bytestrings as Braille cells "
        "(optional color support)."
    ),
    long_description=Path("README.md").read_text(),
    classifiers=[
        "Development Status :: 1 - Prototype",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        #"Topic :: Multimedia :: Graphics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={"console_scripts": ["bytestrings = bytes_as_braille.bytes_as_braille:main"]},
    setup_requires=["setuptools_scm"],
    #extras_require={"images": ["pillow"]},
    include_package_data=True,
)
