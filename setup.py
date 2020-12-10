import os
import re
from glob import glob

from setuptools import find_packages, setup

project_name = "mediamanager"


def get_version(*file_paths):
    """Retrieves the version from [your_package]/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


version = get_version("media_management_api", "__init__.py")


with open("README.md") as readme_file:
    readme = readme_file.read()

with open('media_management_api/requirements/base.txt') as f:
    requirements = list(f)

test_requirements = [
    "black",
    "flake8",
    "isort",
    "pytest",
    "pytest-django",
    "pytest-env",
]


setup(
    name=project_name,
    version=version,
    description="iiif manifests and image manager",
    long_description=readme,
    author="Harvard Academic Technology Group (ATG)",
    author_email="nmaekawa@g.harvard.edu",  # originally atg@fas.harvard.edu
    url="https://github.com/nmaekawa/" + project_name,
    packages=find_packages(exclude=["docs", "tests*"]),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords=project_name,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
    ],
    test_suite="tests",
    tests_require=test_requirements,
)
