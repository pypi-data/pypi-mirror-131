import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
    setuptools.setup(
    name="covid-dashboard-jis206", 
    version="1.0.0",
    author="Jack Souster",
    author_email="jis206@exeter.ac.uk",
    description="A webpage dashboard displaying the latest covid-19 data and news",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JackSouster/covid-dashboard-jis206",
    packages=setuptools.find_packages(),
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
    python_requires='>=3.9.7',
)