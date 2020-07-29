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

7) Add `accounts` app     
