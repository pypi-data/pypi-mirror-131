import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="upload_to_s3_folder_pkg",
    # Replace with your own username above
    version="0.0.1",
    author="Cormac Liston",
    author_email="x21154945@student.ncirl.ie",
    description="A small package that will upload your file to a specific S3 folder",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cormacio100/pypi_upload_to_s3_folder.git",
    packages=setuptools.find_packages(),
    # if you have libraries that your module/package/library
    #you would include them in the install_requires argument
    install_requires=[''],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)