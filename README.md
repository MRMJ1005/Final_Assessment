# Assessment - Competitive Product Search API

A FastAPI-based application that provides competitive product search functionality using LLM-powered keyword generation and intelligent product filtering.

## Features

- **LLM-Powered Keyword Generation**: Automatically generates search keywords from product descriptions using Groq's LLM
- **Intelligent Product Filtering**: Filters products based on rating, reviews, and price range
- **Explainable AI**: Provides reasoning for product acceptance/rejection decisions
- **RESTful API**: FastAPI-based API with automatic documentation

## Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Groq API key (for LLM functionality)

## Setup Instructions

### 1. Install uv (if not already installed)

If you don't have `uv` installed, you can install it using:

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone the Repository

```bash
git clone <repository-url>
cd "Task Submission"
```

### 3. Install Dependencies

Using uv, install all project dependencies:

```bash
uv sync
```

This will create a virtual environment and install all dependencies specified in `pyproject.toml`.

### 4. Set Up Environment Variables

Create a `.env` file in the root directory of the project:

```bash
# .env
GROQ_API_KEY=your_groq_api_key_here
```

Replace `your_groq_api_key_here` with your actual Groq API key. You can obtain a Groq API key from [Groq's website](https://console.groq.com/).

### 5. Initialize the Database

Before running the application, you need to set up the database with initial data. Run the database preparation script:

```bash
uv run python src/db_prep/db_prep.py
```

This will:
- Create the SQLite database (`test.db`)
- Create the necessary tables
- Populate the database with sample product data

### 6. Run the Application

Start the FastAPI server:

```bash
uv run python main.py
```

The application will start on `http://0.0.0.0:8000` (accessible at `http://localhost:8000`).

### 7. Access API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redocs

## API Usage

### Endpoint: `/related-products`

Get related products based on a product description and price.

**Query Parameters:**
- `product_description` (required): Description of the product to search for
- `price` (required): Price of the product (float)

**Example Request:**
```bash
curl "http://localhost:8000/related-products?product_description=Insulated%20water%20bottle%2032oz&price=29.99"
```

**Example Response:**
```json
{
  "input": {
    "keywords": "insulated, water bottle, 32oz, stainless steel"
  },
  "output": {
    "count": 5,
    "result": [
      {
        "id": "...",
        "description": "...",
        "review": 1247,
        "rating": 4.4,
        "result": "passed",
        "reason": "Product passed all filters..."
      }
    ]
  }
}
```

## Project Structure

```
.
├── main.py                 # Application entry point
├── pyproject.toml          # Project dependencies and configuration
├── uv.lock                 # Locked dependency versions
├── test.db                 # SQLite database file
├── src/
│   ├── app.py              # FastAPI application and routes
│   └── db_prep/
│       ├── db.py           # Database models and session management
│       └── db_prep.py      # Database initialization script
├── xray/
│   ├── core.py             # XRay class for explainable AI
│   ├── llm.py              # LLM model initialization
│   └── prompts.py          # LLM prompts
└── results/                # API response results (if any)
```

## Development

### Running in Development Mode

The application runs with auto-reload enabled by default. Any changes to the code will automatically restart the server.

### Database

The application uses SQLite with async support (`aiosqlite`). The database file is `test.db` in the root directory.

To reset the database:
1. Delete `test.db`
2. Run `uv run python src/db_prep/db_prep.py` again

## Dependencies

- **FastAPI**: Web framework for building APIs
- **Uvicorn**: ASGI server
- **SQLAlchemy**: ORM for database operations
- **LangChain**: LLM framework
- **LangChain Groq**: Groq integration for LangChain
- **Pydantic**: Data validation
- **python-dotenv**: Environment variable management

## Troubleshooting

### Issue: Module not found errors
**Solution**: Make sure you've run `uv sync` to install all dependencies.

### Issue: Database errors
**Solution**: Ensure you've run the database preparation script (`uv run python src/db_prep/db_prep.py`).

### Issue: LLM API errors
**Solution**: Verify your `GROQ_API_KEY` is correctly set in the `.env` file.

### Issue: Port already in use
**Solution**: Change the port in `main.py` or stop the process using port 8000.



