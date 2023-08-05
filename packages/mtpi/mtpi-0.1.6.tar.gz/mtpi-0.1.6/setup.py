from setuptools import setup, find_packages
setup(
    author="Patrick Toohey",
    description="A collection of utilities for data analysis.",
    name="mtpi",
    version="0.1.6",
    packages=find_packages(include=["mtpi","mtpi.*"]),
    install_requires=['pandas', 'matplotlib'],
    python_requires='>=3.7',
)