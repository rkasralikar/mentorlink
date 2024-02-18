# Sample Skeleton for Microservices Directory structure #

Please refer to this repository for the directory structure of your repository

### What is this repository for? ###

````
micro-service-skeleton/
├── README.md ==> [This will store the readme of the repo]
├── .gitignore ==> [Gitignore file for your uservice]
└── service-name ==> [Name of your service]
    ├── __init__.py
    ├── config   ==> [All the static config of uservice]
    ├── docs     ==> [Sphynx documentation]
    ├── notebooks ==> [Any Notebook developed]
    ├── requirements.txt ==> [Requirements and Dependencies for uservice]
    ├── src  ==> [Source code]
    │   ├── __init__.py
    │   ├── business-logic ==> [All business Logic will go here]
    │   │   └── __init__.py
    │   ├── datamodel ==> [All the schemas and datamodel]
    │   │   └── __init__.py
    │   └── server    ==> [Api server]
    │       └── __init__.py
    └── test   ==> [Unit tests will be residing here, pytest]
````




### Who do I talk to? ###

* Repo owners

# Mentorlink Instructions
---
## Install required packages
```
python -m pip install -r requirements.txt
```
