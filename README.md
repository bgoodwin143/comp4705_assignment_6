# Comp4705 Assignment 6: Deployed Sentiment Analysis System

This repository contains the culmunation of the term into a project that deploys a sentiment analysis application. The system includes a FastAPI backend for predictions, a Streamlit dashboard for monitoring, a CI/CD pipeline with GitHub Actions, and is deployed live on an AWS EC2 instance.

## Project Architecture

The architecture is composed of several key components that work together:

*   **FastAPI Service**: A containerized API that serves sentiment predictions. It listens for `POST` requests at the `/predict` endpoint and logs every transaction to a shared Docker volume.

*   **Streamlit Dashboard**: A containerized web application that provides real-time monitoring. It reads the logs from the shared volume to visualize data drift, target distribution, and model performance metrics like accuracy.

*   **Docker**: Both the API and dashboard are packaged as Docker images, ensuring their environments are isolated and consistent. They run as two separate containers on the same EC2 instance.

*   **Docker Volume**: A named volume (`prediction_logs_volume`) persists log data and allows the two containers to communicate. The API writes to the volume, and the dashboard reads from it.

*   **CI/CD Pipeline**: A GitHub Actions workflow automates quality checks. On every pull request to the `main` branch, it runs `flake8` for linting and `pytest` for unit testing, preventing bad code from entering the main branch.

*   **AWS EC2**: The entire application is deployed on a `t2.micro` EC2 instance running Ubuntu, making the services accessible over the internet.

## Local Development

To run this project locally, you must have Docker installed.

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/bgoodwin143/comp4705_assignment_6
    cd comp4705_assignment_6
    ```

2.  **Create the Docker Volume**:
    ```bash
    docker volume create prediction_logs_volume
    ```

3.  **Build the Docker Images**:
    ```bash
    docker build -t fastapi-sentiment-api -f api/Dockerfile .
    docker build -t streamlit-monitoring-dashboard -f monitoring/Dockerfile .
    ```

4.  **Run the Containers**:
    ```bash
    docker run -d --name api_container -p 8000:8000 -v prediction_logs_volume:/logs fastapi-sentiment-api
    docker run -d --name dashboard_container -p 8501:8501 -v prediction_logs_volume:/logs streamlit-monitoring-dashboard
    ```

    *   The API will be available at `http://localhost:8000`.
    *   The dashboard will be available at `http://localhost:8501`.

## Manual Deployment Guide (AWS EC2)

This is a detailed guide to deploy the project from scratch on AWS.

### 1. Launch and Configure EC2 Instance
*   In the AWS Console, launch a new `t2.micro` instance with an **Ubuntu Server LTS** AMI.
*   Create a new **Security Group** with the following **inbound rules**:
    *   **Port 22 (SSH)** from your personal IP address.
    *   **Port 8000 (FastAPI)** from anywhere (`0.0.0.0/0`).
    *   **Port 8501 (Streamlit)** from anywhere (`0.0.0.0/0`).
*   Create and download a new `.pem` key pair to connect to the instance.

### 2. Connect to the Server
*   Use SSH to connect to your instance's public IP address.
    ```bash
    # Set the correct read-only permissions for your key
    chmod 400 your-key.pem

    # Connect to the instance
    ssh -i "your-key.pem" ubuntu@<your-ec2-ip-address>
    ```

### 3. Set Up the Server Environment
*   Update packages and install Git and Docker.
    ```bash
    sudo apt-get update -y
    sudo apt-get install git docker.io -y
    sudo usermod -aG docker ${USER}
    ```
*   **Crucial Step**: Log out (`exit`) and log back in for the Docker permissions to take effect.

### 4. Deploy the Application
*   Clone the `dev` branch of your project repository.
    ```bash
    git clone -b dev https://github.com/[your-github-username]/comp4705_assignment_6.git
    cd comp4705_assignment_6
    ```
*   Create the shared Docker volume.
    ```bash
    docker volume create prediction_logs_volume
    ```
*   Build the Docker images for both services using their respective Dockerfiles.
    ```bash
    docker build -t fastapi-sentiment-api -f api/Dockerfile .
    docker build -t streamlit-monitoring-dashboard -f monitoring/Dockerfile .
    ```
*   Run both containers in detached mode, attached to the volume.
    ```bash
    docker run -d --name api_container -p 8000:8000 -v prediction_logs_volume:/logs fastapi-sentiment-api
    docker run -d --name dashboard_container -p 8501:8501 -v prediction_logs_volume:/logs streamlit-monitoring-dashboard
    ```
*   The deployment is complete and accessible at your instance's public IP on ports 8000 and 8501.