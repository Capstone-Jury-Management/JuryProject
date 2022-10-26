#!/bin/bash

pip install -r requirements.txt
cd db
python init_db.py
cd ..
flask --app server run
