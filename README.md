# OneTable

## About this project

OneTable is an open source project helping organizations and teams quickly build small apps to digitalize their operations. The platform works by helping users create lists of data that organically evolve over time into relational databases and advanced functionality.

This project has been inspired by working with businesses across the globe who want to quickly begin to digitalize their operations, but do not have the resources (or time) to go through a full procurement process with an expensive technology providers. Traditional ERP systems are great, but they are insanely overpriced for most businesses in emerging economies. There are other free (or free-trial) software as a service platforms that exist for other specific purposes (i.e. sales platforms, a million different CRM platforms, etc.), but in many cases these solutions are over-engineered with predefined features that dictate how businesses operations must take place and how data should be collected. We definitely do not want to recreate the wheel, but we still find ourselves in a gap that persists within the realm of management information systems for organizations operating in developing nations. This is especially a challenge for organizations in the early stages of digitalization, where data models and requirements are evolving quickly. You can think of OneTable as the absolute most simple, most flexible "no-code" interface that allows users to build simple applications for their businesses. 

Although OneTable can be used in almost any context, the heart of the project and inspiration for building the platform is from years of work in emerging economies, where we've seen time and time again a landscape ripe with opportunity and full of brilliant minds who are changing the world. The name OneTable comes from a two part vision. First that we can come together collaboratively around the same table to share perspectives and ideas and to solve tech challenges together. Second, OneTable is rooted in a belief that everyone should have the chance to sit around the same table of opportunity, that access to technology is a right and a public good, and that technology should always be transparent and fair. 

For these reasons, and many others, OneTable should be open sourced and free for everyone. We hope open sourcing the code will allow: 

- Others to see value in the vision for the platform and contribute to the codebase or the growth of a OneTable community
- Create a community of great minds who can collaborate to shape the vision moving forward
- Inspire others to launch companies and businesses from the foundation the platform provides and through the flexible Apache 2.0 license
- Genuine transparency and honesty to be at the heart of everything we do, including ensuring all stakeholders have clarity into how the platform operates, the way that data is used and stored, the platform's security, and the limitations to the features and functionality


## Why is this project developed on Django?

Django was a natural choice because of the framework's focus on quickly creating relational databases. There are some limits to Django for this use case, which we will try to solve over time. First, there are some cases within the project where we have not yet figured out how to do things the pure 'Django way', such as dynamically building forms using the out of the box Django functionality. We'll likely solve this over time - and other related issues - by switching at some point to the Django Rest Framework with an Angular front end. Similarly, python-based backends have limitations, which we plan to explore and overcome over time as the project grows. For now, the project is considered a 'beta' test concept in the very early stages of development.

Django was also chosen because python is popular programming language that is known by many developers. Django is very easy to learn, and we hope this means that many developers of all levels will be able to contribute to the project and/or use the codebase for their own work in their local communities across the globe. The team for this project is based around the world in places like Washington DC, Nairobi, and Ho Chi Minh City. We are glad to support you in any way we can as you use the OneTable platform, and we look forward to connecting with contributors in new countries.   




## How to run the project and get started

We will always make sure the project is easy to get started with right away so you can spend more time coding and less time fighting configurations and environment setup. You can clone the project and begin by going through the typical Django initiation steps noted below:

- Make sure you are in a virtualenv (we recommend setting up a new one)
- Install everything from `requirements.txt` using ```pip3 install -r requirements.txt```
- You will need to create a `config.py` file under `core > settings` to store your local database credentials (these are not version controlled). The file should contain:
```
local_database = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': 'one-table-local',
          'USER': 'YOUR LOCAL USER',
          'PASSWORD': 'YOUR LOCAL PASSWORD',
          'HOST': 'localhost',
          'PORT': '5432',
      }
}
```
- Make sure you create a local postgres database called `one-table-local` (or whichever local database name you want to use)
- Run ```python3 manage.py makemigrations``` to create database migrations
- Run ```python3 manage.py migrate``` to create database tables / initial setup
- Run ```python3 manage.py createsuperuser``` to create an admin user
- Run ```python3 manage.py runserver``` for start the local server
- The project should be running now at http://127.0.0.1:8000/
- The admin panel should be running now at http://127.0.0.1:8000/admin

Please note that the project does rely on some third party services, such as Mailgun for registration and password reset. For local development these have been configured using Django's web server and smtp, and usually the information (i.e. emails send will be printed to the command line). Please reach out to us if you need help setting up or configuring third party libraries while you are deploying the platform to your own instance. You may also want to test the platform at first using an admin superuser created in the above process, so you do not need to go through the user verification process by email.

We have also setup the project to deploy automatically to Heroku, which offers free hosting for small applications that you can use to get started. We can also help you get setup with this as well if you have any questions.




## Architecture

The application relies on some key Django Models to help create data structures and store records. In OneTable a `List` is a data structure for creating forms and form fields. The user defines these `List` objects to help them collect the data they need. Data is saved into the `List` structure through associated `Record` and `RecordField` objects. Additional detail is provided below:

- `List`: parent object which manages the `ListField` objects that define the form fields
- `ListField`: objects for each form field, defining attributes such as field type and if the form field is required on the form
- `Record`: parent object which manages the `RecordField` objects that hold form data and is directly connected to a `List`
- `RecordField`: objects that store the data for each form field, and are directly connected to a `ListField`



## Deployment

- The app has been configured to be deployed on Heroku, as noted above
- There is a setup for dev and production, using an environment variable `environment` on Heroku to designate 'production' settings should be used. There may be a better approach for switching between development and production settings, but for now an initial setup we are using that works well enough :)
- If deploying a cloned copy of this repository please use the `master` branch which is the most stable, released version; however, note there are some differences between the dev and prod `requirements.txt` files because Heroku does not support packages like `python-magic-bin`
- The `dev` branch is 'bleeding edge' and always still being tested, though usually quite stable and able to be deployed as well




## Contributing to this project

**Casual Contributors**

A list of current issues are always updated on this repository. You are welcome to help solve an issue that is not currently assigned to another person and is marked as 'Help Wanted - Open Issue'. If you are interested in solving an issue, please reach out and we will assign the issue to you so others know you are working on it.

We follow a simple, but strict process for git branches and contributing:

- Each issue will be a small task (usually requiring 8 hours or much less), and will include a description with details. Mockups and videos will be provided in cases where the intended functionality or bug fixes cannot be described without a visual example.

- You will only be assigned one issue at a time. You should complete the current issue that is assigned to you, then follow up for your next task if you are interested in working on another issue. If you need help with an issue, please reach out to @locAtLaheriyam and @mattcapelli, who is happy to assist you with any challenge.

- You should always start with the `dev` branch when branching, so the code you start from is the most recent version being tested

- You should always work on a git branch that is the same name / number as the issue you are assigned using the format `issue-[Issue Number]` (i.e. branch `issue-300` would be the branch for when you are working on issue-300). If you need to submit updates, those would use a `-fixes-#` extension (i.e. `issue-300-fixes-1` for the first submission of fixes for issue #300. 

- Once you have completed your task, you should open up a PR that requests to merge your issue branch into branch `dev` and assign the PR to Matt and Loc (usernames: @mattcapelli and @locAtLaheriyam) as the reviewers. We will merge the code into the main codebase once we have reviewed, or if there are changes needed, we will add feedback to the github issue for you to fix. If you have not completed the task, you can still push your code to the repository, as we consider all branches to be not complete unless you open a PR from the branch you are working on into `dev`. 


**Full-time contributors**

We also have opportunities for you to work on this project in a paid position (as a full / part time job) if you are able to lead large portions of the development and can work regular hours. We are a team that is scattered across the globe in almost every timezone and we are happy to have you work any schedule that is best for you. If you are available to contribute to the project in this way, please do reach out. The setup works as:

- We need people who can work consistent hours each day. This helps us to more easily coordinate tasks, ensure upcoming tasks are prepared in advance, make sure code is reviewed in a timely manner, and to make sure we can track and monitor your progress.

- People on our team are working between London (GMT+0) and Indochina Time (GMT+7), but this opportunity is open to any one in any timezone.

- We are looking for someone to work for at least 4 hours per day, but you can work as many hours as you choose so long as it is consistent hours and you are producing code at a pace and quality to our standards.

- You can choose the hours you prefer to work, but they should be the same hours each each day (i.e. always working 10am - 3pm IST each day Monday - Friday).

- You must work through the platform Upwork, which allows us to transfer salaries easily to multiple countries.  

- At your start time each day, you must check in with Matt (@mattcapelli) for a virtual daily standup meeting to discuss what you are working on, your plans for the day, and the goals of what you plan to complete. During this time, please also ask any questions or clarifications you have.

- At the end of each day, you provide an quick update with Matt through another virtual standup, including a summary of what you completed during the day as well as any questions or requests that came up while you were working. If you have questions about the project’s requirements, need mockups created, or have other clarifications, these should be provided at the end of each day so that we can get you answers before the next day begins.

- You will be expected to push your code to our git repository at the end of every day using the git branch process we have described above.

- The work must be completed by you, and cannot be sent to others or subcontracted to other developers.

Please see our [Contributing Guidelines][contributing] and [Code of Conduct][conduct] for more information

[contributing]: https://github.com/simpledatatools/onetable/blob/master/CONTRIBUTING.md
[conduct]: https://github.com/simpledatatools/onetable/blob/master/CODE_OF_CONDUCT.md

## Not a developer but interested in getting involved?

Fantastic! If you are interested in contributing to the project but you are not a developer, please do reach out. There are a huge amount of other tasks that support the project - from developing mockups or helping to develop the technology roadmap, to connecting with new organizations who can give feedback and test out new features. Please reach out to @mattcapelli and we will schedule a call to get you involved.

## Feature Requests

OneTable is very new and evolving quickly! If you have an idea or feature request, please reach out to @mattcapelli to discuss and we will try to get the new functionality into the backlog and product roadmap. As the project grows, we will formalize this process through a board / steering committee and dedicated product team, including releasing the product roadmap publically with regular updates. 

## Releases

We try to release a new version as soon as a usable feature has passed all tests. We follow a standard X.X.X format for minor / major updates. Of course we are still very much in version 0.X.X and will be for quite some time :) We are targeting a first release by March 1, 2021. Releases are managed by @locAtLaheriyam, and if you would like to be added to a mailing list with an update sent each time there is a release, just let him know. 

## Want to use OneTable but don't want to build from source?

No problem! You can use OneTable through the deployed instance we provide at www.onetableapp.com, including a generous free-forever tier. Contact us through the support chat on the website if you need help getting setup! The first version of this will be available on March 1, 2021. 

## Want to use OneTable to create your own business?

Fantastic! Please reach out if you would like and we can relay at least a decade worth of terrible business ideas that will help you avoid some common landmines. We hope OneTable can be a foundation for you to launch consulting companies with clients in your local communities, or of course, by white labeling the platform through a Software as a Service model. The more businesses the better! 

## OneTable Key Contacts

- **Matt Capelli**: Founder | Mostly focused on the project roadmap and designs. Occasionally tries to hack together python code | Username: _**@mattcapelli**_
- **Bui Tan Loc**: Senior Developer / Architect | Leads project architecture and manages all PR's and issues | Username: _**@locAtLaheriyam**_
