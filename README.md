# Home task 12 (Django "order food online app")

## 1: Initial Setup

#### Clone project in a new directory:
```bash
cd path/to/a/new/directory
git clone https://github.com/MaksNech/pylab2018_ht_12.git
```
## 2: Install PostgreSQL:
```bash
sudo apt-get update

sudo apt-get install postgresql
```
#### Or follow the installation instructions for PostgreSQL from the official website:
https://www.postgresql.org/download

#### Check installation:
```bash
sudo -u postgres psql
```
#### Create app database:
```bash
CREATE DATABASE order_food_db;
```

#### Or exit from postgres command line and create db with linux command:
```bash
\q

sudo -u postgres createdb order_food_db
```

#### Enter to the database:
```bash
sudo -u postgres psql -d order_food_db
```

#### Create user of the db from postgres command line:
```bash
CREATE USER admin WITH PASSWORD '123';

\q
```
#### Go to the postgres command line and do some customization:
```bash
sudo -u postgres psql

ALTER ROLE admin SET client_encoding TO 'utf8';

ALTER ROLE admin SET default_transaction_isolation TO 'read committed';

ALTER ROLE admin SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE order_food_db TO admin;

\q
```

## 3: Getting Started

### Start backend:
#### Inside project create virtual environment:
```bash
virtualenv -p python3 env
```
#### Then start virtual environment:
```bash
source env/bin/activate
```
#### Install packages using pip according to the requirements.txt file:
```bash
pip install -r requirements.txt
```
#### Inside the project directory migrate the database:
```bash
python manage.py makemigrations

python manage.py migrate
```
#### Inside the project directory set the initial data with fixtures:
```bash
python manage.py loaddata sections.json

python manage.py loaddata ingredients.json

python manage.py loaddata dishes.json
```
#### Inside the project directory create an administrative account by typing:
```bash
python manage.py createsuperuser
```
###### Username: admin
###### Email address: admin@mail.com
###### Password: 123

#### Inside the project directory run app with terminal command:
```bash
python manage.py runserver
```
