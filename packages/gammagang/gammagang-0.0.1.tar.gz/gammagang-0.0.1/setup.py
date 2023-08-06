import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gammagang",                     
    version="0.0.1",                        
    author="Ryan Watts",                     
    description="GammaGang Test Package for SQLShack Demo",
    long_description=long_description,      
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      
    python_requires='>=3.6',                
    py_modules=["gammagang"],             
    package_dir={'':'gammagang'},     
    install_requires=["pandas","boto3","os","datetime"]                     
)