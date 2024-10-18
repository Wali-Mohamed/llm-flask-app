#!/bin/sh

# Run the database preparation script
python db_prep.py

# After db_prep.py finishes, start the Flask application
python local_app.py
