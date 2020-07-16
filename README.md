# djmanga

## Hobby Project - Manga Reader with Python Django
This is a hobby project so that I can learn Python and Django. It is currently useful enough for me to host in a docker container and access my Manga collection from different devices at home. Organization features have been implemented, such as books with chapters, authors, illustrators, and tags. Tags can have parent and be grouped in a tree structure. Manga can be scanned if they are organized into folders.

## Basic Steps To Get Started
1. Make sure Docker and Docker Compose is installed on your machine.
2. Rename docker-compose.yml.sample to docker-compose.yml
    1. Set POSTGRES_DB, POSTGRES_USER, and POSTGRES_PASSWORD in docker-compose.yml
    2. OPTIONAL - set a volume to point your manga folder to /www/media/manga. This is where the app will scan for new manga.
3. Rename .env.sample to .env in www/djmanga/
3. Rename settings.py.sample to settings.py in www/djmanga/
    1. Set security key and database in settings.py
4. Run docker-compose up
