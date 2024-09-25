# Cesium Backend Project

This code ll 
    1- make 3d project in webODM , 
    2- ll save its .zip file in s3 bucket.
    3- ll make a 3D streaming model in cesium and return its ID to use at fronend 

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)


## Installation
    1- CLone repository  https://github.com/ahsanjaved2u/cesium.git
    2- pip install -r requirements.txt

## usage
    1- Run pyton main.py.  it ll run to your local host 500
    2- From postman make a POST request to http://localhost:5000/upload 
    3- in body 
        user_name  //webODM username
        password  //webODM password
        project_name // name of cesium project 
        description  // description of project
        images   //minimum five images required

    3- in .env you need to have
        AWS_ACCESS_KEY_ID
        aws_secret_access_key
        cesium_access_token

