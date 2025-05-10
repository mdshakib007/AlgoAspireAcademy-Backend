#!/bin/bash
# build_files.sh

# 1. Install Python dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py makemigrations --no-input --clear
python manage.py migrate --no-input --clear

# 3. Collect static files
python manage.py collectstatic --no-input --clear
