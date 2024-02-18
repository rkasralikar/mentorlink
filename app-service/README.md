


#Project Name
 
 Mentorlink 

 -----------------------------------------------------------------------------------------------------

 #Technology used

 Backend - Node.js,Express.js,Mongoose ORM

 Database - Mongodb

 Mobile Application - React Native

 ------------------------------------------------------------------------------------------------------

 # Installation Guide

 To install npm package - npm install or npm i

 To run the project - npm start

 -------------------------------------------------------------------------------------------------------
 # versioning tool

 git bitbucket for version controll

 jira for task tracking and project management

 -------------------------------------------------------------------------------------------------------

 # project architecture

 Microservice architecture to run every service individually

 Middleware - to maintian common middle service eg authentication

 config - maintains commmon configurations including database config and other thrid party configurations

 lib - maintains common global functionalities

 local\en - contains global common messages

 controller - provides http routes to the services

 service - maintains database queries to the database

 model - maintains database document schema and mongoose functions (pre default)

  -------------------------------------------------------------------------------------------------------

 # project deployment 
  
  development Instance : https://<>

  Jenkins Project : appservice

  The deployment will be done automatically if their is any code changes into master baranch (piple line is enabled on Master only)
  
  ELB Application : appservice-dev
  
  ELB Environment : Appservicedev-env

  Jenkins to AWS steps :
    
    1. Jenkins will downloads lastet code from bitbucket.
    2. It will execute the test cases.
    3. If test cases fails it will stops deployment.
    4. If test cases are passed then it will create a zip from source code and upload it on S3.
    5. Once a code is uploaded on S3 we executed a commmand code using aws to start ELB deployment.
    6. Once a deployment is done on ELB we will update the ELB lable. 
