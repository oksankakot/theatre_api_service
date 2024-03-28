# Theatre API Service

Theatre API Service is an API for managing theatre plays, theatre halls and
reservation tickets for performances.

## Features
* Play Management
* Performance scheduling
* Reservation system
* Admin panel and User authentication
* Pagination
* Docker support
* Swagger API documentation

## Installation
1. Clone the repository
```
https://github.com/oksankakot/theatre_api_service
```

2. Navigate to the project directory, create virtual environment and install all requirements
```
cd theatre-api-service
python -m venv venv
venv\Scripts\activate
source venv/bin/activate
pip install -r requirements.txt
```
3. Make migrations
```
python manage.py makemigrations
python manage.py migrate
```

4. Create an .env file and define the environment variables using .env.sample
5. Build Docker container
```
docker-compose build
```

6. Start the Docker container
```
docker-compose up
```
7. Create superuser
```
docker-compose exec theatre python manage.py createsuperuser
```


## API Endpoints
```
"theatre" : 
                "http://127.0.0.1:8001/api/theatre/theatre_halls/"
                "http://127.0.0.1:8001/api/theatre/genres/"
                "http://127.0.0.1:8001/api/theatre/actors/"
                "http://127.0.0.1:8001/api/theatre/plays/"
                "http://127.0.0.1:8001/api/theatre/performances/"
                "http://127.0.0.1:8001/api/theatre/reservations/"
                
"user" : 
                "http://127.0.0.1:8000/api/user/register/"
                "http://127.0.0.1:8000/api/user/me/"
                "http://127.0.0.1:8000/api/user/token/"
                "http://127.0.0.1:8000/api/user/token/refresh/"
                
"documentation": 
                "http://127.0.0.1:8000/api/doc/"
                "http://127.0.0.1:8000/api/swagger/"
                "http://127.0.0.1:8000/api/redoc/"
```

## DB Structure
![DB Structure](theatre_diagram.png)
