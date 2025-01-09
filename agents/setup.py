from setuptools import setup, find_packages

setup(
    name="scai_test",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pyautogen>=0.2.0",
        "openai>=1.0.0",
    ],
)