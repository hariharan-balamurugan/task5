# FastAPI Weather Summary API

## 1. Project Overview

The Weather Summary API is a REST API built using Python and FastAPI. It fetches hourly weather forecast data from the Open-Meteo public API, processes the temperature data, and returns a clean JSON response.

### Features

- Fetches weather forecast data from Open-Meteo.
- Calculates average, minimum, and maximum temperatures.
- Generates a simple weather summary.
- Accepts latitude and longitude as query parameters.
- Handles API errors and request timeouts.
- Supports Docker containerization.
- Provides interactive API documentation using Swagger UI.

## 2. Technologies Used

- Python
- FastAPI
- HTTPX
- Uvicorn
- Open-Meteo API
- Docker
- python-dotenv

## 3. Project Structure

```text
weather-api/
├── main.py
├── requirements.txt
├── Dockerfile
├── .env
├── .dockerignore
└── README.md
```

## 4. Configuration

Create a `.env` file in the project directory.

```env
OPEN_METEO_URL=https://api.open-meteo.com/v1/forecast
DEFAULT_LATITUDE=11.0168
DEFAULT_LONGITUDE=76.9558
REQUEST_TIMEOUT_SECONDS=10
```

The default coordinates represent Coimbatore.

Open-Meteo does not require an API key for its free, non-commercial API service.

## 5. Installation and Setup

### Prerequisites

- Python 3.12 or a compatible Python version
- pip
- Docker Desktop (optional)
- Git (for version control)

### Run Without Docker

**Step 1: Create a virtual environment**

```bash
python -m venv .venv
```

**Step 2: Activate the environment**

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

**Step 3: Install dependencies**

```bash
python -m pip install -r requirements.txt
```

**Step 4: Start the FastAPI application**

```bash
uvicorn main:app --reload
```

The application will run at:

`http://localhost:8000`

### Run With Docker

**Step 1: Build the Docker image**

```bash
docker build -t weather-api .
```

**Step 2: Run the container**

```bash
docker run --name weather-container --env-file .env -p 8000:8000 weather-api
```

The application will be available at:

`http://localhost:8000`

**Useful Docker commands**

Check running containers:

```bash
docker ps
```

View logs:

```bash
docker logs weather-container
```

Stop the container:

```bash
docker stop weather-container
```

Remove the container:

```bash
docker rm weather-container
```

## 6. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Returns API information |
| GET | `/weather` | Returns processed weather forecast data |
| GET | `/docs` | Opens interactive API documentation |

## 7. Sample Request

Request the weather forecast for Coimbatore:

```http
GET /weather
```

Request the weather forecast for Chennai:

```http
GET /weather?latitude=13.0827&longitude=80.2707
```

You can also test these requests through Swagger UI:

`http://localhost:8000/docs`

## 8. Sample Response

The following JSON illustrates the response structure. The temperature values are examples, not live readings.

```json
{
  "location": {
    "latitude": 11.02,
    "longitude": 76.96,
    "timezone": "Asia/Kolkata"
  },
  "average_temperature": 28.42,
  "minimum_temperature": 24.1,
  "maximum_temperature": 33.6,
  "temperature_unit": "°C",
  "summary": "Warm weather",
  "hourly_forecast": [
    {
      "time": "2026-10-26T00:00",
      "temperature": 25.2
    }
  ]
}
```

The actual response depends on the data returned by Open-Meteo.

## 9. Error Handling

The API handles common errors:

- HTTP 502: The external weather API request fails or returns an unsuccessful response.
- HTTP 504: The external weather API request times out.
- HTTP 422: The latitude or longitude query parameter is invalid.

## 10. How It Works

1. The client sends a request to the FastAPI endpoint.
2. FastAPI validates the latitude and longitude.
3. HTTPX sends an asynchronous request to Open-Meteo.
4. The API returns hourly temperature data.
5. Python calculates the average, minimum, and maximum temperatures.
6. FastAPI returns the processed data as JSON.

## 11. Future Improvements

- Add weather condition descriptions.
- Support forecasts for multiple days.
- Add automated tests.
- Add logging and monitoring.
- Deploy the service to a cloud platform.

## 12. Author

Developed as a learning project to practise FastAPI, external API integration, asynchronous programming, and Docker.