# HubHouse Project

HubHouse is a web application designed for creating chat rooms where users can discuss any topic.

## Features

- **User Authentication:**
  - Sign up and login functionality with validation.
  - Edit user profile (name, email, profile picture, etc.).
  - View profile of hosts or participants .

- **Room Management:**
  - **Create and manage chat rooms** based on specific topics.
  - **Edit or delete** your own room, including the ability to change the name, topic, and description of the room.
  - **Filter rooms by topic** to easily find relevant discussions.
  - **Search for rooms explicitly** using a search feature.

- **Messaging:**
  - Once a user sends a message, they are automatically added to the room.
  - **Delete your own messages** in a room.
  - Guests cannot join or send messages to a room until they log in.

- **API:**
  - Access room data through an API endpoint to retrieve information about available chat rooms.

## Technologies Used

- **Django**: For backend development and handling the web framework.
- **SQLite**: Database used for storing room and user data.
- **HTML, CSS, JavaScript**: For the frontend interface.
- **Django REST Framework**: For API development.

## Installation

1. Clone the repository to your local machine:

   ```
   git clone https://github.com/yourusername/hubhouse.git
   cd hubhouse
   ```
Install the required dependencies:
```
pip install -r requirements.txt
```
Apply the migrations:
```
python manage.py makemigrations
python manage.py migrate
```
Run the development server:
```
python manage.py runserver
```

**API Documentation**
You can access room data through the API endpoint:
GET /api/rooms/
This endpoint retrieves a list of all available chat rooms.

## Home Page
![Home Page](screenshots/home%20page.png)
