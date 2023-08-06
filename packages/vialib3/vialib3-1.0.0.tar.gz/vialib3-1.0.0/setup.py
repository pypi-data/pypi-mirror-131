import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vialib3",
    version="1.0.0",
    author="Jeff Senn",
    author_email="jeffsenn@gmail.com",
    description="minimal VSMF support for Python 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeffsenn/vialib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    setup_requires=['wheel'],
)
