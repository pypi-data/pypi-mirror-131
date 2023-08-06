import setuptools
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="vracer",
    version="0.2.2",
    license="apache-2.0",
    author="Kiran R",
    author_email="kiranr8k@gmail.com",
    description="creates a json data file after debugging the code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ki6an/vracer",
    project_urls={
        "Repo": "https://github.com/Ki6an/vracer",
        "Bug Tracker": "https://github.com/Ki6an/vracer/issues",
    },
    keywords=["debug", "python", "create_debug_json"],
    packages=setuptools.find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "six",
        "cheap_repr>=0.4.0",
        "executing",
        "asttokens",
        "pygments",
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
