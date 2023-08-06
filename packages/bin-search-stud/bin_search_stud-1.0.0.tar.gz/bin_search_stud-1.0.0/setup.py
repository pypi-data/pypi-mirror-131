from setuptools import setup
from setuptools import find_packages


setup(
    name="bin_search_stud",
    version="1.0.0",
    description="Это пакет для реализации бинарного поиска",
    author="Болдырев Владимир",
    author_email="vladimir.boldyrev.2003@mail.ru",
    packages=find_packages(exclude=('package.tests*',)),
)
