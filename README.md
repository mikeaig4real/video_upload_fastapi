# Video Upload FastAPI

A modern, production-ready FastAPI backend for user authentication, video upload, and management. This project is designed as a highly extensible, database-agnostic, and bucket-agnostic template, making it easy to adapt for a wide range of use cases. It features strong typing, generic CRUD patterns, Celery-powered background processing, and robust security. Duplicate video uploads are prevented by design. This backend is built to complement the [video_upload_react_ui](https://github.com/mikeaig4real/video_upload_react_ui) frontend project.

## WORK IN PROGRESS, UPDATES PENDING

## Deployment

This backend is currently deployed at: [https://video-upload-fastapi.onrender.com/](https://video-upload-fastapi.onrender.com/)

## Key Strengths & Features

- **Database Agnostic**: Easily switch between SQL (Postgres/SQLite) and MongoDB backends with minimal code changes.
- **Bucket Agnostic**: Supports Cloudinary, S3, and Google Cloud Storage for video uploads; can be extended to other providers.
- **Extensive Use of Types**: Strong typing throughout the codebase using Pydantic, TypedDict, and custom Enums for safer, more maintainable code.
- **Generic CRUD Pattern**: DRY, reusable CRUD logic for all models, making it easy to add new resources.
- **Celery Worker Integration**: Background tasks (e.g., video processing) handled via Celery and Redis, with Flower for monitoring.
- **Duplicate Prevention**: Prevents uploading duplicate videos by design.
- **Environment-based Configuration**: All secrets and settings loaded from `.env` for security and flexibility.
- **Robust Security**: JWT authentication, secure password hashing (bcrypt), and strict separation of secrets.
- **CORS & Frontend Integration**: Configurable CORS for seamless integration with modern frontends.
- **Extensible Upload System**: Easily switch between bucket and file system storage.
- **Code Quality Tools**: Type-checked (mypy), linted (ruff), formatted (black), and pre-commit hooks for consistency.
- **Alembic Migrations**: For SQL databases, supports schema migrations out of the box.
- **Comprehensive API**: User, video, and upload endpoints with clear separation of concerns.
- **Health Check & Error Handling**: Built-in health endpoint and custom error handlers for reliability.

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

For more details and interactive API documentation, visit: [https://video-upload-fastapi.onrender.com/docs](https://video-upload-fastapi.onrender.com/docs)

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
