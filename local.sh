#!/bin/sh

# google component
gcloud components install beta
gcloud components update

# python env
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install --upgrade -r requirements.txt
# pip install --upgrade google-cloud-storage
# pip install --upgrade pytest

# deploy
# gcloud functions deploy graphqlwfs --runtime python37 --trigger-http

# save packages
# pip freeze > requirements.txt

export FLASK_APP=graphqlwfs
export FLASK_ENV=development
flask run
