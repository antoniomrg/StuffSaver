# Stuff Saver

#### Video Demo:  <https://youtu.be/t111ispTVrk>

#### Description:

Stuff Saver is web-based app that lets you save and store content.
This may be a new word you have just learned, coding concepts and their definition, but basically every type of content.

### Languages used

I used Flask to handle all the logic, and Bootstrap,
HTML and CSS for the front-end, and SQLite for the database.

### Description of files

#### application.py

This is the core of the application, where the logic is handled. The code is based on CS50 Finance app,
so I created a different route for each section of the app.
The routes are the following:

- /: the homepage, with a general overwiew of the web-app
- register: this is the section where you can sign-up for a new account. User must input a username, a password
(which is hashed) and password confirmation. A message error is shown if the user does not fill out all fields
- login: here is where you log in to your account.
- logout: log out of your account.
- add: here you can add some content to Stuff Saver. A form is shown with 4 fields the user has to fill out:
    - Category
    - Title
    - Description
    - URL/LINK.

This route also includes 2 subsections:

    - add/custom: add a new category of content.
    - add/existing: add content to an existing category you previously created.
- summary: see an overview of what you have added to Stuff Saver.

#### helper.py

Pre-existing code from CS50 Finance web-app, containing the functions
apology (used to handle error messages) and login_required (decorates routes to require login)

#### HTML files

They are all templates containing static and dynamic data used by Flask to render content.
They contain Jinja syntax.

#### stuffsaver.db

Database file used to store user sign-ups and content saved by the user.
The main table is used to store user details (username, password, etc.),
and a new table is created every time a new user signs up. This table
takes the name of the username and has their content as its fields.

#### Other

Other files in the project are mostly related to a Bootstrap free template I used
to improve the look and feel of the site.

### Possible improvements

- Ability to remove items from the Summary page
- Ability to filter items by Category in the Summary page
- Ability to sort items alphabetically, by category, date/time or other
- Integrate with AutoHotKey in order to user shortcuts to add content faster
- Enhance username and password requirements (ie. set a minimum length for password, special characters to be used, etc.)
- Improve error messages and alerts shown to user
