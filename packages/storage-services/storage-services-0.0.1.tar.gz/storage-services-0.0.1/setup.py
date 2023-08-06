import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='storage-services',
    version='0.0.1',
    author="Chella S",
    author_email="2chellaa@gmail.com",
    description="A AWS utility package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChellaS/storage-service",
    project_urls={
        "Bug Tracker": "https://github.com/ChellaS/storage-service/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
 )