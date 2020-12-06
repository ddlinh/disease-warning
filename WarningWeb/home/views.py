from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .form import AccountForm

# Create your views here.
def index(request):
    location = request.session.get('location')
    if request.session.get('location'):
        del request.session['location']
    return render(request,"homes.html", {'location': location})


def get_account_form(request):
    print(1)
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['location'])
            locate = form.cleaned_data['location'].split(' ')
            locate = '+'.join(locate)
            request.session['location'] = locate
        return HttpResponseRedirect('/')
    return render(request, 'homes.html')

