# Dronut Project

## Business Overview
Dronut is a business that allows customers to order from a range of gourmet donuts and have them delivered by drone within 20 mins of completing an order. This project aims to develop a product backend to manage donuts and orders.

## Tech Overview
The stack is containerised with Docker and consists of the following: 
1. A Django-based backend: REST APIs with unit tests, basic API tests and message producers.
2. A message broker (RabbitMQ) to support streaming text oriented messages
3. A consumer to receive new donut orders. It is developed as a custom Django command.

## Run
- Install Docker
- `cd backend`
- `docker-compose build`
- `docker-compose up`

## Tech Stack Details
### 1. Django apps and models
The Django project consists of 2 apps:
	- `donuts` app, which has 1 model: `Donut`
	- `orders` app, which has 2 models: `Order` and `OrderLine`

### 2 DRF-based APIs:
1.1. GET `/donuts` to list all available donuts. Also, you can use `/donuts?q=abc` to search for `donut_code` that starts with `abc`
1.2. GET `/donuts/:id` to get details about a specific donut.
1.3. POST `/donuts` to create a new donut. Example payload:
```
{
    "donut_code": "strawberry",
    "name": "Name",
    "description": "These Baked Strawberry Donuts are filled with fresh strawberries.",
    "price_per_unit": 7.5
}
```
1.4. PATCH `/donuts/:id` to update a specific donut.

1.5. GET `/orders` to list all orders.
1.6. GET `/orders/:id` to get details about a specific order.
1.7. POST `/orders` to create a new order. Example payload:
```
{
    "customer_name": "John BB",
    "donuts": [
        {
            "donut_code": "abc_original",
            "quantity": 3
        },
        {
            "donut_code": "xyz_caramel",
            "quantity": 2
        }
    ]
}
```
1.8. PATCH `/orders/:id` to dispatch a specific order.

### 3. Django unit tests and API tests
- 16 unit tests for creating a new order
- 2 unit tests for dispatching an order
- 4 API tests for the `/orders` API
- 5 API tests for the `/donuts` API

Use the following command to run the tests: `python3 manage.py test`

### 4. Data fixtures
Use the following commands to load some initial data:
`python3 manage.py loaddata donuts`
`python3 manage.py loaddata orders`

### 5. Message producers
The backend will produce a message in RabbitMQ for any of the following actions:

- Create a new donut to the queue: `donuts`
- Update a donut to the queue: `donuts`
- Create a new order to the queue: `orders`
- Dispatch an order to the queue: `orders`

### 6. Message consumer
The consumer will wait for new messages in RabbitMQ in the queue `new_donut_order` and use the body of the message as a payload to create a new donut order. It runs in a container by itself, using the following custom Django command to run the consumer:
`python manage.py consume_new_donut_orders`

28-11-2022
H Rayan