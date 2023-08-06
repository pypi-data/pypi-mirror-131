from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "A simple math package"
LONG_DESCRIPTION = (
    "My first simple math package Python package with a slightly longer description"
)

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="example-pkg-Irene",
    version=VERSION,
    author="IrenePS",
    author_email="<ipsomiad@yahoo.gr>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'
    keywords=["python", "first package"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
