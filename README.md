# django-rest-test
A technical test

| Verb | Endpoint | Description | Request Body | Response |
| --- | --- | --- | --- | --- |
| GET | api/v1/balance/ | Consults the account balance. Need authentication. | None | 200 OK, response data: {"balance": float}  / 401 UNAUTHORIZED for Authentication credentials not provided |
| POST | api/v1/create_account/ | Creates a bank account. | {"username": string, "first_name": string, "last_name": string, "email": string, "password": string} | 201 CREATED, response data: {"date_created": timestamp, "is_active": boolean, "balance": float, "username": string, "first_name": string, "last_name": string, "email": string} / 400 BAD REQUEST for invalid request data |
| PUT | api/v1/deposit/{username}/ | Make a deposit to a bank account. | {"amount": float} | 202 ACCEPTED, response data: {"balance": float} / 406 NOT ACCEPTABLE for deposit that exceeds maximum balance / 404 NOT FOUND for account not found / 400 BAD REQUEST  for invalid request data |
| PUT | api/v1/withdrawal/ | Withdraw money from the bank account. | {"amount": float} | 202 ACCEPTED, response data: {"balance": float} / 406 NOT ACCEPTABLE for withdrawing more money than available in balance / 400 BAD REQUEST for invalid request data |
| POST | api/v1/token/ | Takes a set of user credentials and returns an access and refresh JSON web token pair to prove the authentication of those credentials. | { "username": string, "password": string } | 202 ACCEPTED {"balance": float } / 406 NOT ACCEPTABLE / 400 BAD REQUEST |
| POST | api/v1/token/refresh/ | Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid. | { "refresh": string } | 202 ACCEPTED {"balance": float } / 406 NOT ACCEPTABLE / 400 BAD REQUEST |
