import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zipbiaschecker",
    version="0.0.1",
    author="Edwin Zhang",
    description="A quick check for racial bias using zipcode-level Census data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/edjzhang/zipbiaschecker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
