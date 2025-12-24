# TaskFlow - Django Task Management Application

A modern, full-featured task management web application built with Django 5.2 and Python 3.13. TaskFlow follows clean architecture principles and provides an intuitive interface for managing projects and tasks with real-time updates.

![Django](https://img.shields.io/badge/django-5.2-green.svg)
![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

### Project Management
- **Create and organize projects** - Group related tasks under projects
- **Project-based task organization** - Keep tasks organized by project context
- **User isolation** - Each user can only access their own projects and tasks

### Task Management
- **Full CRUD operations** - Create, read, update, and delete tasks
- **Priority system** - 5-level priority system (Very Low to Very High) with visual indicators
- **Deadline tracking** - Set and track task deadlines with validation
- **Status management** - Track task progress (New, In Progress, Done)
- **Smart sorting** - Active tasks sorted by priority, completed tasks at bottom

### User Experience
- **Single Page Application** - Seamless experience with HTMX for dynamic updates
- **Responsive design** - Works perfectly on desktop and mobile devices
- **Real-time updates** - Tasks update without page reloads
- **Form validation** - Both client-side and server-side validation
- **Color-coded priorities** - Visual priority indicators for quick recognition

### Developer Experience
- **Clean Architecture** - Strict 3-layer architecture (Views → Services → DAL)
- **Type Safety** - Comprehensive type hints throughout the codebase
- **Testing** - Full test coverage with unit and integration tests
- **Code Quality** - Automated linting with Ruff and type checking with MyPy
- **Docker Ready** - Complete containerization for easy deployment

## 🛠 Technology Stack

### Backend
- **Python 3.13** - Latest Python with modern language features
- **Django 5.2** - Latest Django framework with improved performance
- **PostgreSQL** - Robust relational database with advanced indexing
- **django-allauth** - Complete authentication solution

### Frontend
- **HTML5 & CSS3** - Modern semantic markup and styling
- **Bootstrap 5** - Responsive UI framework
- **HTMX** - Modern approach to dynamic web applications
- **Alpine.js** - Lightweight JavaScript framework for interactivity
- **Hyperscript** - Event-driven scripting for enhanced UX

### Infrastructure & DevOps
- **Docker & Docker Compose** - Containerized development and deployment
- **Pre-commit hooks** - Automated code quality checks
- **GitHub Actions** (ready) - CI/CD pipeline support

### Code Quality
- **Ruff** - Lightning-fast Python linter and formatter
- **MyPy** - Static type checking for Python
- **Safety** - Security vulnerability scanning for dependencies
- **Comprehensive testing** - Unit and integration test coverage

## 🚀 Quick Start

### Prerequisites
- **Docker** and **Docker Compose** installed on your system
- **Git** for version control

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd task_flow
   ```

2. **Run the setup script** (Recommended)
   ```bash
   bin/setup
   ```
   This script will:
   - Check Docker installation
   - Set up Git hooks for code quality
   - Build Docker containers
   - Run database migrations
   - Create admin user
   - Start the application

3. **Manual setup** (Alternative)
   ```bash
   # Build containers
   docker-compose build
   
   # Start services
   docker-compose up -d
   
   # Run migrations
   bash bin/manage migrate
   
   # Create admin user
   bash bin/manage create_admin_user
   
   # Start development server
   docker-compose up
   ```

4. **Access the application**
   - Open your browser and go to: `http://localhost:8000`
   - Login with the test credentials:
     - **Email**: `admin@mail.com`
     - **Password**: `adminpassword`

## 📚 Development Guide

### Development Commands

#### Project Management
```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f backend
```

#### Django Management
```bash
# Run Django commands
bash bin/manage <command>

# Common commands
bash bin/manage runserver          # Start development server
bash bin/manage shell             # Django shell
bash bin/manage migrate           # Apply migrations
bash bin/manage makemigrations    # Create migrations
bash bin/manage test              # Run tests
bash bin/manage collectstatic     # Collect static files
```

#### Code Quality
```bash
# Run all pre-commit hooks
bash bin/pre-commit

# Individual tools
docker-compose run --rm --entrypoint "ruff check ." backend
docker-compose run --rm --entrypoint "ruff format ." backend
docker-compose run --rm --entrypoint "mypy ." backend
```

### Development Workflow

1. **Make your changes** following the architectural guidelines in `CLAUDE.md`
2. **Run tests** to ensure nothing is broken
   ```bash
   bash bin/manage test
   ```
3. **Check code quality** with pre-commit hooks
   ```bash
   bash bin/pre-commit
   ```
4. **Commit your changes** using semantic commit messages
   ```bash
   git add .
   git commit -m "feat(tasks): add priority sorting functionality"
   ```

## 🏗 Architecture Overview

TaskFlow follows a **strict 3-layer architecture** for maintainability and scalability:

### Layer 1: Views (HTTP Layer)
- Handle HTTP requests/responses
- Authentication and permission checks
- Form validation and serialization
- **No business logic**

### Layer 2: Services (Business Logic)
- Contain all business rules and workflows
- Coordinate between different data sources
- Handle complex business validations
- **Never access models directly**

### Layer 3: DAL (Data Access Layer)
- Repository pattern implementation
- Only layer that interacts with Django ORM
- Query optimization and database operations
- **Simple CRUD operations**

```
HTTP Request → View → Service → DAL → Database
                ↓       ↓       ↓
            HTTP Logic  Business  Data Access
                       Logic     Logic
```

For detailed architectural guidelines, see [CLAUDE.md](CLAUDE.md).

## 🧪 Testing

The project includes comprehensive test coverage:

```bash
# Run all tests
bash bin/manage test

# Run specific app tests
bash bin/manage test apps.tasks
bash bin/manage test apps.projects

# Run with coverage (if coverage is installed)
bash bin/manage test --keepdb --verbosity=2
```

### Test Structure
- **Unit tests** - Test individual components in isolation
- **Integration tests** - Test component interactions
- **Service tests** - Test business logic thoroughly
- **View tests** - Test HTTP layer functionality

## 🔧 Environment Configuration

### Environment Variables
Create a `.env` file in the project root (see `.env.sample`):

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/taskflow
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Docker Configuration
The project uses Docker Compose for development:
- **Backend service** - Django application
- **Database service** - PostgreSQL database
- **Volume mounts** - For live code reloading

## 🛡 Security Features

- **User authentication** with django-allauth
- **CSRF protection** on all forms
- **SQL injection prevention** through Django ORM
- **Security headers** configured in middleware
- **Input validation** on both client and server side
- **User isolation** - users can only access their own data

## 🐛 Troubleshooting

### Common Issues

**Docker containers won't start**
```bash
# Check if ports are available
docker-compose ps
netstat -tulpn | grep :8000

# Reset containers
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

**Database connection issues**
```bash
# Ensure database is running
docker-compose logs db

# Reset database
docker-compose down -v
docker volume prune
docker-compose up -d db
bash bin/manage migrate
```

**Pre-commit hooks failing**
```bash
# Fix formatting issues
docker-compose run --rm --entrypoint "ruff format ." backend

# Check specific issues
docker-compose run --rm --entrypoint "ruff check ." backend
```

**Permission denied on bin/setup**
```bash
chmod +x bin/setup
chmod +x bin/manage
```

### Getting Help

1. Check the logs: `docker-compose logs -f backend`
2. Ensure all services are running: `docker-compose ps`
3. Verify environment variables in `.env` file
4. Check Docker and Docker Compose versions are up to date

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the coding standards and architectural guidelines
4. Write tests for your changes
5. Run the test suite and pre-commit hooks
6. Commit your changes with semantic commit messages
7. Push to your branch and create a Pull Request

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Review the architectural documentation in `CLAUDE.md`
3. Open an issue on GitHub with detailed information about your problem

---

**Built with ❤️ using Django, HTMX, and modern Python practices.**