from setuptools import setup, find_packages 


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.1'
DESCRIPTION = 'NBA data Scrapper for stats analysis'

# Setting up the package
setup(
    name = "fu-scrapper",
    version = VERSION,
    author = 'Fujyn',
    author_email = "fujyn.contact@gmail.com",
    url = 'https://github.com/Endy02/fu-scrapper',
    project_urls={
        "Bug Tracker": "https://github.com/Endy02/fu-scrapper/issues",
    },
    description = DESCRIPTION,
    long_description_content_type = 'text/markdown',
    long_description=long_description,
    install_requires = ['pandas','numpy','requests','joblib'],
    python_requires = '>=3.7',
    keywords = ['python','sports','data-analysis','csv'],
    classifiers = [
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
)