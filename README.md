# RouteFlowAI

RouteFlowAI is a modern, high-performance FastAPI application designed for AI-powered routing and recommendation pipelines. It leverages PostgreSQL as its primary database and integrates with the Google Gemini API (`gemini-3.1-flash-lite`) to generate intelligent recommendations, process search inputs, and prepare trip plans.

---

## Features

- **FastAPI Core**: Async API routes with automatic interactive API documentation (`Swagger UI`).
- **PostgreSQL Database**: Built-in CRUD operations managed via SQLAlchemy ORM and async pg drivers (`asyncpg`).
- **AI Recommendation Engine**: Utilizes Google GenAI (`google-genai`) powered by Gemini models for advanced route planning and recommendations.
- **Modern Package Management**: Managed seamlessly using `uv`, the fast Python package installer and resolver.

---

## Prerequisites

Before setting up the project, ensure you have the following installed on your system:

- **Python**: `>= 3.14` (as defined in `pyproject.toml`)
- **Docker & Docker Compose**: For running the PostgreSQL database services.
- **uv**: The recommended modern Python packaging tool. If you don't have `uv` installed, you can install it using:
  ```bash
  # On macOS/Linux
  curl -LsSf https://astral.sh/uv/install.sh | sh

  # On Windows
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

---

## Getting Started

Follow these steps to set up your local development environment.

### 1. Set Up Environment Variables

Copy the example environment configuration to create your local `.env` file:

```bash
cp .env.example .env
```

Open the newly created `.env` file and configure the values:
- `SQLALCHEMY_DATABASE_URL`: Pre-configured to connect to the local Dockerized PostgreSQL instance.
- `GEMINI_API_KEY`: Provide your Google Gemini API key to enable AI-powered features.

### 2. Launch the PostgreSQL Database

Start the database container using Docker Compose:

```bash
docker compose up -d
```

This starts a PostgreSQL instance accessible on `localhost:5431` with the default username, password, and database configured in `compose.yaml`.

### 3. Set Up the Virtual Environment and Install Dependencies

`uv` is the primary tool used for virtual environment management and package resolution in this project. You have two options for installing dependencies:

#### Option A: Sync Using standard `uv` workspaces (Recommended)
Since the project contains a modern `pyproject.toml` and `uv.lock`, you can let `uv` automatically create a virtual environment and synchronize all dependencies:

```bash
# Sync dependencies and automatically create/update the virtual environment
uv sync
```

#### Option B: Standard Virtual Environment with `requirements.txt`
Alternatively, you can manually create the virtual environment and install dependencies using the generated `requirements.txt`:

```bash
# Create the virtual environment
uv venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt
```

---

## Running the Application

To run the FastAPI development server, make sure your virtual environment is active and run:

```bash
uv run uvicorn src.main:app --reload
```

Once started, the server will be available at:
- **API Endpoint**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive OpenAPI (Swagger) Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Project Structure

```text
RouteFlowAI/
├── src/
│   ├── main.py                # Application entry point and router setups
│   ├── api.py                 # Core API route definitions (Users, pipelines, etc.)
│   ├── models.py              # Pydantic models for request/response validation
│   ├── core/
│   │   ├── config.py          # Application configuration loader
│   │   └── logging.py         # Custom logging configuration
│   ├── db/
│   │   ├── db_operations.py   # SQLAlchemy engine connection and session setups
│   │   ├── schemas.py         # SQLAlchemy database models (declarative base)
│   │   └── crud.py            # CRUD operations helper
│   └── pipeline/
│       ├── ai_functions.py    # Integrations with Google Gemini API & search tools
│       ├── prepare_trip.py    # Logic for preparing trips
│       └── create_recommendations.py # Core pipeline for creating travel recommendations
├── compose.yaml               # Docker Compose file for local PostgreSQL instance
├── pyproject.toml             # Python project metadata and dependencies
├── uv.lock                    # Locked exact dependency versions for uv
└── requirements.txt           # Standard pip dependencies file
```
