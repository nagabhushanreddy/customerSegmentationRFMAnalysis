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

Below also installs required python version and creates a python environment named `customerSegmentation` 

```commandline
cd <<project-home-director>>
```

```commandline
conda env create -f environment.yml
```

Switch to python environment `customerSegmentation`  

```commandline
conda activate customerSegmentation
```

## Steps to run or use proto-type solution for customer segmentation with RFM

- Configuration
- Usage
- Helper tools

### Configuration 

Configuration is placed in file ./conf/app.ini and follow .ini file syntax with various sections. 

* Below are two important configurations and they should be intuitive to understand. 
* The output shall have additional fields adds like RFM score, Cohort-Index to cross validate and for plotting. 


```
[INPUT]
transaction_data=./data/input/SME_training_transaction_data.csv
customer_data=./data/input/customer_data.csv

[OUTPUT]
transaction_data=./data/output/customer_transaction_data.csv
customer_data=./data/output/customer_data.csv
```

Input data fields for each file as as shown below.

```
customer_data
    #   Column                         Non-Null Count  Dtype 
    ---  ------                         --------------  ----- 
    0   customerID                     2000 non-null   int64 
    1   customerName                   2000 non-null   object
    2   customerAge                    2000 non-null   int64 
    3   customerGender                 2000 non-null   object
    4   customerLocation               2000 non-null   object
    5   customerEducation              2000 non-null   object
    6   customerIndustry               2000 non-null   object
    7   customerAuthorizedSignatories  2000 non-null   object
 
transaction_data
    #   Column                Non-Null Count   Dtype         
    ---  ------                --------------   -----         
    0   transactionReference  143860 non-null  object        
    1   transactionDate       143860 non-null  datetime64[ns]
    2   payeeAccountNumber    143860 non-null  int64         
    3   payeeName             143860 non-null  object        
    4   payeeIndustry         0 non-null       float64       
    5   transactionCode       143860 non-null  object        
    6   amount                143860 non-null  float64       
    7   indicator             143860 non-null  object        
    8   transferNotes         116478 non-null  object        
    9   transactionCategory   143860 non-null  object        
    10  customerID            143860 non-null  int64      
 ```

### Usage 

The Customer segemetation tool can be run as a Jupyter notebook from IDE and more explaination is provided in notebook. Alternatively run the python script as below. 

```
python ./CustomerSegmentation.py

```


### Helper tools

1. Generating Training data

Run the script below for generating training data real quick, this is helpful for understanding the prototype and it is highly recommended to use actual data for evaluation and not data from this tool.

```
python ./trainingDataGenerator.py 
```

## Disclaimer 

This project is an open-source/prototype initiative, and as such, it comes with no warranty or guarantee of any kind. The authors and contributors of this project cannot be held liable for any damages or losses arising from the use or inability to use this software. All users of this project do so at their own risk, and they are responsible for ensuring that they comply with all relevant laws and regulations. The authors and contributors do not provide any gurantee on the project. If in cases of any issues you can reach to contributors/authors and at contributors/authors discretion to help or fix the issue. You reach to wider community help too. By using this project, you agree to these terms and conditions.