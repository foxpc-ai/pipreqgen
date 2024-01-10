from setuptools import setup, find_packages
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='pipreqgen',
    version='0.0.1',
    author='Muktadir',
    description='Generates requirement.txt',  
    long_description=long_description,
    long_description_content_type='text/markdown',  
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pipreqgen=pipreqgen.extract_imports:main',
        ],
    },
    install_requires=[
        # none
    ],
)
