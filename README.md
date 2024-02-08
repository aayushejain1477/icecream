# Ice Cream Distribution System

Ice Cream Distribution System is a Django-based web application that allows users to register, authenticate, place ice cream orders, and process payments using the Stripe payment gateway.

## Features

- User Registration: Users can register for an account to place ice cream orders.
- Authentication: Users can log in to their accounts securely.
- Ice Cream Orders: Users can browse available ice creams and place orders.
- Stripe Integration: Payment processing for orders is handled through the Stripe payment gateway.

## Setup

1. Clone the repository:

`https://github.com/aayushejain1477/icecream`

2. Install dependencies:
`cd icecream`

`pip install -r requirements.txt`

3. Run migrations:
`python manage.py migrate`

4. Start the development server:
`python manage.py runserver`

5. The application will be accessible at `http://localhost:8000`.

## Endpoints

- `/register/`: User registration endpoint.
- `/login/`: User login endpoint to obtain authentication tokens.
- `/icecreams/`: Endpoint to list available ice creams and create new ones.
- `/icecreams/<int:pk>/`: Endpoint to retrieve, update, or delete specific ice creams.
- `/orders/`: Endpoint to list all orders and create new orders.
- `/orders/<int:order_id>/`: Endpoint to retrieve, update, or delete specific orders.
- `/order/`: Endpoint to create new orders and process payments.
- `/order/confirm/`: Endpoint to confirm order payment.
