# Nodejs-blog: Markdown Blog Website
Project created following tutorial from [freeCodeCamp.org](https://www.youtube.com/watch?v=0sOvCWFmrtA&t=51919s)
The project is altered for e-commerce needs, which organize products instead of posts

## Table of contents
* [General info](#general-info)
* [Main Technologies](#main-technologies)
* [Pre-requisites](#pre-requisites)
* [Setup](#setup)
* [Project Structure](#project-structure)
* [API URL Paths](#api-url-paths)
* [API Testing](#api-testing)

## General info
This project is simple REST API about products that can perform CRUD.
	
## Main Technologies
Project is created with:
* FastAPI version 0.103.1 as **Framework**
* PostgreSQL version 16 as **Database**
* SQLAlchemy version 2.0.21 as **ORM tool**
* alembic version 1.12.0 as **Database Migration tool**

## Pre-requisites
- Install [Python](https://www.python.org) version 3.11.5
- Install [PostgreSQL](https://www.postgresql.org) version 16
- Create .env file with variables:

| Variable Name              | Description                                         |
|----------------------------|----------------------------------------------------|
| `DATABASE_HOSTNAME`   | The hostname or IP address where PostgreSQL database server is hosted.            |
| `DATABASE_PORT`     | The port number on which the PostgreSQL database server is listening. Typically, PostgreSQL uses port 5432.   |
| `DATABASE_USERNAME`        | The username used to authenticate and connect to the PostgreSQL database.    |
| `DATABASE_PASSWORD`        | The password associated with the specified database username for authentication.    |
| `DATABASE_NAME`            | The name of the PostgreSQL database.     |
| `SECRET_KEY`               | A secret key used for encrypting and decrypting data, such as user authentication tokens.  |
| `ALGORITHM`                | The cryptographic algorithm used for encoding and decoding authentication tokens. Like HS256 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | The duration (in minutes) for which an access token remains valid before it expires and requires reauthentication. |

## Setup
To run this project, install dependencies and run the project with:
```
$ pip install -r requirements.txt
$ uvicorn app.main:app
```

## Project Structure
File structure of the app is explained below:
| Name                  | Description                                                                     |
|-----------------------|-------------------------------------------------------------------------------------------|
| **app/routers/**      | Directory containing FastAPI routes    |
| **app/routers/auth.py** | FastAPI routes related to user authentication and authorization.   |
| **app/routers/oauth2.py** | FastAPI routes handling OAuth 2.0 authentication and authorization processes.   |
| **app/routers/products.py** | FastAPI routes managing products within the application.      |
| **app/routers/ratings.py** | FastAPI routes dealing with product ratings and reviews.         |
| **app/routers/users.py** | FastAPI routes for user-related actions and profiles.              |
| **database.py**       | Python file managing database connections and ORM setup using SQLAlchemy with FastAPI.           |
| **config.py**         | Configuration file serving as the entry point for the FastAPI application.     |
| **main.py**           | Main file serving as the entry point for the FastAPI application, handling API routing and startup logic.   |
| **models.py**         | Python file defining database models and schema structures for the application using SQLAlchemy.             |
| **schemas.py**        | Python file containing Pydantic schemas for validating and serializing data in the FastAPI application.     |
| **utils.py**          | Utility functions file, storing functions related to hashing and verification processes.                     |

## API URL Paths
The application running on `localhost:8000`, API HTTP Method and path as below:
| Category  | HTTP Method | Path              | Description                                        |
|-----------|-------------|-------------------|----------------------------------------------------|
| Product   | GET         | `/products`       | Retrieve a list of all products.                   |
| Product   | GET         | `/products/:id`   | Retrieve details of a specific product by its ID.  |
| Product   | POST        | `/products`       | Create a new product. Required user authentication.                   |
| Product   | PUT         | `/products/:id`   | Update a specific product by its ID. Required user authentication.      |
| Product   | DELETE      | `/products/:id`   | Delete a specific product by its ID. Required user authentication.      |
| User      | GET         | `/users/:id`      | Retrieve details of a specific user by their ID.   |
| User      | POST        | `/users`          | Create a new user.                                 |
| User      | POST        | `/login`          | Authenticate and log in a user.                    |
| Rating    | POST        | `/rating`         | Submit a rating for a product. Required user authentication.    |

Create, Update and Delete require the same user, which means user authentication is required before the action.

## API Testing
API can be tested through **Postman** or **localhost:8000/docs**(Swagger UI)
