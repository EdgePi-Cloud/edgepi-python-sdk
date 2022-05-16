import setuptools

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setuptools.setup(
    name="EdgePi-Python-SDK",
    version="0.0.1-9",
    author="S.Park",
    author_email="spark@osensa.com",
    description="EdgePi Python SDK package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/osensa/edgepi-python-sdk",
    project_urls={
        "Bug Tracker": "https://github.com/osensa/edgepi-python-sdk/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},    
    python_requires=">=3.6",
    install_requires=["python-periphery >= 2.3.0"]
)