# SESH

**WHAT WE KNOW SO FAR**
====================

**TABLES**
-------
1. **USERS**
    * **COLUMNS**
        - primary key id
        - netid
        - email
        - password

* **REQUESTS**
- GET study seshs by user id (will take user id as parameter): Will return all study seshs associated with the user
    - returns a serialized dict with
        * Sesh title
        * Course
        * Date
        * Location
        * Number of students in sesh


- **GET** all study seshs: will return all study seshs in the database
    - returns a serialized dict with
        * Sesh title
        * Course
        * Date
        * Location
        * Number of students in sesh

- **GET** seshs by filtering(will take filter as parameter): will return all seshs that match the filter
    - returns a serialized dict with
        * Sesh title
        * Course
        * Date
        * Location
        * Number of students in sesh

- **POST** join study sesh( will take sesh id as parameter)
    - adds student to a study sesh


- **POST** create study sesh
    - body keys:
        * sesh title
        * course title
        * date
        * time
        * location
        * description
- **DELETE**(drop) out of a study sesh ( will take sesh id and user id as a parameter)
    - removes student from a study sesh


2. **SESHS**
    * **COLUMNS****
        - primary key id
        - title
        - course
        - date
        - start + end time
        - location
        - Number of students in sesh
        - Description

3. **ASSOC TABLE**
    * **COLUMNS**
        - STUDENT ID --> references student in USERS table
        - SESH ID --> references sesh in SESHS table


