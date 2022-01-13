# django-rest-test
A technical test

| Verb | Endpoint | Description | Request Body | Response |
| --- | --- | --- | --- | --- |
| GET | api/v1/balance/ | Consults the account balance. Need authentication. | None | 200 OK {"balance": float } |
| POST | api/v1/create_account/ | Creates a bank account. | { "username": string } | 201 CREATED {"balance": float } / 400 BAD REQUEST |
| PUT | api/v1/deposit/{username}/ | Make a deposit to a bank account. | { "amount": float } | 202 ACCEPTED {"balance": float } / 406 NOT ACCEPTABLE / 404 NOT FOUND / 400 BAD REQUEST |
| PUT | api/v1/withdrawal/ | Withdraw money from the bank account. | { "amount": float } | 202 ACCEPTED {"balance": float } / 406 NOT ACCEPTABLE / 400 BAD REQUEST |
| POST | api/v1/token/ | Takes a set of user credentials and returns an access and refresh JSON web token pair to prove the authentication of those credentials. | { "username": string, "password": string } | 202 ACCEPTED {"balance": float } / 406 NOT ACCEPTABLE / 400 BAD REQUEST |
| POST | api/v1/token/refresh/ | Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid. | { "refresh": string } | 202 ACCEPTED {"balance": float } / 406 NOT ACCEPTABLE / 400 BAD REQUEST |
