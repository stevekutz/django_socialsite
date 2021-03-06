from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm

from django.contrib.auth.decorators import login_required

def register(request):
     # if 'POST', user has submitted a completed form
     if request.method == 'POST':
          user_form = UserRegistrationForm(request.POST)
          if user_form.is_valid():
               # create new_user obj but DO NOT save yet
               new_user = user_form.save(commit=False)
               # Set chosen password
               new_user.set_password(user_form.cleaned_data['password'])
               # Save User obj
               new_user.save()

               context = {
                    'new_user': new_user,
               }

               return render(request, 'account/register_done.html', context)

     # request.method must be 'GET' , present user blank form
     else:
          user_form = UserRegistrationForm()

     context = {
          'user_form': user_form,
     }     
     return render(request, 'account/register.html', context)               


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


@login_required
def dashboard(request):
     return render(request, 'account/dashboard.html', {'section': dashboard})     