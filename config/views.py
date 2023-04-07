from django.http import HttpResponse
from django.shortcuts import render, redirect


def home(request):
    user = request.user.is_authenticated
    if user:
        return redirect('/inventory/')
        # return render(request, 'home.html')
    else:
        return redirect('/sign-in')
