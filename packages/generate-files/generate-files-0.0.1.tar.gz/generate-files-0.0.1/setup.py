import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="generate-files",
    version="0.0.1",
    author="Mohammad Toseef",
    author_email="mohammad.toseef059@gmail.com",
    description="Fetch data from API and generates csv, html , pdf , xlsx , xml files ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mohammad-Toseef/Week1.git",
    project_urls={
        "Bug Tracker": "https://github.com/Mohammad-Toseef/Week1.git",
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
