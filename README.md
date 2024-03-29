# Restful APIs using flask
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/72140ce1c46e08743315)
## Configuration to run locally

1. Install dependencies:
    ```sh
    pip install -r requirement.txt
    ```

2. Set environment variables:
    ```sh
    export FLASK_APP='backend2.py'
    export FLASK_APP='development'
    export DATABASE_URL="postgresql://<USER>:<PASSWORD>@localhost/backend2test"
    ```

3. Initialise database:  
    Database needs to be created before running the migration scripts. As postgres does not create a database if the database with given name doesn't exist.
    ```sh
    flask db init
    flask db migrate
    flask db upgrade
    ```
    As migrations are already part of the repository, there is no need for `flask db init` and `flask db migrate`.

4. Run flask's development server
    ```sh
    flask run
    ```

## Testing
Testing will require that the environment variable FLASK_APP=backend2.py is properly set. Testing will be done in an in-memory database, so no need to specify DATABASE_URL for that. Use `flask test` to run tests.

## TODO:
- [X] - Add tests for start, stop.
- [X] - Deploy on cloud for remote usage
- [ ] - Add API Documentation