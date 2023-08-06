import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="csvlogging_pkg_shri1900",
    version="0.0.2",
    author="Shrikant Thombre",
    author_email="shri1900@gmail.com",
    description="A csv logging package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shri1900/cpplibrary.git",
    packages=setuptools.find_packages(),
    install_requires=[''],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
