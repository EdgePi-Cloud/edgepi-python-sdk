"""' SDK publishing """

import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setuptools.setup(
    name="edgepi-python-sdk",
    version="1.2.13",
    author="S.Park",
    author_email="spark@osensa.com",
    description="EdgePi Python SDK package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EdgePi-Cloud/edgepi-python-sdk",
    project_urls={
        "Bug Tracker": "https://github.com/EdgePi-Cloud/edgepi-python-sdk/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(where="src", exclude=["test_edgepi"]),
    package_dir={"": "src"},
    python_requires=">=3.6",
    install_requires=["python-periphery >= 2.3.0", "bitstring >= 3.1.9", "protobuf>=3.20"],
)
