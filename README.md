# Infinite Analytics Backend

This repository contains the backend implementation for Infinite Analytics. It is built using FastAPI, SQLAlchemy (async), and integrates with Google OAuth, Binance API, and Singapore weather API.

## 🚀 Features

- User authentication:
  - Email/password based registration and login
  - Google OAuth login
- Profile management with image upload
- Fetch cryptocurrency data from Binance API
- Fetch real-time weather data from Singapore government API
- PostgreSQL as the database
- Docker-based PostgreSQL setup for development

## 🛠️ Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Pydantic
- Docker (for local DB)
- Poetry (for dependency management)

## 📦 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Amandeep18-tech/infinite-analytics-backend.git
cd infinite-analytics-backend
```

### 2. Install Python Dependencies

Make sure you have Poetry installed.

```bash
poetry install
```

### 3. Create and Activate Environment

```bash
poetry shell
```

### 4. Setup Local PostgreSQL using Docker

If you don't already have a local PostgreSQL running:

```bash
docker run --name some-postgres \
-e POSTGRES_DB=userdb \
-e POSTGRES_PASSWORD=mysecretpassword \
-p 5432:5432 \
-v postgres_data:/var/lib/postgresql/data \
-d postgres
```

### 5. Create `.env` File

Create a `.env` file in the root directory with the following content:

```ini
DATABASE_URL=postgresql+asyncpg://postgres:mysecretpassword@localhost:5432/userdb
SECRET_KEY=your_super_secret_key
ALGORITHM=HS256
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
WEATHER_API_KEY=your_weather_api_key
```

⚠️ Do **not** commit your `.env` file. It is added to `.gitignore`.

## ▶️ Running the Application

```bash
uvicorn app.main:app --reload
```

## 🧪 Running Tests

Add your test setup here if applicable.

## 🌐 API Docs

Once the server is running, you can access:
* Swagger UI: http://localhost:8000/docs
* ReDoc: http://localhost:8000/redoc
