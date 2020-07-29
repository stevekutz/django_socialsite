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