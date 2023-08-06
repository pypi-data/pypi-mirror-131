from pathlib import Path

from setuptools import find_packages
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='cbaxter1988_utils',
    version='0.3.3',
    url='https://github.com/cbaxter1988/utils.git',
    description='A Package containing my utils',
    author='Courtney S Baxter Jr',
    author_email='cbaxtertech@gmail.com',
    packages=find_packages(),
    install_requires=required,
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True
)
