# Nutrition App

Nutrition pack recommendation system!

## Features

-   Nutrition recommendation system
-   Web scraping for nutrition data
-   RESTful API endpoints
-   SQLite database for storing nutrition information

## Project Structure

```
nutrition-bot/
├── app/                   # Main application package
│   ├── api/               # API endpoints
│   ├── core/              # Core business logic
│   ├── db/                # Database models and functions
│   └── schemas/           # Pydantic models
├── scrapers/              # Scraping infrastructure
├── tests/                 # Test files
└── pyproject.toml         # Project dependencies
```

## Setup

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your configuration

4. Run the application:

```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the application is running, visit:

-   Swagger UI: http://localhost:8000/docs
-   ReDoc: http://localhost:8000/redoc

## Development

-   Run tests: `pytest`
-   Format code: `black .`
-   Lint code: `flake8`

## License

MIT
