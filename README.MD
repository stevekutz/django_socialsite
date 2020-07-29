# Django Social Site

### Project will demonstrate

- Configuring the Django Authentication Network
- Setting up registration views for users
- Using a custom profile model to extend the users model
- Setting up authentication


#### Project setup

1) Create a dir callled `env` in terminal

     ~~~ bash
     mkdir env
     ~~~

2) Create virtual environment

     ~~~ bash
     python3 -m venv env/bookmarks
     ~~~

3) Activate virtual environment

     ~~~ bash
     source env/bookmarks/bin/activate
     ~~~

4) Install `Django` 

     ~~~ bash
     pip install django
     ~~~

5_ Create a new project

     ~~~ bash
     django-admin startproject bookmarks
     ~~~

6) Open new `bookmarks` directory and create `account` application

     ~~~ bash
     cd bookmarks
     django-admin startapp account
     ~~~

7) Update `settings.py` to include the `account` app

     ~~~ py
     INSTALLED_APPS = [
     'account',   # 'account.apps.AccountConfig' also works 
     'django.contrib.admin',
     'django.contrib.auth',
     'django.contrib.contenttypes',
     'django.contrib.sessions',
     'django.contrib.messages',
     'django.contrib.staticfiles',
     ]
     ~~~

8) Run migration

     ~~~ bash
     python manage.py migrate
     ~~~

#### Set up authentication views for login and logout

1) Background info

     - <a href = "https://docs.djangoproject.com/en/3.0/topics/forms/"> Django Forms Ref </a>
     - <a href = "https://docs.djangoproject.com/en/3.0/topics/auth/"> Django Authentication Ref </a>

     - Although authentication(verify user identity) and authentication(verify user permissions), the term `authentication` is used in the Django documenation to refer to both

     - Django's default authentication network manages
         - authentication
         - sessions
         - permissions
         - user groups

     - The authentication framework is part of the default settings of the `bookmarks` project
     - Inside of `settings.py` is comprised of the:
         - `django.contrib.auth` application in `INSTALLED_APPS`
         - `Authentication Middleware` middleware class in `MIDDLEWARE`
         - `SessionMiddleware` midddleware class in `MIDDLEWARE`
         - `User`, `Group`, `Permission` models

     - Although authentication(verify user identity) and authentication(verify user permissions), the term `authentication` is used in the Django documenation to refer to both

2) Set up login form by creating `forms.py` in the app's `account` folder

     - the `LoginForm` inherits from Djngo's `Form` class
     - <a href = "https://docs.djangoproject.com/en/3.0/topics/forms/"> Django Forms Ref </a>
     - the `PasswordInput` widget is used to render HTML element `password` using `type="password"`

     ~~~ py
     from django import forms

     class LoginForm(forms.Form):
          userName = forms.CharField()
          password = forms.CharField(widget = forms.PasswordInput)
     ~~~

3) Create the `user_login` view in the app's `account` folder   

     - <a href = "https://docs.djangoproject.com/en/3.0/topics/http/views/"> Django Views Ref </a>

     - the `GET` request is used to instantiate a new login form template
     - the `POST` request will:
          -  `LoginForm(request.POST)` instantiates the form with user submitted data
          -  `is_valid()` verifies the entered data meets Django's criteria(e.g. password complexity, all fields are completed,...)
          - `cleaned_data` is an attribute saved into the form and allows for updating the database or perform additional processing prior to sending an `HTTP` redirect to the browser
          - `authenticate()` verifies the user data against the database using the `request `obj, `username`, and `password`. If verified, a `User` obj is returned. Failure returns a basic `HttpResponse` obj from the view. Otherwise, it returns `None`
          - `is_active` verifies if a registered user has a `disabled account`
          - the `login` method allows `active` users to join a `session` and returns a message to the user indicating success

     ~~~ py
     from django.shortcuts import render

     # Create your views here.
     from django.http import HttpResponse
     from django.contrib.auth import authenticate, login
     from .forms import LoginForm

     def user_login(request):
          # user has submitted a completed form
          if request.method == 'POST':
               form = LoginForm(request.POST) # instantiate with submiited data
               if form.is_valid():
                    cd = form.cleaned_data # saves validated data in form's cleaned_data attribute
                    user = authenticate(request, username = cd['username'], password = cd['password'])

                    # if valid
                    if user is not None:
                         if user.is_active:  # verify if disabled
                              login(request, user)
                              return HttpResponse('Authentication Successful')
                         else:
                              return HttpResponse('Account Disabled')

                    else:  
                         return HttpResponse('Invalid Login Credentials')        

          # e.g.  request.method == 'GET
          else:
               form = LoginForm() # initialize blank form template

          # present the initialized blank form to user
          context = {
               'form': form
               }
          return render(request, 'account/login.html', context)
     ~~~