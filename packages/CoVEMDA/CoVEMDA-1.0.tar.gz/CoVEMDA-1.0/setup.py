from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="CoVEMDA", 
    version='1.0',
    author="Guangchun Ruan",
    author_email="rgcthu@163.com",
    description='CoronaVirus - Electricity Market Data Analyzer (CoVEMDA)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/tamu-engineering-research/COVID-EMDA',
    classifiers= [
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License ",
    ],
    keywords="COVID-19, extreme event, impact assessment, power system operation, power system resilience, cross-domain analysis",
    package_dir={"": "lib"},
    packages=find_packages(where="lib"),
    python_requires=">=3.5",
    install_requires=[
        "pandas >= 1.2.4",
        "scipy >= 1.6.2",
        "statsmodels >= 0.12.2",
        "scikit-learn >= 0.24.1",
        "matplotlib >= 3.3.4",
    ]    
)

