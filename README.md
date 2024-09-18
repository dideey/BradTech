#This is the wajibika api aimed at promoting accountability and transparency in our leaders
## Project Structure

```
/ (root)
│
├── api/
│   └── wajibika/            # Django project folder
│
├── venv/                    # Virtual environment
├── requirements.txt         # Dependencies for the project
```


## Features

User Authentication: Users can register, log in, and log out.
JWT Token Authentication: Secure access to API endpoints.
Post Representatives: Users can add, edit, and update scandals about their representatives in representative boards.

## Installation
```bash
git clone <repository-url>
cd <repository-folder>
```

## Setting up the vitual environment

create virtual environment
```bash
python -m venv venv
```
**Activation on linux/mac**
```bash
source venv/bin/activate
```
## Install Dependancies
Use the requirements.txt file to install the necessary packages:
```bash
pip install -r requirements.txt
```
## Apply Migrations
Inside the api/wajibika folder, apply the database migrations:
```bash
python manage.py migrate
```
## Running development server
```bash
python manage.py runserver
```

## The depoloyed api
https://dideey.pythonanywhere.com/

#All API endpoints
```
Signup: /dideey.pythonanywhere.com/api/signup/
Login: /dideey.pythonanywhere.com/api/login/
Logout: /dideey.pythonanywhere.com/api/logout/
User Profile: /dideey.pythonanywhere.com/api/profile/
Countie: /dideey.pythonanywhere.com/api/counties/
Constituencies: /dideey.pythonanywhere.com/api/constituencies/
Wards: /dideey.pythonanywhere.com/api/wards/
Leaders: /dideey.pythonanywhere.com/api/leaders/
Search Leaders: /dideey.pythonanywhere.com/api/leaders/search/
Posts: /dideey.pythonanywhere.com/api/leaders/<leader_id>/posts/
Post-comments: /dideey.pythonanywhere.com/api/leaders/<leader_id>/posts/<post_id>/comments/
```
## The Revolution is Here
