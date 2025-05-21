# Web App Challenge


This is a simple web application built with Flask (Python) that counts and displays the number of visits to a specific endpoint. The visit counter is stored in a Redis database to ensure data persistence across container restarts.

## Table of Contents

- [Web App Challenge](#web-app-challenge)
  - [Table of Contents](#table-of-contents)
  - [This project demonstrates:](#this-project-demonstrates)
  - [Tech Stack](#tech-stack)
  - [Build and Run Instructions](#build-and-run-instructions)
      - [Open a terminal or command prompt:](#open-a-terminal-or-command-prompt)
  - [Health Check](#health-check)
  - [CI Pipeline with GitHub Actions](#ci-pipeline-with-github-actions)
  - [Running Tests Locally](#running-tests-locally)
   
<br>   

## This project demonstrates:
*   Flask application development.
*   Integration with Redis for state management.
*   Containerization with Docker and Docker Compose.
*   A CI pipeline using GitHub Actions for automated testing and building.

## Tech Stack

*   **Python 3.9+**
*   **Flask 3.1.1:** A micro web framework
*   **Redis 4.5.0:** An in-memory data store (for the visit counter)
*   **Docker & Docker Compose:** For containerization and service management
*   **GitHub Actions:** For CI/CD pipeline
*   **Pytest 7.4.0:** For automated tests

<br> 

## Build and Run Instructions

Install _[Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)_ distributed version control system tool.


#### Open a terminal or command prompt:
1. Navigate to the directory where you want to clone the repository.
2. Clone the Repository., i.e, download your copy of the repository to your local machine using
   - Open a terminal or command prompt.
   - Navigate to the directory where you want to clone the repository.
   - Run the following command:

1.  **Clone the repository:**
    ```
    git clone https://github.com/FGargov/HWDevOpsScratch.git
    cd HWDevOpsScratch
    ```

2.  **Prerequisites:**
    *   Ensure you have [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed (a version that supports the `docker compose` command, or use `docker-compose` with a hyphen).

3.  **Start the services:**
    Execute the following command from the project's root directory:
    ```
    docker compose up --build
    ```
    *   The `--build` option will build the Docker image for the `web` application if needed.
    *   The services (`web` and `redis`) will start. You can add the `-d` flag (`docker compose up --build -d`) to run them in detached mode (in the background).

4.  **Access the application:**
    *   **Main endpoint:** `http://localhost:8000/`
    *   **Visit endpoint (increments the counter):** `http://localhost:8000/visit`
    *   **Health check endpoint:** `http://localhost:8000/health`

5.  **Stop the services:**
    To stop and remove the containers, networks, and volumes (excluding the named volume `redis_data` by default):
    ```
    docker compose down
    ```
  
<br>

## Health Check

The application has a `/health` endpoint that checks:
1.  If the Flask application is running.
2.  If there is a successful connection to the Redis server (via a `PING` command).

This endpoint is used by the `healthcheck` definition in the `docker-compose.yml` file to monitor the status of the `web` container.

<br>

## CI Pipeline with GitHub Actions

The CI pipeline is defined in the `.github/workflows/test.yml` file and is triggered on:
*   `push` to the `main` branch.
*   Creation or update of a `pull request` targeting the `main` branch.

**The pipeline performs the following main steps:**

1.  **Checkout repository code:** Checks out the repository's code.
2.  **Build and start services with Docker Compose:** Builds the Docker images and starts the `web` and `redis` services.
3.  **Show Docker logs for web service:** Displays logs from the `web` container for debugging purposes.
4.  **Wait for services to be healthy:** Waits for the `web` service to become "healthy" according to its `healthcheck`.
5.  **Verify /health endpoint:** Performs an external `curl` check to the `/health` endpoint.
6.  **Run Pytest tests inside web container:** Executes `pytest` tests (from `tests/test_app.py`) inside the `web` container.
7.  **Clean up Docker Compose services:** Stops and removes the Docker Compose services.

<br>

> [!NOTE]
If any of these steps fail, the entire pipeline is considered unsuccessful!

<br>

## Continuous Delivery (CD) to Docker Hub

When a Pull Request is merged into the `main` branch (or a push is made directly to `main`), the CI pipeline runs all tests and builds the application as described above.

If all CI steps pass successfully, an additional **Continuous Delivery (CD) step** is executed:
- **Builds a Docker image** for the web application.
- **Tags the image** automatically (with `latest`).
- **Pushes the image** to your Docker Hub repository:  
  `windowmaker/web-app-challenge-hw`

This ensures that the latest tested version of the application is always available as a Docker image for deployment or further testing.


## Running Tests Locally

You can run the `pytest` tests locally after starting the services with `docker compose up -d`:

```
docker compose exec web pytest
```

