# Restful APIs using flask

## Configuration to run

1. Install dependencies:
    ```sh
    pip install -r requirement.txt
    ```

2. Set environment variables:
    ```sh
    export FLASK_APP=backend2.py
    export FLASK_APP='development'
    ```

3. Initialise database:
    ```sh
    flask initdb
    ```

4. Run flask's development server
    ```sh
    flask run
    ```

## Testing
Use `flask test` to run tests.

## TODO:
- [ ] - Add tests for start, stop and restart  
- [ ] - Deploy on cloud for remote usage