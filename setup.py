from setuptools import setup, find_packages
from configparser import ConfigParser

version = "0.2"

long_description = "\n\n".join([open("README.md").read(), open("CHANGES.md").read()])


def parse_pipfile():
    """Reads package requirements from Pipfile."""
    cfg = ConfigParser()
    cfg.read("Pipfile")
    dev_packages = [p.strip('"') for p in cfg["dev-packages"]]
    relevant_packages = [
        p.strip('"') for p in cfg["packages"] if "nested-dataclasses" not in p
    ]
    return relevant_packages, dev_packages


# We use Pipenv. Please set requirements in Pipfile.
install_requirements, tests_requirements = parse_pipfile()


setup(
    name="nested-dataclasses",
    version=version,
    description="Implements decorator `nested` that adds a parent and children to a dataclass.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers=["Programming Language :: Python :: 3"],
    keywords=["nested-dataclasses"],
    author="Roel van den Berg",
    author_email="roel.vandenberg@kadaster.nl",
    url="https://github.com/PDOK/nested-dataclasses",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requirements,
    tests_require=tests_requirements,
)
