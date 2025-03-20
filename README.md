# Django Single Sign-On (SSO) System with Multi-Database Management

A scalable Single Sign-On system built with Django that implements centralized authentication using PostgreSQL while managing application-specific data across MySQL and MongoDB databases.

## 🏗️ Architecture

### Database Structure
- **PostgreSQL**: Central authentication database (User credentials, JWT tokens)
- **MySQL**: System A specific user data (User profiles)
- **MongoDB**: System B specific user data (User preferences)
- **Redis**: Caching and session management

### Key Features
- Centralized authentication with JWT tokens
- Multi-database management with database routers
- Role-based access control (Admin/User)
- Lazy loading of user details
- Redis caching for performance optimization
- PostgreSQL read replicas for scalability
- Rate limiting and security measures

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose
- Git

### Quick Start
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd django-sso
   ```

2. Start the services:
   ```bash
   docker-compose up --build
   ```

3. Access the application:
   - Admin Interface: http://localhost:8000/admin
   - API Endpoints: http://localhost:8000/api/

### Default Superuser
- Email: admin@gmail.com
- Password: abc123

## 🔧 Configuration

### Environment Variables
The following environment variables can be configured:
- `DJANGO_SETTINGS_MODULE`: Django settings module
- `POSTGRES_HOST`: PostgreSQL host
- `MYSQL_HOST`: MySQL host
- `MONGODB_HOST`: MongoDB host
- `REDIS_HOST`: Redis host

### Database Configuration
- PostgreSQL (Authentication):
  - Database: sso_auth_db
  - Port: 5432

- MySQL (System A):
  - Database: system_a_db
  - Port: 3306

- MongoDB (System B):
  - Database: system_b_db
  - Port: 27017

- Redis (Cache):
  - Port: 6379

## 📡 API Endpoints

### Authentication
- `POST /api/register/`: User registration
- `POST /api/login/`: User login
- `POST /api/token/refresh/`: Refresh JWT token
- `POST /api/logout/`: User logout

### User Management
- `GET /api/user/profile/`: Get user profile
- `PUT /api/user/profile/`: Update user profile
- `GET /api/user/preferences/`: Get user preferences
- `PUT /api/user/preferences/`: Update user preferences

## 🛡️ Security Features

- Argon2 password hashing
- JWT authentication with refresh tokens
- Rate limiting on authentication endpoints
- CORS configuration
- HTTP-only secure cookies
- XSS and CSRF protection
- HSTS enabled
- Content Security Policy headers

## 🔍 Monitoring and Performance

### Caching Strategy
- Redis caching for frequently accessed data
- Session storage in Redis
- Configurable cache timeout (default: 5 minutes)
- Connection pooling for database connections

### Database Optimization
- Database connection pooling
- PostgreSQL read replicas
- Lazy loading of related data
- Database-specific routers for query optimization

## 🐳 Docker Services

- `web`: Django application with Gunicorn
- `postgres`: Main PostgreSQL database
- `postgres_replica`: PostgreSQL read replica
- `mysql`: MySQL database for System A
- `mongodb`: MongoDB database for System B
- `redis`: Redis for caching
- `nginx`: Nginx reverse proxy

## 📦 Dependencies

Key packages and their versions:
- Django 3.2.24
- Django REST Framework 3.14.0
- djangorestframework-simplejwt 5.3.1
- django-redis 5.4.0
- psycopg2-binary 2.9.9
- mysqlclient 2.2.4
- djongo 1.3.6
- redis 4.6.0
- gunicorn 21.2.0
- whitenoise 6.6.0

## 🔒 Security Recommendations

1. Change default superuser credentials
2. Use environment variables for sensitive data
3. Enable SSL/TLS in production
4. Regular security audits
5. Monitor rate limiting and failed login attempts

## 🚦 Health Checks

The system includes health checks for:
- PostgreSQL database connection
- MySQL database connection
- MongoDB connection
- Redis cache availability

## 📈 Scaling Considerations

- Horizontal scaling with Gunicorn workers
- PostgreSQL read replicas for read-heavy operations
- Redis caching for performance
- Connection pooling for database efficiency
- Nginx for load balancing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details. 