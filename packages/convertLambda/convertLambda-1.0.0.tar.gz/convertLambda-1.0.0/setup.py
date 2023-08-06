import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="convertLambda",
    version="1.0.0",
    author="Ali Alshawabkeh",
    author_email="alialshawabkeh12@gmail.com",
    description="convert lambda calculas to python code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Abuzz1/LambdaToPython",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
