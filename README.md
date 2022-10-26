# INE-challenge
Author: Hugo Chavero


### Pre requisites (installed on your local environment)
* Docker
* docker-compose

### Build and Run application
If this is your first time running the application, you have to:
* create your local env file
```
cp .env.dev .env
```
* Set your staff user vars (into .env)
```
set INITIAL_STAFF_USERNAME=staffuser
set INITIAL_STAFF_EMAIL=staffuser@email.com
set INITIAL_STAFF_PASSWORD=***********
```
> Staff password must include lowercase and upercase letters, digits and symbols. At least 8 chars

* To build and run, run:
```
docker-compose up
```
* Open the app on `http://127.0.0.1:8000/`


### Run tests
```
docker-compose run web --rm web pytest
```

### Run tests with coverage
```
docker-compose run web --rm web pytest --cov
```


## Authentication

To authenticate with our API's, you have to generate an Access Token

### Get user Access Token
```
curl --location --request POST '127.0.0.1:8000/api/token/' \
--form 'username="yourstaffuser"' \
--form 'password="**********"'
```
#### Authentication Header
Each requests to Users API's must send this header
> Authorization: Bearer <your_access_token>


 ## Internal Authentication

If internal authentication is needed, you will have to generate an API Key from Django Admin interface (though API KEY PERMISSION section).
For more information go to official [documentation.](https://florimondmanca.github.io/djangorestframework-api-key/guide/#creating-and-managing-api-keys)

This is kind of token is useful when you need to authorize request from other internal systems.

#### Internal Authentication Header
Each requests to Users API's must send this header
> Authorization: Api-Key <service_api_key>
