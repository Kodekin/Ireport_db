[![Build Status](https://travis-ci.com/tomkeith/Ireport_db.svg?branch=develop)](https://travis-ci.com/tomkeith/Ireport_db)
[![Maintainability](https://api.codeclimate.com/v1/badges/ca2bfb8b0710f13036a5/maintainability)](https://codeclimate.com/github/tomkeith/Ireport_db/maintainability)
[![codecov](https://codecov.io/gh/tomkeith/Ireport_db/branch/develop/graph/badge.svg)](https://codecov.io/gh/tomkeith/Ireport_db)

# IReporter
```
 iReporter enables any/every citizen to bring any form of corruption to the notice of appropriate authorities and the general public. Users can also report on things that needs government intervention
```

## Getting Started
```
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.
```

### Prerequisites


# Technology Used:
* **Python3**
* **Flask**
* **Flask-RESTful**

# [Pivotal Tracker](https://www.pivotaltracker.com/n/projects/2227030)

## Current Endpoints.

| Method | Route | Endpoint Function |
| :--- | :--- | :--- |
| Post | /auth/signup | Creates a new user |
| Post | /auth/login | Enables user login |
| Post | v2/redflags | Creates an incident |
| Get | v2/redflags | Gets all incidents |
| Get | v2/redflags/id | Gets a specific incident |
| Put | v2/redflags/id | Edit a specific incident |
| Delete | v2/redflags/id | Delete a specific incident |


## Installastion Guide.
#### Clone the repo.
```
$ https://github.com/tomkeith/Ireport_db.git

```
#### Create a Virtual Environment and Activate.
```
$ python3 -m venv venv
$ source venv/bin/activate
```
#### Install Dependencies.
```
(venv) $ pip install -r requirements.txt
```
#### Run the app
```
(venv) $ FLASK_APP=run.py
(venv) $ flask run
```
The app should be accessible through : http://127.0.0.1:5000/

## Session Examples
To follow along with this examples get postman app installed.
- Set Up POSTMAN.

- Create A New User

![post man](images/usersignup.png)

- Post data in the format below to the redflag endpoint :
```
http://127.0.0.1:5000/v2/auth/signup
```
```
{
	"firstname" : "tom",
	"lastname" : "Emery",
	"email" : "tomh@gmail.com",
	"username" : "duuhdh",
	"password" : "sdfhsduf"
}
```

- Login in a registered user

![post man](images/userlogin.png)

- Post data in the format below to the redflag endpoint :
```
http://127.0.0.1:5000/v2/auth/login
```
```
{
	"username" : "duuhdh",
	"password" : "sdfhsduf"
}
```

- Create Incident

![post man](images/createincident.png)

- Post data in the format below to the redflag endpoint :
```
http://127.0.0.1:5000/v2/redflags
```
```
{
  "type" : "intervention",
  "location" : "45E, 24N",
  "status" : "draft", 
  "images" : "image", 
  "videos" : "video",
  "comment" : "whats happening.."
}
```

- Get all Incidents

![post man](images/getallincidents.png)


- Get data from the Incidents endpoint :
```
http://127.0.0.1:5000/v2/redflags/1
```

- Get specific Incident

![post man](images/getspecificincident.png)


- Get data from the incidents endpoint :
```
http://127.0.0.1:5000/v2/redflags/1
```

- Edit specific Incident

![post man](images/updatespecificatribute.png)


- Post data in the format below to the incident endpoint : 
```
http://127.0.0.1:5000/v2/redflags/1
```
```
{
  "location" : "45E, 24N",
}
```

- Delete Specific Incident

![post man](images/deletespecificincident.png)


- Delete data from the incident endpoint :
```
http://127.0.0.1:5000/v2/redflags/1
```
#### Run the Tests
```
(venv) $ nosetests --with-coverage --cover-package=app app/tests