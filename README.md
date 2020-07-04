# djmanga

## Hobby Project - Manga Reader with Python Django
This is a hobby project so that I can learn Python and Django. Maybe eventually it will be useful enough for me to host in a docker container and access my Manga collection from different devices at home. It is currently very early stage and does not even have its basic features yet.

## Basic Steps To Get Started
1. Rename docker-compose.yml.sample to docker-compose.yml
    1. Set POSTGRES_DB, POSTGRES_USER, and POSTGRES_PASSWORD in docker-compose.yml
    2. OPTIONAL - set a volume to point your manga folder to /www/media/manga
2. Rename settings.py.sample to settings.py in www/djmanga/
    1. Set security key and database in settings.py
3. Run docker-compose up
