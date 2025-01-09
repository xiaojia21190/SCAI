from setuptools import setup, find_packages

setup(
    name="scai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyautogen>=0.2.0",
        "openai>=1.3.0",
        "elasticsearch>=8.0.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
        "PyPDF2>=3.0.0",
    ],
    author="SCAI Team",
    description="Scientific Conversational AI using autogen",
    python_requires=">=3.8",
)