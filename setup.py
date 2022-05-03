import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setuptools.setup(
    name="EdgePi-Python-SDK",
    version="0.0.1",
    author="S.Park",
    author_email="spark@osensa.com",
    description="EdgePi Python SDK package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="---to be inserted ---",
    project_urls={
        "Bug Tracker": "---to be inserted ---",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(where=".",
                                      include=["DAC"],
                                      exclude=["Tests"]),    
    python_requires=">=3.6",
)