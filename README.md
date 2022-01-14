# django-rest-test
A technical test

## Code styling and linting

In order to be consistent with code style and formatting `pre-commit` was installed with 4 different hooks to help with code formatting and vulnerability checks.

| Package | Description |
| --- | --- |
| black | A PEP 8 compliant opinionated formatter |
| isort | A tool to sort imports alphabetically, and automatically separated into sections and by type |
| flake8 | A linter tool to perform analysis of source code |
| bandit | A tool designed to find common security issues in Python code |

It was chosen not to install `flake-annotations`, used to assure type hints are being properly defined, because the code is very simple and the view parameters are all the same (only the request parameter).

## Installation
In order to install locally for development purposes
```
make install
export DJANGO_DEVELOPMENT=True
python manage.py migrate
```

## Testing
```
export DJANGO_DEVELOPMENT=True
python manage.py test
```

## API documentation
A documentation generated through `coreapi` can also be viewed in `api/docs/`.

| Verb | Endpoint | Description | Request Body | Response |
| --- | --- | --- | --- | --- |
| GET | api/v1/balance/ | Consults the account balance. Need authentication. | None | 200 OK, response data: {"balance": float}  / 401 UNAUTHORIZED for Authentication credentials not provided |
| POST | api/v1/create_account/ | Creates a bank account. | {"username": string, "first_name": string, "last_name": string, "email": string, "password": string} | 201 CREATED, response data: {"date_created": timestamp, "is_active": boolean, "balance": float, "username": string, "first_name": string, "last_name": string, "email": string} / 400 BAD REQUEST for invalid request data |
| PUT | api/v1/deposit/{username}/ | Make a deposit to a bank account. | {"amount": float} | 202 ACCEPTED, response data: {"balance": float} / 406 NOT ACCEPTABLE for deposit that exceeds maximum balance / 404 NOT FOUND for account not found / 400 BAD REQUEST  for invalid request data |
| PUT | api/v1/withdrawal/ | Withdraw money from the bank account. | {"amount": float} | 202 ACCEPTED, response data: {"balance": float} / 406 NOT ACCEPTABLE for withdrawing more money than available in balance / 400 BAD REQUEST for invalid request data |
| POST | api/v1/token/ | Takes a set of user credentials and returns an access and refresh JSON web token pair to prove the authentication of those credentials. | { "username": string, "password": string } | 200 OK, response data: {"refresh": string, "access": string} / 401 UNAUTHORIZED for incorrect login atempt / 400 BAD REQUEST for invalid request data|
| POST | api/v1/token/refresh/ | Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid. | {"refresh": string} | 200 OK, response data: {"access": string} / 401 UNAUTHORIZED for token invalid or expired / 400 BAD REQUEST for invalid request data |
