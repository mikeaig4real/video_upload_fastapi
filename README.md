# Video Upload FastAPI

A robust, production-ready FastAPI backend for user authentication, video upload, and management. Supports both SQL and MongoDB backends, JWT authentication, and secure password hashing.

## Features

- User registration, login, and authentication (JWT)
- Video upload, update, delete, and listing
- SQL (Postgres/SQLite) and MongoDB support
- Secure password hashing (bcrypt via passlib)
- CORS configuration for frontend integration
- Alembic migrations for SQL databases
- Pydantic models and validation
- Generic CRUD architecture for DRY code
- Environment-based configuration via `.env`

## Getting Started

### Prerequisites

- Python 3.10+
- (Optional) Docker for database setup

### Installation

1. Clone the repository:

   ```bash
   git clone <your-repo-url>
   cd video_upload_fastapi
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # Windows
   source .venv/bin/activate      # Linux/Mac
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # For development
   ```

4. Copy `.env.example` to `.env` and fill in your secrets and database config:

   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

### Database Setup

- For SQLite: No setup required (default)
- For Postgres/MongoDB: Update `.env` with your connection details
- For SQL migrations:

  ```bash
  alembic revision --autogenerate -m "Initial migration"
  alembic upgrade head
  ```

### Running the App

```bash
uvicorn main:app --reload
```

## API Endpoints

- `/api/auth/login` - User login
- `/api/auth/register` - User registration
- `/api/user/` - Get, update, delete user
- `/api/video/` - Create, list videos
- `/api/video/{id}` - Get, update, delete video

## Testing

```bash
pytest
```

## Code Quality

- Type-checked with mypy
- Linting with ruff
- Formatting with black
- Pre-commit hooks available

## Security

- Secrets and credentials must be set in `.env` (never commit `.env`)
- Passwords are hashed
- JWT secret and algorithm are configurable

## Contributing

Pull requests and issues are welcome! Please follow the code style and add tests for new features.

## License

MIT

---

For more details, see the source code and comments throughout the project.
