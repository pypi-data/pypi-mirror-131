import setuptools

with open("README.md") as file:
    read_me_description = file.read()

setuptools.setup(
    name="Developing Cockroach",
    version="0.4.1",
    author="Farioso Fernando",
    author_email="farioso.f@gmail.com",
    description="This is a simple package for outputting data to the terminal replacing the print function",
    long_description=read_me_description,
    long_description_content_type="text/markdown",
    url="https://github.com/farioso-fernando/developer",
    packages=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)