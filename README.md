# Django SSO Project with Multi-Database Architecture

A sophisticated Single Sign-On (SSO) system built with Django that demonstrates a microservices-like architecture using multiple databases.

## Architecture Overview

The project uses three different databases to handle different aspects of the application:

1. **PostgreSQL (Authentication Service)**
   - Handles user authentication
   - Manages user credentials and roles
   - JWT token management

2. **MySQL (System A)**
   - Stores user profiles
   - Manages department information
   - Handles employee-specific data

3. **MongoDB (System B)**
   - Stores user preferences
   - Manages dashboard layouts
   - Handles work hours and notification settings

## Features

- Single Sign-On (SSO) authentication
- JWT-based authentication
- Multi-database architecture
- Redis caching
- Swagger API documentation
- Department management
- User preferences management
- Profile management

## Prerequisites

- Docker and Docker Compose
- Python 3.10+
- PostgreSQL
- MySQL
- MongoDB
- Redis

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd django-sso
```

2. Build and run with Docker Compose:
```bash
docker-compose up --build
```

## API Documentation

Access the API documentation at:
- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`
- OpenAPI JSON: `http://localhost:8000/swagger.json`

## API Endpoints

### Authentication
- `POST /api/register/` - Register new user
- `POST /api/login/` - Login user
- `POST /api/token/refresh/` - Refresh JWT token
- `POST /api/token/verify/` - Verify JWT token

### User Profile (MySQL)
- `GET /api/system-a/profiles/` - List all profiles
- `POST /api/system-a/profiles/` - Create new profile
- `GET /api/system-a/profiles/{user_id}/` - Get specific profile
- `PUT /api/system-a/profiles/{user_id}/` - Update profile
- `DELETE /api/system-a/profiles/{user_id}/` - Delete profile

### Departments (MySQL)
- `GET /api/system-a/departments/` - List all departments
- `POST /api/system-a/departments/` - Create new department
- `GET /api/system-a/departments/{id}/` - Get specific department
- `PUT /api/system-a/departments/{id}/` - Update department
- `DELETE /api/system-a/departments/{id}/` - Delete department

### User Preferences (MongoDB)
- `GET /api/system-b/preferences/` - List all preferences
- `POST /api/system-b/preferences/` - Create new preferences
- `GET /api/system-b/preferences/{user_id}/` - Get specific preferences
- `PUT /api/system-b/preferences/{user_id}/` - Update preferences
- `DELETE /api/system-b/preferences/{user_id}/` - Delete preferences

## Usage Examples

1. Register a new user:
```bash
curl --location 'http://localhost:8000/api/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "engineer@example.com",
    "password": "Test@123",
    "first_name": "John",
    "last_name": "Doe",
    "department_id": 1,
    "position": "Software Engineer"
}'
```

2. Login:
```bash
curl --location 'http://localhost:8000/api/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "engineer@example.com",
    "password": "Test@123"
}'
```

3. Update preferences:
```bash
curl --location --request PATCH 'http://localhost:8000/api/system-b/preferences/{user_id}/' \
--header 'Authorization: Bearer <your_token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "theme": "dark",
    "language": "en",
    "notifications_enabled": true
}'
```

## Security Features

- JWT Authentication
- Password hashing with Argon2
- CORS protection
- XSS protection
- CSRF protection
- Secure cookie configuration
- HTTP-only cookies
- Rate limiting
- Redis session backend

## Caching

The project uses Redis for:
- Session storage
- Cache backend
- Rate limiting

## Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create initial departments:
```bash
python manage.py setup_departments
```

## Docker Configuration

The project includes:
- Multi-container setup with Docker Compose
- Separate containers for each database
- Nginx for serving static files
- Redis container for caching
- Wait-for-it scripts for proper container orchestration

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the BSD License.

## Contact

- Email: s.naqvi2129@gmail.com
- Website: https://shabeehnaqvi.com 