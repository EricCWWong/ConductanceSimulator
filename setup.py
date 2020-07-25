from setuptools import setup, find_packages

setup(
    name="GSimulator",
    packages=find_packages(exclude=['*test']),
    version="0.1.1",
    author="Eric Wong",
    description='This package allows user to \
        simulate conductance of quantum wires',
    author_email='c.wing.wong.19@ucl.ac.uk',
    install_requires=['numpy', 'matplotlib', 'prettytable', 'qutip', 'tqdm'],
    entry_points={
        'console_scripts': [
            'gsimulator = GSimulator.command:process'
        ]}
)
