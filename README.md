# Planner API
    - python 3.6.8
    - flask-rest-jsonapi
    - postgresql-contrib


## Setup instructions:
1. create a python3.6 virtualenv (https://github.com/pyenv/pyenv-virtualenv recommended)
2. install requirements.txt, requirements_dev.txt and requirements_tools.txt: `pip install -r requirements.txt -r requirements_dev.txt -r requirements_tools.txt`
3. Install postgresql locally. On Ubuntu, this would be: `sudo apt install postgresql postgresql-contrib`. 
   Running postgresql locally without switching users: `sudo -u postgres psql`.
4. If your postgres is running on a port other than the default one (5432) please run the app using
the env variable `PLANNER_API_DEV_DB_PORT`, assigning the desired port.
5. Create the development DBs using the following command:
`sudo -u postgres psql -f <your_user_path>/work-planner-api/create_dev_dbs.sql`
6. If no revision exists, run the migration script: `python manage.py db migrate -m "Initial revision"`. 
Otherwise, run the upgrade script: `python manage.py db upgrade`
7. Run `setup_for_dev.py` if you wish to input some basic test data.
8. Run app through either Docker (if you wish to set that up) or through: `FLASK_ENV=development python manage.py run`

## CLI commands:
A set of CLI commands has been provided to help populate the database. These can be found through the `python manage.py --help` command.
Please do be mindful that the CLI commands do not utilize the API logic because the data is inserted directly into the DB. This means that any filtering or formatting provided by the API cannot be applied to CLI data.

## Updating project dependencies:
The requirements are managed with pip-tools, 
in order to pin down their versions.
1. To add a new dependency used in production:
    
    1.1 edit requirements.in and add your dependency
    
    1.2 generate a new requirements.txt file by running: `pip-compile --output-file requirements.txt requirements.in` 
2. To add a new dependency used in development:
    
    2.1 edit requirements_dev.in and add your dependency
    
    2.2 generate a new requirements_dev.txt file by running: `pip-compile --output-file requirements_dev.txt requirements_dev.in`
