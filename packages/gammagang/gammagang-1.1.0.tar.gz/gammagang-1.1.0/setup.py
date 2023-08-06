import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gammagang",                     
    version="1.1.0",                        
    author="Ryan Watts",                     
    description="GammaGang Package for distribution",
    long_description=long_description,      
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      
    python_requires='>=3',                
    py_modules=["gammagang"],             
    package_dir={'':'gammagang'},     
    install_requires=["pandas==1.1.3","boto3"]                     
)