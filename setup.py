from setuptools import setup, find_packages

setup(
    name='pipgen',
    version='0.0.1',
    author = 'Muktadir',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'reqgen=reqgen.extract_imports:main',
        ],
    },
    install_requires=[
        # none
    ],
)
