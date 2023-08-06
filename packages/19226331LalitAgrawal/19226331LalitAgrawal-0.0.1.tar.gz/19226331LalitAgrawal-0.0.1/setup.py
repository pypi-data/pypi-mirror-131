import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="19226331LalitAgrawal",
    version="0.0.1",
    author="Lalit Agrawal",
    author_email="agrawal.lalit95@gmail.com",
    description="A package to calculate total cart value",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/agrawallalit/Food_ordering_library",
    packages=setuptools.find_packages(),
    install_requires=[''],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)