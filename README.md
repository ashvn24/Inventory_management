
# Inventory Management App

This is an inventory management system built using Django REST framework. It includes features such as stock management, order management, user management, automated tasks using Celery, and auto stock management using Celery Beat. JWT is used for secure authentication, and all APIs have been tested on Postman. The entire project is dockerized for easy deployment.





## Installation
To run the project, follow these steps:

Clone the repository to your local machine.

Navigate to the project directory.

Run the following command to build and start the Docker containers for the first time:

Install my-project with npm

```
  docker-compose up --build
```
After the initial setup, you can simply use the following command to start the project:
```
  docker-compose up 
```

Access the application

```
http://127.0.0.1:8000/
```

## Tech Stack

**Client:** Postman API

**Server:** Django, Django REST, Celery, Docker


## Features

- Stock Management: Allows users to manage inventory by adding, updating, and deleting stock items.
- Order Management: Provides functionalities for creating, updating, and deleting orders.
- User Management: Allows administrators to manage users, including creating, updating, and deleting user accounts.
- Automated Tasks: Celery is used for scheduling automated tasks such as sending notifications and managing stock levels.
- Secure Authentication: JWT (JSON Web Tokens) are used for secure authentication, providing a robust authentication mechanism.
- Sales Report: Automatically Generated Sales Reports: Generate detailed sales reports in Excel format every month.
- API Testing: All APIs are thoroughly tested using Postman to ensure reliability and functionality.
- Dockerized Project: The entire project is dockerized, making it easy to deploy and manage in various environments.


## Authors

- [@Ashwin vk](https://github.com/ashvn24)

