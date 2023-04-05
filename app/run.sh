#! /usr/bin/bash

gunicorn app:app --key private_key.pem --certfile certificate.pem -w 2 -b 0.0.0.0:8000
