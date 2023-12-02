# SESH - Study Session App

SESH is a collaborative study group application designed to enhance the academic experience for Cornell University students. With SESH, students can effortlessly create and join study sessions, fostering a dynamic learning community. This repository contains the backend code for the SESH app, expertly crafted by Ambrose Blay and Eman Abdu.

## Features

### Account Management

- **Register Account**
  - **Endpoint:** `POST /register/`
  - **Create a new user account by providing essential details.**
  - **Response (201):** Receives user details and returns session information upon successful registration.

- **Get all Users in Database**
  - **Endpoint:** `GET /api/users/`
  - **Retrieve user details from the database.**
  - **Response (200):** Returns user information for all registered users.

- **Log into account**
  - **Endpoint:** `POST /login/`
  - **Authenticate and log in a user by providing email and password.**
  - **Response (200):** Returns session tokens upon successful login.

- **Log out of account**
  - **Endpoint:** `POST /logout/`
  - **Terminate an active session, logging the user out.**
  - **Response (200):** Confirms successful logout.

- **Verify Session Token**
  - **Endpoint:** `GET /secret/`
  - **Verify the validity of a session token.**
  - **Response (200):** Returns a personalized greeting upon successful verification.

### Study Sessions

- **Get all sessions in Database**
  - **Endpoint:** `GET /api/sessions/`
  - **Retrieve information about all study sessions from the database.**
  - **Response (200):** Returns details of all study sessions.

- **Create Study session**
  - **Endpoint:** `POST /api/sessions/`
  - **Create a new study session by providing session details.**
  - **Response (201):** Returns details of the newly created study session.

- **Drop out of a study session**
  - **Endpoint:** `DELETE /api/sessions/<int:session_id>/`
  - **Withdraw from a study session by providing the session ID.**
  - **Response (200):** Returns details of the study session after withdrawal.

- **Get Specific User sessions**
  - **Endpoint:** `GET /api/sessions/user/`
  - **Retrieve study sessions associated with a specific user.**
  - **Response (200):** Returns details of study sessions for a particular user.

- **Filter all sessions in the database by title, course, or location**
  - **Endpoint:** `GET /api/sessions/filter/`
  - **Filter study sessions based on title, course, or location.**
  - **Response (200):** Returns filtered study sessions based on specified criteria.

- **Join study session**
  - **Endpoint:** `POST /api/sessions/<int:session_id>/`
  - **Join a study session by providing the session ID.**
  - **Response (200):** Returns updated details of the study session after successful joining.

## Authors

- **Ambrose Blay**
- **Eman Abdu**