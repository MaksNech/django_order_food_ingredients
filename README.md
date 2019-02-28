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
#### Attention! Be sure to run the commands in the order shown.
```bash
python manage.py loaddata groups.json

python manage.py loaddata sections.json

python manage.py loaddata ingredients.json

python manage.py loaddata dishes.json
```
#### Relocate all files from "order_food_online_project/data_migrations/authentication" folder to the
#### "order_food_online_project/authentication/migrations" folder and again run commands:
```bash
python manage.py makemigrations

python manage.py migrate
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

## 4: Celery:
### Running Locally:
#### Install Redis as a Celery “Broker” in your system, not in virtualenv:
```bash
wget http://download.redis.io/redis-stable.tar.gz

tar xvzf redis-stable.tar.gz

cd redis-stable

make
```
#### Check installation:
```bash
redis-server
```
##### With your Django App and Redis running, open two new terminal windows/tabs. 
##### In each new window, navigate to your project directory where "order_food_online" folder,
##### activate your virtualenv, and then run the following commands (one in each window):
```bash
celery -A order_food_online worker -l info

celery -A order_food_online beat -l info
```
### Running Remotely:
#### SSH into your remote server and run:
```bash
sudo apt-get install supervisor
```
##### We then need to tell Supervisor about our Celery workers by adding configuration files to
##### the “/etc/supervisor/conf.d/” directory on the remote server. In our case, we need two such configuration
##### files - one for the Celery worker and one for the Celery scheduler, now they located in
##### "order_food_online/supervisor" folder you nee to relocate them to “/etc/supervisor/conf.d/” directory on the
##### remote server. Make sure to update the paths in these files to match the remote server’s filesystem.

#### We also need to create the log files that are mentioned in the above scripts on the remote server:
```bash
touch /var/log/celery/order_food_online_worker.log

touch /var/log/celery/order_food_online_beat.log
```

#### Finally, run the following commands to make Supervisor aware of the programs:
```bash
sudo supervisorctl reread

sudo supervisorctl update
```

#### Run the following commands to stop, start, and/or check the status of the order_food_online_celery program::
```bash
$ sudo supervisorctl stop order_food_online_celery

$ sudo supervisorctl start order_food_online_celery

$ sudo supervisorctl status order_food_online_celery
```
