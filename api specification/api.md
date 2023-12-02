## Register Account
>### POST /register/
```
request

{
    "first_name": "David",
    "netid": "da123",
    "email": "david@gmail.com", 
    "password": "ab1234"
}
```

```
<HTTP STATUS CODE 201>
Response

{
    "first_name": "David",
    "netid": "da123",
    "email": "david@gmail.com",
    "session_token": "39e1ac9fb82e12577098fd984c6df861134210dd",
    "session_expiration": "2023-12-02 22:25:07.739906",
    "update_token": "10629cacc7051c80dd6753875c44d882f3bcee8d"
}
```


## Get all Users in Database
>### GET /api/users/
```
<HTTP STATUS CODE 200>
Response

{
    "first_name": "David",
    "netid": "da123",
    "email": "david@gmail.com",
    "session_token": "39e1ac9fb82e12577098fd984c6df861134210dd",
    "session_expiration": "2023-12-02 22:25:07.739906",
    "update_token": "10629cacc7051c80dd6753875c44d882f3bcee8d"
}
```


## Log into account
>### POST /login/
```
request

{
    "email": "ambrose2002blay@gmail.com",
    "password": "ab1234"
}
```

```
<HTTP STATUS CODE 200>
Response

{
    "session_token": "7b7ad4abf70997b4921c4e1da8a0b456caf36490",
    "session_expiration": "2023-12-02 22:27:40.302630",
    "update_token": "8b998f9eb66342cdd7ac2d3c4cc65adcf9d91bd6"
}
```


## Log out of account
>### POST /logout/
```
request

{
    token: <>
}
```

```
<HTTP STATUS CODE 200>
Response

{
    "error": "You have been logged out"
}
```


## Verify Session Token
>### GET /secret/

```
request

{
    token: <>
}
```

```
<HTTP STATUS CODE 200>
Response

"Hello {first_name}"

```


## Get all sessions in Database
>### GET /api/sessions/
```
<HTTP STATUS CODE 200>
Response

[
    {
        "id": 1,
        "title": "CS Prelim",
        "course": "CS 1110",
        "date": "22nd November, 2023",
        "start_time": "4:00 pm",
        "end_time": "6:00 pm",
        "location": "Mann Library",
        "description": "Studying for FWS Prelim",
        "population": 2,
        "users": []
    },
    {
        "id": 4,
        "title": "INfo Prelim",
        "course": "Info 1110",
        "date": "22nd November, 2023",
        "start_time": "4:00 pm",
        "end_time": "6:00 pm",
        "location": "Mann Library",
        "description": "Studying for FWS Prelim",
        "population": 1,
        "users": [
            {
                "id": 2,
                "netid": "da234",
                "email": "david2348@gmail.com"
            }
        ]
    }
]
```


## Create Study session
>### POST /api/sessions/
```
request
{
    token: <>
}

{
    "title": "CS Prelim",
    "course": "CS 1110",
    "start_time": "2023-12-02 15:30:00",
    "end_time": "2023-12-02 17:30:00",
    "location": "Mann Library",
    "description": "Studying for FWS Prelim"
}
```

```
<HTTP STATUS CODE 201>
Response

{
    "id": 1,
    "title": "CS Prelim",
    "course": "CS 1110",
    "start_time": "2023-12-02T15:30:00",
    "end_time": "2023-12-02T17:30:00",
    "location": "Mann Library",
    "population": 1,
    "description": "Studying for FWS Prelim"
}
```


## Drop out of a study session
>### DELETE /api/sessions/<int:session_id>/
```
request
{
    token: <>
}

```

```
<HTTP STATUS CODE 200>
Response

{
    "id": 1,
    "title": "CS Prelim",
    "course": "CS 1110",
    "start_time": "2023-12-02T15:30:00",
    "end_time": "2023-12-02T17:30:00",
    "location": "Mann Library",
    "population": 1,
    "description": "Studying for FWS Prelim"
}
```


## Get Specific User sessions
>### GET /api/sessions/user/

```
request
{
    token: <>
}

```

```
<HTTP STATUS CODE 200>
Response

[
    {
        "id": 1,
        "title": "CS Prelim",
        "course": "CS 1110",
        "start_time": "2023-12-02T15:30:00",
        "end_time": "2023-12-02T17:30:00",
        "location": "Mann Library",
        "population": 2,
        "description": "Studying for FWS Prelim"
    }
]
```


## Filter all sessions in database by title, or course or location
>### GET /api/sessions/filter/

```
request
{
    "title": "CS"
}

```

```
<HTTP STATUS CODE 200>
Response

[
    {
        "id": 1,
        "title": "CS Prelim",
        "course": "CS 1110",
        "start_time": "2023-12-02T15:30:00",
        "end_time": "2023-12-02T17:30:00",
        "location": "Mann Library",
        "population": 1,
        "description": "Studying for FWS Prelim"
    }
]
```


## Join study session
>### POST /api/sessions/<int:session_id>/

```
request
{
    token: <>
}

```

```
<HTTP STATUS CODE 200>
Response

{
    "id": 1,
    "title": "CS Prelim",
    "course": "CS 1110",
    "start_time": "2023-12-02T15:30:00",
    "end_time": "2023-12-02T17:30:00",
    "location": "Mann Library",
    "population": 2,
    "description": "Studying for FWS Prelim"
}
```