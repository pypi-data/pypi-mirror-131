import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mongo_api_yunsou",
    version="0.1.3",
    author="sysuyanxp",
    author_email="yanxp3@mail2.sysu.edu.cn",
    description="A database api for inserting, searching, updating and deleting based on mongdb",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
