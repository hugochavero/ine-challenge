# INE-challenge
Author: Hugo Chavero


### Pre requisites
* Docker
* docker-compose

### Run application
* Build and run on `http://127.0.0.1:8000/`
> docker-compose up

### Run tests
> docker-compose run web --rm web pytest

### Run tests with coverage
> docker-compose run web --rm web pytest --cov


## Authentication

When INE challenge runs for first time, a Staff User is created according this environment vars:

>INITIAL_STAFF_USERNAME=inestaff
>INITIAL_STAFF_EMAIL=email@domain.com
>INITIAL_STAFF_PASSWORD=*******

With this Staff User, you will be able to get an Access Token, wich you'll use to authenticate in Users API's.

#### Authentication Header
Each requests to Users API's must send this header
> Authorization: Bearer <your_access_token>

### Get user Access Token
```
curl --location --request POST '127.0.0.1:8000/api/token/' \
--form 'username="inestaff"' \
--form 'password="**********"'
```
 ## Internal Authentication

If internal authentication is needed, you will have to generate an API Key from Django Admin interface (though API KEY PERMISSION section).

This is kind of token is usefull when you need to autorize request from other internal systems.

#### Internal Authentication Header
Each requests to Users API's must send this header
> Authorization: Api-Key <service_api_key>
