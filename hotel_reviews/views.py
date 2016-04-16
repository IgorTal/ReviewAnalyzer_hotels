from django.shortcuts import render
from django.contrib.auth.decorators import login_required 

# Create your views here.
#view without authenticatyion 
@login_required(login_url="login/")
def home(request):
    return render(request, "home.html")
