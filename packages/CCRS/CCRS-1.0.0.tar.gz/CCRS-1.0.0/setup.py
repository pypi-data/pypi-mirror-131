import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CCRS",
    version="1.0.0",
    author="Victor",
    author_email="chenweibang@genomics.cn",
    description="Risk stratification of coronary heart disease and ischemic stroke",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VVictorChen/CCR",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
