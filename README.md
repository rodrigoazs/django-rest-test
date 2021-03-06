# django-rest-test

Django-test-test is an API for a bank system developed with **Django/REST Framework** that provides 4 different basic operations:

* Creating an account
* Checking balance of an account
* Deposit money to an account
* Withdraw money from an account.

In order to authorize users operations a JSON Web Token has to be generated and refreshed constantly.

## Comments

The code I wrote are in the folder `api`, those are the files `models.py`, `views.py`, `serializers.py`, `tests.py` and `url.py`. Other files were basically generated by Django. All the code and modifications I have made can be seen through [PR 1](https://github.com/rodrigoazs/django-rest-test/pull/1) and [PR 3](https://github.com/rodrigoazs/django-rest-test/pull/3).

The testing environment can be seen in [Heroku Django-rest-test](https://django-rest-test-rodrigo.herokuapp.com/api/docs/). Heroku is set to automatically deploy from GitHub considering the `main` branch. In production, the database used is PostgreSQL. Testing isntructions are provided in the end of this README file.

Django/REST framework was chosen due to the type of the testing task (backend). I have worked with Django two years ago but REST framework was my first time. Currently, I work with Flask/Fast API in order to provide APIs for the machine learning models. Django provides me a much easier framework for what the testing task requires.

The testing task is not clear about if it is possible to withdraw from any account or if the user/account should be logged in. Then, I've chosen to proceed with with an authorization method that will allow people to withdraw/balance only for their own account. The operation of deposit is able for everyone that wants to deposit in any account. The type of autorhization used is [JSON Web Token Authentication](https://jpadilla.github.io/django-rest-framework-jwt/).

In addition, testing task does not mention if transactions must be pending and then authorized, then all deposits and withdrawals are instantly made to the account balance.

## Code styling and linting

In order to be consistent with code style and formatting `pre-commit` was installed with 4 different hooks to help with code formatting and vulnerability checks.

| Package | Description |
| --- | --- |
| black | A PEP 8 compliant opinionated formatter |
| isort | A tool to sort imports alphabetically, and automatically separated into sections and by type |
| flake8 | A linter tool to perform analysis of source code |
| bandit | A tool designed to find common security issues in Python code |

> It was chosen not to install `flake-annotations`, used to assure type hints are being properly defined, because the code is very simple and the view parameters are all the same (only the request parameter).

## Installation
In order to install locally for development purposes it is necessary to have Python 3.8 and pip installed. Then, run the following code:

```
make install
export DJANGO_DEVELOPMENT=True
python manage.py migrate
```

The `make install` will install pre-commit and the libraries presented in the `requirements.txt`. The enviroment variable `DJANGO_DEVELOPMENT` will make sure we are running considering SQLite as the database and Debug also set as True. Migrate will then apply the migrations to the database.

> It was chosen not to proceed with Docker solution because it would be too much for simpling running Django and Postgresql images, and in order to make sure it also runs without Docker the tester would need to have a Postgresql instance installed. Then it was chosen to uses SQLite when running the web server on development mode. 

## Run locally

In order to run locally, run the following command:

```
python manage.y runserver 0.0.0.0:8080
```

And you will be able to access the endpoint `http://localhost:8080/api/v1/` locally.

Make sure `DJANGO_DEVELOPMENT` environment variable is set as True.

## Testing

In order assert endpoints and models are working properly a bunch of automated tests were designed to be checked. This can be done with Django through the following command:

```
python manage.py test
```

Make sure `DJANGO_DEVELOPMENT` environment variable is set as True.

## API documentation
A documentation generated through `coreapi` can also be viewed in the endpoint `api/docs/`.

| Verb | Endpoint | Description | Request Body | Response |
| --- | --- | --- | --- | --- |
| GET | api/v1/balance/ | Consults the account balance. Need authentication. | None | 200 OK, response data: {"balance": float}  / 401 UNAUTHORIZED for Authentication credentials not provided |
| POST | api/v1/create_account/ | Creates a bank account. | {"username": string, "first_name": string, "last_name": string, "email": string, "password": string} | 201 CREATED, response data: {"date_created": timestamp, "is_active": boolean, "balance": float, "username": string, "first_name": string, "last_name": string, "email": string} / 406 NOT ACCEPTABLE for existing username / 400 BAD REQUEST for invalid request data |
| PUT | api/v1/deposit/{username}/ | Make a deposit to a bank account. | {"amount": float} | 202 ACCEPTED, response data: {"balance": float} / 406 NOT ACCEPTABLE for deposit that exceeds maximum balance / 404 NOT FOUND for account not found / 400 BAD REQUEST  for invalid request data |
| PUT | api/v1/withdrawal/ | Withdraw money from the bank account. | {"amount": float} | 202 ACCEPTED, response data: {"balance": float} / 406 NOT ACCEPTABLE for withdrawing more money than available in balance / 400 BAD REQUEST for invalid request data |
| POST | api/v1/token/ | Takes a set of user credentials and returns an access and refresh JSON web token pair to prove the authentication of those credentials. | { "username": string, "password": string } | 200 OK, response data: {"refresh": string, "access": string} / 401 UNAUTHORIZED for incorrect login atempt / 400 BAD REQUEST for invalid request data|
| POST | api/v1/token/refresh/ | Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid. | {"refresh": string} | 200 OK, response data: {"access": string} / 401 UNAUTHORIZED for token invalid or expired / 400 BAD REQUEST for invalid request data |

## Testing requests manually

In order to test the API manually we can perform requests locally to `http://localhost:8080/api/v1/` or in production to `http://django-rest-test-rodrigo.herokuapp.com/api/v1/`.

I recommend the use of [HTTPie](https://httpie.io/) as testing client. It can be install through `pip install httpie`.

### Creating an account

```
http post http://django-rest-test-rodrigo.herokuapp.com/api/v1/create_account/ username=test first_name=Test last_name=Test email=test@test.com password=test
```

A new account will be created if the request is ok and it is a new user account.

### Requesting token

```
http post http://django-rest-test-rodrigo.herokuapp.com/api/v1/token/ username=test password=test
```

A response data containing `access token` and `refresh token` will be sent. Collect the `access token` in order to be authorized to request withdrawal and check balance.

### Refreshing token

If the access token expires you need to refresh it. In order to do that make a request sending the `refresh token`.

```
http post http://django-rest-test-rodrigo.herokuapp.com/api/v1/token/refresh/ refresh={refresh token}
```

You will receive a new `access token`.

### Checking balance

```
http get http://django-rest-test-rodrigo.herokuapp.com/api/v1/balance/ "Authorization: Bearer {access token}"
```

You will check the balance of the authorized account considering the token provided.

### Making a deposit

```
http put http://django-rest-test-rodrigo.herokuapp.com/api/v1/deposit/{username}/ amount=10.0
```

You will make a deposit of 10.0 to an account considering the username provided as the parameter.

### Making a withdrawal

```
http put http://django-rest-test-rodrigo.herokuapp.com/api/v1/withdrawal/ "Authorization: Bearer {access token}" amount=10.0
```

You will make a withdrawal of 10.0 from the authorized account considering the token provided.
