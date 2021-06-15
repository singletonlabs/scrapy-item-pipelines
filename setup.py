import os
import re

from setuptools import find_packages, setup


def get_version():
    with open(os.path.join("scrapy_item_pipelines", "__init__.py")) as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)


with open("README.md") as readme_file:
    README = readme_file.read()

install_requires = [
    "confluent-kafka",
]

setup_args = dict(
    name="scrapy-item-pipelines",
    version=get_version(),
    description="Various Scrapy item pipelines",
    long_description_content_type="text/markdown",
    long_description=README,
    license="MIT",
    packages=find_packages(),
    author="Kasun Herath",
    author_email="kasunh01@gmail.com",
    keywords=["scrapy", "pipelines"],
    url="https://github.com/singletonlabs/scrapy-item-pipelines",
    install_requires=install_requires,
    classifiers=[
        "Framework :: Scrapy",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)


if __name__ == "__main__":
    setup(**setup_args)
