# Image uploader with Django Rest Framework

Following project is a recruitment task. I managed to fulfill all functional
requirements listed in the task. This assignment focuses on creating a backend application,
which enables its users to upload images and store them on server. Later on, the users
are able to fetch links to thumbnails, original images and expiring links for 
original images. 

The project has been done using Django Rest Framework and a few other helping libraries.

Also, one can easily run the application using docker-compose. The only thing
that needs to be done afterwards is creating a superuser. I left it out of the
automatic stand-up as every user can (and should) use his own credentials as 
superuser. To get the application up and running one should: <br>
- download project (git clone https://github.com/gorbart/image_uploader can be useful)
- open project directory in cmd <br>
- type in "docker-compose up --build" (of course having Docker installed and working
  earlier is a must)<br>
- open image_uploader_web_1's CLI <br>
- type in "python manage.py createsuperuser" and go on with his credentials <br>
- use application's REST API with localhost:8000/api/(insert what you want to do).