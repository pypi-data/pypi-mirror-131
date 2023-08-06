# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.12.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
from setuptools import setup, find_packages

setup(
    name='realestatedata533',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description="A package that helps to find various properties of two types of real-estate properties (Apartments and Family Homes) and display all the relevant information.",
    url='https://github.com/navdeep94/DATA533-Lab4',
    author='Mehul, Navdeep & Andrew',
    author_email='emailrandom@gmail.com'
)
# -


