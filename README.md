# TaskApp

Application for creating thumbnails based on arbitrary created plans connected with users.

## Prerequisites
* docker compose

## Setup
Clone git repository
```
git clone https://github.com/Scource/TaskApp
cd TaskApp
```

#### Docker setup

- From root application folder run `docker compose up`
- Application should be up and running at `http://localhost:8000`

#### PostgresDB setup

- Migrate tables to new DB
  `docker-compose exec backend python manage.py migrate`

- Create first user in new DB
  `docker-compose exec backend python manage.py createsuperuser`
  
## First Data Configuration
At first database is empty and all data must be provided by User:
- Log in to django-admin `http://localhost:8000/admin`
- In `Thumbnail sizes` table create object and set width and height
- In `Plans` table create new object and connect Plan with Thumbnail size -  it's possible to add multiple sizes to the same plan
- Check `Get origial` and `Get expiring link` if user should have acces to originally posted files and time expiring links
- In `User details` connect User with Plan

Now application is ready to upload files and data will be presented according to Plan connected with User in request.
