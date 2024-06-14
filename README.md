
# Weather Data Project

## Overview
This project provides a REST API to manage and query weather data records. It includes:
- Ingesting weather data from text files
- Calculating yearly statistics
- Providing endpoints to query the ingested data and statistics

## Project Structure
- `wx_data/`: Directory to store weather data files
- `src/`: Contains the application modules
  - `__init__.py`: Initialize the Flask app
  - `static/`:
    - swagger.json: API definitions
  - `database.py`: Database setup and session management
  - `ingest.py`: Script to ingest weather data and calculate stats
  - `api.py`: Flask API endpoints
- `setup_db.py`: Script to set up the database
- `requirements.txt`: Project dependencies
- `README.md`: Project documentation

## Setup

### How to Run the Project

1. Clone the repository and navigate to the project directory:

    ```bash
    git clone <repository-url>
    cd weather_analysis_api
    ```

2. Set up the virtual environment and install dependencies:

    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Set up the database:

    ```bash
    python setup_db.py
    ```

4. Place your weather data files in the `wx_data/` directory.

5. Ingest the weather data:

    ```bash
    python src/ingest.py
    ```
 

6. Run the Flask API server:

    ```bash
    python src/api.py
    ```

Now, you can access the API endpoints at `http://127.0.0.1:5000/api/weather` and `http://127.0.0.1:5000/api/weather/stats`.

Sample request -> ```curl -X 'GET' 'http://127.0.0.1:5000/api/weather?page=1' -H 'accept: application/json'```

This project structure and code will allow you to ingest weather data, calculate yearly statistics, and provide a REST API to query the data.
