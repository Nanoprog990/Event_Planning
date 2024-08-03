Check 'https://youtu.be/Ie6akfeoO4A?si=p2GIK1Go3FteaU0v' To see the project in action. It has been updated on 2x to make it fit in the 5min length course requirement. Put on 0.5x to see in the original speed.

***Distinctiveness and Complexity

The main feature that disctincs my app is that the functionalities intended for superusers are not addressed through admin interface, but from the same interface than any regular user(using template  tags to render those functionalities only to superusers) making the User experiencs WAY more intuitive and friendly.
The other main feature that i am using that leverages the complexity (and also distictiveness) of my django app is the usage of SMTP. The same fuctionalities could have been addressed more easily with in-app notification system, but this way we will make sure to achieve the comunication even if the user is not in our django app at the moment. It also shows how environment variables can be used to hide sensitive information, credentials in this case.
The way we achieved filtering content and granting a special status to common users to colaborate with superusers is also something conspicuous. 
The separation between the events and the auth templates might be useful if, in the future, we develop another app to be used by the same people (i.e. A company). in that case we should separate not only the templates, but develop a whole auth app inside the same project.
Last (But not least) i would like to mention the integration of a weather API and the use of JS to fetch geolocation and displaying something user-friendly while the fetching is happening.

***How to Run apllication
Install Requirements. There is dockerfile already created that includes that. But it is not mandatory to use it. it can be done manually.
run 'manage.py migrate' command to create tables in database. no need to run 'makemigrations' The migrations are included in the 'migrations' folder of the repository.
Create superuser. Is not mandatory, but recomended to do it first so you are able to use all functionalities.
Run Django server. Enjoy

***Project Files content

--Inside Main project folder--

.gitignore: 
Assures that enironment variables (which can contain sensitive information such as credentials) are not pushed into the repository.

dockerfile:
*Use Python 3.10 as base image.
*Set environment variables to optimize Python environment.
*Set /code as working directory inside the container.
*Copy requirements.txt and install Python dependencies.
*Copy entire application code to the container.
*Expose port 8000 for Django server.
*Command to start Django development server on 0.0.0.0:8000

docker-compose.yml:
*version: '3.8': Specifies the Docker Compose file format.
*services: Defines the services (containers) that make up the application.
*web: Defines the configuration for the Django application service.
*build: Specifies the build context for the Docker image (current directory).
*command: Command to run when the container starts (python manage.py runserver 0.0.0.0:8000 starts Django *development server).
*volumes: Mounts the current directory (.) into the container's /code directory for live code reloading.
*ports: Maps port 8000 on the host to port 8000 on the container, allowing access to the Django application.

requirements.txt:
A list of every package thar needs to be installed in order to make the web app wprk correctly. It will also be useful for dockerization.

--Inside Events app folder--

Admin.py:
Registers the models that we will be able to access from the admin app.

forms.py: 
Custom forms for creating users, authenticating, creating events, updating profiles, filtering events, grantong colabborator status and inviting users.

models.py:
Models for populating the database.
There's tables for users, events, RSVP status, user profiles and event invitations. 

urls.py:
Contains the URLS for accesing all tmeplates and handling all endpoints for different views. As you can see it includes the auth URLS, which in 'views.py' specify the path for the template in their own app folder.

utils.py:
Contains the 'send_notification' function that will be used in the 'RSVP_event', 'Grant_colabborator_status' and 'Send_invitation' Views.

views.py:
*Imports: Various Django and Python modules are imported to handle views, forms, models, authentication, and utility functions.
*register: Handles user registration using a custom form (CustomUserCreationForm). Upon successful registration, the user is authenticated and redirected to the event list.
*user_profile: Renders the user's profile page (profile.html) if authenticated.
*update_profile: Allows users to update their profile information (UserProfileForm). Supports AJAX requests for updating profile details.
*event_list: Displays a list of events with optional filtering based on organizer and location (EventFilterForm).
*event_detail: Shows details of a specific event, including RSVP status of the logged-in user and users available to invite.
*create_event: Allows superusers to create new events using EventForm.
*my_events: Lists events created by the logged-in user, along with RSVP status (my_events.html).
*edit_event & delete_event: Provides functionalities for editing and deleting events, restricted to event organizers or superusers.
*grant_collaborator_status: Allows superusers to grant collaborator status to other users for a specific event (CollaboratorForm).
*send_invitation: Enables superusers to send invitations to other users for a specific event (InvitationForm).
*rsvp_event: Handles RSVP actions for events, updating the status and sending notifications to the event organizer.


.env:
Contains environment variables. In this case the settings and credentiales to be used by SMTP.

templatetags/custom_filters.py:
*Imports the template module from Django.
*Creates a Library instance from Django's template module, which is used to register custom template tags and filters.
*Decorates the function get_item to register it as a custom filter. The @register.filter decorator tells Django that get_item is a custom template filter.
*Defines the get_item function that takes two arguments: dictionary (the dictionary from which to retrieve the item) and key (the key of the item to retrieve).
*Filter function logic:
return dictionary.get(key): Retrieves the value from the dictionary using the key provided. If the key exists in the dictionary, it returns the corresponding value; otherwise, it returns None.

Templates/events:
*base.html:
This base template provides a structured layout with a navigation bar, content area, and footer. Child templates can extend this base template ({% extends 'base.html' %}) and override specific blocks ({% block content %}{% endblock %}) to customize their content while maintaining a consistent overall layout and styling. It intagrates static files, such as CSS and JS to be used by every files that extends this one in order to,not only keep styling consistent, but also improve modularity.
*event detail.html:
Extends base template and displays the event inforation, a list of atendees(if there's any), a form to RSVP the event and (if we are superusers) two form to invite users to the event and ask user to clabborate in the event organization respectively.
*event_form.html:
Extends base template and disĺays a form to creatr a new event (It is important to consider hat this will be accessed by a button that is only displayed for superusers).
*event_list.html:
Extends base template and displays a list of the events with some data and the creator, which gives access to the event deatail. It also features a filter button that displays a filter form to filter events by it's creator and/or locaton.
*my_events.html:
Extends base template and displays the events created by the user and a list of users who RSVP'd the invitation (It is important to consider hat this will be accessed by a button that is only displayed for superusers).
*profile.html:
Extends base template. Displays profile information and allow us to access the profile update page.
*update_profile.html:
Extends base template and displayes a profile update form to allow us to modifiy our profile information.

Templates/Registration:
*Login.html:
Extends base template and displays an authentication form for us to access the web app.
*Register.html: 
Extends base template and displays a registering form for us to create a user.

static/css/styes.css:
Contains the styling for all the base template (in which is loaded) and each one that extends it.

static/js/javascript.js:
Contains functions to handle profile forms, event edition and deletion, RSVP, geolocation fetch for weather API and weather displaying, and events filtering form visibility.
