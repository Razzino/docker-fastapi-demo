# FastAPI Docker Application

This project demonstrates how to use FastAPI and MySQL with Docker. It contains a simple FastAPI application that connects to a MySQL database.

## Prerequisites

Before you start, make sure you have the following installed:

- Docker
- Docker Compose
- Git

## Setup Instructions

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/Razzino/docker-fastapi-demo
cd your-repository-name







2. Build and Start the Containers
In the project directory, where the docker-compose.yml file is located, run the following command to build and start the containers:

                    docker-compose up --build


3. Access the Application
Once the containers are up and running, open your browser and visit:
                http://localhost:8000
                http://localhost:8000/docs to create, read, update, delete recipes/comments/ratings
                

4. Stop the Application
To stop the running containers, press Ctrl+C in your terminal or run:

                docker-compose down


Troubleshooting
If MySQL is not connecting, check the MySQL container logs for any errors.
If the port 3306 is already in use, you might need to stop any services using it or change the port in the docker-compose.yml file.


