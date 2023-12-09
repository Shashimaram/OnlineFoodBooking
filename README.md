### Online Food Booking App


## Overview
This is an online food booking app that allows customers to browse and order food from various restaurants. The app is built using HTML, CSS, JS for the frontend, and Django, Python, and ORM for the backend.

## Features
# Customer Account
- Browse Restaurants: Customers can search for restaurants based on their location using Google Maps API. This makes it easy for users to find nearby restaurants.
- Add to Cart: Customers can add their favorite food items to the cart for easy checkout.
- Checkout: The app supports a seamless checkout process, allowing customers to review their order and proceed to payment.
- Payment Integration: Razor Pay integration is implemented to facilitate secure and efficient payment transactions.

# Vendor Account
- Add Food Items: Vendors can add new food items to their menu, providing a detailed description of each item.
- Food Categories: Vendors can organize their menu by creating different categories for food items.
- Restaurant Timings: Vendors can set and update their restaurant timings, providing users with accurate information about when they can place an order.
- Build Menu: Vendors have the flexibility to build and customize their menu according to their offerings.

# Technologies Used
- Frontend: HTML, CSS, JS
- Backend: Django, Python, ORM
- Payment Integration: Razor Pay
- APIs: Google Maps API for location-based restaurant search

# Getting Started
- Clone the repository: git clone https://github.com/Shashimaram/OnlineFoodBooking.git
- Set up the database: python manage.py migrate
- Create a superuser account: python manage.py createsuperuser
- Run the development server: python manage.py runserver
