# Loyola-Project
## terminal commands to runserver

- python venv venv
- venv/Scripts/activate

- pip install django
- python.exe -m pip install -U pip

- pip install mysqlclient

## for database:
- py manage.py makemigrations
- py manage.py migrate

## to run server:
- py manage.py runserver

## to make account
- py manage.py createsuperuser

## mySQL:
- create database LoyolaDB;
- use LoyolaDB;

- SELECT * FROM auth_user;
- SELECT * FROM users_userrole;
- select * from loyolasystem_vibercontact;
- select * from loyolasystem_announcement;

- insert into users_roles (role_desc) values ('Admin'), ('Regular');

- insert into users_userrole (role_id, user_id) values (1, 3), (1,5);

- insert into loyolasystem_emaillevel (level_desc) values ('National'),('Regional'),('Global'),('Local');

- insert into loyolasystem_emailtype (type_desc) values ('Submission'),('Announcement'),('Reminders');

