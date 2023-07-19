from setuptools import setup, find_packages

setup(
    name = "website_similarty_analyzer",
    version="0.1.1",
    author="Munj B Patel",
    author_email="patelmunj2011@gmail.com",
    description="A simple package which can be used for calculating the amount of similarity between given string to the content on different websites.",
    packages=find_packages(),
    install_requires=[
    "beautifulsoup4",
    "colorlog",
    "fake_useragent",
    "fuzzywuzzy",
    "my_fake_useragent",
    "requests",
    "python-Levenshtein"
    ],
    classifiers=[
        "Programming Language::Python"
        ],
    entry_points = {
        'pytest11':[
            'tox_tested_package = tox_tested_package.fixtures'
        ]
    }
)