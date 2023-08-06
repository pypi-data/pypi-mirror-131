import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gammagang",                     
    version="0.0.3",                        
    author="Ryan Watts",                     
    description="GammaGang Package for distribution",
    long_description=long_description,      
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      
    python_requires='>=2',                
    py_modules=["gammagang"],             
    package_dir={'':'gammagang'},     
    install_requires=["pandas","boto3","os","datetime"]                     
)