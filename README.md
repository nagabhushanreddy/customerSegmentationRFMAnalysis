# Bank Customer RFM Analysis

## About 

This project is a prototype of Dataanlytics for performing RFM analysis on bank transactions and combining customer deomgraphics to derive business insights.

## Environment

- Developer IDE
- Anaconda 
- Python 

## Developer IDE

Visual Studio code is used as developer IDE and it comes with huge plugin ecosystem to work with various programming languages (is a personal choice for Python programming). A few to mention that are helpful in this solution context. 

- Python
- Python Extension Pack 
- Python Environment Manager 
- Jupyter 
- Intelli Code etc.

## Install Anaconda

1. Anaconda is a popular distribution of the Python programming language that provides a comprehensive ecosystem for data science, machine learning, and scientific computing, including a powerful package manager and extensive libraries.

2. Anaconda simplifies the process of setting up and managing Python environments, making it easier to work with different Python versions, manage dependencies, and create reproducible data analytics solutions, making it a preferred choice for many Python developers and data scientists.


[Download-Link](https://www.anaconda.com/products/distribution) 

## Check if installation is successful 

### From Terminal run below command 

```commandline
(base) naga@MAC011 ~ % conda -V
conda 22.11.1
(base) naga@MAC011 ~ %
```

## Install required libraries

Below also installs required python version and creates a python environment named `CustomerSegmentation` 

```commandline
cd <<project-home-director>>
```

```commandline
conda env create -f environment.yml
```

Switch to python environment `TransactionClassification`  

```commandline
conda activate CustomerSegmentation
```

## Steps to run or use proto-type solution for customer segmentation with RFM

- Configuration
- Usage
- Helper tools

### Configuration 

Configuration is placed in file ./conf/app.ini and follow .ini file syntax with various sections. 

### Usage 


### Helper tools


## Disclaimer 

This project is an open-source/prototype initiative, and as such, it comes with no warranty or guarantee of any kind. The authors and contributors of this project cannot be held liable for any damages or losses arising from the use or inability to use this software. All users of this project do so at their own risk, and they are responsible for ensuring that they comply with all relevant laws and regulations. The authors and contributors do not provide any gurantee on the project. If in cases of any issues you can reach to contributors/authors and at contributors/authors discretion to help or fix the issue. You reach to wider community help too. By using this project, you agree to these terms and conditions.