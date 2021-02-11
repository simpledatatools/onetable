# OneTable

--------------

### About this project

OneTable is a simple interface for helping users to quickly create relational database structures for storing data. It is designed to be used for small businesses, projects, or groups who want to store simple lists of data that they define themselves (and that may change over time). The interface is designed to help them create 'links' between lists of data (i.e. relations) similar to how relational databases work, but through an interface that all users would understand. 

This project has been inspired by working with businesses across the globe who want to quickly begin to digitalize their operations, but do not have the resources (or time) to go through a full procurement proceswith an expensive technology provider of traditional ERP systems. There are other free, or free-trial, software as a service platforms exists for specific purposes (i.e. sales, crm, etc.) but we've found in many cases these are over-engineered and with pre-defined features that dictate how businesses operations and data collection need to take place. With OneTable, we are hoping to create the absolute simplest, most flexible platform possible that allows users to build anything they need. In this way, you can think of OneTable as the most simple "no-code" interface possible for building relational databases. 

OneTable is open sourced for the following reasons:
- We hope others will see value in the vision for the platform and contribute to the codebase. We hope to create a community of great minds who can collaborate to shape the vision moving forward
- We hope others will launch companies and businesses from the foundation the platform provides
- We hope that there is always transparency into how the platform operates and the way that data is used and stored, as well as ensuring the platform is secure


--------------


### Why this is developed on Django

Django was a natural choice because of the framework's focus on quickly creating relational databases. There are some limits to this approach, which we will try to solve over time. First, there are some cases within the project where we have not yet figured out how to do things the pure 'Django way', such as dynamically building forms using the Django forms module. We'll likely solve this - and other related issues - over time by switching at some point to the Django Rest Framework with an Angular front end. Similarly, python-based backends have limitations, which we plan to explore and overcome overtime as the project grows. For now, the project is considered a 'beta' test concept in the very early stages of development.

Django was also chosen because python is popular programming language that is known by many developers. Django is also a very easy framework to pickup quickly. We hope this means that many developers of all levels will be able to contribute to the project and/or use the codebase for their own work across the globe.


--------------


### How to run the project and get started

We will always make sure the project is easy to get starte with right away. You can clone the project and begin by going through the typical Django initiation steps noted below:

- Make sure you are in a virtualenv
- Install everything from requirements.txt using ```pip3 install -r requirements.txt```
- Make sure you create a local database in your local postgres called 'one-table-local' (see the base.py and config.py settings files under core.settings)
- Run ```python3 manage.py makemigrations``` to create database migrations
- Run ```python3 manage.py migrate``` to create database tables / initial setup
- Run ```python3 manage.py createsuperuser``` to create an admin user
- Run ```python3 manage.py runserver``` for start the local server
- The project should be running now at http://127.0.0.1:8000/

Please note that the project does rely on some third party services, such as Mailgun for registration and password reset. Please reach out to us if you need help setting up or configuring these third parties while you are using or exploring the platform.


--------------


### Architecture

The application relies on some key Models to help create lists and store records. In OneTable a `List` is a data structure for creating forms and form fields. The user defines these `List` objects to help them collect the data they need. Data is saved into the `List` structure through associated `Record` and `RecordField` objects. Additional detail is provided below: 

`List`: parent object which manages the `ListField` objects that define the form fields
`ListField`: objects for each form field, defining attributes such as field type and if the form field is required on the form
`Record`: parent object which manages the `RecordField` objects that hold form data and is directly connected to a `List`
`RecordField`: objects that store the data for each form field, and are directly connected to a `ListField`


Please also note: 

- Right now caching is not setup on the app - should probably implement redis at some point soon so we have that ready for other projects
- Whitenoise is being used for serving static files, which seems like the recommendation
- Static files used on the website (i.e. images on the homepage) are served from the same intance that hosts the app / as part of django, but S3 is used for user uploads when in production using the django-storages and boto3 libraries. In development, we don't use S3 -- just uploads to django project. I need to move the S3 credentials to environment variables in heroku so these are protected, once I create a new S3 bucket for this site. 


--------------


### Deployment

- The app has been configured to be deployed on Heroku
- Note that anything pushed to the `prod` branch on the github repo will trigger a deployment automatically on heroku
- There is a setup for dev and production, using an environment variable `environment` on Heroku to designate 'production' settings should be used. There may be a better approach for switching between development and production settings (just an initial approach I tried)
- Use `dev` branch for development




