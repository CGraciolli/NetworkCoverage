# Network Coverage API

This project provides an API to retrieve 2G/3G/4G network coverage by provider using a textual address. It processes the address, converts it to GPS coordinates, and fetches coverage data from a database.

## How to Install

1. Clone the repository:
   ```bash
   git clone https://github.com/CGraciolli/NetworkCoverage
   cd papernest
   ```

2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

3. Alternatively, install dependencies using `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure you have Docker installed if you plan to use Docker for running the project.

## How to Run

### Using Docker

1. Build the Docker image:
   ```bash
   docker build -t network-coverage-api .
   ```

2. Start the application using Docker Compose:
   ```bash
   docker-compose up
   ```

### Running Locally

1. Initialize the database by running the `main.py` script:
   ```bash
   python src/main.py
   ```
   This step ensures that the database is set up and populated with data from the `providers.csv` file.

2. Start the application using `uvicorn`:
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```

3. The API will be available at `http://localhost:8000`.

## How It Works

1. **Input**: The user provides a textual address. An accuracy level can also specified.
2. **Address Conversion**: The address is converted to GPS coordinates using the `address_to_gps` helper.
3. **Data Retrieval**: The GPS coordinates are used to query the database for network coverage data.
4. **Response**: The API returns the network coverage details by provider.

### Project Structure

- `src/network_coverage/application`: Contains application logic, such as converting addresses to GPS coordinates and fetching coverage data.
- `src/network_coverage/domain`: Defines the domain entities and repository interfaces.
- `src/network_coverage/infrastructure`: Implements infrastructure details, including database access and HTTP routing.
- `tests`: Contains unit and integration tests for the application.

## API Endpoints

### Get Network Coverage by Address

- **Endpoint**: `GET /papernest/network-coverage/`
- **Query Parameters**:
  - `address` (required): The textual address to retrieve network coverage for.
  - `accuracy` (optional): An integer specifying the desired accuracy level.
  The default accuracy is approximately 1 km in each cardinal direction, by providing a value n, it will be approximately n km in each.

**Example Request**:
```
GET /papernest/network-coverage/?address=123+Main+St&accuracy=5
```

**Example Response**:
```json
{
  "provider": "ProviderName",
  "coverage": {
    "2G": true,
    "3G": true,
    "4G": false
  }
}
```

## Additional Notes

- The `data/providers.csv` file contains provider data used for coverage calculations.
Its coordinates are Lambert93, the file `src/network_coverage/infrastructure/csv/lambert_to_gps.py` converts the Lambert93 to GPS coordinates before populating the database.
- The `coverage.db` SQLite database stores network coverage information.
