# PC BUILDER
PC BUILDER is a web-app, empowered by Flask, MongoDB, Jquery and Docker, that allows user
to make pc builds, view single parts cost and save builds to their account (Google Authentication).

This project has been made for the university course of TECWEB (Web Technologies)

## How to run the app
- Register you application as client to Google here https://console.cloud.google.com/apis/credentials
- Make a copy of `config.yml.example` into the `app/` directory, open the file and insert your client id and client secret
- Edit `secret:` inside `config.yml` and insert a random string
- Inside `config.yml`, insert a connection string to a MongoDB database 
- Generate a self signed certificate with `openssl req -x509 -nodes -days 3650 -newkey ec:<(openssl ecparam -name prime256v1) -keyout private_key.pem -out certificate.pem` and copy them inside `app/`
- Install `virtualenv` with `pip install virtualenv`
- Create a virtual env and install requirements with `pip install -r app/requirements.txt`
- Execute the script `app/run.sh` (if you're on linux)
- Go to https://localhost:8000 and your app should be on