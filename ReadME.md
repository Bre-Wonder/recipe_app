# Recipe App Python with Django

### Project Description
A Python Django project built to store recipes in a database and a UI for users to interact with recipes by adding, deleting, updating or viewing. 

### Technologies Used:
Python | virtualenvwrapper | Django | DataFrame(pandas) | matplotlib


### How to start this Project:

* Install Python, at the time of writing this Python 3.13.5. I was able to do this by going to Python's website and using their MacOS installer. 
* Create yourself a virtual environtment by typing this command into your terminal (for MacOS users) : `pip3.13 install virtualenvwrapper` (note pip is automatically installed when you install Python)
* Confirm your terminal knows the path to this virtualenvwrapper install by typig this into your terminal: `which virtualenvvwrapper.sh`
* Modify Shell Start Up File by running `sudo nano ~/.zshrc` for MacOS 10.15 or newer. 
* Add these lines the bottom of the file that is showing in the terminal by typing this in at the very end:
  `export VIRTUALENVWRAPPER_PYTHON=$(which python3.8)`
   `source $(which virtualenvwrapper.sh)`
  Then be sure to close the editor by pressing Ctrl X and they type Y and press enter. This will modify the shell start up file so that it will always show up.
* To create your own new virtual environment type in your terminal this command: 
  `mkvirtualenv   <your-chosen-environment-name>`
* Note: see terminal commands defined - `deactivate`, use to deactivate a virtual environment. `workon`, to display all options of install environments. `workon <environment name>`, to load an installed environment. `rmvirtualenv <environment name>`, remove installed environment. 
* You have many places you can go from here. You can create a script in your preferred IDE and once saved you    can navigate to it in your terminal. Once in your terminal, you can run the command: `python3 <name-of-your-script-file>`. For example if you named your script `app.py`, you would write - `python3 app.py` in your terminal. This will run the Python commands in your script file. Be sure to make sure you are in your virtual environment.
* Another option you have to run Python code is to run the Python code in your command line. Once in your virtual environment, you can just type `python3` and then begin by writing the command directly into the terminal. 
* Note: If you would like to install the ipython shell you can type: `pip install ipython`.
* Creating a Requirement.txt File: First, go to the desired directory in your terminal. Second, run you chosen virtual environment. Third, type this command into your terminal and it will create a requirement.txt file for you - `pip freeze > requirements.txt`. 

* Install Django, remote your terminal to the directory you would like to work in. 
* Activate your virtual environment you would like to work in with this command `workon <environment name>`
* Run `pip install django` to install django framework
* Check version of django by running this command in your terminal `django-admin --version`

* Creating your project in Django. A Django project is built out with a Model View Template (MVT) type of architecture. It allows you to built out a database and UIs all within it structure. I have listed some suggestions below for consideration.
  * To start your own project in the command line, be sure your have your virtual environment open in your root directory and run: `django-admin startproject <name chose for project>`
  * Next it is a good idea to write out your schema for how you wanted your project and database to be built, know where you want different parts of your applicaiton to show up or be deined. 
  * To creat an app inside your Django project run this command: `python manage.py startapp <name you have chosen for that app>`
  * To create a superuser in the admin of djanago run this command: `python manage.py createsuperuser`
      These are all steps that will serve you while creating a project in Django


### Lessons Learned:

* I've learned to structure my project in the way that Django requires with MVT type of architacture. One awesome advantage of this is that parts can be reused without have to re-written. If something from one project was applicaable to some other project, I could just re-use it, such as a login. 


GitHub Repository site: 

Live application deployed to the Azure Cloud:

Note: Cursor AI used to help in builing out html files with style and formatting. Chapt GPT used for helping to create testing files.
