# OneTable

### About this project

OneTable is a simple interface for helping users to quickly create relational database structures for storing data. It is designed to be used for small businesses, projects, or groups who want to store simple lists of data that they define themselves (and that may change over time). The interface is designed to help them create 'links' between lists of data (i.e. relations) similar to how relational databases work, but through an interface that all users would understand. 

This project has been inspired by working with businesses across the globe who want to quickly begin to digitalize their operations, but do not have the resources (or time) to go through a full procurement proces with an expensive technology provider of traditional ERP systems. There are other free, or free-trial, software as a service platforms exists for specific purposes (i.e. sales, crm, etc.) but we've found in many cases these are over-engineered and with pre-defined features that dictate how businesses operations and data collection need to take place. With OneTable, we are hoping to create the absolute simplest, most flexible platform possible that allows users to build anything they need. In this way, you can think of OneTable as the most simple "no-code" interface possible for building relational databases. 

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

We will always make sure the project is easy to get started with right away. You can clone the project and begin by going through the typical Django initiation steps noted below:

- Make sure you are in a virtualenv
- Install everything from requirements.txt using ```pip3 install -r requirements.txt```
- Make sure you create a local database in your local postgres called 'one-table-local' (see the base.py and config.py settings files under core.settings)
- Run ```python3 manage.py makemigrations``` to create database migrations
- Run ```python3 manage.py migrate``` to create database tables / initial setup
- Run ```python3 manage.py createsuperuser``` to create an admin user
- Run ```python3 manage.py runserver``` for start the local server
- The project should be running now at http://127.0.0.1:8000/
- The admin panel should be running now at http://127.0.0.1:8000/admin

Please note that the project does rely on some third party services, such as Mailgun for registration and password reset. Please reach out to us if you need help setting up or configuring these third parties while you are using or exploring the platform. You may want to test at first using an admin superuser noted in the process above, so you do not need to go through the user verification process by email.


--------------


### Architecture

The application relies on some key Models to help create lists and store records. In OneTable a `List` is a data structure for creating forms and form fields. The user defines these `List` objects to help them collect the data they need. Data is saved into the `List` structure through associated `Record` and `RecordField` objects. Additional detail is provided below: 

- `List`: parent object which manages the `ListField` objects that define the form fields
- `ListField`: objects for each form field, defining attributes such as field type and if the form field is required on the form
- `Record`: parent object which manages the `RecordField` objects that hold form data and is directly connected to a `List`
- `RecordField`: objects that store the data for each form field, and are directly connected to a `ListField`


Please also note: 

- Right now caching is not setup on the app - should probably implement redis at some point soon
- Whitenoise is being used for serving static files, which seems like the recommendation
- Static files used on the website (i.e. images on the homepage) are served from the same intance that hosts the app / as part of django, but S3 is used for user uploads when in production using the django-storages and boto3 libraries. In development, we don't use S3 -- just uploads to django project. I need to move the S3 credentials to environment variables in heroku so these are protected, once I create a new S3 bucket for this site. 


--------------


### Deployment

- The app has been configured to be deployed on Heroku
- Note that anything pushed to the `prod` branch on the github repo will trigger a deployment automatically on heroku
- There is a setup for dev and production, using an environment variable `environment` on Heroku to designate 'production' settings should be used. There may be a better approach for switching between development and production settings (just an initial approach I tried)
- Use `dev` branch for development


--------------


### Contributing to this project

**Casual Contributors**

A list of current issues are always updated on this repository. You are welcome to help solve an issue that is not current assigned to another and is marked as 'Open'. If you are interested in solving an issue, please reach out and we will assign the issue to you so others know you are working on it.

We follow a simple, but strict process for git branches and contributing:

- Each github issue will be a small task (usually requiring 8 hours or much less), and will include a description with details. Mockups and videos will be provided in cases where the intended functionality cannot be described without a visual example.

- You will only be assigned one issue at a time. You should complete the current issue that is assigned to you, then follow up for your next task if you are interested in working on another issue.

- You should always work on a git branch that is the same name / number as the issue using format `issue-[Issue Number]` (i.e. branch `issue-300` would be the branch for when you are working on issue-300).

- If you have not completed the task, you can still push your code to the repository at the end of the day on the issue’s branch. Once you have completed your
task, you should open up a Pull Request (PR) merging your issue branch into branch `dev` and assign Matt and Loc (usernames: mattcapelli and locAtLaheriyam) to the PR as a reviewer. We will merge the code once we have reviewed, or if there are changes needed, we will add feedback to the github issue for you to fix.


**Full-time contributors**

We also have opportunities for you to work on this project in a paid position (as a full / part time job) if you are able to lead large portions of the development and can work regular hours. If you are available to contribute to the project in this way, please reach out. The setup would work as:

- We would like someone who works consistent hours each day. This helps us to more easily coordinate tasks, ensure upcoming tasks are prepared in advance, make sure code is reviewed in a timely manner, and to make sure we can track and monitor your progress.

- People on our team are working between London (GMT+0) and Indochina Time (GMT+7), but this opportunity is open to any one in any timezone

- We are looking for someone to work for at least 5 hours per day, but you can work as many hours as you choose so long as it is consistent hours and you are producing code at the pace and quality to our standards.

- You can choose the hours you prefer to work, but they should be the same hours each each day (i.e. always working 10am - 3pm IST each day Monday - Friday)

- You must work through the platform Upwork, which we are setup for and allows us to transfer salaries easily to multiple countries

- At your start time each day, you would check in with Matt for a virtual daily standup meeting to discuss what you are working on, plans for the day and goals of what you plan to complete. During this time, please also ask any questions or clarifications you have.

- While working throughout the day during your regular time block, you would be expected to focus only on the OneTable project, leaving other tasks for other hours of the day.

- At the end of each day, you would provide an update with Matt, providing a summary of what you completed during the day as well as any questions or requests that came up while you were working. If you have questions about the project’s requirements, need mockups created, or have other clarifications, these should be provided at the end of each day so that we can get you answers before the next day begins.

- You will be expected to push your code to our git repository at the end of every day using the git branch process we have described above.

- The work must be completed by you, and cannot be sent to others or subcontracted to other developers. 


**For people who are not developers**

If you are interested in contributing to the project more regularly through this way, by developing mockups or helping to develop the roadmap, please reach out as well and we will schedule a call to help you get involved. 


### OneTable Key Contacts

**Matt Capelli**: Founder, mostly focused on the project roadmap and designs. Occationally tries to hack together python code. Username: _**mattcapelli**_
**Bui Tan Loc**: Senior Developer / Achitect, leads project architecture and manages all PR's and issues. Username: _**locAtLaheriyam**_


